"""Smoke real de sincronizacao entre duas bases SQLite e uma Central HTTP.

O script preserva as bases e o relatorio JSON para auditoria. Credenciais efemeras
nao sao gravadas no relatorio nem exibidas no terminal.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MANAGE = REPO / "manage.py"


def run_manage(env: dict[str, str], *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(MANAGE), *args],
        cwd=REPO,
        env=env,
        text=True,
        capture_output=True,
        check=check,
    )


def django_shell(env: dict[str, str], code: str) -> str:
    result = run_manage(env, "shell", "-c", code)
    return result.stdout.strip().splitlines()[-1]


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_until_ready(url: str, process: subprocess.Popen[str]) -> None:
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("A Central temporaria encerrou antes de ficar disponivel.")
        try:
            urllib.request.urlopen(url, timeout=1).close()
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError("A Central temporaria nao respondeu no prazo esperado.")


def base_env(data_dir: Path, database: Path, role: str) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "MHEIBOS_DB_MODE": "sqlite",
            "SQLITE_DB_NAME": str(database),
            "MHEIBOS_DATA_DIR": str(data_dir),
            "MHEIBOS_RUNTIME_ROLE": role,
            "DJANGO_ALLOWED_HOSTS": "localhost,127.0.0.1",
            "DJANGO_DEBUG": "False",
        }
    )
    return env


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path, required=True)
    options = parser.parse_args()
    evidence_dir = options.evidence_dir.resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)

    central_dir = evidence_dir / "central"
    client_dir = evidence_dir / "client"
    central_dir.mkdir(exist_ok=True)
    client_dir.mkdir(exist_ok=True)
    central_env = base_env(central_dir, central_dir / "central.sqlite3", "central")
    client_env = base_env(client_dir, client_dir / "client.sqlite3", "client_offline")

    run_manage(central_env, "migrate", "--noinput")
    run_manage(client_env, "migrate", "--noinput")

    credential = json.loads(
        django_shell(
            central_env,
            "from apps.catalogo.models import OperadorGestor, PapelOperador; "
            "from apps.sincronizacao.services import criar_estacao; "
            "o=OperadorGestor.objects.create(nome='Autora Smoke HTTP', senha='efemera', "
            "papel=PapelOperador.USUARIO, codigo_origem_offline='SH'); "
            "c=criar_estacao(nome='Cliente Smoke HTTP'); "
            "import json; print(json.dumps({'station_id':str(c.estacao.pk),'secret':c.segredo}))",
        )
    )

    station_id = credential["station_id"]
    client_env.update(
        {
            "MHEIBOS_STATION_ID": station_id,
            "MHEIBOS_STATION_SECRET": credential["secret"],
            "MHEIBOS_POLICY_VERSION": "smoke-http-1",
        }
    )
    django_shell(
        client_env,
        "import uuid; from decimal import Decimal; "
        "from apps.catalogo.models import OperadorGestor, PapelOperador; "
        "from apps.clientes.models import Cliente; from apps.pedidos.models import Pedido, PedidoItem; "
        "from apps.sincronizacao.services import enfileirar_pedido_local; "
        "o=OperadorGestor.objects.create(nome='Autora Smoke HTTP', senha='efemera', "
        "papel=PapelOperador.USUARIO, codigo_origem_offline='SH'); "
        "p=Pedido.objects.create(cliente=Cliente.objects.create(nome='Cliente isolado'), "
        "tema='Smoke duas instancias', valor_total=Decimal('42.00'), usuario_cadastro=o.nome); "
        "PedidoItem.objects.create(pedido=p, ordem=1, nome='Item smoke', quantidade=Decimal('1'), "
        "preco_unitario=Decimal('42.00')); "
        f"u=enfileirar_pedido_local(pedido=p, operador=o, estacao_id=uuid.UUID('{station_id}'), "
        "versao_politica='smoke-http-1'); print(str(u.chave_idempotencia))",
    )

    before = run_manage(client_env, "verificar_retorno_online", check=False)
    if before.returncode == 0 or "Retorno bloqueado por 1 unidade" not in (before.stdout + before.stderr):
        raise RuntimeError("A fila pendente nao bloqueou o retorno online.")

    port = free_port()
    central_url = f"http://127.0.0.1:{port}"
    client_env["MHEIBOS_CENTRAL_URL"] = central_url
    process = subprocess.Popen(
        [sys.executable, str(MANAGE), "runserver", f"127.0.0.1:{port}", "--noreload"],
        cwd=REPO,
        env=central_env,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_until_ready(central_url + "/", process)
        sent = run_manage(client_env, "enviar_fila_offline", "--limite", "10")
        if "Confirmadas: 1; falhas: 0" not in sent.stdout:
            raise RuntimeError("A Central nao confirmou exatamente uma unidade.")
        after = run_manage(client_env, "verificar_retorno_online")
        if "RETORNO_SEGURO" not in after.stdout:
            raise RuntimeError("O Cliente nao liberou o retorno seguro.")

        repeated = json.loads(
            django_shell(
                client_env,
                "import json; from apps.sincronizacao.models import UnidadeSincronizacao; "
                "from apps.sincronizacao.services import envelope_da_unidade; "
                "from apps.sincronizacao.transport import enviar_envelope; from django.conf import settings; "
                "u=UnidadeSincronizacao.objects.get(); r=enviar_envelope(central_url=settings.MHEIBOS_CENTRAL_URL, "
                "estacao_id=settings.MHEIBOS_STATION_ID, segredo=settings.MHEIBOS_STATION_SECRET, "
                "envelope=envelope_da_unidade(u)); print(json.dumps(r.payload))",
            )
        )
        if repeated.get("codigo") != "JA_INCORPORADO":
            raise RuntimeError("A repeticao nao foi reconhecida como idempotente.")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

    central_counts = json.loads(
        django_shell(
            central_env,
            "import json; from apps.pedidos.models import Pedido; "
            "from apps.sincronizacao.models import IncorporacaoOffline; "
            "print(json.dumps({'pedidos':Pedido.objects.filter(origem_offline=True).count(), "
            "'incorporacoes':IncorporacaoOffline.objects.count()}))",
        )
    )
    if central_counts != {"pedidos": 1, "incorporacoes": 1}:
        raise RuntimeError(f"A idempotencia falhou na Central: {central_counts}")

    report = {
        "status": "PASSED",
        "central_database": str(central_dir / "central.sqlite3"),
        "client_database": str(client_dir / "client.sqlite3"),
        "pending_queue_blocked_return": True,
        "actual_http_confirmation": True,
        "safe_return_after_confirmation": True,
        "idempotent_replay": repeated["codigo"],
        "central_counts": central_counts,
        "credentials_persisted_in_report": False,
    }
    (evidence_dir / "result.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

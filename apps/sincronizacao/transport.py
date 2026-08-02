import json
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


class TransporteIndisponivel(Exception):
    pass


@dataclass(frozen=True)
class RespostaCentral:
    status: int
    payload: dict


class _SemRedirecionamento(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_abrir_url = build_opener(_SemRedirecionamento()).open


def enviar_envelope(
    *,
    central_url: str,
    estacao_id: str,
    segredo: str,
    envelope: dict,
    timeout: float = 8.0,
) -> RespostaCentral:
    base = central_url.strip().rstrip("/")
    parsed = urlparse(base)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise TransporteIndisponivel("URL da Central invalida.")
    if not estacao_id or not segredo:
        raise TransporteIndisponivel("Credencial da Estacao ausente.")
    request = Request(
        f"{base}/sincronizacao/incorporar/",
        data=json.dumps(envelope, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Mheibos-Station-ID": estacao_id,
            "X-Mheibos-Station-Secret": segredo,
        },
    )
    try:
        with _abrir_url(request, timeout=timeout) as response:
            body = response.read(2_000_001)
            status = response.status
    except HTTPError as exc:
        body = exc.read(2_000_001)
        status = exc.code
    except OSError as exc:
        raise TransporteIndisponivel("Central indisponivel.") from exc
    if len(body) > 2_000_000:
        raise TransporteIndisponivel("Resposta da Central excede o limite.")
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TransporteIndisponivel("Resposta da Central invalida.") from exc
    if not isinstance(payload, dict):
        raise TransporteIndisponivel("Resposta da Central invalida.")
    return RespostaCentral(status=status, payload=payload)

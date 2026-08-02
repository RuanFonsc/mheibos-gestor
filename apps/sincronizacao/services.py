import hashlib
import json
import uuid
import secrets
from dataclasses import dataclass
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.models import OperadorGestor
from apps.clientes.models import Cliente
from apps.pedidos.models import PagamentoPedido, Pedido, PedidoItem

from .models import EstadoUnidade, EstacaoCliente, IncorporacaoOffline, SequenciaOffline, UnidadeSincronizacao


class SincronizacaoInvalida(Exception):
    pass


@dataclass(frozen=True)
class ResultadoIncorporacao:
    pedido: Pedido
    repetida: bool


@dataclass(frozen=True)
class CredencialEstacaoCriada:
    estacao: EstacaoCliente
    segredo: str


def criar_estacao(*, nome: str) -> CredencialEstacaoCriada:
    nome = nome.strip()
    if not nome:
        raise SincronizacaoInvalida("Informe um nome para a Estacao.")
    if EstacaoCliente.objects.filter(nome__iexact=nome).exists():
        raise SincronizacaoInvalida("Ja existe uma Estacao com este nome.")
    segredo = secrets.token_urlsafe(32)
    estacao = EstacaoCliente.objects.create(
        nome=nome, segredo_hash=make_password(segredo)
    )
    return CredencialEstacaoCriada(estacao=estacao, segredo=segredo)


def _json_canonico(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def calcular_checksum(payload: dict) -> str:
    return hashlib.sha256(_json_canonico(payload).encode("utf-8")).hexdigest()


def _snapshot_pedido(pedido: Pedido) -> dict:
    return {
        "pedido": {
            "tema": pedido.tema,
            "data_pedido": pedido.data_pedido.isoformat() if pedido.data_pedido else None,
            "data_entrega": pedido.data_entrega.isoformat() if pedido.data_entrega else None,
            "hora_entrega": pedido.hora_entrega.isoformat() if pedido.hora_entrega else None,
            "observacoes": pedido.observacoes,
            "valor_total": str(pedido.valor_total),
            "valor_pago_legado": str(pedido.valor_pago_legado),
            "desconto_ajuste": str(pedido.desconto_ajuste),
            "forma_pagamento_legada": pedido.forma_pagamento_legada,
            "prioridade": pedido.prioridade,
            "status": pedido.status,
            "estado_comercial": pedido.estado_comercial,
            "estado_entrega": pedido.estado_entrega,
            "canal_atendimento": pedido.canal_atendimento,
            "usuario_cadastro": pedido.usuario_cadastro,
        },
        "cliente": {
            "nome": pedido.cliente.nome,
            "email": pedido.cliente.email,
            "telefone_principal": pedido.cliente.telefone_principal,
            "telefone_secundario": pedido.cliente.telefone_secundario,
            "cpf_cnpj": pedido.cliente.cpf_cnpj,
            "endereco": pedido.cliente.endereco,
        },
        "itens": [
            {
                "ordem": item.ordem,
                "nome": item.nome,
                "descricao": item.descricao,
                "quantidade": str(item.quantidade),
                "preco_unitario": str(item.preco_unitario),
                "custo_unitario_estimado": str(item.custo_unitario_estimado),
            }
            for item in pedido.itens.all()
        ],
        "pagamentos": [
            {
                "valor": str(pagamento.valor),
                "forma": pagamento.forma,
                "data_pagamento": pagamento.data_pagamento.isoformat() if pagamento.data_pagamento else None,
                "status": pagamento.status,
                "observacoes": pagamento.observacoes,
            }
            for pagamento in pedido.pagamentos.all()
        ],
    }


@transaction.atomic
def enfileirar_pedido_local(*, pedido: Pedido, operador: OperadorGestor, estacao_id: uuid.UUID, versao_politica: str) -> UnidadeSincronizacao:
    if not operador.codigo_origem_offline:
        raise SincronizacaoInvalida("Operador sem codigo permanente de origem offline.")
    existente = UnidadeSincronizacao.objects.filter(pedido_local=pedido).first()
    if existente:
        return existente
    sequencia, _ = SequenciaOffline.objects.select_for_update().get_or_create(estacao_id=estacao_id, codigo_origem=operador.codigo_origem_offline)
    sequencia.ultimo_numero += 1
    sequencia.save(update_fields=["ultimo_numero"])
    entidade_id = uuid.uuid4()
    codigo_visivel = f"{operador.codigo_origem_offline}{sequencia.ultimo_numero}"
    pedido.identificador_offline = entidade_id
    pedido.codigo_visivel_offline = codigo_visivel
    pedido.estacao_origem_offline = estacao_id
    pedido.origem_offline = True
    pedido.save(update_fields=["identificador_offline", "codigo_visivel_offline", "estacao_origem_offline", "origem_offline"])
    payload = _snapshot_pedido(pedido)
    unidade = UnidadeSincronizacao.objects.create(entidade_local_id=entidade_id, pedido_local=pedido, estacao_id=estacao_id, operador=operador, codigo_visivel=codigo_visivel, sequencia_local=sequencia.ultimo_numero, versao_politica=versao_politica, payload=payload, checksum=calcular_checksum(payload))
    registrar_evento(tipo="PedidoOfflineCriado", operador=operador, origem="cliente_offline", origem_offline=True, alvo_tipo="Pedido", alvo_id=str(entidade_id), acao="criar_e_enfileirar", valores_anteriores={}, valores_posteriores={"codigo_visivel": codigo_visivel}, chave_idempotencia=f"offline-criar:{entidade_id}", metadados={"estacao_id": str(estacao_id), "sequencia_local": sequencia.ultimo_numero, "versao_politica": versao_politica})
    return unidade


def envelope_da_unidade(unidade: UnidadeSincronizacao) -> dict:
    return {"chave_idempotencia": str(unidade.chave_idempotencia), "entidade_local_id": str(unidade.entidade_local_id), "estacao_id": str(unidade.estacao_id), "codigo_origem": unidade.operador.codigo_origem_offline, "codigo_visivel": unidade.codigo_visivel, "sequencia_local": unidade.sequencia_local, "versao_esquema": unidade.versao_esquema, "versao_politica": unidade.versao_politica, "payload": unidade.payload, "checksum": unidade.checksum}


def _validar_envelope(envelope: dict) -> tuple[uuid.UUID, uuid.UUID, uuid.UUID]:
    try:
        chave = uuid.UUID(envelope["chave_idempotencia"])
        entidade = uuid.UUID(envelope["entidade_local_id"])
        estacao = uuid.UUID(envelope["estacao_id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SincronizacaoInvalida("Identificadores tecnicos invalidos.") from exc
    if envelope.get("versao_esquema") != 1:
        raise SincronizacaoInvalida("Versao de esquema incompativel.")
    if calcular_checksum(envelope.get("payload", {})) != envelope.get("checksum"):
        raise SincronizacaoInvalida("Conteudo corrompido ou incompleto.")
    return chave, entidade, estacao


@transaction.atomic
def incorporar_pedido_offline(
    envelope: dict, *, estacao_autenticada: EstacaoCliente
) -> ResultadoIncorporacao:
    chave, entidade, estacao = _validar_envelope(envelope)
    if not estacao_autenticada.ativa or estacao != estacao_autenticada.pk:
        raise SincronizacaoInvalida("Estacao do pacote nao corresponde a origem autenticada.")
    existente = IncorporacaoOffline.objects.select_related("pedido_global").filter(chave_idempotencia=chave).first()
    if existente:
        if existente.checksum != envelope["checksum"]:
            raise SincronizacaoInvalida("Chave idempotente reutilizada com outro conteudo.")
        return ResultadoIncorporacao(existente.pedido_global, True)
    if IncorporacaoOffline.objects.filter(entidade_local_id=entidade).exists():
        raise SincronizacaoInvalida("Entidade local ja incorporada por outra operacao.")
    try:
        operador = OperadorGestor.objects.get(codigo_origem_offline=envelope["codigo_origem"])
    except (KeyError, OperadorGestor.DoesNotExist) as exc:
        raise SincronizacaoInvalida("Autoria offline nao reconhecida pela Central.") from exc
    dados = envelope["payload"]
    cliente = Cliente.objects.create(**dados["cliente"])
    pedido = Pedido.objects.create(cliente=cliente, identificador_offline=entidade, codigo_visivel_offline=envelope["codigo_visivel"], estacao_origem_offline=estacao, origem_offline=True, **dados["pedido"])
    for item in dados.get("itens", []):
        PedidoItem.objects.create(pedido=pedido, **item)
    for pagamento in dados.get("pagamentos", []):
        PagamentoPedido.objects.create(pedido=pedido, **pagamento)
    incorporacao = IncorporacaoOffline.objects.create(chave_idempotencia=chave, entidade_local_id=entidade, estacao_id=estacao, codigo_visivel=envelope["codigo_visivel"], pedido_global=pedido, checksum=envelope["checksum"])
    registrar_evento(tipo="PedidoOfflineIncorporado", operador=operador, origem="sincronizacao_central", alvo_tipo="Pedido", alvo_id=str(pedido.pk), acao="incorporar_pedido_offline", valores_anteriores={}, valores_posteriores={"identificador_offline": str(entidade), "codigo_visivel": envelope["codigo_visivel"]}, chave_idempotencia=f"offline-incorporar:{chave}", metadados={"estacao_id": str(estacao), "sequencia_local": envelope["sequencia_local"], "versao_politica": envelope["versao_politica"], "incorporacao_id": incorporacao.pk})
    return ResultadoIncorporacao(pedido, False)


def registrar_falha(unidade: UnidadeSincronizacao, motivo: str) -> None:
    unidade.tentativas += 1
    unidade.ultima_tentativa_em = timezone.now()
    unidade.ultimo_resultado = "FALHA"
    unidade.motivo_falha = motivo
    unidade.estado = "FALHA_TEMPORARIA"
    unidade.save(update_fields=["tentativas", "ultima_tentativa_em", "ultimo_resultado", "motivo_falha", "estado", "atualizada_em"])


@transaction.atomic
def preparar_proxima_unidade() -> UnidadeSincronizacao | None:
    agora = timezone.now()
    unidade = (
        UnidadeSincronizacao.objects.select_for_update()
        .filter(
            estado__in=[
                EstadoUnidade.AGUARDANDO,
                EstadoUnidade.FALHA_TEMPORARIA,
                EstadoUnidade.PREPARANDO,
                EstadoUnidade.ENVIANDO,
            ]
        )
        .filter(Q(proxima_tentativa_em__isnull=True) | Q(proxima_tentativa_em__lte=agora))
        .order_by("sequencia_local", "criada_em")
        .first()
    )
    if unidade is None:
        return None
    unidade.estado = EstadoUnidade.ENVIANDO
    unidade.tentativas += 1
    unidade.ultima_tentativa_em = agora
    unidade.ultimo_resultado = "ENVIANDO"
    unidade.motivo_falha = ""
    unidade.proxima_tentativa_em = None
    unidade.save(
        update_fields=[
            "estado",
            "tentativas",
            "ultima_tentativa_em",
            "ultimo_resultado",
            "motivo_falha",
            "proxima_tentativa_em",
            "atualizada_em",
        ]
    )
    return unidade


@transaction.atomic
def confirmar_unidade(unidade: UnidadeSincronizacao, confirmacao: dict) -> None:
    unidade = UnidadeSincronizacao.objects.select_for_update().get(pk=unidade.pk)
    codigo = str(confirmacao.get("codigo") or "")
    if codigo not in {"INCORPORADO", "JA_INCORPORADO"}:
        raise SincronizacaoInvalida("Confirmacao central desconhecida.")
    if str(confirmacao.get("identificador_offline") or "") != str(unidade.entidade_local_id):
        raise SincronizacaoInvalida("Confirmacao central pertence a outra entidade.")
    try:
        pedido_global_id = int(confirmacao["pedido_global_id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SincronizacaoInvalida("Confirmacao central sem Pedido global valido.") from exc
    if pedido_global_id <= 0:
        raise SincronizacaoInvalida("Confirmacao central sem Pedido global valido.")

    unidade.estado = EstadoUnidade.INCORPORADA
    unidade.codigo_confirmacao = codigo
    unidade.pedido_global_id_confirmado = pedido_global_id
    unidade.incorporada_em = timezone.now()
    unidade.ultimo_resultado = codigo
    unidade.motivo_falha = ""
    unidade.proxima_tentativa_em = None
    unidade.save(
        update_fields=[
            "estado",
            "codigo_confirmacao",
            "pedido_global_id_confirmado",
            "incorporada_em",
            "ultimo_resultado",
            "motivo_falha",
            "proxima_tentativa_em",
            "atualizada_em",
        ]
    )
    registrar_evento(
        tipo="PedidoOfflineConfirmado",
        operador=unidade.operador,
        origem="cliente_offline",
        origem_offline=True,
        alvo_tipo="Pedido",
        alvo_id=str(unidade.entidade_local_id),
        acao="confirmar_incorporacao_central",
        valores_anteriores={"estado_sincronizacao": EstadoUnidade.ENVIANDO},
        valores_posteriores={
            "estado_sincronizacao": EstadoUnidade.INCORPORADA,
            "pedido_global_id": pedido_global_id,
            "codigo_confirmacao": codigo,
        },
        chave_idempotencia=f"offline-confirmar:{unidade.chave_idempotencia}",
        metadados={"estacao_id": str(unidade.estacao_id)},
    )


@transaction.atomic
def reagendar_unidade(unidade: UnidadeSincronizacao, motivo: str, *, permanente: bool = False) -> None:
    unidade = UnidadeSincronizacao.objects.select_for_update().get(pk=unidade.pk)
    unidade.estado = EstadoUnidade.REQUER_ATENCAO if permanente else EstadoUnidade.FALHA_TEMPORARIA
    unidade.ultimo_resultado = "RECUSADA" if permanente else "FALHA_TEMPORARIA"
    unidade.motivo_falha = motivo[:2000]
    unidade.proxima_tentativa_em = None if permanente else timezone.now() + timedelta(
        seconds=min(30 * (2 ** max(unidade.tentativas - 1, 0)), 1800)
    )
    unidade.save(
        update_fields=[
            "estado",
            "ultimo_resultado",
            "motivo_falha",
            "proxima_tentativa_em",
            "atualizada_em",
        ]
    )

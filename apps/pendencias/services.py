from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.models import OperadorGestor
from apps.operacao.models import Processo

from .models import EstadoPendencia, FormaEncerramentoPendencia, Pendencia

TIPO_BLOQUEIO_PROCESSO = "BLOQUEIO_PROCESSO"


@transaction.atomic
def abrir_pendencia_bloqueio(
    *, processo: Processo, responsavel: OperadorGestor, descricao: str
) -> Pendencia:
    pendencia, criada = Pendencia.objects.get_or_create(
        processo=processo,
        tipo=TIPO_BLOQUEIO_PROCESSO,
        encerrada_em__isnull=True,
        defaults={
            "pedido": processo.pedido,
            "descricao": descricao,
            "responsavel_principal": responsavel,
        },
    )
    if not criada:
        return pendencia
    registrar_evento(
        tipo="PendenciaCriada",
        operador=responsavel,
        origem="operacao",
        alvo_tipo="Pendencia",
        alvo_id=str(pendencia.pk),
        acao="criar",
        valores_anteriores={},
        valores_posteriores={"estado": pendencia.estado, "tipo": pendencia.tipo},
        metadados={"processo_id": str(processo.pk), "pedido_id": processo.pedido_id},
    )
    return pendencia


@transaction.atomic
def encerrar_pendencia_bloqueio(
    *, processo: Processo, operador: OperadorGestor, forma: str
) -> Pendencia | None:
    pendencia = Pendencia.objects.filter(
        processo=processo,
        tipo=TIPO_BLOQUEIO_PROCESSO,
        encerrada_em__isnull=True,
    ).first()
    if pendencia is None:
        return None
    pendencia.estado = EstadoPendencia.ENCERRADA
    pendencia.forma_encerramento = forma
    pendencia.encerrada_por = operador
    pendencia.encerrada_em = timezone.now()
    pendencia.save(
        update_fields=["estado", "forma_encerramento", "encerrada_por", "encerrada_em"]
    )
    registrar_evento(
        tipo="PendenciaEncerrada",
        operador=operador,
        origem="operacao",
        alvo_tipo="Pendencia",
        alvo_id=str(pendencia.pk),
        acao="encerrar",
        valores_anteriores={"estado": EstadoPendencia.ABERTA},
        valores_posteriores={
            "estado": pendencia.estado,
            "forma_encerramento": pendencia.forma_encerramento,
        },
        metadados={"processo_id": str(processo.pk), "pedido_id": processo.pedido_id},
    )
    return pendencia

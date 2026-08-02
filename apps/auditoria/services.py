import uuid

from django.utils import timezone

from apps.auditoria.models import EventoOperacional, ResultadoEvento


def registrar_evento(
    *,
    tipo: str,
    operador,
    origem: str,
    alvo_tipo: str,
    alvo_id: str,
    acao: str,
    valores_anteriores: dict,
    valores_posteriores: dict,
    correlacao_id: uuid.UUID | None = None,
    chave_idempotencia: str | None = None,
    metadados: dict | None = None,
    resultado: str = ResultadoEvento.CONCLUIDO,
    origem_offline: bool = False,
) -> EventoOperacional:
    if chave_idempotencia:
        existente = EventoOperacional.objects.filter(
            chave_idempotencia=chave_idempotencia
        ).first()
        if existente:
            return existente
    return EventoOperacional.objects.create(
        tipo=tipo,
        ocorrido_em=timezone.now(),
        operador=operador,
        origem=origem,
        origem_offline=origem_offline,
        alvo_tipo=alvo_tipo,
        alvo_id=str(alvo_id),
        acao=acao,
        valores_anteriores=valores_anteriores,
        valores_posteriores=valores_posteriores,
        correlacao_id=correlacao_id or uuid.uuid4(),
        chave_idempotencia=chave_idempotencia,
        resultado=resultado,
        metadados=metadados or {},
    )

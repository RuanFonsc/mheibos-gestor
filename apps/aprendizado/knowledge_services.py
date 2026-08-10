from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.models import PapelOperador
from .models import CamadaConhecimento, Conhecimento, EstadoConhecimento


def buscar_conhecimento(*, consulta, operador=None, camadas=None, limite=20):
    """Busca determinística; não chama IA e só retorna conteúdo aprovado."""
    consulta = (consulta or "").strip()
    if not consulta:
        return Conhecimento.objects.none()
    palavras = [p for p in consulta.lower().split() if len(p) > 2]
    if not palavras:
        return Conhecimento.objects.none()
    queryset = Conhecimento.objects.filter(estado=EstadoConhecimento.APROVADO)
    if camadas:
        queryset = queryset.filter(camada__in=list(camadas))
    agora = timezone.now()
    queryset = queryset.filter(valido_de__isnull=True) | queryset.filter(valido_de__lte=agora)
    queryset = queryset.exclude(valido_ate__lt=agora)
    itens = list(queryset.order_by("-atualizado_em")[:200])
    ordenados = sorted(
        itens,
        key=lambda item: sum(p in f"{item.titulo} {item.conteudo}".lower() for p in palavras),
        reverse=True,
    )
    return ordenados[:limite]


@transaction.atomic
def registrar_conhecimento(*, operador, titulo, conteudo, camada, fonte):
    if not operador or not operador.ativo or operador.papel == PapelOperador.TEMPORARIO:
        raise PermissionDenied("Somente uma identidade ativa pode registrar conhecimento.")
    if camada not in CamadaConhecimento.values:
        raise ValidationError("Camada de conhecimento inválida.")
    titulo, conteudo, fonte = [(valor or "").strip() for valor in (titulo, conteudo, fonte)]
    if not titulo or not conteudo or not fonte:
        raise ValidationError("Título, conteúdo e fonte são obrigatórios.")
    item = Conhecimento.objects.create(
        titulo=titulo, conteudo=conteudo, camada=camada, fonte=fonte, autor=operador,
    )
    registrar_evento(
        tipo="ConhecimentoRegistrado", operador=operador, origem="aprendizado_web",
        alvo_tipo="Conhecimento", alvo_id=str(item.pk), acao="registrar_conhecimento",
        valores_anteriores={}, valores_posteriores={"estado": item.estado, "camada": item.camada},
    )
    return item


@transaction.atomic
def aprovar_conhecimento(*, conhecimento, operador):
    if not operador or not operador.ativo or not operador.is_admin:
        raise PermissionDenied("Somente gerente ou administrador pode aprovar conhecimento.")
    item = Conhecimento.objects.select_for_update().get(pk=conhecimento.pk)
    if item.estado == EstadoConhecimento.APROVADO:
        return item
    if item.estado != EstadoConhecimento.PENDENTE:
        raise ValidationError("Somente conhecimento pendente pode ser aprovado.")
    anterior = item.estado
    item.estado = EstadoConhecimento.APROVADO
    item.versao += 1
    item.save(update_fields=["estado", "versao", "atualizado_em"])
    registrar_evento(
        tipo="ConhecimentoAprovado", operador=operador, origem="aprendizado_web",
        alvo_tipo="Conhecimento", alvo_id=str(item.pk), acao="aprovar_conhecimento",
        valores_anteriores={"estado": anterior}, valores_posteriores={"estado": item.estado, "versao": item.versao},
    )
    return item

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from apps.auditoria.services import registrar_evento
from apps.catalogo.models import PapelOperador
from .models import EstadoMissao, Missao, OrigemMissao


@transaction.atomic
def criar_missao_individual_voluntaria(*, operador, titulo, objetivo, criterio_conclusao, resultado_esperado=""):
    if not operador or not operador.ativo or operador.papel == PapelOperador.TEMPORARIO:
        raise PermissionDenied("Somente uma identidade ativa pode criar uma missão.")
    campos = {"titulo": (titulo or "").strip(), "objetivo": (objetivo or "").strip(), "criterio_conclusao": (criterio_conclusao or "").strip()}
    if not all(campos.values()):
        raise ValidationError("Título, objetivo e critério de conclusão são obrigatórios.")
    missao = Missao.objects.create(**campos, resultado_esperado=(resultado_esperado or "").strip(), origem=OrigemMissao.VOLUNTARIA, estado=EstadoMissao.PLANEJADA, criador=operador, responsavel_principal=operador)
    registrar_evento(tipo="MissaoCriada", operador=operador, origem="missoes_web", alvo_tipo="Missao", alvo_id=str(missao.pk), acao="criar_missao_individual_voluntaria", valores_anteriores={}, valores_posteriores={"origem": missao.origem, "estado": missao.estado, "responsavel_principal_id": operador.pk})
    return missao

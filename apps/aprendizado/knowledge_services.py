from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.models import PapelOperador
from .models import CamadaConhecimento, Conhecimento, EstadoConhecimento, MemoriaOperacional


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
    queryset = queryset.filter(Q(valido_de__isnull=True) | Q(valido_de__lte=agora))
    queryset = queryset.filter(Q(valido_ate__isnull=True) | Q(valido_ate__gt=agora))
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


@transaction.atomic
def guardar_memoria(*, operador, chave, conteudo, curta=True, expira_em=None, fonte="sessao_mheibos"):
    if not operador or not operador.ativo:
        raise PermissionDenied("Somente uma identidade ativa pode guardar memória.")
    chave = (chave or "").strip()
    if not chave or not isinstance(conteudo, dict):
        raise ValidationError("Chave e conteúdo estruturado são obrigatórios.")
    anterior = MemoriaOperacional.objects.filter(operador=operador, chave=chave).first()
    memoria, criada = MemoriaOperacional.objects.update_or_create(
        operador=operador,
        chave=chave,
        defaults={
            "conteudo": conteudo,
            "curta": bool(curta),
            "expira_em": expira_em,
            "fonte": fonte or "sessao_mheibos",
        },
    )
    registrar_evento(
        tipo="MemoriaOperacionalGuardada",
        operador=operador,
        origem="aprendizado_servico",
        alvo_tipo="MemoriaOperacional",
        alvo_id=str(memoria.pk),
        acao="criar_memoria" if criada else "atualizar_memoria",
        valores_anteriores=(
            {}
            if anterior is None
            else {"conteudo": anterior.conteudo, "curta": anterior.curta, "expira_em": anterior.expira_em.isoformat() if anterior.expira_em else None}
        ),
        valores_posteriores={"curta": memoria.curta, "expira_em": memoria.expira_em.isoformat() if memoria.expira_em else None},
    )
    return memoria


def recuperar_memorias(*, operador, curta=None, chave=None):
    if not operador or not operador.ativo:
        raise PermissionDenied("Identidade inválida para recuperar memória.")
    queryset = MemoriaOperacional.objects.filter(operador=operador)
    if curta is not None:
        queryset = queryset.filter(curta=curta)
    if chave:
        queryset = queryset.filter(chave=chave)
    agora = timezone.now()
    return queryset.filter(Q(expira_em__isnull=True) | Q(expira_em__gt=agora)).order_by("-atualizada_em", "-id")


def recuperar_contexto(
    *, operador, consulta, camadas=None, contexto_atual=None,
    limite_conhecimento=20, limite_memorias=20,
):
    """Monta contexto transversal determinístico sem depender de um modelo de IA."""
    consulta = (consulta or "").strip()
    conhecimento = buscar_conhecimento(
        consulta=consulta,
        operador=operador,
        camadas=camadas,
        limite=limite_conhecimento,
    )
    memorias = list(recuperar_memorias(operador=operador)[:limite_memorias])
    return {
        "consulta": consulta,
        "conhecimento": conhecimento,
        "memorias": memorias,
        "contexto_atual": contexto_atual if isinstance(contexto_atual, dict) else {},
        "ia_necessaria": False,
        "fontes": [
            *({"tipo": "conhecimento", "id": item.pk, "camada": item.camada} for item in conhecimento),
            *({"tipo": "memoria", "id": item.pk, "curta": item.curta} for item in memorias),
        ],
    }

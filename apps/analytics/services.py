from datetime import timedelta

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.models import PapelOperador
from apps.missoes.services import criar_missao_individual_voluntaria
from apps.pedidos.models import Pedido, PrioridadePedido, StatusPedido

from .models import Analise, EstadoSimulacao, EvidenciaAnalitica, Simulacao, TipoEvidencia


def _exigir_operador(operador):
    if not operador or not operador.ativo or operador.papel == PapelOperador.TEMPORARIO:
        raise PermissionDenied("Somente uma identidade ativa pode usar o Analytics.")


def obter_metricas_operacionais(*, operador):
    """Projeta fatos atuais do domínio; não interpreta nem chama IA."""
    _exigir_operador(operador)
    pedidos = Pedido.objects.exclude(status=StatusPedido.CANCELADO)
    if not operador.is_admin:
        pedidos = pedidos.filter(usuario_cadastro__iexact=operador.nome)
    hoje = timezone.localdate()
    limite = hoje + timedelta(days=2)
    return {
        "pedidos_ativos": pedidos.count(),
        "aguardando_arte": pedidos.filter(status=StatusPedido.AGUARDANDO_ARTE).count(),
        "em_preparacao_arte": pedidos.filter(status=StatusPedido.ARTE_EM_PREPARO).count(),
        "em_producao": pedidos.filter(status=StatusPedido.EM_PRODUCAO).count(),
        "prontos_entrega": pedidos.filter(status=StatusPedido.PRONTO).count(),
        "prioridade_urgente": pedidos.filter(prioridade=PrioridadePedido.URGENTE).count(),
        "prazo_proximo": pedidos.filter(data_entrega__isnull=False, data_entrega__range=(hoje, limite)).count(),
        "fonte": "Pedido/Processo oficial",
    }


@transaction.atomic
def registrar_evidencia(*, operador, titulo, descricao, tipo, fonte, dados=None, confianca=100, referencia=""):
    _exigir_operador(operador)
    if tipo not in TipoEvidencia.values:
        raise ValidationError("Tipo de evidência inválido.")
    titulo, descricao, fonte = [(valor or "").strip() for valor in (titulo, descricao, fonte)]
    if not titulo or not descricao or not fonte:
        raise ValidationError("Título, descrição e fonte são obrigatórios.")
    if not isinstance(dados or {}, dict) or not 0 <= int(confianca) <= 100:
        raise ValidationError("Dados devem ser estruturados e a confiança deve estar entre 0 e 100.")
    evidencia = EvidenciaAnalitica.objects.create(titulo=titulo, descricao=descricao, tipo=tipo, fonte=fonte, referencia=(referencia or "").strip(), dados=dados or {}, confianca=int(confianca), coletada_em=timezone.now(), autor=operador)
    registrar_evento(tipo="EvidenciaAnaliticaRegistrada", operador=operador, origem="analytics_deterministico", alvo_tipo="EvidenciaAnalitica", alvo_id=str(evidencia.pk), acao="registrar_evidencia", valores_anteriores={}, valores_posteriores={"tipo": evidencia.tipo, "fonte": evidencia.fonte})
    return evidencia


@transaction.atomic
def criar_analise_deterministica(*, operador, pergunta, resumo, evidencias=(), confianca=0):
    _exigir_operador(operador)
    pergunta, resumo = [(valor or "").strip() for valor in (pergunta, resumo)]
    if not pergunta or not resumo:
        raise ValidationError("Pergunta e resumo são obrigatórios.")
    if not 0 <= int(confianca) <= 100:
        raise ValidationError("A confiança deve estar entre 0 e 100.")
    evidencias = list(evidencias or [])
    if not evidencias:
        raise ValidationError("Uma análise precisa preservar ao menos uma evidência.")
    if any(not isinstance(item, EvidenciaAnalitica) for item in evidencias):
        raise ValidationError("As evidências precisam ser registros oficiais do Analytics.")
    analise = Analise.objects.create(pergunta=pergunta, resumo=resumo, confianca=int(confianca), autor=operador)
    analise.evidencias.set(evidencias)
    registrar_evento(tipo="AnaliseDeterministicaCriada", operador=operador, origem="analytics_deterministico", alvo_tipo="Analise", alvo_id=str(analise.pk), acao="criar_analise", valores_anteriores={}, valores_posteriores={"confianca": analise.confianca, "evidencias": [item.pk for item in evidencias]})
    return analise


@transaction.atomic
def validar_analise(*, analise, operador):
    _exigir_operador(operador)
    if not operador.is_admin:
        raise PermissionDenied("Somente gerente ou administrador pode validar uma análise.")
    analise = Analise.objects.select_for_update().get(pk=analise.pk)
    if not analise.evidencias.exists():
        raise ValidationError("Não é possível validar análise sem evidências.")
    analise.estado = "VALIDADA"
    analise.save(update_fields=["estado", "atualizada_em"])
    registrar_evento(
        tipo="AnaliseValidada", operador=operador, origem="analytics_deterministico",
        alvo_tipo="Analise", alvo_id=str(analise.pk), acao="validar_analise",
        valores_anteriores={"estado": "RASCUNHO"}, valores_posteriores={"estado": analise.estado},
    )
    return analise


@transaction.atomic
def salvar_simulacao(*, operador, titulo, objetivo, premissas, resultado, validade_ate=None):
    _exigir_operador(operador)
    titulo, objetivo = [(valor or "").strip() for valor in (titulo, objetivo)]
    if not titulo or not objetivo or not isinstance(premissas, dict) or not isinstance(resultado, dict):
        raise ValidationError("Simulação exige título, objetivo, premissas e resultado estruturados.")
    if not premissas or not resultado:
        raise ValidationError("Sem dados internos suficientes, a simulação deve ser bloqueada.")
    if validade_ate and validade_ate <= timezone.now():
        raise ValidationError("A validade da simulação deve estar no futuro.")
    simulacao = Simulacao.objects.create(titulo=titulo, objetivo=objetivo, premissas=premissas, resultado=resultado, validade_ate=validade_ate, autor=operador)
    registrar_evento(tipo="SimulacaoSalva", operador=operador, origem="analytics_deterministico", alvo_tipo="Simulacao", alvo_id=str(simulacao.pk), acao="salvar_simulacao", valores_anteriores={}, valores_posteriores={"estado": simulacao.estado})
    return simulacao


def promover_simulacao_para_missao(*, simulacao, operador):
    _exigir_operador(operador)
    expirou = False
    missao = None
    with transaction.atomic():
        simulacao = Simulacao.objects.select_for_update().get(pk=simulacao.pk)
        if simulacao.autor_id != operador.pk and not operador.is_admin:
            raise PermissionDenied("Somente o autor ou administrador pode promover a simulação.")
        if simulacao.estado != EstadoSimulacao.SALVA:
            raise ValidationError("Somente uma simulação salva pode ser promovida.")
        if simulacao.validade_ate and simulacao.validade_ate <= timezone.now():
            simulacao.estado = EstadoSimulacao.EXPIRADA
            simulacao.save(update_fields=["estado", "atualizada_em"])
            expirou = True
        else:
            missao = criar_missao_individual_voluntaria(operador=operador, titulo=simulacao.titulo, objetivo=simulacao.objetivo, criterio_conclusao="Executar o cenário aprovado e registrar o resultado real.", resultado_esperado=str(simulacao.resultado))
            simulacao.estado = EstadoSimulacao.PROMOVIDA
            simulacao.missao = missao
            simulacao.save(update_fields=["estado", "missao", "atualizada_em"])
            registrar_evento(tipo="SimulacaoPromovidaParaMissao", operador=operador, origem="analytics_deterministico", alvo_tipo="Simulacao", alvo_id=str(simulacao.pk), acao="promover_simulacao", valores_anteriores={"estado": EstadoSimulacao.SALVA}, valores_posteriores={"estado": simulacao.estado, "missao_id": str(missao.pk)})
    if expirou:
        raise ValidationError("A simulação expirou e não pode ser promovida.")
    return missao

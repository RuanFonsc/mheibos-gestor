from datetime import date, timedelta
from typing import Any, cast

from django.core.exceptions import PermissionDenied, ValidationError
from django.test import RequestFactory, TestCase
from django.utils import timezone

from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.catalogo.authentication import SESSION_OPERATOR_ID
from apps.missoes.models import EstadoMissao

from .models import EstadoAnalise, EstadoSimulacao, TipoEvidencia
from .services import (
    criar_analise_deterministica,
    gerar_relatorio_operacional,
    obter_metricas_operacionais,
    promover_simulacao_para_missao,
    registrar_evidencia,
    salvar_simulacao,
    validar_analise,
)
from .views import analytics_home, dashboard


class AnalyticsDeterministicoTests(TestCase):
    def setUp(self):
        self.admin = OperadorGestor.objects.create(nome="Admin Analytics", papel=PapelOperador.ADMIN)
        self.usuario = OperadorGestor.objects.create(nome="Usuario Analytics", papel=PapelOperador.USUARIO)

    def test_evidencia_analise_preservam_tipo_confianca_e_fonte(self):
        evidencia = registrar_evidencia(
            operador=self.usuario,
            titulo="Prazo do pedido",
            descricao="O prazo está próximo do limite.",
            tipo=TipoEvidencia.FATO,
            fonte="pedido:42",
            dados={"dias": 1},
            confianca=90,
        )
        analise = criar_analise_deterministica(
            operador=self.usuario,
            pergunta="Por que o pedido exige atenção?",
            resumo="Fato: resta um dia. Inferência: a fila deve ser priorizada.",
            evidencias=[evidencia],
            confianca=80,
        )

        self.assertEqual(analise.evidencias.get(), evidencia)
        self.assertEqual(analise.confianca, 80)
        self.assertEqual(evidencia.fonte, "pedido:42")

    def test_simulacao_exige_dados_internos_e_pode_virar_missao(self):
        with self.assertRaises(ValidationError):
            salvar_simulacao(operador=self.usuario, titulo="Vazia", objetivo="Testar", premissas={}, resultado={})
        simulacao = salvar_simulacao(
            operador=self.usuario,
            titulo="Reforçar produção",
            objetivo="Avaliar reforço temporário da fila.",
            premissas={"capacidade_atual": 4},
            resultado={"prazo_estimado": 2},
            validade_ate=timezone.now() + timedelta(hours=2),
        )

        missao = promover_simulacao_para_missao(simulacao=simulacao, operador=self.usuario)

        simulacao.refresh_from_db()
        self.assertEqual(simulacao.estado, EstadoSimulacao.PROMOVIDA)
        self.assertEqual(missao.estado, EstadoMissao.PLANEJADA)
        self.assertEqual(simulacao.missao_id, missao.pk)

    def test_simulacao_expirada_nao_pode_ser_promovida(self):
        simulacao = salvar_simulacao(
            operador=self.usuario,
            titulo="Expirada",
            objetivo="Não executar",
            premissas={"origem": "interna"},
            resultado={"status": "incerto"},
            validade_ate=timezone.now() + timedelta(seconds=1),
        )
        simulacao.validade_ate = timezone.now() - timedelta(seconds=1)
        simulacao.save(update_fields=["validade_ate"])

        with self.assertRaises(ValidationError):
            promover_simulacao_para_missao(simulacao=simulacao, operador=self.usuario)

        simulacao.refresh_from_db()
        self.assertEqual(simulacao.estado, EstadoSimulacao.EXPIRADA)

    def test_administrador_pode_promover_simulacao_de_outro_usuario(self):
        simulacao = salvar_simulacao(
            operador=self.usuario,
            titulo="Cenário compartilhado",
            objetivo="Validar intervenção",
            premissas={"fonte": "interna"},
            resultado={"viavel": True},
        )

        missao = promover_simulacao_para_missao(simulacao=simulacao, operador=self.admin)

        self.assertEqual(missao.criador_id, self.admin.pk)

    def test_operador_temporario_nao_pode_registrar_analytics(self):
        temporario = OperadorGestor.objects.create(nome="Temporario Analytics", papel=PapelOperador.TEMPORARIO)

        with self.assertRaises(PermissionDenied):
            registrar_evidencia(operador=temporario, titulo="x", descricao="y", tipo=TipoEvidencia.FATO, fonte="z")

    def test_dashboard_oficial_e_analytics_renderizam(self):
        dashboard_request = RequestFactory().get("/dashboard/")
        analytics_request = RequestFactory().get("/dashboard/analytics/")
        dashboard_request.session = cast(Any, {SESSION_OPERATOR_ID: self.usuario.pk})
        analytics_request.session = cast(Any, {SESSION_OPERATOR_ID: self.usuario.pk})
        dashboard_response = dashboard(dashboard_request)
        analytics_response = analytics_home(analytics_request)

        self.assertEqual(dashboard_response.status_code, 200)
        self.assertEqual(analytics_response.status_code, 200)

    def test_metricas_operacionais_sao_fatos_deterministicos(self):
        metricas = obter_metricas_operacionais(operador=self.usuario)

        self.assertEqual(metricas["pedidos_ativos"], 0)
        self.assertEqual(metricas["aguardando_arte"], 0)
        self.assertEqual(metricas["fonte"], "Pedido/Processo oficial")

    def test_relatorio_do_periodo_preserva_fatos_sem_interpretacao(self):
        relatorio = gerar_relatorio_operacional(operador=self.usuario, inicio=date(2026, 8, 1), fim=date(2026, 8, 10))

        self.assertEqual(relatorio["pedidos"], 0)
        self.assertFalse(relatorio["interpretacao_automatica"])
        self.assertFalse(relatorio["ia_necessaria"])

    def test_validacao_de_analise_exige_autoridade_humana(self):
        evidencia = registrar_evidencia(operador=self.usuario, titulo="Fato", descricao="Fato observado", tipo=TipoEvidencia.FATO, fonte="pedido:1")
        analise = criar_analise_deterministica(operador=self.usuario, pergunta="O que ocorreu?", resumo="O fato ocorreu.", evidencias=[evidencia], confianca=70)

        with self.assertRaises(PermissionDenied):
            validar_analise(analise=analise, operador=self.usuario)
        validar_analise(analise=analise, operador=self.admin)

        analise.refresh_from_db()
        self.assertEqual(analise.estado, EstadoAnalise.VALIDADA)

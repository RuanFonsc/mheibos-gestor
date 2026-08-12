from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido

from .gateway import FALLBACK_RESUMO, GatewayIA, SolicitacaoCognitiva
from .configuracoes_ia import resolve_ai_policy, normalizar_configuracoes_ia


class GatewayIATests(TestCase):
    def test_locked_financial_action_never_becomes_autonomous(self):
        decision = resolve_ai_policy(action="finance.approve_payment", ia_enabled=True)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.blocked_by, "Proteção permanente do Mheibos")

    def test_disabled_ai_keeps_deterministic_path_available(self):
        decision = resolve_ai_policy(action="optional.summary", ia_enabled=False)
        self.assertFalse(decision.allowed)
        self.assertIn("IA desligada", decision.blocked_by)

    def test_mission_autonomy_is_scoped_to_that_mission(self):
        disabled = resolve_ai_policy(action="mission.replan", mission={}, ia_enabled=True)
        enabled = resolve_ai_policy(
            action="mission.replan",
            mission={"ai.mission_autonomy": True},
            ia_enabled=True,
        )
        self.assertFalse(disabled.allowed)
        self.assertTrue(enabled.allowed)

    def test_normalizer_ignores_locked_values(self):
        values = normalizar_configuracoes_ia({"ai.locked_financial": True, "ai.user_mode": "intelligent"})
        self.assertNotIn("ai.locked_financial", values)
        self.assertEqual(values["ai.user_mode"], "intelligent")

    def test_disabled_gateway_returns_non_blocking_fallback(self):
        resposta = GatewayIA(None).solicitar(SolicitacaoCognitiva("teste", "fatos"))

        self.assertFalse(resposta.disponivel)
        self.assertEqual(resposta.texto, FALLBACK_RESUMO)
        self.assertEqual(resposta.codigo, "IA_DESLIGADA")

    def test_provider_failure_returns_non_blocking_fallback(self):
        provedor = Mock(nome="gemini")
        provedor.nome = "gemini"
        provedor.gerar.side_effect = RuntimeError("indisponivel")

        resposta = GatewayIA(provedor, modelo="modelo").solicitar(
            SolicitacaoCognitiva("teste", "fatos")
        )

        self.assertFalse(resposta.disponivel)
        self.assertEqual(resposta.codigo, "PROVEDOR_INDISPONIVEL")

    def test_provider_success_is_a_read_only_response(self):
        provedor = Mock(nome="gemini")
        provedor.nome = "gemini"
        provedor.gerar.return_value = "Resumo sugerido"

        resposta = GatewayIA(provedor, modelo="modelo").solicitar(
            SolicitacaoCognitiva("teste", "fatos")
        )

        self.assertTrue(resposta.disponivel)
        self.assertEqual(resposta.texto, "Resumo sugerido")


class ResumoPedidoTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operador IA", senha="senha", papel=PapelOperador.USUARIO
        )
        self.pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente IA"),
            usuario_cadastro=self.operador.nome,
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

    @override_settings(MHEIBOS_IA_ENABLED=False)
    def test_endpoint_works_with_ai_disabled_and_does_not_change_order(self):
        response = self.client.post(f"/cognicao/pedidos/{self.pedido.pk}/resumo/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fallback seguro")
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.usuario_cadastro, self.operador.nome)
        self.assertTrue(
            EventoOperacional.objects.filter(
                tipo="AssistenciaCognitivaSolicitada", alvo_id=str(self.pedido.pk)
            ).exists()
        )

    @patch("apps.cognicao.views.resumir_pedido")
    def test_audit_failure_does_not_block_assistance(self, resumir):
        from .gateway import RespostaCognitiva

        resumir.return_value = RespostaCognitiva(
            "Resumo", True, "fake", "fake-model", "SUCESSO"
        )
        with patch("apps.cognicao.views.registrar_evento", side_effect=RuntimeError):
            response = self.client.post(
                f"/cognicao/pedidos/{self.pedido.pk}/resumo/"
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resumo")

    def test_endpoint_rejects_get(self):
        response = self.client.get(f"/cognicao/pedidos/{self.pedido.pk}/resumo/")
        self.assertEqual(response.status_code, 405)

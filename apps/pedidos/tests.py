from decimal import Decimal
from types import SimpleNamespace

from unittest.mock import patch

from django.test import SimpleTestCase, TestCase

from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.auditoria.models import EventoOperacional
from apps.clientes.models import Cliente

from .models import (
    PedidoItem,
    PrioridadePedido,
    StatusPedido,
    arte_upload_to,
)
from .models import HistoricoStatusPedido, Pedido
from .use_cases import AlteracaoStatusNegada, alterar_status_pedido


class PedidoDomainBaselineTests(SimpleTestCase):
    """Caracteriza regras puras já existentes, sem depender do banco de produção."""

    def test_item_calculates_subtotal_and_estimated_cost(self):
        item = PedidoItem(
            nome="Banner",
            quantidade=Decimal("2.50"),
            preco_unitario=Decimal("40.00"),
            custo_unitario_estimado=Decimal("12.00"),
        )

        self.assertEqual(item.subtotal, Decimal("100.0000"))
        self.assertEqual(item.custo_total_estimado, Decimal("30.0000"))

    def test_order_defaults_preserve_current_operational_flow(self):
        quantidade = PedidoItem._meta.get_field("quantidade")

        self.assertEqual(getattr(quantidade, "default"), 1)
        self.assertEqual(PrioridadePedido.NORMAL.value, "NORMAL")
        self.assertEqual(StatusPedido.AGUARDANDO_ARTE.value, "AGUARDANDO_ARTE")

    def test_art_upload_path_is_scoped_to_order(self):
        instance = SimpleNamespace(pedido_id=42)

        self.assertEqual(
            arte_upload_to(instance, "arte-final.png"),
            "pedidos/42/artes/arte-final.png",
        )

    def test_art_upload_path_handles_order_not_saved_yet(self):
        instance = SimpleNamespace(pedido_id=None)

        self.assertEqual(
            arte_upload_to(instance, "rascunho.png"),
            "pedidos/sem-pedido/artes/rascunho.png",
        )


class AlterarStatusPedidoTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome="Cliente Teste")
        self.operador = OperadorGestor.objects.create(
            nome="Ana",
            senha="hash-legado",
            papel=PapelOperador.USUARIO,
        )
        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            usuario_cadastro=self.operador.nome,
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_authorized_transition_updates_order_and_records_actor(self, sync_financeiro):
        resultado = alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )

        self.pedido.refresh_from_db()
        historico = HistoricoStatusPedido.objects.get(pedido=self.pedido)
        self.assertTrue(resultado.alterado)
        self.assertEqual(self.pedido.status, StatusPedido.EM_PRODUCAO)
        self.assertEqual(historico.status_anterior, StatusPedido.AGUARDANDO_ARTE)
        self.assertEqual(historico.status_novo, StatusPedido.EM_PRODUCAO)
        self.assertEqual(historico.operador, self.operador)
        evento = EventoOperacional.objects.get(alvo_id=str(self.pedido.pk))
        self.assertEqual(evento.tipo, "PedidoStatusAlterado")
        self.assertEqual(evento.operador, self.operador)
        self.assertEqual(evento.valores_anteriores, {"status": StatusPedido.AGUARDANDO_ARTE})
        self.assertEqual(evento.valores_posteriores, {"status": StatusPedido.EM_PRODUCAO})
        sync_financeiro.assert_called_once_with(self.pedido)

    @patch("apps.pedidos.use_cases.registrar_evento", side_effect=RuntimeError("falha"))
    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_event_failure_rolls_back_status_and_history(self, _sync_financeiro, _evento):
        with self.assertRaises(RuntimeError):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.EM_PRODUCAO,
                operador=self.operador,
            )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertFalse(HistoricoStatusPedido.objects.exists())

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_unauthorized_transition_changes_nothing(self, sync_financeiro):
        outro = OperadorGestor.objects.create(
            nome="Bruno",
            senha="hash-legado",
            papel=PapelOperador.USUARIO,
        )

        with self.assertRaises(AlteracaoStatusNegada):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.EM_PRODUCAO,
                operador=outro,
            )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertFalse(HistoricoStatusPedido.objects.exists())
        sync_financeiro.assert_not_called()

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_repeated_status_is_idempotent(self, sync_financeiro):
        resultado = alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.AGUARDANDO_ARTE,
            operador=self.operador,
        )

        self.assertFalse(resultado.alterado)
        self.assertFalse(HistoricoStatusPedido.objects.exists())
        sync_financeiro.assert_not_called()


class FluxosStatusPedidoIntegrationTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome="Cliente Integração")
        self.operador = OperadorGestor.objects.create(
            nome="Carla",
            senha="hash-legado",
            papel=PapelOperador.USUARIO,
        )
        session = self.client.session
        session["operador_nome"] = self.operador.nome
        session.save()

    def novo_pedido(self, status=StatusPedido.AGUARDANDO_ARTE):
        return Pedido.objects.create(
            cliente=self.cliente,
            usuario_cadastro=self.operador.nome,
            status=status,
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_individual_status_route_uses_audited_use_case(self, _sync_financeiro):
        pedido = self.novo_pedido()

        response = self.client.post(
            f"/pedidos/{pedido.pk}/status/",
            {"status": StatusPedido.EM_PRODUCAO},
        )

        pedido.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(pedido.status, StatusPedido.EM_PRODUCAO)
        self.assertTrue(
            HistoricoStatusPedido.objects.filter(pedido=pedido, operador=self.operador).exists()
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_bulk_status_route_records_each_changed_order(self, _sync_financeiro):
        pedidos = [self.novo_pedido(), self.novo_pedido()]

        response = self.client.post(
            "/pedidos/acao-massa/",
            {
                "acao": "enviar_producao",
                "pedido_ids": [str(pedido.pk) for pedido in pedidos],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(HistoricoStatusPedido.objects.count(), 2)
        self.assertFalse(
            Pedido.objects.filter(pk__in=[pedido.pk for pedido in pedidos]).exclude(
                status=StatusPedido.EM_PRODUCAO
            ).exists()
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_production_rejection_preserves_reason_and_actor(self, _sync_financeiro):
        pedido = self.novo_pedido(StatusPedido.EM_PRODUCAO)

        response = self.client.post(
            f"/pedidos/{pedido.pk}/rejeitar-producao/",
            {"motivo": "Arquivo sem sangria", "next": "/producao/"},
        )

        pedido.refresh_from_db()
        historico = HistoricoStatusPedido.objects.get(pedido=pedido)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertEqual(historico.operador, self.operador)
        self.assertIn("Arquivo sem sangria", historico.observacao)

from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase

from .models import (
    PedidoItem,
    PrioridadePedido,
    StatusPedido,
    arte_upload_to,
)


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

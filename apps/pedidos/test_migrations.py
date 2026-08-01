from decimal import Decimal

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class EstadosIndependentesMigrationTests(TransactionTestCase):
    migrate_from = ("pedidos", "0008_historicostatuspedido_operador")
    migrate_to = ("pedidos", "0009_pedido_estado_comercial_pedido_estado_entrega")

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        targets_from = [self.migrate_from, ("clientes", "0003_cliente_status_cadastro_and_more")]
        executor.migrate(targets_from)
        apps = executor.loader.project_state(targets_from).apps
        Cliente = apps.get_model("clientes", "Cliente")
        Pedido = apps.get_model("pedidos", "Pedido")
        Pagamento = apps.get_model("pedidos", "PagamentoPedido")
        cliente = Cliente.objects.create(nome="Cliente Migracao")
        self.ids = {}
        for nome, status, total in (
            ("cancelado", "CANCELADO", "100.00"),
            ("pronto", "PRONTO", "100.00"),
            ("entregue_quitado", "ENTREGUE", "100.00"),
            ("entregue_pendente", "ENTREGUE", "100.00"),
        ):
            pedido = Pedido.objects.create(
                cliente=cliente,
                status=status,
                valor_total=Decimal(total),
            )
            self.ids[nome] = pedido.pk
        Pagamento.objects.create(
            pedido_id=self.ids["entregue_quitado"],
            valor=Decimal("100.00"),
            status="CONFIRMADO",
        )
        executor = MigrationExecutor(connection)
        targets_to = [self.migrate_to, ("clientes", "0003_cliente_status_cadastro_and_more")]
        executor.migrate(targets_to)
        self.apps = executor.loader.project_state(targets_to).apps

    def tearDown(self):
        MigrationExecutor(connection).migrate([self.migrate_to])
        super().tearDown()

    def test_backfill_preserves_meaning_without_inventing_payment(self):
        Pedido = self.apps.get_model("pedidos", "Pedido")
        cancelado = Pedido.objects.get(pk=self.ids["cancelado"])
        pronto = Pedido.objects.get(pk=self.ids["pronto"])
        entregue_quitado = Pedido.objects.get(pk=self.ids["entregue_quitado"])
        entregue_pendente = Pedido.objects.get(pk=self.ids["entregue_pendente"])

        self.assertEqual(cancelado.estado_comercial, "CANCELADO")
        self.assertEqual(cancelado.estado_entrega, "PENDENTE")
        self.assertEqual(pronto.estado_entrega, "PRONTO")
        self.assertEqual(entregue_quitado.estado_comercial, "CONCLUIDO")
        self.assertEqual(entregue_quitado.estado_entrega, "ENTREGUE")
        self.assertEqual(entregue_pendente.estado_comercial, "CONFIRMADO")
        self.assertEqual(entregue_pendente.estado_entrega, "ENTREGUE")

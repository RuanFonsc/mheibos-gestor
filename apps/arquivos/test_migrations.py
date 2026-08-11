from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from typing import Any, cast


class ArquivoLegadoMigrationTests(TransactionTestCase):
    migrate_from = ("arquivos", None)
    migrate_to = ("arquivos", "0001_initial")

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        targets_from = [
            self.migrate_from,
            ("pedidos", "0010_pedido_codigo_visivel_offline_and_more"),
            ("clientes", "0003_cliente_status_cadastro_and_more"),
        ]
        executor.migrate(targets_from)
        apps = executor.loader.project_state(cast(Any, targets_from[1:])).apps
        Cliente = apps.get_model("clientes", "Cliente")
        Pedido = apps.get_model("pedidos", "Pedido")
        cliente = Cliente.objects.create(nome="Cliente Legado Arquivo")
        self.pedido_id = Pedido.objects.create(
            cliente=cliente,
            caminho_arquivo_corel=r"\\SERVIDOR\Artes\legado.cdr",
        ).pk

        executor = MigrationExecutor(connection)
        executor.migrate([self.migrate_to])
        self.apps = executor.loader.project_state([self.migrate_to]).apps

    def tearDown(self):
        MigrationExecutor(connection).migrate(MigrationExecutor(connection).loader.graph.leaf_nodes())
        super().tearDown()

    def test_backfill_preserva_caminho_sem_inventar_autoria_ou_integridade(self):
        Arquivo = self.apps.get_model("arquivos", "ArquivoOficialArte")
        arquivo = Arquivo.objects.get(pedido_id=self.pedido_id)
        self.assertEqual(arquivo.nome_oficial, "legado.cdr")
        self.assertEqual(arquivo.origem, "LEGADO")
        self.assertEqual(arquivo.estado_integridade, "NAO_VERIFICADO")
        self.assertIsNone(arquivo.criado_por_id)

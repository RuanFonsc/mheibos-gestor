from decimal import Decimal
from types import SimpleNamespace

from unittest.mock import patch

from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.auditoria.models import EventoOperacional
from apps.clientes.models import Cliente
from apps.arquivos.models import ArquivoOficialArte, ExcecaoAusenciaArquivoOficial

from .models import (
    EstadoComercialPedido,
    EstadoEntregaPedido,
    EstadoFinanceiroPedido,
    PagamentoPedido,
    PedidoItem,
    PrioridadePedido,
    StatusPedido,
    arte_upload_to,
)
from .models import ArtePedido, HistoricoStatusPedido, Pedido
from .use_cases import (
    AlteracaoStatusNegada,
    ArteNecessariaParaProducao,
    ArquivoOficialAusenteBloqueiaOperacao,
    EntregaComSaldoNegada,
    alterar_status_pedido,
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
        ArtePedido.objects.create(
            pedido=self.pedido,
            arquivo="pedidos/testes/arte.png",
            nome_original="arte.png",
            criado_por=self.operador,
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_order_without_art_cannot_advance_to_production(self, sync_financeiro):
        self.pedido.artes.update(desvinculado_em=timezone.now())

        with self.assertRaises(ArteNecessariaParaProducao):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.EM_PRODUCAO,
                operador=self.operador,
            )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertFalse(HistoricoStatusPedido.objects.exists())
        sync_financeiro.assert_not_called()

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_arquivo_oficial_ausente_bloqueia_sem_excecao_gerencial(self, sync_financeiro):
        ArquivoOficialArte.objects.create(
            pedido=self.pedido,
            caminho_oficial=r"C:\\Artes\\pedido.cdr",
            nome_oficial="pedido.cdr",
            extensao="cdr",
            ausencia_critica_ativa=True,
        )

        with self.assertRaises(ArquivoOficialAusenteBloqueiaOperacao):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.EM_PRODUCAO,
                operador=self.operador,
            )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertFalse(ExcecaoAusenciaArquivoOficial.objects.exists())
        sync_financeiro.assert_not_called()

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_gerente_autoriza_uma_transicao_e_alerta_permanece(self, _sync_financeiro):
        arquivo = ArquivoOficialArte.objects.create(
            pedido=self.pedido,
            caminho_oficial=r"C:\\Artes\\pedido.cdr",
            nome_oficial="pedido.cdr",
            extensao="cdr",
            ausencia_critica_ativa=True,
        )
        gerente = OperadorGestor.objects.create(
            nome="Gerente",
            senha="senha-gerente",
            papel=PapelOperador.ADMIN,
        )

        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
            autorizador_ausencia=gerente,
            senha_autorizador_ausencia="senha-gerente",
            justificativa_ausencia="Prazo critico; restauracao em andamento.",
        )

        excecao = ExcecaoAusenciaArquivoOficial.objects.get()
        arquivo.refresh_from_db()
        self.assertEqual(excecao.autorizador, gerente)
        self.assertEqual(excecao.solicitante, self.operador)
        self.assertEqual(excecao.acao, "ALTERAR_STATUS:EM_PRODUCAO")
        self.assertTrue(arquivo.ausencia_critica_ativa)

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_excecao_recusa_senha_invalida_e_justificativa_vazia(self, sync_financeiro):
        ArquivoOficialArte.objects.create(
            pedido=self.pedido,
            caminho_oficial=r"C:\\Artes\\pedido.cdr",
            nome_oficial="pedido.cdr",
            extensao="cdr",
            ausencia_critica_ativa=True,
        )
        gerente = OperadorGestor.objects.create(
            nome="Gerente Bloqueio",
            senha="senha-gerente",
            papel=PapelOperador.ADMIN,
        )
        for senha, justificativa in [
            ("senha-invalida", "Urgencia operacional"),
            ("senha-gerente", ""),
        ]:
            with self.assertRaises(ArquivoOficialAusenteBloqueiaOperacao):
                alterar_status_pedido(
                    pedido=self.pedido,
                    novo_status=StatusPedido.EM_PRODUCAO,
                    operador=self.operador,
                    autorizador_ausencia=gerente,
                    senha_autorizador_ausencia=senha,
                    justificativa_ausencia=justificativa,
                )
        self.assertFalse(ExcecaoAusenciaArquivoOficial.objects.exists())
        sync_financeiro.assert_not_called()

    @patch("apps.pedidos.use_cases.registrar_evento", side_effect=RuntimeError("falha"))
    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_falha_da_transicao_reverte_excecao_gerencial(self, _sync, _evento):
        ArquivoOficialArte.objects.create(
            pedido=self.pedido,
            caminho_oficial=r"C:\\Artes\\pedido.cdr",
            nome_oficial="pedido.cdr",
            extensao="cdr",
            ausencia_critica_ativa=True,
        )
        gerente = OperadorGestor.objects.create(
            nome="Gerente Rollback",
            senha="senha-gerente",
            papel=PapelOperador.ADMIN,
        )
        with self.assertRaises(RuntimeError):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.EM_PRODUCAO,
                operador=self.operador,
                autorizador_ausencia=gerente,
                senha_autorizador_ausencia="senha-gerente",
                justificativa_ausencia="Excecao auditada para o teste.",
            )
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertFalse(ExcecaoAusenciaArquivoOficial.objects.exists())

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
        self.assertEqual(
            evento.valores_anteriores["status_legado"], StatusPedido.AGUARDANDO_ARTE
        )
        self.assertEqual(evento.valores_posteriores["status_legado"], StatusPedido.EM_PRODUCAO)
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

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_ready_and_paid_delivery_update_independent_states(self, _sync_financeiro):
        self.pedido.valor_total = Decimal("100.00")
        self.pedido.status = StatusPedido.PRONTO
        self.pedido.estado_entrega = EstadoEntregaPedido.PRONTO
        self.pedido.save(update_fields=["valor_total", "status", "estado_entrega"])
        PagamentoPedido.objects.create(
            pedido=self.pedido,
            valor=Decimal("100.00"),
            status="CONFIRMADO",
        )

        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.ENTREGUE,
            operador=self.operador,
        )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.estado_entrega, EstadoEntregaPedido.ENTREGUE)
        self.assertEqual(self.pedido.estado_comercial, EstadoComercialPedido.CONCLUIDO)
        self.assertEqual(self.pedido.estado_financeiro, EstadoFinanceiroPedido.QUITADO)

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_delivery_with_open_balance_is_refused(self, sync_financeiro):
        self.pedido.valor_total = Decimal("100.00")
        self.pedido.status = StatusPedido.PRONTO
        self.pedido.estado_entrega = EstadoEntregaPedido.PRONTO
        self.pedido.save(update_fields=["valor_total", "status", "estado_entrega"])

        with self.assertRaises(EntregaComSaldoNegada):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.ENTREGUE,
                operador=self.operador,
            )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.PRONTO)
        self.assertEqual(self.pedido.estado_entrega, EstadoEntregaPedido.PRONTO)
        self.assertEqual(self.pedido.estado_financeiro, EstadoFinanceiroPedido.SALDO_EM_ABERTO)
        self.assertFalse(HistoricoStatusPedido.objects.exists())
        sync_financeiro.assert_not_called()

    def test_financial_state_is_derived_from_confirmed_payments(self):
        self.pedido.valor_total = Decimal("100.00")
        self.pedido.save(update_fields=["valor_total"])
        self.assertEqual(self.pedido.estado_financeiro, EstadoFinanceiroPedido.SALDO_EM_ABERTO)
        PagamentoPedido.objects.create(
            pedido=self.pedido,
            valor=Decimal("40.00"),
            status="CONFIRMADO",
        )
        self.assertEqual(self.pedido.estado_financeiro, EstadoFinanceiroPedido.PAGAMENTO_PARCIAL)


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
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            usuario_cadastro=self.operador.nome,
            status=status,
        )
        ArtePedido.objects.create(
            pedido=pedido,
            arquivo=f"pedidos/testes/arte-{pedido.pk}.png",
            nome_original="arte.png",
            criado_por=self.operador,
        )
        return pedido

    def test_detail_exposes_same_operational_projection_as_order_list(self):
        from apps.operacao.services import iniciar_producao_pedido

        pedido = self.novo_pedido(StatusPedido.EM_PRODUCAO)
        iniciar_producao_pedido(pedido=pedido, operador=self.operador)

        response = self.client.get(f"/pedidos/{pedido.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pedido"].projecao.operacional, "Em andamento")
        self.assertEqual(
            response.context["pedido"].projecao.fonte_operacional,
            "PRODUCAO_PEDIDO v1",
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_status_route_keeps_order_without_art_in_preparation(self, _sync_financeiro):
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            usuario_cadastro=self.operador.nome,
            status=StatusPedido.AGUARDANDO_ARTE,
        )

        response = self.client.post(
            f"/pedidos/{pedido.pk}/status/",
            {"status": StatusPedido.EM_PRODUCAO},
        )

        pedido.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertFalse(HistoricoStatusPedido.objects.filter(pedido=pedido).exists())

    def test_art_preparation_queue_includes_order_without_category(self):
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            usuario_cadastro=self.operador.nome,
            status=StatusPedido.AGUARDANDO_ARTE,
            tema="Pedido sem categoria",
        )

        response = self.client.get("/preparacao-arte/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preparação de arte")
        self.assertContains(response, pedido.tema)

    def test_printing_assistance_is_separate_from_art_preparation(self):
        response = self.client.get("/assistencia-envio/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assistência de Impressão")
        self.assertNotIn("aguardando_arte", response.context)
        self.assertContains(response, 'href="/producao/"')

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

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from typing import Any, cast

from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import ArtePedido, Pedido, StatusPedido
from apps.pedidos.use_cases import alterar_status_pedido

from .models import EstadoEtapa, EstadoProcesso, ModeloFluxo, Processo
from .projections import projetar_lista, queryset_com_projecao, queryset_fila_producao
from .services import CODIGO_FLUXO_PRODUCAO, ProcessoEncerrado


class FluxoPilotoProducaoTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operador Producao", senha="senha", papel=PapelOperador.USUARIO
        )
        cliente = Cliente.objects.create(nome="Cliente Operacao")
        self.pedido = Pedido.objects.create(
            cliente=cliente,
            usuario_cadastro=self.operador.nome,
            status=StatusPedido.AGUARDANDO_ARTE,
        )
        ArtePedido.objects.create(
            pedido=self.pedido,
            arquivo="pedidos/testes/arte-operacao.png",
            nome_original="arte-operacao.png",
            criado_por=self.operador,
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_entering_production_instantiates_versioned_flow(self, _financeiro):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )

        processo = Processo.objects.get(pedido=self.pedido)
        etapa = processo.etapas.get()
        self.assertEqual(processo.tipo, CODIGO_FLUXO_PRODUCAO)
        self.assertEqual(processo.estado_operacional, EstadoProcesso.EM_ANDAMENTO)
        self.assertEqual(processo.modelo_codigo_snapshot, CODIGO_FLUXO_PRODUCAO)
        self.assertEqual(processo.modelo_versao_snapshot, 1)
        self.assertEqual(etapa.estado, EstadoEtapa.EM_ANDAMENTO)
        self.assertEqual(etapa.responsavel, self.operador)
        self.assertTrue(
            EventoOperacional.objects.filter(
                tipo="ProcessoConfirmado", alvo_id=str(processo.pk)
            ).exists()
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_ready_concludes_stage_without_changing_commercial_finance(self, _financeiro):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )
        comercial = self.pedido.estado_comercial
        financeiro = self.pedido.estado_financeiro

        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.PRONTO,
            operador=self.operador,
            origem_operacional=True,
        )

        processo = Processo.objects.get(pedido=self.pedido)
        etapa = processo.etapas.get()
        self.pedido.refresh_from_db()
        self.assertEqual(processo.estado_operacional, EstadoProcesso.CONCLUIDO)
        self.assertEqual(etapa.estado, EstadoEtapa.CONCLUIDA)
        self.assertEqual(etapa.concluida_por, self.operador)
        self.assertEqual(self.pedido.estado_comercial, comercial)
        self.assertEqual(self.pedido.estado_financeiro, financeiro)

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_rejection_blocks_process_and_preserves_reason(self, _financeiro):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.AGUARDANDO_ARTE,
            operador=self.operador,
            origem_operacional=True,
            observacao="Arquivo sem sangria",
        )

        processo = Processo.objects.get(pedido=self.pedido)
        etapa = processo.etapas.get()
        self.assertEqual(processo.estado_operacional, EstadoProcesso.BLOQUEADO)
        self.assertEqual(etapa.estado, EstadoEtapa.BLOQUEADA)
        self.assertEqual(etapa.motivo_bloqueio, "Arquivo sem sangria")

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_repeated_production_command_is_idempotent(self, _financeiro):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )
        processo = Processo.objects.get(pedido=self.pedido)
        modelo = processo.modelo_fluxo
        modelo.definicao_etapas = [{"chave": "ALTERADA"}]
        with self.assertRaises(ValidationError):
            modelo.save(update_fields=["definicao_etapas"])

        resultado = alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )

        self.assertFalse(resultado.alterado)
        self.assertEqual(Processo.objects.count(), 1)
        self.assertEqual(ModeloFluxo.objects.count(), 1)
        self.assertEqual(processo.etapas.count(), 1)

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_blocked_process_can_resume_explicitly(self, _financeiro):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.AGUARDANDO_ARTE,
            operador=self.operador,
            origem_operacional=True,
            observacao="Corrigir arquivo",
        )
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )

        processo = Processo.objects.get(pedido=self.pedido)
        etapa = processo.etapas.get()
        self.assertEqual(processo.estado_operacional, EstadoProcesso.EM_ANDAMENTO)
        self.assertEqual(etapa.estado, EstadoEtapa.EM_ANDAMENTO)
        self.assertEqual(etapa.motivo_bloqueio, "")

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_finished_process_cannot_be_reopened_by_legacy_status(self, _financeiro):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.PRONTO,
            operador=self.operador,
            origem_operacional=True,
        )

        with self.assertRaises(ProcessoEncerrado):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.EM_PRODUCAO,
                operador=self.operador,
            )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.PRONTO)

    @patch("apps.operacao.services.registrar_evento", side_effect=RuntimeError("falha"))
    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_process_event_failure_rolls_back_order_and_flow(self, _financeiro, _evento):
        with self.assertRaises(RuntimeError):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.EM_PRODUCAO,
                operador=self.operador,
            )

        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, StatusPedido.AGUARDANDO_ARTE)
        self.assertFalse(Processo.objects.exists())


class ProjecaoOperacionalIntegradaTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Vendedor Integrado", senha="senha", papel=PapelOperador.USUARIO
        )
        cliente = Cliente.objects.create(nome="Cliente Projecao")
        self.pedido = Pedido.objects.create(
            cliente=cliente,
            usuario_cadastro=self.operador.nome,
            origem="VENDAS",
            status=StatusPedido.AGUARDANDO_ARTE,
        )
        ArtePedido.objects.create(
            pedido=self.pedido,
            arquivo="pedidos/testes/arte-projecao.png",
            nome_original="arte-projecao.png",
            criado_por=self.operador,
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_formal_process_wins_over_stale_legacy_status_in_all_views(self, _financeiro):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )
        Pedido.objects.filter(pk=self.pedido.pk).update(status=StatusPedido.AGUARDANDO_ARTE)

        pedido = projetar_lista(
            queryset_com_projecao(Pedido.objects.filter(pk=self.pedido.pk))
        )[0]
        self.assertEqual(cast(Any, pedido).projecao.operacional, "Em andamento")
        self.assertIn(self.pedido.pk, queryset_fila_producao().values_list("pk", flat=True))

        producao = self.client.get("/producao/")
        vendas = self.client.get("/vendas/pedidos/")
        gestor = self.client.get("/pedidos/")
        self.assertContains(producao, "Em andamento")
        self.assertContains(vendas, "Em andamento")
        self.assertContains(gestor, "Em andamento")

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_concluded_process_leaves_active_queue_even_if_legacy_status_is_stale(
        self, _financeiro
    ):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.PRONTO,
            operador=self.operador,
            origem_operacional=True,
        )
        Pedido.objects.filter(pk=self.pedido.pk).update(status=StatusPedido.EM_PRODUCAO)

        self.assertNotIn(
            self.pedido.pk, queryset_fila_producao().values_list("pk", flat=True)
        )
        self.assertIn(
            self.pedido.pk,
            queryset_fila_producao(prontos=True).values_list("pk", flat=True),
        )

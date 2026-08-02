from unittest.mock import patch

from django.test import TestCase

from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.operacao.models import EstadoProcesso, Processo
from apps.pedidos.models import ArtePedido, Pedido, StatusPedido
from apps.pedidos.use_cases import alterar_status_pedido

from .models import EstadoPendencia, FormaEncerramentoPendencia, Pendencia


class PendenciaBloqueioProcessoTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Responsavel", senha="senha", papel=PapelOperador.USUARIO
        )
        cliente = Cliente.objects.create(nome="Cliente Pendencia")
        self.pedido = Pedido.objects.create(
            cliente=cliente,
            usuario_cadastro=self.operador.nome,
            status=StatusPedido.AGUARDANDO_ARTE,
        )
        ArtePedido.objects.create(
            pedido=self.pedido,
            arquivo="pedidos/testes/arte-pendencia.png",
            nome_original="arte-pendencia.png",
            criado_por=self.operador,
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_rejection_creates_one_open_pending_obligation(self, _financeiro):
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
            observacao="Corrigir sangria",
        )

        pendencia = Pendencia.objects.get()
        self.assertEqual(pendencia.estado, EstadoPendencia.ABERTA)
        self.assertEqual(pendencia.responsavel_principal, self.operador)
        self.assertEqual(pendencia.processo.pedido, self.pedido)
        self.assertEqual(pendencia.descricao, "Corrigir sangria")
        self.assertTrue(
            EventoOperacional.objects.filter(
                tipo="PendenciaCriada", alvo_id=str(pendencia.pk)
            ).exists()
        )

    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_resuming_process_explicitly_closes_pending_obligation(self, _financeiro):
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

        pendencia = Pendencia.objects.get()
        self.assertEqual(pendencia.estado, EstadoPendencia.ENCERRADA)
        self.assertEqual(
            pendencia.forma_encerramento, FormaEncerramentoPendencia.RESOLUCAO
        )
        self.assertEqual(pendencia.encerrada_por, self.operador)
        self.assertTrue(pendencia.encerrada_em)

    @patch("apps.pendencias.services.registrar_evento", side_effect=RuntimeError("falha"))
    @patch("apps.pedidos.use_cases.sincronizar_financeiro_pedido")
    def test_pending_event_failure_rolls_back_block_and_order(self, _financeiro, _evento):
        alterar_status_pedido(
            pedido=self.pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=self.operador,
        )

        with self.assertRaises(RuntimeError):
            alterar_status_pedido(
                pedido=self.pedido,
                novo_status=StatusPedido.AGUARDANDO_ARTE,
                operador=self.operador,
                origem_operacional=True,
                observacao="Falha de arte",
            )

        self.pedido.refresh_from_db()
        processo = Processo.objects.get(pedido=self.pedido)
        self.assertEqual(self.pedido.status, StatusPedido.EM_PRODUCAO)
        self.assertEqual(processo.estado_operacional, EstadoProcesso.EM_ANDAMENTO)
        self.assertFalse(Pendencia.objects.exists())


class PendenciasAccessTests(TestCase):
    def setUp(self):
        self.responsavel = OperadorGestor.objects.create(
            nome="Dona da Pendencia", senha="senha", papel=PapelOperador.USUARIO
        )
        self.outro = OperadorGestor.objects.create(
            nome="Outro Usuario", senha="senha", papel=PapelOperador.USUARIO
        )
        cliente = Cliente.objects.create(nome="Cliente Acesso")
        pedido = Pedido.objects.create(cliente=cliente)
        from apps.operacao.services import iniciar_producao_pedido

        processo = iniciar_producao_pedido(
            pedido=pedido, operador=self.responsavel
        )
        Pendencia.objects.create(
            tipo="TESTE",
            descricao="Privada ao responsavel",
            processo=processo,
            pedido=pedido,
            responsavel_principal=self.responsavel,
        )

    def _entrar(self, operador):
        session = self.client.session
        session["operador_id"] = operador.pk
        session.save()

    def test_common_user_only_sees_owned_or_addressed_pending_items(self):
        self._entrar(self.outro)
        response = self.client.get("/pendencias/")
        self.assertNotContains(response, "Privada ao responsavel")

        pendencia = Pendencia.objects.get()
        pendencia.destinatarios.add(self.outro)
        response = self.client.get("/pendencias/")
        self.assertContains(response, "Privada ao responsavel")

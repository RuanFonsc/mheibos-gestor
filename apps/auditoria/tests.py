from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.catalogo.models import CanalAtendimento, OperadorGestor, PapelOperador
from apps.auditoria.models import EventoOperacional
from apps.auditoria.services import registrar_evento
from apps.pedidos.models import FormaPagamento, PrioridadePedido
from apps.pedidos.views import _criar_pedido
from apps.vendas.services import criar_pedido_vendas


class EventoOperacionalTests(TestCase):
    def test_event_is_immutable_and_idempotency_key_deduplicates(self):
        primeiro = registrar_evento(
            tipo="TesteExecutado",
            operador=None,
            origem="testes",
            alvo_tipo="Teste",
            alvo_id="1",
            acao="executar",
            valores_anteriores={},
            valores_posteriores={"ok": True},
            chave_idempotencia="teste:1",
        )
        repetido = registrar_evento(
            tipo="TesteExecutado",
            operador=None,
            origem="testes",
            alvo_tipo="Teste",
            alvo_id="1",
            acao="executar",
            valores_anteriores={},
            valores_posteriores={"ok": True},
            chave_idempotencia="teste:1",
        )

        self.assertEqual(primeiro.pk, repetido.pk)
        primeiro.acao = "reescrever"
        with self.assertRaises(ValidationError):
            primeiro.save()
        with self.assertRaises(ValidationError):
            primeiro.delete()

    def test_admin_can_consult_audit_but_common_operator_cannot(self):
        admin = OperadorGestor.objects.create(nome="Admin", senha="1234", papel=PapelOperador.ADMIN)
        comum = OperadorGestor.objects.create(nome="Comum", senha="1234", papel=PapelOperador.USUARIO)
        registrar_evento(tipo="Teste", operador=admin, origem="testes", alvo_tipo="Teste", alvo_id="1", acao="ver", valores_anteriores={}, valores_posteriores={})
        session = self.client.session
        session["operador_id"] = admin.pk
        session.save()
        self.assertContains(self.client.get("/auditoria/"), "Eventos operacionais")
        session = self.client.session
        session["operador_id"] = comum.pk
        session.save()
        self.assertRedirects(self.client.get("/auditoria/"), "/", fetch_redirect_response=False)

    def dados_formulario(self):
        return {
            "nome_cliente": "Cliente Evento", "telefone_1": "", "telefone_2": "", "cpf_cnpj": "", "endereco": "",
            "tema": "Tema", "data_pedido": date.today(), "data_entrega": date.today(), "hora_entrega": None,
            "observacoes": "", "caminho_arquivo_corel": "", "desconto_ajuste": Decimal("0"),
            "valor_pago": Decimal("0"), "forma_pagamento": FormaPagamento.PIX, "prioridade": PrioridadePedido.NORMAL,
            "canal_atendimento": CanalAtendimento.PRESENCIAL, "marcar_pronto": False, "aguardar_arte": True,
        }

    def test_both_current_order_creation_channels_emit_event(self):
        operador = OperadorGestor.objects.create(nome="Vendedora", senha="1234", papel=PapelOperador.USUARIO)
        formulario = SimpleNamespace(cleaned_data=self.dados_formulario(), data={})
        with self.settings(MHEIBOS_LICENSE_ENFORCED=False):
            pedido_gestor = _criar_pedido(formulario, [], operador)
            pedido_vendas = criar_pedido_vendas(formulario, operador)
        ids = {str(pedido_gestor.pk), str(pedido_vendas.pk)}
        self.assertEqual(set(EventoOperacional.objects.filter(tipo="PedidoCriado").values_list("alvo_id", flat=True)), ids)

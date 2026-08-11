from datetime import date

from django.test import SimpleTestCase

from .forms import VendasPedidoForm


class VendasFormTests(SimpleTestCase):
    def test_formulario_de_vendas_preserva_dados_operacionais_minimos(self):
        form = VendasPedidoForm(
            data={
                "nome_cliente": "Cliente Teste",
                "tema": "Pedido de teste",
                "data_entrega": date(2026, 8, 20).isoformat(),
                "prioridade": "NORMAL",
                "canal_atendimento": "PRESENCIAL",
                "valor_pago": "0",
                "forma_pagamento": "PIX",
                "desconto_ajuste": "0",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["nome_cliente"], "Cliente Teste")

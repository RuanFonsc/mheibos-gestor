from datetime import date
from decimal import Decimal

from django.test import TestCase

from .crm import fluxo_caixa_anual
from .models import CategoriaFinanceira, LancamentoFinanceiro, StatusLancamento, TipoLancamento


class FinanceiroCrmTests(TestCase):
    def test_fluxo_caixa_anual_agrega_lancamentos_nao_cancelados(self):
        categoria = CategoriaFinanceira.objects.create(nome="Serviço", tipo=TipoLancamento.RECEITA)
        LancamentoFinanceiro.objects.create(
            tipo=TipoLancamento.RECEITA,
            categoria=categoria,
            descricao="Teste de receita",
            valor=Decimal("125.50"),
            data_competencia=date(2026, 8, 10),
            status=StatusLancamento.REALIZADO,
        )
        LancamentoFinanceiro.objects.create(
            tipo=TipoLancamento.RECEITA,
            categoria=categoria,
            descricao="Cancelado",
            valor=Decimal("900.00"),
            data_competencia=date(2026, 8, 10),
            status=StatusLancamento.CANCELADO,
        )

        resultado = fluxo_caixa_anual(2026)

        self.assertEqual(resultado["linhas"][7]["receitas"], 125.5)
        self.assertEqual(resultado["linhas"][7]["despesas"], 0.0)

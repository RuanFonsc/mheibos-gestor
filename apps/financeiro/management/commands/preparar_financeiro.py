from django.core.management.base import BaseCommand

from apps.financeiro.models import CategoriaFinanceira, ContaFinanceira, GrupoFinanceiro, TipoLancamento


CATEGORIAS = [
    ("Vendas de pedidos", TipoLancamento.RECEITA, GrupoFinanceiro.VENDAS, 10),
    ("Servicos avulsos", TipoLancamento.RECEITA, GrupoFinanceiro.SERVICOS, 20),
    ("Aluguel", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_FIXOS, 10),
    ("Internet", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_FIXOS, 20),
    ("Conta de luz", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_FIXOS, 30),
    ("Conta de agua", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_FIXOS, 40),
    ("Conta de telefone", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_FIXOS, 50),
    ("Fornecedores", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_VARIAVEIS, 60),
    ("Marketing", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_VARIAVEIS, 70),
    ("Embalagens", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_VARIAVEIS, 80),
    ("Impostos", TipoLancamento.DESPESA, GrupoFinanceiro.IMPOSTOS, 90),
    ("Fretes", TipoLancamento.DESPESA, GrupoFinanceiro.CUSTOS_VARIAVEIS, 100),
    ("Retirada mensal", TipoLancamento.DESPESA, GrupoFinanceiro.RETIRADAS, 110),
    ("Despesas extras", TipoLancamento.DESPESA, GrupoFinanceiro.OUTROS, 120),
]


class Command(BaseCommand):
    help = "Cria categorias financeiras iniciais equivalentes a planilha Solides."

    def handle(self, *args, **options):
        ContaFinanceira.objects.get_or_create(nome="Caixa principal")

        criadas = 0
        for nome, tipo, grupo, ordem in CATEGORIAS:
            _, created = CategoriaFinanceira.objects.get_or_create(
                nome=nome,
                tipo=tipo,
                defaults={"grupo": grupo, "ordem": ordem},
            )
            criadas += int(created)

        self.stdout.write(self.style.SUCCESS(f"Categorias preparadas. Novas categorias: {criadas}."))

from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.catalogo.models import CategoriaProduto, CategoriaServico, ProdutoServico, UnidadeMedida


PADRAO = [
    ("Bolsas", 10),
    ("Painéis", 20),
    ("Gráfica rápida", 30),
]


class Command(BaseCommand):
    help = "Cria categorias de servico iniciais."

    def handle(self, *args, **options):
        criadas = 0
        for nome, ordem in PADRAO:
            _, created = CategoriaServico.objects.get_or_create(
                nome=nome,
                defaults={"ordem": ordem, "ativa": True},
            )
            criadas += int(created)

        ProdutoServico.objects.get_or_create(
            nome="Bolsa Personalizada",
            defaults={
                "categoria_servico": CategoriaServico.objects.get(nome="Bolsas"),
                "categoria": CategoriaProduto.BOLSA,
                "unidade": UnidadeMedida.UNIDADE,
                "preco_venda_padrao": Decimal("5.00"),
                "custo_estimado": Decimal("5.00"),
                "origem_legado": "seed",
            },
        )
        self.stdout.write(self.style.SUCCESS(f"Categorias preparadas. Novas: {criadas}."))

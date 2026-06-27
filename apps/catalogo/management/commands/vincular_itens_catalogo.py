from django.core.management.base import BaseCommand

from apps.catalogo.models import ProdutoServico
from apps.pedidos.models import PedidoItem


class Command(BaseCommand):
    help = "Vincula itens de pedido existentes a produtos do catalogo pelo nome."

    def handle(self, *args, **options):
        vinculados = 0
        produtos = {p.nome.strip().lower(): p for p in ProdutoServico.objects.all()}
        for item in PedidoItem.objects.filter(produto__isnull=True):
            produto = produtos.get(item.nome.strip().lower())
            if not produto:
                continue
            item.produto = produto
            item.custo_unitario_estimado = produto.custo_estimado
            item.save(update_fields=["produto", "custo_unitario_estimado"])
            vinculados += 1
        self.stdout.write(self.style.SUCCESS(f"Itens vinculados: {vinculados}."))

import sys
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand

from apps.catalogo.models import CategoriaProduto, CategoriaServico, ProdutoServico, UnidadeMedida


LEGACY_DIR = Path(r"C:\Users\ruan_\Documents\GESTOR\GESTOR NOVO")


def categoria_servico_para(nome_legado, nome_produto=""):
    texto = f"{nome_legado or ''} {nome_produto or ''}".lower()
    if "bolsa" in texto:
        return "Bolsas", CategoriaProduto.BOLSA
    if "painel" in texto:
        return "Painéis", CategoriaProduto.PAINEL
    return "Gráfica rápida", CategoriaProduto.GRAFICA_RAPIDA


def unidade_para(valor):
    texto = str(valor or "").lower()
    if "metro" in texto:
        return UnidadeMedida.METRO
    return UnidadeMedida.UNIDADE


class Command(BaseCommand):
    help = "Importa catalogo de produtos do modulo_custos legado."

    def handle(self, *args, **options):
        if str(LEGACY_DIR) not in sys.path:
            sys.path.insert(0, str(LEGACY_DIR))

        from modulo_custos import listar_catalogo_produtos

        for nome, ordem in [("Bolsas", 10), ("Painéis", 20), ("Gráfica rápida", 30)]:
            CategoriaServico.objects.get_or_create(nome=nome, defaults={"ordem": ordem})

        criados = 0
        atualizados = 0
        for item in listar_catalogo_produtos(forcar_recarga=True):
            nome = str(item.get("nome") or item.get("descricao") or "").strip()
            if not nome:
                continue
            categoria_nome, categoria_tipo = categoria_servico_para(item.get("categoria"), nome)
            categoria_servico = CategoriaServico.objects.get(nome=categoria_nome)
            _, created = ProdutoServico.objects.update_or_create(
                nome=nome,
                defaults={
                    "categoria_servico": categoria_servico,
                    "categoria": categoria_tipo,
                    "unidade": unidade_para(item.get("unidade")),
                    "preco_venda_padrao": Decimal(str(item.get("preco_venda") or 0)),
                    "custo_estimado": Decimal(str(item.get("custo_total") or 0)),
                    "ativo": True,
                    "origem_legado": str(item.get("origem") or "legado"),
                },
            )
            criados += int(created)
            atualizados += int(not created)

        self.stdout.write(
            self.style.SUCCESS(f"Catalogo importado. Criados: {criados}. Atualizados: {atualizados}.")
        )

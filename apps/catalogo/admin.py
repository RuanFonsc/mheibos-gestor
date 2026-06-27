from django.contrib import admin

from apps.catalogo.models import CategoriaServico, ProdutoServico


@admin.register(CategoriaServico)
class CategoriaServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "ordem", "ativa")
    list_filter = ("ativa",)
    search_fields = ("nome",)


@admin.register(ProdutoServico)
class ProdutoServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria_servico", "categoria", "unidade", "preco_venda_padrao", "custo_estimado", "ativo")
    list_filter = ("categoria_servico", "categoria", "unidade", "ativo")
    search_fields = ("nome",)

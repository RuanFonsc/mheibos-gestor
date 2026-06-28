from django.contrib import admin

from apps.financeiro.models import CategoriaFinanceira, ContaFinanceira, LancamentoFinanceiro, MetaVendasUsuario


@admin.register(CategoriaFinanceira)
class CategoriaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "grupo", "ativa", "ordem")
    list_filter = ("tipo", "grupo", "ativa")
    search_fields = ("nome",)


@admin.register(ContaFinanceira)
class ContaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativa")
    list_filter = ("ativa",)


@admin.register(LancamentoFinanceiro)
class LancamentoFinanceiroAdmin(admin.ModelAdmin):
    list_display = ("descricao", "tipo", "categoria", "valor", "status", "data_competencia", "data_pagamento", "pedido")
    list_filter = ("tipo", "status", "categoria", "data_competencia", "data_pagamento")
    search_fields = ("descricao", "pedido__cliente__nome", "pedido__legado_id")


@admin.register(MetaVendasUsuario)
class MetaVendasUsuarioAdmin(admin.ModelAdmin):
    list_display = ("operador", "mes", "ano", "valor")
    list_filter = ("ano", "mes", "operador")
    search_fields = ("operador__nome",)

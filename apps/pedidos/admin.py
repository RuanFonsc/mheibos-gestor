from django.contrib import admin

from apps.pedidos.models import ArtePedido, HistoricoStatusPedido, PagamentoPedido, Pedido, PedidoItem


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0


class ArtePedidoInline(admin.TabularInline):
    model = ArtePedido
    extra = 0
    can_delete = False
    readonly_fields = (
        "arquivo",
        "nome_original",
        "tamanho_bytes",
        "legado_base64_hash",
        "conteudo_sha256",
        "criado_por",
        "criado_em",
        "desvinculado_por",
        "desvinculado_em",
    )


class PagamentoPedidoInline(admin.TabularInline):
    model = PagamentoPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "legado_id", "cliente", "status", "canal_atendimento", "designer", "data_pedido", "data_entrega", "valor_total")
    list_filter = ("status", "origem", "canal_atendimento", "designer", "data_pedido")
    search_fields = ("cliente__nome", "tema", "descricao_legada", "legado_id")
    inlines = [PedidoItemInline, PagamentoPedidoInline, ArtePedidoInline]


@admin.register(HistoricoStatusPedido)
class HistoricoStatusPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "status_anterior", "status_novo", "usuario", "criado_em")
    list_filter = ("status_novo", "criado_em")

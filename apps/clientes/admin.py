from django.contrib import admin

from apps.clientes.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "status_cadastro", "telefone_principal", "email", "criado_em")
    list_filter = ("status_cadastro",)
    search_fields = ("nome", "telefone_principal", "telefone_secundario", "email")

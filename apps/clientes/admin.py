from django.contrib import admin

from apps.clientes.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone_principal", "email", "criado_em")
    search_fields = ("nome", "telefone_principal", "telefone_secundario", "email")

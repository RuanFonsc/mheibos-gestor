from django import forms

from apps.clientes.models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nome",
            "telefone_principal",
            "telefone_secundario",
            "email",
            "cpf_cnpj",
            "endereco",
            "observacoes",
        ]
        widgets = {
            "endereco": forms.Textarea(attrs={"rows": 3}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }

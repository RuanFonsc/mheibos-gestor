from django import forms
from typing import cast

from apps.financeiro.models import CategoriaFinanceira, ContaFinanceira, LancamentoFinanceiro, MetaVendasUsuario, StatusLancamento, TipoLancamento


class LancamentoCRMForm(forms.ModelForm):
    class Meta:
        model = LancamentoFinanceiro
        fields = [
            "tipo",
            "categoria",
            "conta",
            "descricao",
            "valor",
            "data_competencia",
            "data_vencimento",
            "data_pagamento",
            "status",
            "observacoes",
        ]
        widgets = {
            "data_competencia": forms.DateInput(attrs={"type": "date"}),
            "data_vencimento": forms.DateInput(attrs={"type": "date"}),
            "data_pagamento": forms.DateInput(attrs={"type": "date"}),
            "observacoes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cast(forms.ModelChoiceField, self.fields["categoria"]).queryset = CategoriaFinanceira.objects.filter(ativa=True).order_by("tipo", "ordem", "nome")
        cast(forms.ModelChoiceField, self.fields["conta"]).queryset = ContaFinanceira.objects.filter(ativa=True)
        self.fields["conta"].required = False
        self.fields["data_vencimento"].required = False
        self.fields["data_pagamento"].required = False
        self.fields["observacoes"].required = False
        self.fields["status"].initial = StatusLancamento.REALIZADO

    def clean(self):
        dados = super().clean() or {}
        tipo = dados.get("tipo")
        categoria = dados.get("categoria")
        if tipo and categoria and categoria.tipo != tipo:
            self.add_error("categoria", "A categoria precisa ser do mesmo tipo do lançamento.")
        return dados


class MetaVendasUsuarioForm(forms.ModelForm):
    class Meta:
        model = MetaVendasUsuario
        fields = ["valor"]
        widgets = {
            "valor": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
        }

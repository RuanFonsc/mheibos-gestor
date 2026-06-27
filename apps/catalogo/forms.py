from django import forms

from apps.catalogo.models import CategoriaServico, ProdutoServico, UnidadeMedida


class CategoriaServicoForm(forms.ModelForm):
    class Meta:
        model = CategoriaServico
        fields = ["nome", "ordem", "ativa"]


class ProdutoServicoForm(forms.ModelForm):
    class Meta:
        model = ProdutoServico
        fields = [
            "nome",
            "categoria_servico",
            "unidade",
            "preco_venda_padrao",
            "custo_estimado",
            "ativo",
        ]
        widgets = {
            "unidade": forms.Select(choices=UnidadeMedida.choices),
        }

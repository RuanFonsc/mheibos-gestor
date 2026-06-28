from django import forms

from apps.catalogo.models import CategoriaServico, OperadorGestor, PerfilEmpresa, ProdutoServico, UnidadeMedida


class CategoriaServicoForm(forms.ModelForm):
    class Meta:
        model = CategoriaServico
        fields = ["nome", "ordem", "ativa", "alerta_prazo_ativo", "alerta_dias_uteis", "alerta_mesmo_dia_apos_14h"]


class ProdutoServicoForm(forms.ModelForm):
    class Meta:
        model = ProdutoServico
        fields = [
            "nome",
            "categoria_servico",
            "unidade",
            "preco_venda_padrao",
            "custo_estimado",
            "prazo_entrega_dias_uteis",
            "ativo",
        ]
        widgets = {
            "unidade": forms.Select(choices=UnidadeMedida.choices),
            "prazo_entrega_dias_uteis": forms.NumberInput(attrs={"min": 0}),
        }


class OperadorGestorForm(forms.ModelForm):
    class Meta:
        model = OperadorGestor
        fields = ["nome", "foto", "senha", "papel", "observacoes", "ativo"]
        widgets = {
            "foto": forms.FileInput(attrs={"accept": "image/*"}),
            "senha": forms.PasswordInput(render_value=True),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }


class OperadorPerfilForm(forms.ModelForm):
    class Meta:
        model = OperadorGestor
        fields = ["nome", "foto"]
        widgets = {
            "foto": forms.FileInput(attrs={"accept": "image/*"}),
        }


class OperadorSenhaForm(forms.Form):
    senha_atual = forms.CharField(
        label="Senha atual",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    senha_nova = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    senha_confirmacao = forms.CharField(
        label="Confirmar nova senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean(self):
        dados = super().clean()
        nova = dados.get("senha_nova")
        confirmacao = dados.get("senha_confirmacao")
        if nova and confirmacao and nova != confirmacao:
            self.add_error("senha_confirmacao", "As senhas novas precisam ser iguais.")
        return dados


def senha_operador_valida(operador, senha):
    return (senha or "") == (operador.senha or "")


class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = [
            "nome_fantasia",
            "razao_social",
            "cnpj",
            "telefone",
            "telefone_secundario",
            "instagram",
            "email",
            "endereco",
            "logo",
            "observacoes",
        ]
        widgets = {
            "endereco": forms.Textarea(attrs={"rows": 3}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
            "logo": forms.FileInput(attrs={"accept": "image/*"}),
        }

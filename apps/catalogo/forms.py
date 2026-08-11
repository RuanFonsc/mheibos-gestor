from django import forms
from django.contrib.auth.hashers import make_password

from apps.catalogo.models import CategoriaServico, CategoriaUsuario, OperadorGestor, PerfilEmpresa, ProdutoServico, UnidadeMedida


class CategoriaServicoForm(forms.ModelForm):
    class Meta:
        model = CategoriaServico
        fields = ["nome", "ordem", "ativa", "alerta_prazo_ativo", "alerta_dias_uteis", "alerta_mesmo_dia_apos_14h"]


class CategoriaUsuarioForm(forms.ModelForm):
    class Meta:
        model = CategoriaUsuario
        fields = ["nome", "descricao", "ordem", "ativa"]
        widgets = {
            "descricao": forms.TextInput(attrs={"placeholder": "Ex: vendas, atendimento, producao"}),
            "ordem": forms.NumberInput(attrs={"min": 0}),
        }


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["senha"].required = False
            self.fields["senha"].help_text = "Deixe em branco para manter a senha atual."
            self.fields["senha"].widget.attrs["placeholder"] = "Manter senha atual"

    def clean_senha(self):
        senha = self.cleaned_data.get("senha")
        if self.instance and self.instance.pk and not senha:
            return self.instance.senha
        return make_password(senha) if senha else senha

    class Meta:
        model = OperadorGestor
        fields = ["nome", "foto", "senha", "papel", "categoria_usuario", "canal_atendimento_padrao", "observacoes", "ativo"]
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
        dados = super().clean() or {}
        nova = dados.get("senha_nova")
        confirmacao = dados.get("senha_confirmacao")
        if nova and confirmacao and nova != confirmacao:
            self.add_error("senha_confirmacao", "As senhas novas precisam ser iguais.")
        return dados


def senha_operador_valida(operador, senha):
    from apps.catalogo.authentication import validar_senha_operador

    return validar_senha_operador(operador, senha)


class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = [
            "nome_fantasia",
            "razao_social",
            "cnpj",
            "telefone",
            "telefone_secundario",
            "telefone_terciario",
            "instagram",
            "instagram_secundario",
            "email",
            "endereco",
            "logo",
            "observacoes",
            "diretorio_artes_raiz",
            "retencao_copias_locais_dias",
        ]
        widgets = {
            "endereco": forms.Textarea(attrs={"rows": 3}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
            "logo": forms.FileInput(attrs={"accept": "image/*"}),
        }

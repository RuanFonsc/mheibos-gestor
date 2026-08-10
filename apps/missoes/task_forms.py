from django import forms
from apps.catalogo.models import OperadorGestor


class TarefaMissaoForm(forms.Form):
    titulo = forms.CharField(max_length=160, label="Título da tarefa")
    descricao = forms.CharField(required=False, widget=forms.Textarea, label="Descrição")
    responsavel = forms.ModelChoiceField(queryset=OperadorGestor.objects.none(), required=False, label="Responsável")

    def __init__(self, *args, missao=None, **kwargs):
        super().__init__(*args, **kwargs)
        if missao:
            ids = missao.participacoes.filter(
                estado_participacao__in=["ACEITO", "ATRIBUIDO"], encerrado_em__isnull=True
            ).values("operador_id")
            self.fields["responsavel"].queryset = OperadorGestor.objects.filter(pk__in=ids, ativo=True).order_by("nome")


class NotaMissaoForm(forms.Form):
    titulo = forms.CharField(max_length=160, label="Título")
    conteudo = forms.CharField(widget=forms.Textarea, label="Nota")


class MensagemChatMissaoForm(forms.Form):
    conteudo = forms.CharField(widget=forms.Textarea, label="Mensagem")

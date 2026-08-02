from django import forms
from apps.catalogo.models import OperadorGestor, PapelOperador
from .models import PapelParticipacao, TipoManifestacaoConvite


class CriarMissaoIndividualForm(forms.Form):
    titulo = forms.CharField(max_length=160, label="Título")
    objetivo = forms.CharField(widget=forms.Textarea, label="Objetivo")
    criterio_conclusao = forms.CharField(widget=forms.Textarea, label="Como saberemos que terminou?")
    resultado_esperado = forms.CharField(required=False, widget=forms.Textarea, label="Resultado esperado")


class CriarMissaoColetivaForm(CriarMissaoIndividualForm):
    convidados = forms.ModelMultipleChoiceField(
        queryset=OperadorGestor.objects.none(),
        label="Pessoas convidadas",
    )

    def __init__(self, *args, operador=None, **kwargs):
        super().__init__(*args, **kwargs)
        consulta = OperadorGestor.objects.filter(ativo=True).exclude(
            papel=PapelOperador.TEMPORARIO
        )
        if operador:
            consulta = consulta.exclude(pk=operador.pk)
        campo = self.fields["convidados"]
        assert isinstance(campo, forms.ModelMultipleChoiceField)
        campo.queryset = consulta.order_by("nome")


class ConvidarParticipanteForm(forms.Form):
    operador = forms.ModelChoiceField(queryset=OperadorGestor.objects.none(), label="Pessoa")
    papel = forms.ChoiceField(
        choices=[
            (PapelParticipacao.PARTICIPANTE, "Participante"),
            (PapelParticipacao.OBSERVADOR, "Observador autorizado"),
            (PapelParticipacao.APROVADOR, "Aprovador"),
        ]
    )

    def __init__(self, *args, missao=None, **kwargs):
        super().__init__(*args, **kwargs)
        ids_correntes = missao.participacoes.filter(encerrado_em__isnull=True).values("operador_id") if missao else []
        campo = self.fields["operador"]
        assert isinstance(campo, forms.ModelChoiceField)
        campo.queryset = OperadorGestor.objects.filter(ativo=True).exclude(
            papel=PapelOperador.TEMPORARIO
        ).exclude(pk__in=ids_correntes).order_by("nome")


class ManifestarConviteForm(forms.Form):
    tipo = forms.ChoiceField(choices=TipoManifestacaoConvite.choices)
    texto = forms.CharField(widget=forms.Textarea, label="Mensagem")


class SairMissaoForm(forms.Form):
    confirmacao = forms.CharField(label="Digite SAIR")
    motivo = forms.CharField(widget=forms.Textarea)


class PausarMissaoForm(forms.Form):
    motivo = forms.CharField(widget=forms.Textarea, label="Motivo da pausa")


class RetomarMissaoForm(forms.Form):
    atualizacao = forms.CharField(
        required=False, widget=forms.Textarea, label="O que mudou durante a interrupção?"
    )


class BloquearMissaoForm(forms.Form):
    motivo = forms.CharField(widget=forms.Textarea)
    dependencia = forms.CharField(widget=forms.Textarea)
    impacto = forms.CharField(widget=forms.Textarea)
    ajuda_necessaria = forms.CharField(widget=forms.Textarea, label="Ajuda necessária")
    urgencia = forms.CharField(max_length=80)


class ConcluirMissaoForm(forms.Form):
    resultado_alcancado = forms.CharField(widget=forms.Textarea, label="Resultado alcançado")

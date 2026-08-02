from django import forms


class CriarMissaoIndividualForm(forms.Form):
    titulo = forms.CharField(max_length=160, label="Título")
    objetivo = forms.CharField(widget=forms.Textarea, label="Objetivo")
    criterio_conclusao = forms.CharField(widget=forms.Textarea, label="Como saberemos que terminou?")
    resultado_esperado = forms.CharField(required=False, widget=forms.Textarea, label="Resultado esperado")


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

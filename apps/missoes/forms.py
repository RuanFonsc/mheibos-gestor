from django import forms


class CriarMissaoIndividualForm(forms.Form):
    titulo = forms.CharField(max_length=160, label="Título")
    objetivo = forms.CharField(widget=forms.Textarea, label="Objetivo")
    criterio_conclusao = forms.CharField(widget=forms.Textarea, label="Como saberemos que terminou?")
    resultado_esperado = forms.CharField(required=False, widget=forms.Textarea, label="Resultado esperado")

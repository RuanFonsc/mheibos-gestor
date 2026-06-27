from django import forms

from apps.pedidos.models import FormaPagamento, PrioridadePedido, StatusPedido


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class PedidoCreateForm(forms.Form):
    nome_cliente = forms.CharField(label="Nome do Cliente", max_length=180)
    data_pedido = forms.DateField(
        label="Data do Pedido",
        widget=forms.HiddenInput(),
    )
    tema = forms.CharField(label="Tema", max_length=180)
    telefone_1 = forms.CharField(label="Telefone 1", max_length=32, required=False)
    telefone_2 = forms.CharField(label="Telefone 2", max_length=32, required=False)
    data_entrega = forms.DateField(
        label="Data de Entrega",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "required": "required"}),
    )
    hora_entrega = forms.TimeField(label="Hora da Entrega", required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    observacoes = forms.CharField(label="Observações", required=False, widget=forms.Textarea(attrs={"rows": 3}))
    caminho_arquivo_corel = forms.CharField(label="Caminho do arquivo Corel", max_length=500, required=False)
    prioridade = forms.ChoiceField(label="Prioridade", choices=PrioridadePedido.choices, initial=PrioridadePedido.NORMAL)
    valor_pago = forms.DecimalField(label="Valor Pago", max_digits=12, decimal_places=2, initial=0)
    forma_pagamento = forms.ChoiceField(label="Forma de Pagamento", choices=FormaPagamento.choices)
    desconto_ajuste = forms.DecimalField(label="Desconto / Acréscimo", max_digits=12, decimal_places=2, initial=0)
    marcar_pronto = forms.BooleanField(label="Marcar como pronto imediatamente", required=False)


class PedidoStatusForm(forms.Form):
    status = forms.ChoiceField(choices=StatusPedido.choices)


class PedidoEditForm(forms.Form):
    nome_cliente = forms.CharField(label="Nome do Cliente", max_length=180)
    data_pedido = forms.DateField(label="Data do Pedido", widget=forms.DateInput(attrs={"type": "date"}))
    tema = forms.CharField(label="Tema", max_length=180)
    telefone_1 = forms.CharField(label="Telefone 1", max_length=32, required=False)
    telefone_2 = forms.CharField(label="Telefone 2", max_length=32, required=False)
    data_entrega = forms.DateField(
        label="Data de Entrega",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    hora_entrega = forms.TimeField(label="Hora da Entrega", required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    observacoes = forms.CharField(label="Observações", required=False, widget=forms.Textarea(attrs={"rows": 3}))
    caminho_arquivo_corel = forms.CharField(label="Caminho do arquivo Corel", max_length=500, required=False)
    prioridade = forms.ChoiceField(label="Prioridade", choices=PrioridadePedido.choices)
    valor_pago = forms.DecimalField(label="Valor Pago", max_digits=12, decimal_places=2, initial=0)
    forma_pagamento = forms.ChoiceField(label="Forma de Pagamento", choices=FormaPagamento.choices)
    desconto_ajuste = forms.DecimalField(label="Desconto / Acréscimo", max_digits=12, decimal_places=2, initial=0)
    status = forms.ChoiceField(label="Status", choices=StatusPedido.choices)
    usuario_cadastro = forms.CharField(
        label="Usuário que cadastrou",
        max_length=80,
        widget=forms.TextInput(attrs={"list": "usuarios-list", "autocomplete": "off"}),
    )
    artes = forms.FileField(
        label="Adicionar artes",
        required=False,
        widget=MultipleFileInput(attrs={
            "multiple": True,
            "accept": "image/png,image/jpeg,image/webp,image/jfif,.jfif,.bmp",
        }),
    )

    def clean_artes(self):
        return None

    def clean_hora_entrega(self):
        return self.cleaned_data.get("hora_entrega") or None

    def clean_data_entrega(self):
        return self.cleaned_data.get("data_entrega") or None

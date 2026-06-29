from django import forms
from django.utils import timezone

from apps.pedidos.models import CanalAtendimentoPedido, FormaPagamento, PrioridadePedido


class VendasPedidoForm(forms.Form):
    nome_cliente = forms.CharField(label="Cliente", max_length=180)
    telefone_1 = forms.CharField(label="Telefone principal", max_length=32, required=False)
    telefone_2 = forms.CharField(label="Telefone secundario", max_length=32, required=False)
    cpf_cnpj = forms.CharField(label="CPF/CNPJ", max_length=32, required=False)
    endereco = forms.CharField(label="Endereco", required=False, widget=forms.Textarea(attrs={"rows": 2}))
    tema = forms.CharField(label="Resumo do pedido", max_length=180)
    data_entrega = forms.DateField(
        label="Data de entrega",
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    hora_entrega = forms.TimeField(label="Hora", required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    observacoes = forms.CharField(label="Observacoes", required=False, widget=forms.Textarea(attrs={"rows": 3}))
    prioridade = forms.ChoiceField(
        label="Prioridade",
        choices=[
            (PrioridadePedido.NORMAL, "Normal"),
            (PrioridadePedido.URGENTE, "Urgente"),
        ],
        initial=PrioridadePedido.NORMAL,
    )
    canal_atendimento = forms.ChoiceField(
        label="Canal de atendimento",
        choices=CanalAtendimentoPedido.choices,
        initial=CanalAtendimentoPedido.PRESENCIAL,
    )
    valor_pago = forms.DecimalField(label="Valor pago", max_digits=12, decimal_places=2, initial=0)
    forma_pagamento = forms.ChoiceField(label="Forma de pagamento", choices=FormaPagamento.choices)
    desconto_ajuste = forms.DecimalField(label="Desconto / acrescimo", max_digits=12, decimal_places=2, initial=0)

    def clean_hora_entrega(self):
        return self.cleaned_data.get("hora_entrega") or None

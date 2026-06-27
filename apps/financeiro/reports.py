from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear

from apps.financeiro.models import LancamentoFinanceiro, StatusLancamento


def resumo_fluxo_caixa(inicio=None, fim=None, usar_pagamento=True):
    campo_data = "data_pagamento" if usar_pagamento else "data_competencia"
    qs = LancamentoFinanceiro.objects.exclude(status=StatusLancamento.CANCELADO)

    if usar_pagamento:
        qs = qs.filter(status=StatusLancamento.REALIZADO, data_pagamento__isnull=False)

    if inicio:
        qs = qs.filter(**{f"{campo_data}__gte": inicio})
    if fim:
        qs = qs.filter(**{f"{campo_data}__lte": fim})

    return (
        qs.annotate(ano=ExtractYear(campo_data), mes=ExtractMonth(campo_data))
        .values("ano", "mes", "tipo", "categoria__nome", "categoria__grupo")
        .annotate(total=Sum("valor"))
        .order_by("ano", "mes", "tipo", "categoria__nome")
    )

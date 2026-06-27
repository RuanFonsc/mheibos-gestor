from collections import defaultdict
from datetime import date, datetime, timedelta
import unicodedata

from django.db.models import Prefetch
from django.utils import timezone

from apps.catalogo.models import CategoriaServico, ProdutoServico
from apps.pedidos.models import Pedido, PedidoItem, STATUS_PRE_PRODUCAO


def normalizar(texto):
    valor = unicodedata.normalize("NFD", str(texto or ""))
    valor = "".join(ch for ch in valor if unicodedata.category(ch) != "Mn")
    return valor.lower().strip()


def regra_categoria(categoria):
    nome = normalizar(categoria.nome)
    if getattr(categoria, "alerta_mesmo_dia_apos_14h", False):
        return {"tipo": "mesmo_dia", "limite_dias_uteis": None, "ativo": categoria.alerta_prazo_ativo}
    if "grafica" in nome or "rapida" in nome:
        tipo = "grafica"
    elif "bolsa" in nome:
        tipo = "bolsas"
    elif "painel" in nome or "paine" in nome:
        tipo = "paineis"
    else:
        tipo = "padrao"
    return {
        "tipo": tipo,
        "limite_dias_uteis": getattr(categoria, "alerta_dias_uteis", 2),
        "ativo": getattr(categoria, "alerta_prazo_ativo", True),
    }


def _pascoa(ano):
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(ano, mes, dia)


def _feriados_obrigatorios(ano):
    pascoa = _pascoa(ano)
    return {
        date(ano, 1, 1),
        pascoa - timedelta(days=2),
        date(ano, 4, 21),
        date(ano, 5, 1),
        date(ano, 9, 7),
        date(ano, 10, 12),
        date(ano, 11, 2),
        date(ano, 11, 15),
        date(ano, 12, 25),
    }


def _eh_dia_util(dia):
    return dia.weekday() < 5 and dia not in _feriados_obrigatorios(dia.year)


def dias_uteis_restantes(data_entrega, hoje=None):
    if not data_entrega:
        return 1
    hoje = hoje or timezone.localdate()
    if data_entrega <= hoje:
        return 0
    total = 0
    dia = hoje + timedelta(days=1)
    while dia <= data_entrega:
        if _eh_dia_util(dia):
            total += 1
        dia += timedelta(days=1)
    return total


def _painel_entrou_na_regra(pedido, agora=None):
    agora = agora or timezone.localtime()
    registro = pedido.data_registro or pedido.criado_em
    if not registro:
        return True
    registro = timezone.localtime(registro)
    limite_hoje = agora.replace(hour=14, minute=0, second=0, microsecond=0)
    return not (registro.date() == agora.date() and registro > limite_hoje)


def pedido_entrou_na_regra(pedido, categoria, agora=None):
    regra = regra_categoria(categoria)
    if not regra.get("ativo", True):
        return False
    if regra["tipo"] == "mesmo_dia":
        return _painel_entrou_na_regra(pedido, agora)
    limite = regra["limite_dias_uteis"]
    if limite is None:
        return True
    return dias_uteis_restantes(pedido.data_entrega, (agora or timezone.localtime()).date()) < limite


def pedido_em_alerta(pedido, agora=None):
    agora = agora or timezone.localtime()
    return any(pedido_entrou_na_regra(pedido, categoria, agora) for categoria in categorias_do_pedido(pedido))


def categorias_do_pedido(pedido):
    categorias = set()
    itens_atualizar = []
    for item in pedido.itens.all():
        categoria = None
        if item.categoria_servico:
            categoria = item.categoria_servico
        elif item.produto and item.produto.categoria_servico:
            categoria = item.produto.categoria_servico
            item.categoria_servico = categoria
            itens_atualizar.append(item)
        else:
            produto = ProdutoServico.objects.filter(nome__iexact=item.nome).select_related("categoria_servico").first()
            if produto:
                if not item.produto_id:
                    item.produto = produto
                categoria = produto.categoria_servico
                if categoria:
                    item.categoria_servico = categoria
                itens_atualizar.append(item)
        if categoria:
            categorias.add(categoria)
    for item in itens_atualizar:
        item.save(update_fields=["produto", "categoria_servico"])
    return categorias


def pedidos_assistencia():
    categorias = list(CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"))
    itens_prefetch = Prefetch(
        "itens",
        queryset=PedidoItem.objects.select_related("produto__categoria_servico", "categoria_servico"),
    )
    pedidos = (
        Pedido.objects.filter(
            status__in=STATUS_PRE_PRODUCAO,
        )
        .select_related("cliente")
        .prefetch_related(itens_prefetch, "artes")
        .order_by("data_entrega", "id")
    )
    agrupados = defaultdict(list)
    agora = timezone.localtime()

    for pedido in pedidos:
        for categoria in categorias_do_pedido(pedido):
            if pedido_entrou_na_regra(pedido, categoria, agora):
                if pedido not in agrupados[categoria.id]:
                    agrupados[categoria.id].append(pedido)

    return [
        {
            "categoria": categoria,
            "regra": regra_categoria(categoria),
            "pedidos": agrupados.get(categoria.id, []),
        }
        for categoria in categorias
    ]

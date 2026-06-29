from collections import defaultdict
from datetime import date, datetime, timedelta
import unicodedata

from django.db.models import Prefetch
from django.db.models import Q
from django.utils import timezone

from apps.catalogo.models import CategoriaServico, ProdutoServico
from apps.pedidos.models import Pedido, PedidoItem, STATUS_ASSISTENCIA


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


def preparar_categorias_pedidos(pedidos):
    pedidos_lista = list(pedidos)
    nomes_pendentes = set()
    for pedido in pedidos_lista:
        pedido._categorias_preparadas = True
        for item in pedido.itens.all():
            if item.categoria_servico:
                continue
            if item.produto and item.produto.categoria_servico:
                item.categoria_servico = item.produto.categoria_servico
                continue
            nomes_pendentes.add(normalizar(item.nome))
    if nomes_pendentes:
        produtos_por_nome = {}
        for produto in ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True):
            chave = normalizar(produto.nome)
            if chave in nomes_pendentes and chave not in produtos_por_nome:
                produtos_por_nome[chave] = produto
        for pedido in pedidos_lista:
            for item in pedido.itens.all():
                if item.categoria_servico:
                    continue
                produto = produtos_por_nome.get(normalizar(item.nome))
                if produto:
                    if not item.produto_id:
                        item.produto = produto
                    if produto.categoria_servico:
                        item.categoria_servico = produto.categoria_servico
    return pedidos_lista


def categorias_do_pedido(pedido):
    categorias = set()
    itens_atualizar = []
    categorias_preparadas = getattr(pedido, "_categorias_preparadas", False)
    for item in pedido.itens.all():
        categoria = None
        if item.categoria_servico:
            categoria = item.categoria_servico
        elif item.produto and item.produto.categoria_servico:
            categoria = item.produto.categoria_servico
            item.categoria_servico = categoria
            itens_atualizar.append(item)
        elif not categorias_preparadas:
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


def pedidos_assistencia(busca="", categorias_ids=None, usuarios=None):
    categorias = list(CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"))
    if categorias_ids:
        ids = {int(item) for item in categorias_ids if str(item).isdigit()}
        categorias = [categoria for categoria in categorias if categoria.id in ids]
    itens_prefetch = Prefetch(
        "itens",
        queryset=PedidoItem.objects.select_related("produto__categoria_servico", "categoria_servico"),
    )
    pedidos = (
        Pedido.objects.filter(
            status__in=STATUS_ASSISTENCIA,
        )
        .select_related("cliente")
        .prefetch_related(itens_prefetch, "artes")
        .order_by("data_entrega", "id")
    )
    busca = str(busca or "").strip()
    if busca:
        filtros_busca = (
            Q(cliente__nome__icontains=busca)
            | Q(tema__icontains=busca)
            | Q(descricao_legada__icontains=busca)
            | Q(legado_id__icontains=busca)
            | Q(itens__nome__icontains=busca)
            | Q(itens__descricao__icontains=busca)
            | Q(itens__produto__nome__icontains=busca)
        )
        if busca.isdigit():
            filtros_busca |= Q(pk=int(busca)) | Q(legado_id=int(busca))
        pedidos = pedidos.filter(filtros_busca).distinct()
    if usuarios:
        nomes = [str(item).strip() for item in usuarios if str(item).strip()]
        if nomes:
            filtros_usuarios = Q()
            for nome in nomes:
                filtros_usuarios |= Q(usuario_cadastro__iexact=nome) | Q(designer__iexact=nome)
            pedidos = pedidos.filter(filtros_usuarios).distinct()
    agrupados = defaultdict(list)
    agora = timezone.localtime()

    for pedido in preparar_categorias_pedidos(pedidos):
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

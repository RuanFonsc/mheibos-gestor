from apps.catalogo.assistencia import pedidos_assistencia, regra_categoria

MAX_ITENS_WIDGET = 9

_CATEGORIA_CURTA = {
    "paineis": "Painel",
    "grafica": "Gráfica",
    "bolsas": "Bolsa",
    "padrao": "Pedido",
}


def _categoria_curta(tipo):
    return _CATEGORIA_CURTA.get(tipo, "Pedido")


def _calcular_quotas(grupos, categorias):
    categorias = [c for c in categorias if grupos.get(c)]
    if not categorias:
        return {}
    if len(categorias) == 1:
        cat = categorias[0]
        return {cat: min(MAX_ITENS_WIDGET, len(grupos[cat]))}
    if len(categorias) == 2:
        ordenadas = sorted(categorias, key=lambda c: len(grupos[c]), reverse=True)
        return {ordenadas[0]: 5, ordenadas[1]: 4}
    quotas = {c: 3 for c in categorias}
    restante = MAX_ITENS_WIDGET - sum(quotas.values())
    while restante > 0:
        candidatos = [c for c in categorias if quotas[c] < len(grupos[c])]
        if not candidatos:
            break
        candidatos.sort(key=lambda c: (len(grupos[c]) - quotas[c], len(grupos[c])), reverse=True)
        for categoria in candidatos:
            if restante <= 0:
                break
            quotas[categoria] += 1
            restante -= 1
    return quotas


def _serializar_pedido(pedido, categoria, tipo):
    arte = pedido.artes.first()
    return {
        "id": pedido.pk,
        "legado_id": pedido.legado_id,
        "cliente": pedido.cliente.nome,
        "tema": pedido.tema or "",
        "categoria_id": categoria.id,
        "categoria_nome": categoria.nome,
        "categoria_tipo": tipo,
        "categoria_curta": _categoria_curta(tipo),
        "arte_url": arte.arquivo.url if arte else "",
        "data_entrega": pedido.data_entrega.isoformat() if pedido.data_entrega else "",
        "alerta": True,
    }


def pedidos_para_widget(categorias_ids=None):
    grupos_raw = pedidos_assistencia()
    if categorias_ids:
        ids = {int(item) for item in categorias_ids if str(item).isdigit()}
        grupos_raw = [grupo for grupo in grupos_raw if grupo["categoria"].id in ids]

    grupos = {}
    meta = {}
    for grupo in grupos_raw:
        categoria = grupo["categoria"]
        tipo = grupo["regra"]["tipo"]
        pedidos = list(grupo["pedidos"])
        pedidos.sort(key=lambda p: (p.data_entrega or p.criado_em.date(), p.pk))
        grupos[categoria.id] = pedidos
        meta[categoria.id] = {"categoria": categoria, "tipo": tipo}

    categorias = list(grupos.keys())
    quotas = _calcular_quotas(grupos, categorias)
    pedidos = []
    for categoria_id in categorias:
        info = meta[categoria_id]
        for pedido in grupos[categoria_id][: quotas.get(categoria_id, 0)]:
            pedidos.append(_serializar_pedido(pedido, info["categoria"], info["tipo"]))

    pedidos.sort(key=lambda item: (item["data_entrega"], item["id"]))
    return pedidos[:MAX_ITENS_WIDGET]


def resumo_assistencia_envio(categorias_ids=None):
    grupos_raw = pedidos_assistencia()
    if categorias_ids:
        ids = {int(item) for item in categorias_ids if str(item).isdigit()}
        grupos_raw = [grupo for grupo in grupos_raw if grupo["categoria"].id in ids]

    por_categoria = []
    total = 0
    for grupo in grupos_raw:
        quantidade = len(grupo["pedidos"])
        if not quantidade:
            continue
        total += quantidade
        por_categoria.append(
            {
                "id": grupo["categoria"].id,
                "nome": grupo["categoria"].nome,
                "tipo": grupo["regra"]["tipo"],
                "count": quantidade,
            }
        )
    return {"total": total, "por_categoria": por_categoria, "alerta": total > 0}

from difflib import SequenceMatcher

from django.urls import reverse

from apps.arquivos.models import (
    ArquivoOficialArte,
    EstadoPreparacaoArte,
    EstadoVinculoArquivo,
    PreparacaoArtePedido,
)
from apps.arquivos.services import avaliar_alerta_inatividade_arte
from apps.catalogo.assistencia import normalizar, pedidos_assistencia, regra_categoria
from apps.catalogo.permissions import pode_editar_pedido
from apps.pedidos.models import Pedido, StatusPedido

MAX_ITENS_WIDGET = 9
MAX_ALERTAS_INTERFACE = 30

_CATEGORIA_CURTA = {
    "paineis": "Painel",
    "grafica": "Gráfica",
    "bolsas": "Bolsa",
    "padrao": "Pedido",
}


def _categoria_curta(tipo):
    return _CATEGORIA_CURTA.get(tipo, "Pedido")


def _chave_nome_categoria(nome):
    return "".join(ch for ch in normalizar(nome) if ch.isalnum())


def _nomes_equivalentes(nome_a, nome_b):
    chave_a = _chave_nome_categoria(nome_a)
    chave_b = _chave_nome_categoria(nome_b)
    if not chave_a or not chave_b:
        return False
    if chave_a == chave_b or chave_a in chave_b or chave_b in chave_a:
        return True
    return SequenceMatcher(None, chave_a, chave_b).ratio() >= 0.72


def _expandir_categorias_equivalentes(grupos_raw, categorias_ids):
    if not categorias_ids:
        return None
    ids = {int(item) for item in categorias_ids if str(item).isdigit()}
    if not ids:
        return None
    grupos_por_id = {grupo["categoria"].id: grupo for grupo in grupos_raw}
    nomes = []
    assinaturas = set()
    tipos = set()
    for categoria_id in ids:
        grupo = grupos_por_id.get(categoria_id)
        if not grupo:
            continue
        categoria = grupo["categoria"]
        nomes.append(categoria.nome)
        assinaturas.add((normalizar(categoria.nome), grupo["regra"]["tipo"]))
        tipos.add(grupo["regra"]["tipo"])
    if not assinaturas:
        return ids
    equivalentes = set(ids)
    for grupo in grupos_raw:
        categoria = grupo["categoria"]
        assinatura = (normalizar(categoria.nome), grupo["regra"]["tipo"])
        if assinatura in assinaturas or grupo["regra"]["tipo"] in tipos or any(_nomes_equivalentes(categoria.nome, nome) for nome in nomes):
            equivalentes.add(categoria.id)
    return equivalentes


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
    arte = pedido.artes_ativas.first()
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
        ids = _expandir_categorias_equivalentes(grupos_raw, categorias_ids)
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
        ids = _expandir_categorias_equivalentes(grupos_raw, categorias_ids)
        grupos_raw = [grupo for grupo in grupos_raw if grupo["categoria"].id in ids]

    aguardando_arte = Pedido.objects.filter(status=StatusPedido.AGUARDANDO_ARTE).count()
    por_categoria = []
    total = aguardando_arte
    if aguardando_arte:
        por_categoria.append(
            {
                "id": "aguardando-arte",
                "nome": "Aguardando arte",
                "tipo": "pre_producao",
                "count": aguardando_arte,
            }
        )
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


def _pedido_autorizado(pedido, operador):
    return operador is None or operador.is_admin or pode_editar_pedido(pedido, operador)


def _alerta_pedido(
    *, pedido, identificador, categoria_id, categoria_nome, tipo, nivel,
    titulo, mensagem, href, acao_label, exige_acao, pode_dispensar,
    acoes_disponiveis=None, arquivo_id=None, numero=None,
):
    return {
        "id": identificador,
        "pedido_id": pedido.pk,
        "pedido_label": f"Pedido #{pedido.legado_id or pedido.pk}",
        "cliente": pedido.cliente.nome if pedido.cliente_id else "",
        "categoria_id": categoria_id,
        "categoria_nome": categoria_nome,
        "tipo": tipo,
        "nivel": nivel,
        "criticidade": "critico" if nivel >= 4 else "importante" if nivel >= 3 else "informativo",
        "titulo": titulo,
        "mensagem": mensagem,
        "href": href,
        "acao_label": acao_label,
        "exige_acao": exige_acao,
        "pode_dispensar": pode_dispensar,
        "acoes_disponiveis": list(acoes_disponiveis or []),
        "arquivo_id": str(arquivo_id) if arquivo_id else "",
        "numero": numero,
    }


def alertas_operacionais(categorias_ids=None, operador=None, limite=MAX_ALERTAS_INTERFACE):
    """Monta alertas usando classificações já existentes no domínio."""
    alertas = []
    pedidos_priorizados = set()
    ausencias = (
        ArquivoOficialArte.objects.filter(
            estado_vinculo=EstadoVinculoArquivo.ATIVO,
            ausencia_critica_ativa=True,
        )
        .select_related("pedido__cliente")
        .order_by("pedido_id", "criado_em")
    )
    for arquivo in ausencias:
        pedido = arquivo.pedido
        if not _pedido_autorizado(pedido, operador):
            continue
        pedidos_priorizados.add(pedido.pk)
        alertas.append(_alerta_pedido(
            pedido=pedido,
            identificador=f"arquivo-ausente-{arquivo.pk}",
            categoria_id="ausencia-arquivo-oficial",
            categoria_nome="Arquivo oficial ausente",
            tipo="critico",
            nivel=4,
            titulo="Arquivo oficial ausente",
            mensagem=f"Restaure e vincule novamente {arquivo.nome_oficial} no caminho oficial.",
            href=f"{reverse('pedido_detail', args=[pedido.pk])}#arquivos-oficiais",
            acao_label="Restaurar arquivo",
            exige_acao=True,
            pode_dispensar=False,
            acoes_disponiveis=["Restaurar arquivo oficial"],
            arquivo_id=arquivo.pk,
        ))

    preparacoes = (
        PreparacaoArtePedido.objects.exclude(estado=EstadoPreparacaoArte.CONCLUIDA)
        .select_related("pedido__cliente", "responsavel")
        .order_by("pedido_id")[:120]
    )
    for preparacao in preparacoes:
        pedido = preparacao.pedido
        if pedido.pk in pedidos_priorizados or not _pedido_autorizado(pedido, operador):
            continue
        alerta = avaliar_alerta_inatividade_arte(pedido=pedido)
        if not alerta.ativo:
            continue
        pedidos_priorizados.add(pedido.pk)
        acoes = ["Concluir arte", "Ainda estou trabalhando", "Lembrar em 30 minutos"]
        if alerta.prazo_critico:
            acoes.append("Solicitar ajuda urgente")
        elif alerta.pode_adiar_amanha:
            acoes.append("Deixar a arte para amanhã")
        alertas.append(_alerta_pedido(
            pedido=pedido,
            identificador=f"inatividade-arte-{pedido.pk}",
            categoria_id="inatividade-arte",
            categoria_nome="Arte sem atualização",
            tipo="critico" if alerta.prazo_critico else "pre_producao",
            nivel=4 if alerta.prazo_critico else 3,
            titulo="A arte precisa de uma resposta",
            mensagem=(
                "O prazo está crítico; responda ao alerta agora."
                if alerta.prazo_critico
                else "A arte está sem atualização há mais de duas horas."
            ),
            href=f"{reverse('pedido_detail', args=[pedido.pk])}#arquivos-oficiais",
            acao_label="Responder alerta",
            exige_acao=True,
            pode_dispensar=False,
            acoes_disponiveis=acoes,
            numero=alerta.numero,
        ))

    aguardando = (
        Pedido.objects.filter(status=StatusPedido.AGUARDANDO_ARTE)
        .select_related("cliente")
        .order_by("data_entrega", "pk")
    )
    for pedido in aguardando:
        if pedido.pk in pedidos_priorizados or not _pedido_autorizado(pedido, operador):
            continue
        pedidos_priorizados.add(pedido.pk)
        alertas.append(_alerta_pedido(
            pedido=pedido,
            identificador=f"aguardando-arte-{pedido.pk}",
            categoria_id="aguardando-arte",
            categoria_nome="Aguardando arte",
            tipo="pre_producao",
            nivel=1,
            titulo="Pedido aguardando arte",
            mensagem="O pedido ainda precisa passar pela preparação de arte antes da produção.",
            href=f"{reverse('pedido_detail', args=[pedido.pk])}#arquivos-oficiais",
            acao_label="Abrir pedido",
            exige_acao=False,
            pode_dispensar=True,
            acoes_disponiveis=["Abrir pedido"],
        ))

    grupos = pedidos_assistencia(categorias_ids=categorias_ids)
    for grupo in grupos:
        categoria = grupo["categoria"]
        for pedido in grupo["pedidos"]:
            if pedido.pk in pedidos_priorizados or not _pedido_autorizado(pedido, operador):
                continue
            pedidos_priorizados.add(pedido.pk)
            alertas.append(_alerta_pedido(
                pedido=pedido,
                identificador=f"assistencia-{pedido.pk}-{categoria.pk}",
                categoria_id=categoria.pk,
                categoria_nome=categoria.nome,
                tipo=grupo["regra"]["tipo"],
                nivel=1,
                titulo="Pedido aguardando assistência",
                mensagem="O pedido está na fila de assistência pela regra de prazo da categoria.",
                href=f"{reverse('pedido_detail', args=[pedido.pk])}#status-pedido",
                acao_label="Abrir pedido",
                exige_acao=False,
                pode_dispensar=True,
                acoes_disponiveis=["Abrir pedido", "Enviar para produção"],
            ))

    alertas.sort(key=lambda item: (-item["nivel"], item["pedido_id"], item["id"]))
    visiveis = alertas[: max(1, int(limite or MAX_ALERTAS_INTERFACE))]
    criticos = [item for item in alertas if item["nivel"] >= 4]
    obrigatorios = [item for item in alertas if item["exige_acao"]]
    grupos = {}
    for item in alertas:
        chave = item["categoria_id"]
        grupo = grupos.setdefault(chave, {
            "id": chave,
            "nome": item["categoria_nome"],
            "tipo": item["tipo"],
            "count": 0,
        })
        grupo["count"] += 1
    return {
        "alertas": visiveis,
        "por_categoria": list(grupos.values()),
        "total_alertas": len(alertas),
        "total_criticos": len(criticos),
        "total_exige_acao": len(obrigatorios),
        "critico": bool(criticos),
        "exige_acao": bool(obrigatorios),
    }
"""Ferramentas controladas que podem ser usadas pela camada cognitiva.

O modelo nunca recebe acesso direto ao ORM, à sessão ou à interface. Ele só pode
solicitar ferramentas registradas aqui; cada ferramenta valida a identidade e
devolve dados estruturados e limitados ao contexto autorizado.
"""

from dataclasses import dataclass, field
from typing import Any, Callable

from apps.catalogo.models import OperadorGestor
from apps.catalogo.widget_data import alertas_operacionais
from apps.catalogo.permissions import pode_editar_pedido
from apps.operacao.projections import projetar_pedido
from apps.pedidos.models import Pedido
from apps.pedidos.models import StatusPedido
from .interface_viva import INTERFACE_INVENTARIO


@dataclass(frozen=True)
class ResultadoFerramenta:
    nome: str
    sucesso: bool
    dados: dict[str, Any] = field(default_factory=dict)
    erro: str = ""
    requer_confirmacao: bool = False


@dataclass(frozen=True)
class ComandoInterface:
    comando: str
    parametros: dict[str, Any] = field(default_factory=dict)
    requer_confirmacao: bool = False
    motivo: str = ""


def _pedido_contexto(pedido: Pedido) -> dict[str, Any]:
    projecao = projetar_pedido(pedido)
    return {
        "id": pedido.pk,
        "identificador": str(pedido),
        "cliente": pedido.cliente.nome if pedido.cliente_id else "",
        "comercial": projecao.comercial,
        "financeiro": projecao.financeiro,
        "entrega": projecao.entrega,
        "operacional": projecao.operacional,
        "bloqueio": projecao.bloqueio or None,
    }


def consultar_pedido(*, operador: OperadorGestor, pedido_id: int) -> ResultadoFerramenta:
    try:
        pedido = Pedido.objects.select_related("cliente").get(pk=pedido_id)
    except Pedido.DoesNotExist:
        return ResultadoFerramenta("consultar_pedido", False, erro="Pedido não encontrado.")
    if not pode_editar_pedido(pedido, operador) and not operador.is_admin:
        return ResultadoFerramenta("consultar_pedido", False, erro="Pedido fora do escopo autorizado.")
    return ResultadoFerramenta("consultar_pedido", True, {"pedido": _pedido_contexto(pedido)})


def preparar_abertura_pedido(*, operador: OperadorGestor, pedido_id: int) -> ResultadoFerramenta:
    resultado = consultar_pedido(operador=operador, pedido_id=pedido_id)
    if not resultado.sucesso:
        return resultado
    return ResultadoFerramenta(
        "abrir_pedido",
        True,
        dados={"pedido": resultado.dados["pedido"], "interface": ComandoInterface(
            comando="navegar",
            parametros={"tela": "pedido_detalhe", "pedido_id": pedido_id, "rota": f"/pedidos/{pedido_id}/"},
            motivo="Abrir o pedido consultado no contexto atual.",
        )},
    )


def propor_alteracao_status(*, operador: OperadorGestor, pedido_id: int, novo_status: str, motivo: str = "") -> ResultadoFerramenta:
    resultado = consultar_pedido(operador=operador, pedido_id=pedido_id)
    if not resultado.sucesso:
        return resultado
    if novo_status not in {valor for valor, _ in StatusPedido.choices}:
        return ResultadoFerramenta("propor_alteracao_status", False, erro="Status inválido.")
    return ResultadoFerramenta(
        "propor_alteracao_status",
        True,
        dados={
            "pedido": resultado.dados["pedido"],
            "acao": {"tipo": "alterar_status_pedido", "pedido_id": pedido_id, "novo_status": novo_status, "motivo": motivo},
            "interface": ComandoInterface(
                comando="confirmar_alteracao_status",
                parametros={"pedido_id": pedido_id, "novo_status": novo_status, "motivo": motivo},
                requer_confirmacao=True,
                motivo="A alteração muda o estado persistente do pedido e será auditada.",
            ),
        },
        requer_confirmacao=True,
    )


def inventario_interface(*, operador: OperadorGestor) -> ResultadoFerramenta:
    return ResultadoFerramenta("inventario_interface", True, {"inventario": INTERFACE_INVENTARIO})


def consultar_alertas(*, operador: OperadorGestor, somente_criticos: bool = False) -> ResultadoFerramenta:
    contrato = alertas_operacionais(operador=operador)
    alertas = contrato["alertas"]
    if somente_criticos:
        alertas = [item for item in alertas if item["nivel"] >= 4]
    return ResultadoFerramenta(
        "consultar_alertas",
        True,
        dados={
            "alertas": alertas,
            "total_alertas": contrato["total_alertas"],
            "total_criticos": contrato["total_criticos"],
            "total_exige_acao": contrato["total_exige_acao"],
            "exige_acao": contrato["exige_acao"],
        },
    )


def pesquisar_pedidos(*, operador: OperadorGestor, termo: str = "") -> ResultadoFerramenta:
    termo = (termo or "").strip()[:100]
    consulta = Pedido.objects.select_related("cliente").all()
    if not operador.is_admin:
        consulta = consulta.filter(usuario_cadastro=operador.nome)
    if termo:
        from django.db.models import Q
        consulta = consulta.filter(Q(pk__icontains=termo) | Q(cliente__nome__icontains=termo) | Q(tema__icontains=termo))
    pedidos = [_pedido_contexto(pedido) for pedido in consulta.order_by("-id")[:20]]
    return ResultadoFerramenta("pesquisar_pedidos", True, {"pedidos": pedidos, "termo": termo})


def preparar_navegacao(*, operador: OperadorGestor, tela: str, pedido_id: int | None = None) -> ResultadoFerramenta:
    definicao = INTERFACE_INVENTARIO["telas"].get(tela)
    if not definicao:
        return ResultadoFerramenta("navegar", False, erro="Tela não registrada no inventário oficial.")
    rota = definicao["rota"].replace("{pedido_id}", str(pedido_id or ""))
    if "{pedido_id}" in definicao["rota"] and not pedido_id:
        return ResultadoFerramenta("navegar", False, erro="Esta tela exige um pedido autorizado.")
    if tela == "pedido_detalhe" and pedido_id:
        autorizado = consultar_pedido(operador=operador, pedido_id=pedido_id)
        if not autorizado.sucesso:
            return ResultadoFerramenta("navegar", False, erro=autorizado.erro)
    return ResultadoFerramenta("navegar", True, {"interface": ComandoInterface("navegar", {"tela": tela, "rota": rota})})


def preparar_destaque(*, operador: OperadorGestor, tela: str, campo: str = "", acao: str = "") -> ResultadoFerramenta:
    definicao = INTERFACE_INVENTARIO["telas"].get(tela)
    if not definicao:
        return ResultadoFerramenta("destacar", False, erro="Tela não registrada no inventário oficial.")
    if campo and campo not in definicao.get("campos", {}):
        return ResultadoFerramenta("destacar", False, erro="Campo não registrado nessa tela.")
    if acao and acao not in definicao.get("acoes", {}):
        return ResultadoFerramenta("destacar", False, erro="Ação não registrada nessa tela.")
    if not campo and not acao:
        return ResultadoFerramenta("destacar", False, erro="Informe um campo ou uma ação registrada.")
    comando = "destacar_campo" if campo else "destacar_acao"
    return ResultadoFerramenta("destacar", True, {"interface": ComandoInterface(comando, {"tela": tela, "campo": campo, "acao": acao})})

def preparar_preenchimento(*, operador: OperadorGestor, tela: str, valores: dict[str, Any]) -> ResultadoFerramenta:
    definicao = INTERFACE_INVENTARIO["telas"].get(tela)
    if tela != "novo_pedido" or not definicao or not isinstance(valores, dict) or not valores:
        return ResultadoFerramenta("preencher_campos", False, erro="Preenchimento permitido apenas em campos registrados do Novo Pedido.")
    campos = definicao.get("campos", {})
    if any(nome not in campos for nome in valores):
        return ResultadoFerramenta("preencher_campos", False, erro="Há campo não registrado no inventário oficial.")
    comando = ComandoInterface("preencher_campos", {"tela": tela, "valores": {str(nome): valor for nome, valor in valores.items()}}, requer_confirmacao=True, motivo="O preenchimento é uma proposta reversível e não envia o formulário.")
    return ResultadoFerramenta("preencher_campos", True, {"interface": comando}, requer_confirmacao=True)

FERRAMENTAS_CONSULTA: dict[str, Callable[..., ResultadoFerramenta]] = {
    "consultar_pedido": consultar_pedido,
    "inventario_interface": inventario_interface,
    "consultar_alertas": consultar_alertas,
    "pesquisar_pedidos": pesquisar_pedidos,
    "navegar": preparar_navegacao,
    "destacar": preparar_destaque,
    "preencher_campos": preparar_preenchimento,
    "abrir_pedido": preparar_abertura_pedido,
    "propor_alteracao_status": propor_alteracao_status,
}


def executar_ferramenta(*, nome: str, operador: OperadorGestor, parametros: dict[str, Any]) -> ResultadoFerramenta:
    ferramenta = FERRAMENTAS_CONSULTA.get(nome)
    if ferramenta is None:
        return ResultadoFerramenta(nome, False, erro="Ferramenta não autorizada.")
    try:
        return ferramenta(operador=operador, **parametros)
    except (TypeError, ValueError):
        return ResultadoFerramenta(nome, False, erro="Parâmetros inválidos para a ferramenta.")

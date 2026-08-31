import json
from dataclasses import dataclass, field
from typing import Protocol

from django.conf import settings

from .interface_viva import INTERFACE_INVENTARIO, inventario_para_modelo

FALLBACK_RESUMO = (
    "Assistencia por IA indisponivel. Consulte os estados e processos exibidos no Pedido; "
    "nenhuma operacao foi interrompida."
)


@dataclass(frozen=True)
class SolicitacaoCognitiva:
    capacidade: str
    contexto: str


@dataclass(frozen=True)
class RespostaCognitiva:
    texto: str
    disponivel: bool
    provider: str
    modelo: str
    codigo: str
    comandos: list[dict] = field(default_factory=list)


class ProvedorIA(Protocol):
    nome: str
    def gerar(self, solicitacao: SolicitacaoCognitiva) -> str: ...


class ProvedorGemini:
    nome = "gemini"

    def __init__(self, *, api_key: str, modelo: str) -> None:
        self._api_key = api_key
        self._modelo = modelo

    def gerar(self, solicitacao: SolicitacaoCognitiva) -> str:
        from google import genai
        client = genai.Client(api_key=self._api_key)
        resposta = client.models.generate_content(
            model=self._modelo,
            contents=(
                "Você é o assistente operacional do Mheibos Gestor. Use apenas os nomes canônicos "
                "do inventário. Nunca invente tela, rótulo, campo, botão ou ação. Nunca execute "
                "mudanças persistentes; apenas proponha comandos de interface reversíveis. Responda "
                "SOMENTE JSON válido no formato {\"texto\": string, \"comandos\": [{\"comando\": string, \"parametros\": object, \"rotulo\": string}]}. "
                "Quando o usuário pedir onde fica um campo, retorne um comando navegar com tela e campo; o cliente abrirá a tela e destacará o campo. Se não houver comando seguro, retorne comandos vazios.\n\n"
                f"Capacidade: {solicitacao.capacidade}\nSolicitação: {solicitacao.contexto}\n\n"
                f"Inventário oficial da Interface Viva:\n{inventario_para_modelo()}"
            ),
        )
        return (resposta.text or "").strip()


def _comandos_validos(raw: object) -> list[dict]:
    if not isinstance(raw, list):
        return []
    aceitos = set(INTERFACE_INVENTARIO["comandos"])
    comandos = []
    for item in raw[:6]:
        if not isinstance(item, dict):
            continue
        nome = item.get("comando")
        parametros = item.get("parametros", {})
        if nome not in aceitos or not isinstance(parametros, dict):
            continue
        tela = parametros.get("tela")
        if tela and tela not in INTERFACE_INVENTARIO["telas"]:
            continue
        campo = parametros.get("campo")
        if campo and (not tela or campo not in INTERFACE_INVENTARIO["telas"][tela].get("campos", {})):
            continue
        if nome == "navegar" and tela:
            rota = INTERFACE_INVENTARIO["telas"][tela]["rota"]
            pedido_id = parametros.get("pedido_id")
            if "{pedido_id}" in rota and not pedido_id:
                continue
            parametros = {**parametros, "rota": rota.replace("{pedido_id}", str(pedido_id or ""))}
        if nome == "destacar_acao":
            acoes = INTERFACE_INVENTARIO["telas"].get(tela, {}).get("acoes", {}) if tela else {}
            if not tela or parametros.get("acao") not in acoes:
                continue
        if nome == "preencher_campos":
            valores = parametros.get("valores")
            if tela != "novo_pedido" or not isinstance(valores, dict):
                continue
            campos = INTERFACE_INVENTARIO["telas"][tela]["campos"]
            if any(chave not in campos for chave in valores):
                continue
        comandos.append({"comando": nome, "parametros": parametros, "rotulo": str(item.get("rotulo") or "Executar")[:90]})
    return comandos


def _normalizar_resposta(texto: str) -> tuple[str, list[dict]]:
    candidato = texto.strip()
    if candidato.startswith("```"):
        candidato = candidato.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        payload = json.loads(candidato)
    except (json.JSONDecodeError, TypeError):
        return texto, []
    if not isinstance(payload, dict) or not isinstance(payload.get("texto"), str):
        return texto, []
    return payload["texto"].strip() or FALLBACK_RESUMO, _comandos_validos(payload.get("comandos"))


class GatewayIA:
    def __init__(self, provedor: ProvedorIA | None, *, modelo: str = "") -> None:
        self._provedor = provedor
        self._modelo = modelo

    def solicitar(self, solicitacao: SolicitacaoCognitiva) -> RespostaCognitiva:
        if self._provedor is None:
            return RespostaCognitiva(FALLBACK_RESUMO, False, "none", self._modelo, "IA_DESLIGADA")
        try:
            bruto = self._provedor.gerar(solicitacao)
        except Exception:
            return RespostaCognitiva(FALLBACK_RESUMO, False, self._provedor.nome, self._modelo, "PROVEDOR_INDISPONIVEL")
        if not bruto:
            return RespostaCognitiva(FALLBACK_RESUMO, False, self._provedor.nome, self._modelo, "RESPOSTA_VAZIA")
        texto, comandos = _normalizar_resposta(bruto)
        return RespostaCognitiva(texto, True, self._provedor.nome, self._modelo, "SUCESSO", comandos)


def gateway_configurado() -> GatewayIA:
    modelo = settings.MHEIBOS_IA_MODEL
    if not settings.MHEIBOS_IA_ENABLED:
        return GatewayIA(None, modelo=modelo)
    if settings.MHEIBOS_IA_PROVIDER != "gemini" or not settings.GEMINI_API_KEY:
        return GatewayIA(None, modelo=modelo)
    return GatewayIA(ProvedorGemini(api_key=settings.GEMINI_API_KEY, modelo=modelo), modelo=modelo)
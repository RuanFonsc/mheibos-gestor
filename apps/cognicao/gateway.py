import json
import time
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Protocol

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
    workload: str = "assistant"


@dataclass(frozen=True)
class GeracaoIA:
    texto: str
    tokens_input: int | None = None
    tokens_output: int | None = None
    thinking_tokens: int | None = None
    duracao_ms: int | None = None


@dataclass(frozen=True)
class RespostaCognitiva:
    texto: str
    disponivel: bool
    provider: str
    modelo: str
    codigo: str
    comandos: list[dict] = field(default_factory=list)
    estrategia: str = "assistant"
    intervir: bool | None = None
    motivo: str = ""
    tokens_input: int | None = None
    tokens_output: int | None = None
    thinking_tokens: int | None = None
    duracao_ms: int | None = None
    custo_estimado: Decimal | None = None


class ProvedorIA(Protocol):
    nome: str
    def gerar(self, solicitacao: SolicitacaoCognitiva) -> str | GeracaoIA: ...


class ProvedorGemini:
    nome = "gemini"

    def __init__(self, *, api_key: str, modelo: str) -> None:
        self._api_key = api_key
        self._modelo = modelo

    def gerar(self, solicitacao: SolicitacaoCognitiva) -> GeracaoIA:
        from google import genai

        inicio = time.perf_counter()
        client = genai.Client(api_key=self._api_key)
        resposta = client.models.generate_content(
            model=self._modelo,
            contents=(
                "Você é o assistente operacional do Mheibos Gestor. Use apenas os nomes canônicos "
                "do inventário. Nunca invente tela, rótulo, campo, botão ou ação. Nunca execute "
                "mudanças persistentes; apenas proponha comandos de interface reversíveis. Responda "
                "SOMENTE JSON válido no formato {\"texto\": string, \"intervir\": boolean, \"motivo\": string, \"comandos\": [{\"comando\": string, \"parametros\": object, \"rotulo\": string}]}. "
                "Quando o usuário pedir onde fica um campo, retorne um comando navegar com tela e campo; o cliente abrirá a tela e destacará o campo. Se não houver comando seguro, retorne comandos vazios.\n\n"
                f"Capacidade: {solicitacao.capacidade}\nWorkload: {solicitacao.workload}\nSolicitação: {solicitacao.contexto}\n\n"
                f"Inventário oficial da Interface Viva:\n{inventario_para_modelo()}"
            ),
        )
        uso = getattr(resposta, "usage_metadata", None)
        return GeracaoIA(
            texto=(getattr(resposta, "text", "") or "").strip(),
            tokens_input=_inteiro_uso(uso, "prompt_token_count"),
            tokens_output=_inteiro_uso(uso, "candidates_token_count"),
            thinking_tokens=_inteiro_uso(uso, "thoughts_token_count"),
            duracao_ms=max(0, int((time.perf_counter() - inicio) * 1000)),
        )


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
    payload = _payload_json(texto)
    if payload is None:
        return texto, []
    if not isinstance(payload, dict) or not isinstance(payload.get("texto"), str):
        return texto, []
    return payload["texto"].strip() or FALLBACK_RESUMO, _comandos_validos(payload.get("comandos"))


def _payload_json(texto: str) -> dict[str, Any] | None:
    candidato = (texto or "").strip()
    if candidato.startswith("```"):
        candidato = candidato.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        payload = json.loads(candidato)
    except (json.JSONDecodeError, TypeError):
        return None
    return payload if isinstance(payload, dict) else None


def _inteiro_uso(uso: object, campo: str) -> int | None:
    valor = getattr(uso, campo, None)
    try:
        return int(valor) if valor is not None else None
    except (TypeError, ValueError):
        return None


def modelo_para_workload(workload: str = "assistant") -> str:
    if workload == "triage":
        return settings.MHEIBOS_IA_MODEL_FLASH_LITE
    if workload in {"intervention", "complex_intervention"}:
        return settings.MHEIBOS_IA_MODEL_FLASH
    return settings.MHEIBOS_IA_MODEL


def estimar_custo(*, modelo: str, tokens_input: int | None, tokens_output: int | None) -> Decimal | None:
    if tokens_input is None and tokens_output is None:
        return None
    lite = "lite" in (modelo or "").casefold()
    input_rate = getattr(settings, "MHEIBOS_IA_CUSTO_INPUT_FLASH_LITE_1K" if lite else "MHEIBOS_IA_CUSTO_INPUT_FLASH_1K", 0)
    output_rate = getattr(settings, "MHEIBOS_IA_CUSTO_OUTPUT_FLASH_LITE_1K" if lite else "MHEIBOS_IA_CUSTO_OUTPUT_FLASH_1K", 0)
    total = ((tokens_input or 0) / 1000 * input_rate) + ((tokens_output or 0) / 1000 * output_rate)
    return Decimal(str(total)).quantize(Decimal("0.000001"))


class GatewayIA:
    def __init__(self, provedor: ProvedorIA | None, *, modelo: str = "", workload: str = "assistant") -> None:
        self._provedor = provedor
        self._modelo = modelo
        self._workload = workload

    def solicitar(self, solicitacao: SolicitacaoCognitiva) -> RespostaCognitiva:
        if self._provedor is None:
            return RespostaCognitiva(FALLBACK_RESUMO, False, "none", self._modelo, "IA_DESLIGADA", estrategia=self._workload)
        inicio = time.perf_counter()
        try:
            geracao = self._provedor.gerar(solicitacao)
        except Exception:
            return RespostaCognitiva(FALLBACK_RESUMO, False, self._provedor.nome, self._modelo, "PROVEDOR_INDISPONIVEL", estrategia=self._workload)
        if isinstance(geracao, GeracaoIA):
            bruto = geracao.texto
            tokens_input = geracao.tokens_input
            tokens_output = geracao.tokens_output
            thinking_tokens = geracao.thinking_tokens
            duracao_ms = geracao.duracao_ms
        else:
            bruto = str(geracao or "").strip()
            tokens_input = tokens_output = thinking_tokens = None
            duracao_ms = max(0, int((time.perf_counter() - inicio) * 1000))
        if not bruto:
            return RespostaCognitiva(FALLBACK_RESUMO, False, self._provedor.nome, self._modelo, "RESPOSTA_VAZIA", estrategia=self._workload, tokens_input=tokens_input, tokens_output=tokens_output, thinking_tokens=thinking_tokens, duracao_ms=duracao_ms, custo_estimado=estimar_custo(modelo=self._modelo, tokens_input=tokens_input, tokens_output=tokens_output))
        payload = _payload_json(bruto)
        if self._workload == "triage" and (payload is None or "intervir" not in payload):
            return RespostaCognitiva(FALLBACK_RESUMO, False, self._provedor.nome, self._modelo, "RESPOSTA_INVALIDA", estrategia=self._workload, motivo="A triagem não retornou uma decisão estruturada.", tokens_input=tokens_input, tokens_output=tokens_output, thinking_tokens=thinking_tokens, duracao_ms=duracao_ms, custo_estimado=estimar_custo(modelo=self._modelo, tokens_input=tokens_input, tokens_output=tokens_output))
        texto, comandos = _normalizar_resposta(bruto)
        return RespostaCognitiva(
            texto,
            True,
            self._provedor.nome,
            self._modelo,
            "SUCESSO",
            comandos,
            estrategia=self._workload,
            intervir=bool(payload.get("intervir")) if self._workload == "triage" and payload else None,
            motivo=str(payload.get("motivo") or "")[:500] if payload else "",
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            thinking_tokens=thinking_tokens,
            duracao_ms=duracao_ms,
            custo_estimado=estimar_custo(modelo=self._modelo, tokens_input=tokens_input, tokens_output=tokens_output),
        )


def gateway_configurado(*, workload: str = "assistant") -> GatewayIA:
    modelo = modelo_para_workload(workload)
    if not settings.MHEIBOS_IA_ENABLED:
        return GatewayIA(None, modelo=modelo, workload=workload)
    if settings.MHEIBOS_IA_PROVIDER != "gemini" or not settings.GEMINI_API_KEY:
        return GatewayIA(None, modelo=modelo, workload=workload)
    return GatewayIA(ProvedorGemini(api_key=settings.GEMINI_API_KEY, modelo=modelo), modelo=modelo, workload=workload)

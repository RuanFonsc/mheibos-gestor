from dataclasses import dataclass
from typing import Protocol

from django.conf import settings


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
                "Voce e um assistente operacional do Mheibos Gestor. "
                "Resuma objetivamente os fatos fornecidos, sem autorizar acoes, criar fatos, "
                "alterar estados ou afirmar que executou operacoes.\n\n"
                f"Capacidade: {solicitacao.capacidade}\n{solicitacao.contexto}"
            ),
        )
        return (resposta.text or "").strip()


class GatewayIA:
    def __init__(self, provedor: ProvedorIA | None, *, modelo: str = "") -> None:
        self._provedor = provedor
        self._modelo = modelo

    def solicitar(self, solicitacao: SolicitacaoCognitiva) -> RespostaCognitiva:
        if self._provedor is None:
            return RespostaCognitiva(
                FALLBACK_RESUMO, False, "none", self._modelo, "IA_DESLIGADA"
            )
        try:
            texto = self._provedor.gerar(solicitacao)
        except Exception:
            return RespostaCognitiva(
                FALLBACK_RESUMO,
                False,
                self._provedor.nome,
                self._modelo,
                "PROVEDOR_INDISPONIVEL",
            )
        if not texto:
            return RespostaCognitiva(
                FALLBACK_RESUMO,
                False,
                self._provedor.nome,
                self._modelo,
                "RESPOSTA_VAZIA",
            )
        return RespostaCognitiva(
            texto, True, self._provedor.nome, self._modelo, "SUCESSO"
        )


def gateway_configurado() -> GatewayIA:
    modelo = settings.MHEIBOS_IA_MODEL
    if not settings.MHEIBOS_IA_ENABLED:
        return GatewayIA(None, modelo=modelo)
    if settings.MHEIBOS_IA_PROVIDER != "gemini" or not settings.GEMINI_API_KEY:
        return GatewayIA(None, modelo=modelo)
    return GatewayIA(
        ProvedorGemini(api_key=settings.GEMINI_API_KEY, modelo=modelo), modelo=modelo
    )

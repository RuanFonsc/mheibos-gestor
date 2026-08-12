"""Catálogo e resolução determinística das configurações da IA.

O catálogo é código versionado; a tela apenas escolhe valores já permitidos.
Nenhuma configuração deste módulo substitui regras LOCKED ou permissões.
"""

from dataclasses import dataclass
from typing import Any


LOCKED = "LOCKED"
COMPANY = "COMPANY"
USER = "USER"
MISSION = "MISSION"


CONFIGURACOES_IA: tuple[dict[str, Any], ...] = (
    {"key": "ai.proactivity", "title": "Iniciativa proativa da IA", "scope": COMPANY, "type": "choice", "default": "balanced", "options": (("essential", "Essencial"), ("balanced", "Equilibrada"), ("proactive", "Proativa"))},
    {"key": "ai.preventive_assistance", "title": "Assistência preventiva operacional", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.improvement_suggestions", "title": "Sugestões de melhoria organizacional", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.background_analysis", "title": "Análises cognitivas em segundo plano", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.sensitive_actions", "title": "Política de ações sensíveis", "scope": COMPANY, "type": "locked_info", "default": "managed"},
    {"key": "ai.automatic_reports", "title": "Relatórios e resumos automáticos", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.action_plans", "title": "Sugestões de planos de ação", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.training_suggestions", "title": "Sugestões de treinamento e melhoria", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.strategic_analysis", "title": "Análises estratégicas e simulações", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.system_health", "title": "Recomendações de saúde do sistema", "scope": COMPANY, "type": "bool", "default": False},
    {"key": "ai.user_mode", "title": "Modo inteligente da interface", "scope": USER, "type": "choice", "default": "apathetic", "options": (("intelligent", "Inteligente"), ("apathetic", "Padrão"))},
    {"key": "ai.contextual_facilities", "title": "Facilitações contextuais", "scope": USER, "type": "bool", "default": False},
    {"key": "ai.side_panel_help", "title": "Ajuda contextual pelo painel lateral", "scope": USER, "type": "bool", "default": False},
    {"key": "ai.optional_suggestions", "title": "Sugestões não urgentes", "scope": USER, "type": "bool", "default": False},
    {"key": "ai.personal_summaries", "title": "Resumos pessoais automáticos", "scope": USER, "type": "bool", "default": False},
    {"key": "ai.adaptive_view", "title": "Visualização adaptada por comportamento", "scope": USER, "type": "bool", "default": False},
    {"key": "ai.mission_autonomy", "title": "Autonomia da IA nesta Missão", "scope": MISSION, "type": "mission", "default": False},
    {"key": "ai.mission_workspace", "title": "Organização autônoma do workspace", "scope": MISSION, "type": "mission", "default": False},
    {"key": "ai.mission_suggestions", "title": "Sugestões proativas da Missão", "scope": MISSION, "type": "mission", "default": False},
    {"key": "ai.mission_summaries", "title": "Resumos automáticos da Missão", "scope": MISSION, "type": "mission", "default": False},
    {"key": "ai.locked_financial", "title": "Decisão financeira autônoma", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_official_knowledge", "title": "Promoção autônoma a conhecimento oficial", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_permissions", "title": "Ampliação das permissões do usuário", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_audit", "title": "Desligamento da auditoria obrigatória", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_deterministic", "title": "Desligamento de bloqueios determinísticos", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_offline_chat", "title": "Chat conversacional durante o offline", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_art_analysis", "title": "Análise visual autônoma de arte", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_normative", "title": "Alteração autônoma de regras normativas", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_self_authority", "title": "Ampliação da autoridade da própria IA", "scope": LOCKED, "type": "locked", "default": False},
    {"key": "ai.locked_silent_prohibited", "title": "Execução silenciosa de ação proibida", "scope": LOCKED, "type": "locked", "default": False},
)


CATALOGO_POR_CHAVE = {item["key"]: item for item in CONFIGURACOES_IA}


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    autonomous: bool = False
    requires_confirmation: bool = True
    source: str = "LOCKED"
    blocked_by: str = ""


def valores_padrao_ia() -> dict[str, Any]:
    return {item["key"]: item["default"] for item in CONFIGURACOES_IA if item["scope"] != LOCKED}


def normalizar_configuracoes_ia(values: dict[str, Any] | None) -> dict[str, Any]:
    result = valores_padrao_ia()
    for key, value in (values or {}).items():
        definition = CATALOGO_POR_CHAVE.get(key)
        if not definition or definition["scope"] == LOCKED:
            continue
        if definition["type"] in {"bool", "mission"}:
            result[key] = bool(value)
        elif definition["type"] == "choice":
            allowed = {item[0] for item in definition["options"]}
            if value in allowed:
                result[key] = value
    return result


def resolve_ai_policy(*, action: str, company: dict[str, Any] | None = None, user: dict[str, Any] | None = None, mission: dict[str, Any] | None = None, ia_enabled: bool = False) -> PolicyDecision:
    """Resolve uma ação sem permitir que camadas inferiores ampliem autoridade."""
    if action.startswith("finance") or action in {"promote_official_knowledge", "change_normative_rule", "analyze_art_visual"}:
        return PolicyDecision(False, source=LOCKED, blocked_by="Proteção permanente do Mheibos")
    if not ia_enabled:
        return PolicyDecision(False, source="SYSTEM", blocked_by="IA desligada; fluxo determinístico permanece ativo")
    company = normalizar_configuracoes_ia(company)
    user = normalizar_configuracoes_ia(user)
    mission = normalizar_configuracoes_ia(mission)
    if action.startswith("mission.") and not mission.get("ai.mission_autonomy", False):
        return PolicyDecision(False, source=MISSION, blocked_by="Autonomia desta Missão está desligada")
    if action.startswith("optional.") and not (company.get("ai.proactivity") == "proactive" or user.get("ai.user_mode") == "intelligent"):
        return PolicyDecision(False, source=USER, blocked_by="Assistência opcional não autorizada")
    return PolicyDecision(True, autonomous=False, requires_confirmation=True, source="POLICY")

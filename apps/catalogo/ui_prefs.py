from copy import deepcopy
from hashlib import sha1
from decouple import config

from apps.catalogo.models import OperadorGestor, PreferenciaUI

PREFERENCIAS_PADRAO = {
    "tema": "dark",
    "zoom": 100,
    "usuario": "Ruan",
    "widgets": {
        "prazos": {
            "ativo": True,
            "modo": "periodico",
            "intervalo_minutos": 30,
            "visivel_segundos": 60,
            "categorias": [],
        },
        "assistencia": {
            "ativo": True,
            "modo": "periodico",
            "intervalo_minutos": 15,
            "visivel_segundos": 30,
        },
    },
}

ZOOM_OPCOES = (85, 90, 95, 100, 110, 125, 150, 175)


def _merge_dict(base, patch):
    resultado = deepcopy(base)
    if not isinstance(patch, dict):
        return resultado
    for chave, valor in patch.items():
        if isinstance(valor, dict) and isinstance(resultado.get(chave), dict):
            resultado[chave] = {**resultado[chave], **valor}
        elif valor is not None:
            resultado[chave] = valor
    return resultado


def normalizar_zoom(zoom):
    try:
        valor = int(zoom)
    except (TypeError, ValueError):
        valor = 100
    if valor not in ZOOM_OPCOES:
        valor = min(ZOOM_OPCOES, key=lambda item: abs(item - valor))
    return valor


def normalizar_preferencias(dados):
    base = deepcopy(PREFERENCIAS_PADRAO)
    merged = _merge_dict(base, dados or {})
    merged["tema"] = "light" if merged.get("tema") == "light" else "dark"
    merged["zoom"] = normalizar_zoom(merged.get("zoom"))
    merged["usuario"] = str(merged.get("usuario") or PREFERENCIAS_PADRAO["usuario"]).strip()[:80]
    for chave in ("prazos", "assistencia"):
        widget = merged["widgets"][chave]
        widget["ativo"] = bool(widget.get("ativo", True))
        widget["modo"] = widget.get("modo") if widget.get("modo") in {"periodico", "sempre"} else "periodico"
        widget["intervalo_minutos"] = int(widget.get("intervalo_minutos") or 30)
        widget["visivel_segundos"] = int(widget.get("visivel_segundos") or 60)
        if chave == "prazos":
            widget["categorias"] = [int(item) for item in widget.get("categorias", []) if str(item).isdigit()]
    return merged


def _chave_usuario(operador=None, request=None):
    if operador and getattr(operador, "pk", None):
        return f"operador:{operador.pk}"
    nome = ""
    if request is not None:
        nome = (request.session.get("operador_nome") or "").strip()
    if nome:
        operador = OperadorGestor.objects.filter(nome__iexact=nome, ativo=True).first()
        if operador:
            return f"operador:{operador.pk}"
        digest = sha1(nome.casefold().encode("utf-8")).hexdigest()[:16]
        return f"usuario:{digest}"
    return "global"


def carregar_preferencias(operador=None, request=None):
    chave = _chave_usuario(operador=operador, request=request)
    registro = PreferenciaUI.objects.filter(chave=chave).first()
    if not registro and chave != "global":
        registro = PreferenciaUI.objects.filter(chave="global").first()
    if not registro:
        return normalizar_preferencias(PREFERENCIAS_PADRAO)
    return normalizar_preferencias(registro.dados)


def salvar_preferencias(patch, operador=None, request=None):
    chave = _chave_usuario(operador=operador, request=request)
    if isinstance(patch, dict) and {"tema", "zoom", "usuario", "widgets"}.issubset(patch.keys()):
        merged = normalizar_preferencias(patch)
    else:
        atual = carregar_preferencias(operador=operador, request=request)
        merged = normalizar_preferencias(_merge_dict(atual, patch or {}))
    PreferenciaUI.objects.update_or_create(chave=chave, defaults={"dados": merged})
    return merged


def garantir_operadores_padrao():
    from apps.catalogo.authentication import definir_senha_operador
    from apps.catalogo.models import OperadorGestor, PapelOperador

    if config("GESTOR_FIRST_ADMIN_SETUP", default=False, cast=bool) and not OperadorGestor.objects.exists():
        return

    for nome in ("Ruan", "Diogo", "Alexandre"):
        operador, criado = OperadorGestor.objects.update_or_create(
            nome=nome,
            defaults={"ativo": True, "papel": PapelOperador.ADMIN_GERAL},
        )
        if criado or not operador.senha:
            definir_senha_operador(operador, "1234")
    temporario, criado = OperadorGestor.objects.get_or_create(
        nome="Usuario Temporario",
        defaults={"ativo": True, "papel": PapelOperador.TEMPORARIO},
    )
    if criado or not temporario.senha:
        definir_senha_operador(temporario, "1234")

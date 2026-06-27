import json

from apps.catalogo.ui_prefs import carregar_preferencias


def preferencias_ui(request):
    return {"preferencias_ui_json": json.dumps(carregar_preferencias())}

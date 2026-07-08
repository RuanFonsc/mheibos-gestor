from apps.catalogo.models import OperadorGestor, PerfilEmpresa
from apps.catalogo.permissions import operador_atual
from apps.catalogo.ui_prefs import carregar_preferencias


def preferencias_ui(request):
    operador = operador_atual(request)
    perfil_empresa, _ = PerfilEmpresa.objects.get_or_create(chave="global")
    preferencias = carregar_preferencias(operador=operador, request=request)
    if operador:
        preferencias["usuario"] = operador.nome
    return {
        "preferencias_ui_json": preferencias,
        "operador_atual": operador,
        "perfil_empresa": perfil_empresa,
    }

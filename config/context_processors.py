from apps.catalogo.models import OperadorGestor, PerfilEmpresa
from apps.catalogo.permissions import operador_atual
from apps.catalogo.ui_prefs import carregar_preferencias


def preferencias_ui(request):
    operador = operador_atual()
    perfil_empresa, _ = PerfilEmpresa.objects.get_or_create(chave="global")
    return {
        "preferencias_ui_json": carregar_preferencias(),
        "operador_atual": operador,
        "perfil_empresa": perfil_empresa,
    }

from apps.catalogo.models import OperadorGestor, PerfilEmpresa
from apps.catalogo.permissions import operador_atual
from apps.catalogo.ui_prefs import carregar_preferencias
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError


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


def estado_runtime(request):
    offline = settings.MHEIBOS_RUNTIME_ROLE == "client_offline"
    pendentes = 0
    if offline:
        try:
            from apps.sincronizacao.models import EstadoUnidade, UnidadeSincronizacao

            pendentes = UnidadeSincronizacao.objects.exclude(
                estado=EstadoUnidade.INCORPORADA
            ).count()
        except (OperationalError, ProgrammingError):
            pendentes = 0
    return {"runtime_offline": offline, "sincronizacao_pendentes": pendentes}

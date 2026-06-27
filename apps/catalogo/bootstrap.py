from decouple import config

from apps.catalogo.models import OperadorGestor


def primeiro_admin_pendente():
    return config("GESTOR_FIRST_ADMIN_SETUP", default=False, cast=bool) and not OperadorGestor.objects.filter(
        ativo=True
    ).exists()

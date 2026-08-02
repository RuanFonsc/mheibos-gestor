from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.sincronizacao.models import EstadoUnidade, UnidadeSincronizacao


class Command(BaseCommand):
    help = "Confirma que nenhuma unidade local impede o retorno seguro a Central."

    def handle(self, *args, **options):
        if settings.MHEIBOS_RUNTIME_ROLE != "client_offline":
            raise CommandError("A verificacao de retorno so e permitida no Cliente offline.")
        pendentes = UnidadeSincronizacao.objects.exclude(
            estado=EstadoUnidade.INCORPORADA
        ).count()
        if pendentes:
            raise CommandError(f"Retorno bloqueado por {pendentes} unidade(s) local(is).")
        self.stdout.write("RETORNO_SEGURO")

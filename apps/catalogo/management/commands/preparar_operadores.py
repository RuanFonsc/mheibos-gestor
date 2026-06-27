from django.core.management.base import BaseCommand

from apps.catalogo.ui_prefs import garantir_operadores_padrao


class Command(BaseCommand):
    help = "Garante usuários operadores padrão (Ruan, Diogo, Alexandre)."

    def handle(self, *args, **options):
        garantir_operadores_padrao()
        self.stdout.write(self.style.SUCCESS("Operadores padrão garantidos."))

import json
import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.catalogo.authentication import definir_senha_operador
from apps.catalogo.models import OperadorGestor, PapelOperador


class Command(BaseCommand):
    help = "Instala no banco local novo a ultima identidade validada pela Central."

    def handle(self, *args, **options):
        if settings.MHEIBOS_RUNTIME_ROLE != "client_offline":
            raise CommandError("O bootstrap de identidade so e permitido no cliente offline.")
        try:
            payload = json.load(sys.stdin)
        except (TypeError, ValueError) as exc:
            raise CommandError("Identidade offline invalida.") from exc

        station_id = str(payload.get("estacao_id") or "")
        if not settings.MHEIBOS_STATION_ID or station_id != settings.MHEIBOS_STATION_ID:
            raise CommandError("A identidade nao pertence a esta estacao.")

        data = payload.get("operador") or {}
        nome = str(data.get("nome") or "").strip()
        senha = str(payload.get("senha") or "")
        papel = str(data.get("papel") or "")
        codigo = str(data.get("codigo_origem_offline") or "").strip()
        if not nome or not senha or not codigo or papel not in PapelOperador.values:
            raise CommandError("A identidade nao contem os campos obrigatorios.")

        permissoes = payload.get("permissoes") or {}
        esperado_criar = papel != PapelOperador.TEMPORARIO
        esperado_cancelar = papel in {PapelOperador.ADMIN_GERAL, PapelOperador.ADMIN}
        if (
            permissoes.get("pode_criar_pedido") is not esperado_criar
            or permissoes.get("pode_cancelar_pedido") is not esperado_cancelar
        ):
            raise CommandError("As permissoes da identidade nao correspondem ao papel validado.")

        with transaction.atomic():
            outros = OperadorGestor.objects.exclude(nome=nome)
            if outros.exists():
                raise CommandError("O banco local contem outra identidade; nenhuma alteracao foi feita.")
            operador = OperadorGestor.objects.filter(nome=nome).first() or OperadorGestor(nome=nome)
            operador.email = str(data.get("email") or "")
            operador.papel = papel
            operador.codigo_origem_offline = codigo
            operador.ativo = True
            definir_senha_operador(operador, senha, salvar=False)
            operador.save()

        self.stdout.write(self.style.SUCCESS("Identidade offline instalada."))

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.sincronizacao.services import (
    SincronizacaoInvalida,
    confirmar_unidade,
    envelope_da_unidade,
    preparar_proxima_unidade,
    reagendar_unidade,
)
from apps.sincronizacao.transport import TransporteIndisponivel, enviar_envelope


class Command(BaseCommand):
    help = "Envia unidades elegiveis do Cliente offline para a Central."

    def add_arguments(self, parser):
        parser.add_argument("--limite", type=int, default=10)

    def handle(self, *args, **options):
        if settings.MHEIBOS_RUNTIME_ROLE != "client_offline":
            raise CommandError("O envio da fila so e permitido no Cliente offline.")
        limite = max(1, min(int(options["limite"]), 100))
        central_url = settings.MHEIBOS_CENTRAL_URL
        estacao_id = settings.MHEIBOS_STATION_ID
        segredo = settings.MHEIBOS_STATION_SECRET
        if not central_url or not estacao_id or not segredo:
            raise CommandError("Configuracao de sincronizacao incompleta.")

        confirmadas = 0
        falhas = 0
        for _ in range(limite):
            unidade = preparar_proxima_unidade()
            if unidade is None:
                break
            try:
                resposta = enviar_envelope(
                    central_url=central_url,
                    estacao_id=estacao_id,
                    segredo=segredo,
                    envelope=envelope_da_unidade(unidade),
                )
            except TransporteIndisponivel as exc:
                reagendar_unidade(unidade, str(exc))
                falhas += 1
                break

            if resposta.status in {200, 201}:
                try:
                    confirmar_unidade(unidade, resposta.payload)
                except SincronizacaoInvalida as exc:
                    reagendar_unidade(unidade, str(exc), permanente=True)
                    falhas += 1
                else:
                    confirmadas += 1
                continue

            permanente = 400 <= resposta.status < 500
            codigo = str(resposta.payload.get("codigo") or f"HTTP_{resposta.status}")
            motivo = str(resposta.payload.get("motivo") or codigo)
            reagendar_unidade(unidade, motivo, permanente=permanente)
            falhas += 1
            if not permanente or resposta.status in {401, 403, 404, 409}:
                break

        self.stdout.write(f"Confirmadas: {confirmadas}; falhas: {falhas}.")

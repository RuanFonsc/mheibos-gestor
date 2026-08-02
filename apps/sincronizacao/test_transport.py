import io
import json
import uuid
from decimal import Decimal
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase, override_settings

from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido
from apps.sincronizacao.models import UnidadeSincronizacao
from apps.sincronizacao.services import enfileirar_pedido_local
from apps.sincronizacao.transport import (
    _SemRedirecionamento,
    RespostaCentral,
    TransporteIndisponivel,
    enviar_envelope,
)


class _RespostaFake:
    status = 201

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, _limite):
        return json.dumps({"codigo": "INCORPORADO"}).encode()


class TransporteHttpTests(SimpleTestCase):
    @patch("apps.sincronizacao.transport._abrir_url", return_value=_RespostaFake())
    def test_envia_envelope_com_credencial_de_estacao(self, abrir_mock):
        resposta = enviar_envelope(
            central_url="https://central.example",
            estacao_id="station-1",
            segredo="segredo-estacao",
            envelope={"chave": "valor"},
        )

        request = abrir_mock.call_args.args[0]
        self.assertEqual(resposta.status, 201)
        self.assertEqual(request.get_header("X-mheibos-station-id"), "station-1")
        self.assertEqual(request.get_header("X-mheibos-station-secret"), "segredo-estacao")
        self.assertEqual(json.loads(request.data), {"chave": "valor"})

    def test_rejeita_url_sem_http(self):
        with self.assertRaisesMessage(TransporteIndisponivel, "URL"):
            enviar_envelope(
                central_url="file:///central",
                estacao_id="station-1",
                segredo="segredo",
                envelope={},
            )

    def test_nao_segue_redirecionamento_com_credencial(self):
        handler = _SemRedirecionamento()
        self.assertIsNone(handler.redirect_request(None, None, 302, "Moved", {}, "https://outro.example"))


@override_settings(
    MHEIBOS_RUNTIME_ROLE="client_offline",
    MHEIBOS_CENTRAL_URL="https://central.example",
    MHEIBOS_STATION_ID="11111111-1111-1111-1111-111111111111",
    MHEIBOS_STATION_SECRET="segredo-estacao",
)
class EnviarFilaOfflineCommandTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operadora Transporte",
            senha="segura",
            papel=PapelOperador.USUARIO,
            codigo_origem_offline="OT",
        )
        pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Local"),
            tema="Transporte",
            valor_total=Decimal("20.00"),
            usuario_cadastro=self.operador.nome,
        )
        self.unidade = enfileirar_pedido_local(
            pedido=pedido,
            operador=self.operador,
            estacao_id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
            versao_politica="politica-1",
        )

    def executar(self):
        saida = io.StringIO()
        call_command("enviar_fila_offline", limite=10, stdout=saida)
        return saida.getvalue()

    @patch("apps.sincronizacao.management.commands.enviar_fila_offline.enviar_envelope")
    def test_confirmacao_http_valida_encerra_unidade(self, enviar_mock):
        enviar_mock.return_value = RespostaCentral(
            status=201,
            payload={
                "codigo": "INCORPORADO",
                "pedido_global_id": 77,
                "identificador_offline": str(self.unidade.entidade_local_id),
            },
        )

        saida = self.executar()

        self.unidade.refresh_from_db()
        self.assertEqual(self.unidade.estado, "INCORPORADA")
        self.assertEqual(self.unidade.pedido_global_id_confirmado, 77)
        self.assertNotIn("segredo-estacao", saida)

    @patch("apps.sincronizacao.management.commands.enviar_fila_offline.enviar_envelope")
    def test_indisponibilidade_reagenda_sem_perder_envelope(self, enviar_mock):
        enviar_mock.side_effect = TransporteIndisponivel("Central indisponivel.")

        self.executar()

        self.unidade.refresh_from_db()
        self.assertEqual(self.unidade.estado, "FALHA_TEMPORARIA")
        self.assertIsNotNone(self.unidade.proxima_tentativa_em)
        self.assertTrue(self.unidade.payload["pedido"])

    @patch("apps.sincronizacao.management.commands.enviar_fila_offline.enviar_envelope")
    def test_recusa_de_credencial_exige_atencao_sem_loop(self, enviar_mock):
        enviar_mock.return_value = RespostaCentral(
            status=401, payload={"codigo": "ESTACAO_NAO_AUTORIZADA"}
        )

        self.executar()

        self.unidade.refresh_from_db()
        self.assertEqual(self.unidade.estado, "REQUER_ATENCAO")
        self.assertIsNone(self.unidade.proxima_tentativa_em)

    @override_settings(MHEIBOS_RUNTIME_ROLE="central")
    def test_central_nao_pode_executar_envio_local(self):
        with self.assertRaisesMessage(CommandError, "Cliente offline"):
            self.executar()

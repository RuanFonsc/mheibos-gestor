import io
import json
from unittest.mock import patch

from django.contrib.auth.hashers import check_password
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from apps.catalogo.models import OperadorGestor, PapelOperador


@override_settings(MHEIBOS_RUNTIME_ROLE="client_offline", MHEIBOS_STATION_ID="station-1")
class BootstrapIdentidadeOfflineTests(TestCase):
    def payload(self, **changes):
        data = {
            "estacao_id": "station-1",
            "operador": {
                "nome": "Ana",
                "email": "ana@example.com",
                "papel": PapelOperador.USUARIO,
                "codigo_origem_offline": "ANA01",
            },
            "permissoes": {"pode_criar_pedido": True, "pode_cancelar_pedido": False},
            "versao_politica": "baseline-1",
            "senha": "segredo-local",
        }
        data.update(changes)
        return data

    def executar(self, payload):
        with patch("sys.stdin", io.StringIO(json.dumps(payload))):
            call_command("bootstrap_identidade_offline", stdout=io.StringIO())

    def test_instala_um_operador_com_senha_protegida(self):
        self.executar(self.payload())
        operador = OperadorGestor.objects.get(nome="Ana")
        self.assertTrue(operador.ativo)
        self.assertTrue(check_password("segredo-local", operador.senha))
        self.assertEqual(OperadorGestor.objects.count(), 1)

    def test_rejeita_identidade_de_outra_estacao(self):
        with self.assertRaisesMessage(CommandError, "nao pertence"):
            self.executar(self.payload(estacao_id="station-2"))
        self.assertFalse(OperadorGestor.objects.exists())

    def test_rejeita_permissoes_incompativeis(self):
        payload = self.payload(permissoes={"pode_criar_pedido": True, "pode_cancelar_pedido": True})
        with self.assertRaisesMessage(CommandError, "nao correspondem"):
            self.executar(payload)

    def test_preserva_banco_que_ja_contem_outra_identidade(self):
        anterior = OperadorGestor.objects.create(nome="Anterior", senha="antiga")
        with self.assertRaisesMessage(CommandError, "nenhuma alteracao"):
            self.executar(self.payload())
        anterior.refresh_from_db()
        self.assertTrue(anterior.ativo)
        self.assertEqual(OperadorGestor.objects.count(), 1)

    @override_settings(MHEIBOS_RUNTIME_ROLE="central")
    def test_rejeita_execucao_na_central(self):
        with self.assertRaisesMessage(CommandError, "cliente offline"):
            self.executar(self.payload())

from unittest.mock import patch
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, override_settings
from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from .models import EstadoMissao, Missao, OrigemMissao
from .services import criar_missao_individual_voluntaria


class MissaoIndividualTests(TestCase):
    def setUp(self):
        self.dona = OperadorGestor.objects.create(nome="Dona Missão", senha="segura", papel=PapelOperador.USUARIO)
        self.outra = OperadorGestor.objects.create(nome="Outra Pessoa", senha="segura", papel=PapelOperador.USUARIO)

    def _entrar(self, operador):
        session = self.client.session
        session["operador_id"] = operador.pk
        session.save()

    def test_criacao_voluntaria_preserva_contrato_minimo_e_evento(self):
        missao = criar_missao_individual_voluntaria(operador=self.dona, titulo=" Preparar mostra ", objetivo="Organizar materiais", criterio_conclusao="Mostra pronta")
        self.assertEqual(missao.origem, OrigemMissao.VOLUNTARIA)
        self.assertEqual(missao.estado, EstadoMissao.PLANEJADA)
        self.assertEqual(missao.criador, self.dona)
        self.assertEqual(missao.responsavel_principal, self.dona)
        self.assertTrue(EventoOperacional.objects.filter(tipo="MissaoCriada", alvo_id=str(missao.pk)).exists())

    def test_contrato_minimo_e_identidade_temporaria_sao_recusados(self):
        with self.assertRaises(ValidationError):
            criar_missao_individual_voluntaria(operador=self.dona, titulo="", objetivo="Objetivo", criterio_conclusao="Fim")
        temporario = OperadorGestor.objects.create(nome="Temporário", senha="x", papel=PapelOperador.TEMPORARIO)
        with self.assertRaises(PermissionDenied):
            criar_missao_individual_voluntaria(operador=temporario, titulo="Missão", objetivo="Objetivo", criterio_conclusao="Fim")

    @patch("apps.missoes.services.registrar_evento", side_effect=RuntimeError("falha"))
    def test_falha_de_auditoria_reverte_criacao(self, _evento):
        with self.assertRaises(RuntimeError):
            criar_missao_individual_voluntaria(operador=self.dona, titulo="Missão", objetivo="Objetivo", criterio_conclusao="Fim")
        self.assertFalse(Missao.objects.exists())

    def test_lista_e_detalhe_nao_expoem_missao_de_outra_pessoa(self):
        missao = criar_missao_individual_voluntaria(operador=self.dona, titulo="Privada", objetivo="Objetivo", criterio_conclusao="Fim")
        self._entrar(self.outra)
        self.assertNotContains(self.client.get("/missoes/"), "Privada")
        self.assertEqual(self.client.get(f"/missoes/{missao.pk}/").status_code, 404)

    @override_settings(MHEIBOS_RUNTIME_ROLE="client_offline")
    def test_modo_offline_permite_consulta_mas_bloqueia_criacao(self):
        self._entrar(self.dona)
        self.assertEqual(self.client.get("/missoes/").status_code, 200)
        response = self.client.post("/missoes/nova/", {"titulo": "Offline", "objetivo": "Objetivo", "criterio_conclusao": "Fim"})
        self.assertEqual(response.status_code, 409)
        self.assertFalse(Missao.objects.exists())

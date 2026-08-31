import json

from django.contrib.auth.hashers import check_password
from django.test import RequestFactory, TestCase

from apps.catalogo.authentication import (
    autenticar_operador,
    iniciar_sessao_operador,
    senha_esta_protegida,
    validar_senha_operador,
)
from apps.catalogo.models import OperadorGestor, PapelOperador, PerfilEmpresa, PreferenciaUI
from apps.catalogo.ui_prefs import carregar_preferencias
from apps.catalogo.permissions import operador_atual


class CredencialOperadorTests(TestCase):
    def test_new_operator_never_persists_plain_text_password(self):
        operador = OperadorGestor.objects.create(
            nome="Ana Segura",
            senha="segredo123",
            papel=PapelOperador.ADMIN_GERAL,
        )

        operador.refresh_from_db()
        self.assertNotEqual(operador.senha, "segredo123")
        self.assertTrue(senha_esta_protegida(operador.senha))
        self.assertTrue(check_password("segredo123", operador.senha))

    def test_valid_legacy_password_is_upgraded_on_first_authentication(self):
        operador = OperadorGestor.objects.create(
            nome="Operador Legado",
            senha="provisoria",
            papel=PapelOperador.USUARIO,
        )
        OperadorGestor.objects.filter(pk=operador.pk).update(senha="1234")
        operador.refresh_from_db()

        self.assertTrue(validar_senha_operador(operador, "1234"))

        operador.refresh_from_db()
        self.assertTrue(senha_esta_protegida(operador.senha))
        self.assertTrue(check_password("1234", operador.senha))

    def test_invalid_legacy_password_does_not_modify_credential(self):
        operador = OperadorGestor.objects.create(
            nome="Legado Inválido",
            senha="provisoria",
            papel=PapelOperador.USUARIO,
        )
        OperadorGestor.objects.filter(pk=operador.pk).update(senha="1234")
        operador.refresh_from_db()

        self.assertFalse(validar_senha_operador(operador, "errada"))

        operador.refresh_from_db()
        self.assertEqual(operador.senha, "1234")


class SessaoOperadorTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Carla",
            senha="senha123",
            papel=PapelOperador.ADMIN_GERAL,
        )

    def test_web_login_stores_stable_operator_id(self):
        response = self.client.post(
            "/login/",
            {"usuario": self.operador.nome, "senha": "senha123"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["operador_id"], self.operador.pk)
        self.assertEqual(self.client.session["operador_nome"], self.operador.nome)

    def test_configuracoes_expoem_preferencias_de_arte_e_perfil_da_empresa(self):
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

        response = self.client.get("/configuracoes/")

        self.assertContains(response, "Programa padrao para arte oficial")
        self.assertContains(response, "Perfil da Empresa")
        self.assertContains(response, "Pasta compartilhada das artes oficiais")
        self.assertContains(response, 'id="gestaoUsuariosDestino"')

    def test_configuracoes_separam_artes_da_identidade_da_empresa_e_expoem_alertas(self):
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

        response = self.client.get("/configuracoes/?aba=operacao")
        content = response.content.decode("utf-8")
        empresa = content.split('id="tab-empresa"', 1)[1].split('id="tab-aparencia"', 1)[0]
        operacao = content.split('id="tab-operacao"', 1)[1].split('id="tab-aparencia"', 1)[0]

        self.assertNotIn("diretorioArtesRaiz", empresa)
        self.assertNotIn("retencaoCopiasLocaisDias", empresa)
        self.assertIn("operacao-artes-oficiais", operacao)
        self.assertIn('id="btnEscolherDiretorio"', operacao)
        self.assertIn("Escolher diretório", operacao)
        self.assertIn("status-alertas-sistemicos", operacao)
        self.assertIn("Arquivo oficial ausente", operacao)
        self.assertIn("Arte sem atualização", operacao)
        self.assertIn("Aguardando arte", operacao)
        self.assertIn("Widget de prazos", operacao)
        self.assertIn("Notificação da Assistência de Impressão", operacao)

    def test_configuracao_de_artes_persiste_fora_do_perfil_da_empresa(self):
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

        response = self.client.post(
            "/configuracoes/",
            {
                "acao": "salvar_configuracao_artes",
                "diretorio_artes_raiz": r"\\servidor\artes-oficiais",
                "retencao_copias_locais_dias": "45",
            },
        )

        self.assertEqual(response.status_code, 302)
        perfil = PerfilEmpresa.objects.get(chave="global")
        self.assertEqual(perfil.diretorio_artes_raiz, r"\\servidor\artes-oficiais")
        self.assertEqual(perfil.retencao_copias_locais_dias, 45)

    def test_usuario_salva_programa_de_arte_preferido(self):
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

        response = self.client.post(
            "/configuracoes/",
            {"acao": "salvar_preferencias_perfil", "programa_arte": "affinity_photo"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            carregar_preferencias(operador=self.operador)["programa_arte"],
            "affinity_photo",
        )

    def test_configuracoes_ia_expoem_escopos_e_protecoes_locked(self):
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()
        response = self.client.get("/configuracoes/?aba=ia")
        self.assertContains(response, "Política organizacional")
        self.assertContains(response, "Autonomia por Missão")
        self.assertContains(response, "Decisões não configuráveis")
        self.assertContains(response, "LOCKED")

    def test_empresa_ia_requires_admin_password_and_persists_allowed_values(self):
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()
        response = self.client.post("/configuracoes/", {"acao": "salvar_ia_empresa", "ai.proactivity": "proactive", "senha_admin": "senha123"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PreferenciaUI.objects.get(chave="ia:empresa").dados["ai.proactivity"], "proactive")

    def test_user_ia_preferences_are_scoped_to_operator(self):
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()
        response = self.client.post("/configuracoes/", {"acao": "salvar_ia_usuario", "ai.user_mode": "intelligent", "ai.contextual_facilities": "on"})
        self.assertEqual(response.status_code, 302)
        dados = PreferenciaUI.objects.get(chave=f"operador:{self.operador.pk}").dados
        self.assertEqual(dados["ia"]["ai.user_mode"], "intelligent")
        self.assertTrue(dados["ia"]["ai.contextual_facilities"])

    def test_launcher_login_uses_same_authentication_contract(self):
        response = self.client.post(
            "/api/launcher/login/",
            data=json.dumps({"usuario": self.operador.nome, "senha": "senha123"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(self.client.session["operador_id"], self.operador.pk)

    def test_session_survives_operator_rename_by_technical_id(self):
        request = RequestFactory().get("/")
        request.session = self.client.session
        iniciar_sessao_operador(request, self.operador)
        request.session.save()
        self.operador.nome = "Carla Renomeada"
        self.operador.save(update_fields=["nome", "atualizado_em"])

        encontrado = operador_atual(request)

        self.assertEqual(encontrado.pk, self.operador.pk)
        self.assertEqual(encontrado.nome, "Carla Renomeada")
        self.assertEqual(request.session["operador_nome"], "Carla Renomeada")

    def test_wrong_password_is_rejected(self):
        self.assertIsNone(autenticar_operador(self.operador.nome, "incorreta"))

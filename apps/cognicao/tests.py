from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido
from apps.aprendizado.models import ConversaAprendizado, MensagemAprendizado, OrigemConversa, DirecaoMensagem

from .gateway import FALLBACK_RESUMO, GatewayIA, SolicitacaoCognitiva, _normalizar_resposta
from .configuracoes_ia import resolve_ai_policy, normalizar_configuracoes_ia
from .alertas import encaminhar_alertas_para_ia
from .models import AlertaCognitiva, ConversaCognitiva, MensagemCognitiva, TarefaCognitiva
from .tools import ComandoInterface, executar_ferramenta
from .whatsapp import espelhar_mensagem_whatsapp
from .management.commands.processar_cognicao import _proposta_deterministica


class GatewayIATests(TestCase):
    def test_locked_financial_action_never_becomes_autonomous(self):
        decision = resolve_ai_policy(action="finance.approve_payment", ia_enabled=True)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.blocked_by, "Proteção permanente do Mheibos")

    def test_disabled_ai_keeps_deterministic_path_available(self):
        decision = resolve_ai_policy(action="optional.summary", ia_enabled=False)
        self.assertFalse(decision.allowed)
        self.assertIn("IA desligada", decision.blocked_by)

    def test_mission_autonomy_is_scoped_to_that_mission(self):
        disabled = resolve_ai_policy(action="mission.replan", mission={}, ia_enabled=True)
        enabled = resolve_ai_policy(
            action="mission.replan",
            mission={"ai.mission_autonomy": True},
            ia_enabled=True,
        )
        self.assertFalse(disabled.allowed)
        self.assertTrue(enabled.allowed)

    def test_normalizer_ignores_locked_values(self):
        values = normalizar_configuracoes_ia({"ai.locked_financial": True, "ai.user_mode": "intelligent"})
        self.assertNotIn("ai.locked_financial", values)
        self.assertEqual(values["ai.user_mode"], "intelligent")

    def test_disabled_gateway_returns_non_blocking_fallback(self):
        resposta = GatewayIA(None).solicitar(SolicitacaoCognitiva("teste", "fatos"))

        self.assertFalse(resposta.disponivel)
        self.assertEqual(resposta.texto, FALLBACK_RESUMO)
        self.assertEqual(resposta.codigo, "IA_DESLIGADA")

    def test_provider_failure_returns_non_blocking_fallback(self):
        provedor = Mock(nome="gemini")
        provedor.nome = "gemini"
        provedor.gerar.side_effect = RuntimeError("indisponivel")

        resposta = GatewayIA(provedor, modelo="modelo").solicitar(
            SolicitacaoCognitiva("teste", "fatos")
        )

        self.assertFalse(resposta.disponivel)
        self.assertEqual(resposta.codigo, "PROVEDOR_INDISPONIVEL")

    def test_structured_response_only_keeps_registered_interface_commands(self):
        texto, comandos = _normalizar_resposta(
            '{"texto":"Use Data de Entrega.","comandos":[{"comando":"navegar","parametros":{"tela":"novo_pedido","campo":"data_entrega"},"rotulo":"Mostrar campo"},{"comando":"apagar_banco","parametros":{},"rotulo":"Perigoso"}]}'
        )
        self.assertEqual(texto, "Use Data de Entrega.")
        self.assertEqual(len(comandos), 1)
        self.assertEqual(comandos[0]["parametros"]["campo"], "data_entrega")
        self.assertEqual(comandos[0]["parametros"]["rota"], "/pedidos/novo/")
    def test_provider_success_is_a_read_only_response(self):
        provedor = Mock(nome="gemini")
        provedor.nome = "gemini"
        provedor.gerar.return_value = "Resumo sugerido"

        resposta = GatewayIA(provedor, modelo="modelo").solicitar(
            SolicitacaoCognitiva("teste", "fatos")
        )

        self.assertTrue(resposta.disponivel)
        self.assertEqual(resposta.texto, "Resumo sugerido")


class ResumoPedidoTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operador IA", senha="senha", papel=PapelOperador.USUARIO
        )
        self.pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente IA"),
            usuario_cadastro=self.operador.nome,
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

    @override_settings(MHEIBOS_IA_ENABLED=False)
    def test_endpoint_works_with_ai_disabled_and_does_not_change_order(self):
        response = self.client.post(f"/cognicao/pedidos/{self.pedido.pk}/resumo/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fallback seguro")
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.usuario_cadastro, self.operador.nome)
        self.assertTrue(
            EventoOperacional.objects.filter(
                tipo="AssistenciaCognitivaSolicitada", alvo_id=str(self.pedido.pk)
            ).exists()
        )

    @patch("apps.cognicao.views.resumir_pedido")
    def test_audit_failure_does_not_block_assistance(self, resumir):
        from .gateway import RespostaCognitiva

        resumir.return_value = RespostaCognitiva(
            "Resumo", True, "fake", "fake-model", "SUCESSO"
        )
        with patch("apps.cognicao.views.registrar_evento", side_effect=RuntimeError):
            response = self.client.post(
                f"/cognicao/pedidos/{self.pedido.pk}/resumo/"
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resumo")

    def test_endpoint_rejects_get(self):
        response = self.client.get(f"/cognicao/pedidos/{self.pedido.pk}/resumo/")
        self.assertEqual(response.status_code, 405)


class CognitiveToolTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operador Ferramentas", senha="senha", papel=PapelOperador.USUARIO
        )
        self.pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Ferramentas"),
            usuario_cadastro=self.operador.nome,
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

    def test_consult_tool_returns_authorized_operational_projection(self):
        resultado = executar_ferramenta(
            nome="consultar_pedido",
            operador=self.operador,
            parametros={"pedido_id": self.pedido.pk},
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["pedido"]["id"], self.pedido.pk)
        self.assertIn("operacional", resultado.dados["pedido"])

    def test_tool_does_not_expose_another_operator_order(self):
        outro = OperadorGestor.objects.create(
            nome="Outro Operador", senha="senha", papel=PapelOperador.USUARIO
        )
        pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Restrito"),
            usuario_cadastro=outro.nome,
        )

        resultado = executar_ferramenta(
            nome="consultar_pedido",
            operador=self.operador,
            parametros={"pedido_id": pedido.pk},
        )

        self.assertFalse(resultado.sucesso)
        self.assertIn("escopo", resultado.erro)

    def test_alert_tool_returns_authorized_contract(self):
        resultado = executar_ferramenta(
            nome="consultar_alertas",
            operador=self.operador,
            parametros={"somente_criticos": True},
        )

        self.assertTrue(resultado.sucesso)
        self.assertIn("alertas", resultado.dados)
        self.assertEqual(resultado.dados["total_criticos"], 0)
        self.assertEqual(resultado.dados["alertas"], [])

    def test_open_tool_returns_structured_interface_command(self):
        resultado = executar_ferramenta(
            nome="abrir_pedido",
            operador=self.operador,
            parametros={"pedido_id": self.pedido.pk},
        )

        self.assertTrue(resultado.sucesso)
        self.assertIsInstance(resultado.dados["interface"], ComandoInterface)
        self.assertEqual(resultado.dados["interface"].comando, "navegar")

    def test_fill_tool_returns_confirmable_registered_fields(self):
        resultado = executar_ferramenta(
            nome="preencher_campos",
            operador=self.operador,
            parametros={"tela": "novo_pedido", "valores": {"data_entrega": "2026-09-05"}},
        )

        self.assertTrue(resultado.sucesso)
        self.assertTrue(resultado.requer_confirmacao)
        self.assertEqual(resultado.dados["interface"].comando, "preencher_campos")

    def test_fill_tool_rejects_unregistered_fields(self):
        resultado = executar_ferramenta(
            nome="preencher_campos",
            operador=self.operador,
            parametros={"tela": "novo_pedido", "valores": {"campo_inventado": "x"}},
        )

        self.assertFalse(resultado.sucesso)


    def test_unknown_tool_is_rejected(self):
        resultado = executar_ferramenta(
            nome="executar_codigo",
            operador=self.operador,
            parametros={},
        )

        self.assertFalse(resultado.sucesso)
        self.assertIn("não autorizada", resultado.erro)

    def test_status_change_is_only_a_confirmable_proposal(self):
        resultado = executar_ferramenta(
            nome="propor_alteracao_status",
            operador=self.operador,
            parametros={"pedido_id": self.pedido.pk, "novo_status": "ARTE_EM_PREPARO", "motivo": "Solicitado pelo cliente"},
        )

        self.assertTrue(resultado.sucesso)
        self.assertTrue(resultado.requer_confirmacao)
        self.pedido.refresh_from_db()
        self.assertNotEqual(self.pedido.status, "ARTE_EM_PREPARO")

    def test_confirmed_status_change_uses_domain_case_and_audit(self):
        response = self.client.post(
            "/cognicao/assistente/acoes/alterar-status/",
            data='{"pedido_id": %d, "novo_status": "ARTE_EM_PREPARO", "motivo": "Solicitado pelo cliente"}' % self.pedido.pk,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["sucesso"])
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, "ARTE_EM_PREPARO")
        self.assertTrue(EventoOperacional.objects.filter(tipo="PedidoStatusAlterado", alvo_id=str(self.pedido.pk)).exists())

    def test_whatsapp_page_exposes_selected_conversation_context(self):
        conversa = ConversaAprendizado.objects.create(
            origem=OrigemConversa.WHATSAPP,
            instancia="principal",
            contato_id="5511999999999@s.whatsapp.net",
            telefone="5511999999999",
            nome_contato="Contato da Tela",
        )
        MensagemAprendizado.objects.create(
            conversa=conversa,
            mensagem_id="page-msg-1",
            direcao=DirecaoMensagem.CLIENTE,
            texto="Quero acompanhar meu pedido.",
        )

        response = self.client.get(f"/cognicao/whatsapp/?conversa={conversa.pk}")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contato da Tela")
        self.assertContains(response, "5511999999999")
        self.assertContains(response, "Quero acompanhar meu pedido.")
        self.assertContains(response, "whatsapp-context-data")
    def test_whatsapp_message_is_available_in_cognitive_context_without_auto_reply(self):
        conversa = ConversaAprendizado.objects.create(
            origem=OrigemConversa.WHATSAPP,
            instancia="principal",
            contato_id="5511999999999@s.whatsapp.net",
            telefone="5511999999999",
            nome_contato="Contato WhatsApp",
        )
        MensagemAprendizado.objects.create(
            conversa=conversa,
            mensagem_id="msg-1",
            direcao=DirecaoMensagem.CLIENTE,
            texto="Preciso saber o prazo do meu pedido.",
        )

        contexto = espelhar_mensagem_whatsapp(conversa)

        self.assertEqual(contexto.origem, "WHATSAPP")
        self.assertEqual(contexto.mensagens.count(), 1)
        self.assertFalse(contexto.tarefas.exists())

    def test_evolution_webhook_mirrors_message_without_automatic_reply(self):
        response = self.client.post(
            "/aprendizado/webhook/evolution/",
            data={
                "instance": "principal",
                "data": {
                    "key": {"remoteJid": "5511888888888@s.whatsapp.net", "id": "evo-1", "fromMe": False},
                    "pushName": "Contato Evolution",
                    "message": {"conversation": "Quero acompanhar meu pedido."},
                    "messageType": "conversation",
                },
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("contexto_cognitivo_id", response.json())
        self.assertEqual(TarefaCognitiva.objects.count(), 0)

    def test_explicit_order_search_creates_registered_interface_command(self):
        tarefa = type("Tarefa", (), {"conversa": self})()
        resultado = _proposta_deterministica("Pesquise pedidos de Cliente Ferramentas", tarefa)
        self.assertEqual(resultado["comandos"][0]["comando"], "pesquisar_pedidos")
        self.assertEqual(resultado["comandos"][0]["parametros"]["termo"], "Cliente Ferramentas")
    def test_interface_context_keeps_only_visible_metadata(self):
        response = self.client.post(
            "/cognicao/assistente/mensagens/",
            data='{"texto":"Onde fica este campo?","interface_context":{"rota":"/pedidos/novo/","titulo":"Novo Pedido","campos":[{"nome":"data_entrega","rotulo":"Data de Entrega","tipo":"date","obrigatorio":true,"valor":"segredo"}],"acoes":[{"texto":"Salvar","tipo":"button","href":"","token":"segredo"}]}}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        tarefa = TarefaCognitiva.objects.get(pk=response.json()["tarefa_id"])
        campo = tarefa.contexto["interface"]["campos"][0]
        acao = tarefa.contexto["interface"]["acoes"][0]
        self.assertEqual(campo["rotulo"], "Data de Entrega")
        self.assertNotIn("valor", campo)
        self.assertNotIn("token", acao)
    def test_interface_context_keeps_whatsapp_conversation(self):
        payload = {
            "texto": "Analise esta conversa.",
            "interface_context": {
                "rota": "/cognicao/whatsapp/",
                "titulo": "WhatsApp",
                "whatsapp": {
                    "conversa_id": "17",
                    "nome": "Cliente Contextual",
                    "telefone": "5511999999999",
                    "mensagens": [
                        {"direcao": "CLIENTE", "texto": "Preciso atualizar meu pedido.", "token": "não enviar"},
                    ],
                },
            },
        }

        response = self.client.post(
            "/cognicao/assistente/mensagens/",
            data=__import__("json").dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        tarefa = TarefaCognitiva.objects.get(pk=response.json()["tarefa_id"])
        whatsapp = tarefa.contexto["interface"]["whatsapp"]
        self.assertEqual(whatsapp["nome"], "Cliente Contextual")
        self.assertEqual(whatsapp["mensagens"][0]["texto"], "Preciso atualizar meu pedido.")
        self.assertNotIn("token", whatsapp["mensagens"][0])
    def test_assistant_page_and_message_endpoint_enqueue_without_waiting_for_provider(self):
        page = self.client.get("/cognicao/assistente/")
        self.assertEqual(page.status_code, 200)
        response = self.client.post(
            "/cognicao/assistente/mensagens/",
            data='{"texto":"Mostre o estado do meu pedido."}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "PENDENTE")
        self.assertEqual(TarefaCognitiva.objects.count(), 1)


class AlertTriggerTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operador Alertas", senha="senha", papel="USUARIO"
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()
        self.alerta = {
            "id": "inatividade-arte-42",
            "pedido_id": 42,
            "pedido_label": "Pedido #42",
            "cliente": "Cliente Alertas",
            "categoria_id": "inatividade-arte",
            "categoria_nome": "Arte sem atualização",
            "tipo": "critico",
            "nivel": 4,
            "criticidade": "critico",
            "titulo": "A arte precisa de uma resposta",
            "mensagem": "O prazo está crítico; responda ao alerta agora.",
            "href": "/pedidos/42/#arquivos-oficiais",
            "acao_label": "Responder alerta",
            "exige_acao": True,
            "pode_dispensar": False,
            "acoes_disponiveis": ["Responder alerta"],
            "arquivo_id": "",
            "numero": 1,
        }

    @override_settings(MHEIBOS_IA_ENABLED=True, MHEIBOS_IA_PROVIDER="gemini", GEMINI_API_KEY="test-key")
    @patch("apps.cognicao.alertas.alertas_operacionais")
    def test_alert_is_forwarded_once_and_again_after_material_change(self, consultar):
        consultar.return_value = {
            "alertas": [self.alerta],
            "total_alertas": 1,
            "total_criticos": 1,
            "total_exige_acao": 1,
            "exige_acao": True,
        }

        primeira = encaminhar_alertas_para_ia(operador=self.operador)
        segunda = encaminhar_alertas_para_ia(operador=self.operador)

        self.assertEqual(len(primeira), 1)
        self.assertEqual(segunda, [])
        self.assertEqual(TarefaCognitiva.objects.filter(contexto__tipo="gatilho_alerta").count(), 1)
        self.assertEqual(AlertaCognitiva.objects.count(), 1)
        TarefaCognitiva.objects.filter(contexto__tipo="gatilho_alerta").update(estado="CONCLUIDA")

        consultar.return_value["alertas"] = [{**self.alerta, "mensagem": "O alerta continua crítico e exige resposta."}]
        terceira = encaminhar_alertas_para_ia(operador=self.operador)

        self.assertEqual(len(terceira), 1)
        self.assertEqual(TarefaCognitiva.objects.filter(contexto__tipo="gatilho_alerta").count(), 2)

    def test_alert_notification_endpoint_delivers_each_task_once(self):
        conversa = ConversaCognitiva.objects.create(
            operador=self.operador,
            titulo="Alertas operacionais",
            referencia_externa="alertas-operacionais",
        )
        mensagem = MensagemCognitiva.objects.create(
            conversa=conversa,
            papel="SISTEMA",
            texto="Alerta para análise.",
        )
        tarefa = TarefaCognitiva.objects.create(
            conversa=conversa,
            mensagem_usuario=mensagem,
            estado="CONCLUIDA",
            contexto={"tipo": "gatilho_alerta", "alerta": self.alerta},
            resultado={
                "texto": "O Pedido #42 precisa de uma decisão.",
                "disponivel": True,
                "comandos": [],
            },
        )

        primeira = self.client.get("/cognicao/assistente/notificacoes-alertas/")
        segunda = self.client.get("/cognicao/assistente/notificacoes-alertas/")

        self.assertEqual(primeira.status_code, 200)
        self.assertEqual(len(primeira.json()["notificacoes"]), 1)
        self.assertEqual(segunda.json()["notificacoes"], [])
        tarefa.refresh_from_db()
        self.assertIsNotNone(tarefa.notificado_em)

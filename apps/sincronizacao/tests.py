import copy
import json
import uuid
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, override_settings

from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido, PedidoItem

from .models import EstacaoCliente, IncorporacaoOffline, SequenciaOffline, UnidadeSincronizacao
from .services import (
    SincronizacaoInvalida,
    calcular_checksum,
    criar_estacao,
    enfileirar_pedido_local,
    incorporar_pedido_offline,
    registrar_falha,
)


class FilaOfflineTests(TestCase):
    def setUp(self):
        self.estacao = uuid.uuid4()
        self.operador = OperadorGestor.objects.create(
            nome="Autora Offline",
            senha="segura",
            papel=PapelOperador.USUARIO,
            codigo_origem_offline="AO",
        )
        self.pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Local"),
            tema="Pedido local",
            valor_total=Decimal("35.00"),
            usuario_cadastro=self.operador.nome,
        )
        PedidoItem.objects.create(
            pedido=self.pedido,
            nome="Caneca",
            quantidade=Decimal("2"),
            preco_unitario=Decimal("17.50"),
        )

    def test_enqueue_reserves_durable_identity_and_event_atomically(self):
        unidade = enfileirar_pedido_local(
            pedido=self.pedido,
            operador=self.operador,
            estacao_id=self.estacao,
            versao_politica="politica-1",
        )

        self.pedido.refresh_from_db()
        self.assertTrue(self.pedido.origem_offline)
        self.assertEqual(self.pedido.codigo_visivel_offline, "AO1")
        self.assertEqual(unidade.entidade_local_id, self.pedido.identificador_offline)
        self.assertEqual(unidade.checksum, calcular_checksum(unidade.payload))
        self.assertEqual(SequenciaOffline.objects.get().ultimo_numero, 1)
        evento = EventoOperacional.objects.get(tipo="PedidoOfflineCriado")
        self.assertEqual(evento.origem, "cliente_offline")
        self.assertEqual(evento.metadados["estacao_id"], str(self.estacao))

    def test_repeated_enqueue_returns_same_unit_without_consuming_sequence(self):
        primeira = enfileirar_pedido_local(
            pedido=self.pedido,
            operador=self.operador,
            estacao_id=self.estacao,
            versao_politica="politica-1",
        )
        segunda = enfileirar_pedido_local(
            pedido=self.pedido,
            operador=self.operador,
            estacao_id=self.estacao,
            versao_politica="politica-1",
        )

        self.assertEqual(primeira.pk, segunda.pk)
        self.assertEqual(UnidadeSincronizacao.objects.count(), 1)
        self.assertEqual(SequenciaOffline.objects.get().ultimo_numero, 1)

    @patch("apps.sincronizacao.services.registrar_evento", side_effect=RuntimeError)
    def test_event_failure_rolls_back_identity_queue_and_sequence(self, _evento):
        with self.assertRaises(RuntimeError):
            enfileirar_pedido_local(
                pedido=self.pedido,
                operador=self.operador,
                estacao_id=self.estacao,
                versao_politica="politica-1",
            )

        self.pedido.refresh_from_db()
        self.assertFalse(self.pedido.origem_offline)
        self.assertIsNone(self.pedido.identificador_offline)
        self.assertFalse(UnidadeSincronizacao.objects.exists())
        self.assertFalse(SequenciaOffline.objects.exists())

    def test_operator_without_permanent_origin_code_cannot_enqueue(self):
        self.operador.codigo_origem_offline = None
        self.operador.save(update_fields=["codigo_origem_offline"])

        with self.assertRaises(SincronizacaoInvalida):
            enfileirar_pedido_local(
                pedido=self.pedido,
                operador=self.operador,
                estacao_id=self.estacao,
                versao_politica="politica-1",
            )

    def test_failure_remains_visible_and_does_not_delete_payload(self):
        unidade = enfileirar_pedido_local(
            pedido=self.pedido,
            operador=self.operador,
            estacao_id=self.estacao,
            versao_politica="politica-1",
        )

        registrar_falha(unidade, "Central indisponivel")

        unidade.refresh_from_db()
        self.assertEqual(unidade.tentativas, 1)
        self.assertEqual(unidade.estado, "FALHA_TEMPORARIA")
        self.assertEqual(unidade.motivo_falha, "Central indisponivel")
        self.assertTrue(unidade.payload["pedido"])

    def test_causal_payload_cannot_be_rewritten_after_enqueue(self):
        unidade = enfileirar_pedido_local(
            pedido=self.pedido,
            operador=self.operador,
            estacao_id=self.estacao,
            versao_politica="politica-1",
        )
        unidade.payload["pedido"]["tema"] = "Reescrito"

        with self.assertRaises(ValueError):
            unidade.save()


class IncorporacaoCentralTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Autora Central",
            senha="segura",
            papel=PapelOperador.USUARIO,
            codigo_origem_offline="AC",
        )
        self.payload = {
            "pedido": {
                "tema": "Pedido incorporado",
                "data_pedido": "2026-08-01",
                "data_entrega": "2026-08-03",
                "hora_entrega": None,
                "observacoes": "Preservar",
                "valor_total": "50.00",
                "valor_pago_legado": "0.00",
                "desconto_ajuste": "0.00",
                "forma_pagamento_legada": "PIX",
                "prioridade": "NORMAL",
                "status": "AGUARDANDO_ARTE",
                "estado_comercial": "CONFIRMADO",
                "estado_entrega": "PENDENTE",
                "canal_atendimento": "PRESENCIAL",
                "usuario_cadastro": self.operador.nome,
            },
            "cliente": {
                "nome": "Cliente Incorporado",
                "email": "",
                "telefone_principal": "",
                "telefone_secundario": "",
                "cpf_cnpj": "",
                "endereco": "",
            },
            "itens": [
                {
                    "ordem": 1,
                    "nome": "Camisa",
                    "descricao": "",
                    "quantidade": "1.00",
                    "preco_unitario": "50.00",
                    "custo_unitario_estimado": "0.00",
                }
            ],
            "pagamentos": [],
        }
        self.envelope = {
            "chave_idempotencia": str(uuid.uuid4()),
            "entidade_local_id": str(uuid.uuid4()),
            "estacao_id": "22222222-2222-2222-2222-222222222222",
            "operador_id": self.operador.pk,
            "codigo_origem": "AC",
            "codigo_visivel": "AC7",
            "sequencia_local": 7,
            "versao_esquema": 1,
            "versao_politica": "politica-1",
            "payload": self.payload,
            "checksum": calcular_checksum(self.payload),
        }
        self.estacao = EstacaoCliente.objects.create(
            id=uuid.UUID(self.envelope["estacao_id"]),
            nome="Estacao Central",
            segredo_hash="nao-usado-no-servico",
        )

    def test_incorporation_preserves_content_origin_and_audit(self):
        resultado = incorporar_pedido_offline(
            self.envelope, estacao_autenticada=self.estacao
        )

        pedido = resultado.pedido
        self.assertFalse(resultado.repetida)
        self.assertTrue(pedido.origem_offline)
        self.assertEqual(pedido.codigo_visivel_offline, "AC7")
        self.assertEqual(pedido.tema, "Pedido incorporado")
        self.assertEqual(pedido.itens.get().nome, "Camisa")
        self.assertTrue(IncorporacaoOffline.objects.filter(pedido_global=pedido).exists())
        evento = EventoOperacional.objects.get(tipo="PedidoOfflineIncorporado")
        self.assertEqual(evento.operador, self.operador)

    def test_retry_returns_durable_confirmation_without_duplicate_effects(self):
        primeira = incorporar_pedido_offline(
            self.envelope, estacao_autenticada=self.estacao
        )
        segunda = incorporar_pedido_offline(
            self.envelope, estacao_autenticada=self.estacao
        )

        self.assertTrue(segunda.repetida)
        self.assertEqual(primeira.pedido.pk, segunda.pedido.pk)
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(PedidoItem.objects.count(), 1)
        self.assertEqual(IncorporacaoOffline.objects.count(), 1)
        self.assertEqual(EventoOperacional.objects.count(), 1)

    def test_corrupted_payload_is_rejected_without_partial_data(self):
        envelope = copy.deepcopy(self.envelope)
        envelope["payload"]["pedido"]["tema"] = "Alterado depois do checksum"

        with self.assertRaises(SincronizacaoInvalida):
            incorporar_pedido_offline(envelope, estacao_autenticada=self.estacao)

        self.assertFalse(Pedido.objects.exists())
        self.assertFalse(Cliente.objects.exists())
        self.assertFalse(IncorporacaoOffline.objects.exists())

    def test_unknown_or_changed_authorship_is_rejected(self):
        self.envelope["codigo_origem"] = "OUTRO"

        with self.assertRaises(SincronizacaoInvalida):
            incorporar_pedido_offline(
                self.envelope, estacao_autenticada=self.estacao
            )

        self.assertFalse(Pedido.objects.exists())


@override_settings(MHEIBOS_RUNTIME_ROLE="central")
class IncorporacaoHttpTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Autora HTTP",
            senha="segura",
            papel=PapelOperador.USUARIO,
            codigo_origem_offline="AH",
        )
        credencial = criar_estacao(nome="Balcao HTTP")
        self.estacao = credencial.estacao
        self.segredo = credencial.segredo
        payload = {
            "pedido": {
                "tema": "HTTP",
                "data_pedido": "2026-08-01",
                "data_entrega": "2026-08-03",
                "hora_entrega": None,
                "observacoes": "",
                "valor_total": "10.00",
                "valor_pago_legado": "0.00",
                "desconto_ajuste": "0.00",
                "forma_pagamento_legada": "PIX",
                "prioridade": "NORMAL",
                "status": "AGUARDANDO_ARTE",
                "estado_comercial": "CONFIRMADO",
                "estado_entrega": "PENDENTE",
                "canal_atendimento": "PRESENCIAL",
                "usuario_cadastro": self.operador.nome,
            },
            "cliente": {
                "nome": "Cliente HTTP",
                "email": "",
                "telefone_principal": "",
                "telefone_secundario": "",
                "cpf_cnpj": "",
                "endereco": "",
            },
            "itens": [],
            "pagamentos": [],
        }
        self.envelope = {
            "chave_idempotencia": str(uuid.uuid4()),
            "entidade_local_id": str(uuid.uuid4()),
            "estacao_id": str(self.estacao.pk),
            "codigo_origem": "AH",
            "codigo_visivel": "AH1",
            "sequencia_local": 1,
            "versao_esquema": 1,
            "versao_politica": "politica-http",
            "payload": payload,
            "checksum": calcular_checksum(payload),
        }

    def enviar(self, *, segredo=None, envelope=None, estacao_id=None):
        return self.client.post(
            "/sincronizacao/incorporar/",
            data=json.dumps(envelope or self.envelope),
            content_type="application/json",
            headers={
                "Authorization": f"Bearer {segredo or self.segredo}",
                "X-Mheibos-Station-ID": estacao_id or str(self.estacao.pk),
            },
        )

    def test_station_secret_is_stored_only_as_hash(self):
        self.assertNotEqual(self.estacao.segredo_hash, self.segredo)
        self.assertTrue(self.estacao.verifica_segredo(self.segredo))

    def test_authenticated_station_receives_durable_idempotent_confirmation(self):
        primeira = self.enviar()
        segunda = self.enviar()

        self.assertEqual(primeira.status_code, 201)
        self.assertEqual(primeira.json()["codigo"], "INCORPORADO")
        self.assertEqual(segunda.status_code, 200)
        self.assertEqual(segunda.json()["codigo"], "JA_INCORPORADO")
        self.assertEqual(Pedido.objects.count(), 1)

    def test_invalid_secret_is_rejected_without_persistence(self):
        response = self.enviar(segredo="incorreto")

        self.assertEqual(response.status_code, 401)
        self.assertFalse(Pedido.objects.exists())

    def test_authenticated_station_cannot_submit_another_station_identity(self):
        envelope = copy.deepcopy(self.envelope)
        envelope["estacao_id"] = str(uuid.uuid4())

        response = self.enviar(envelope=envelope)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(Pedido.objects.exists())


class ProvisionamentoEstacaoTests(TestCase):
    def entrar(self, operador):
        session = self.client.session
        session["operador_id"] = operador.pk
        session.save()

    def test_common_user_cannot_access_station_provisioning(self):
        operador = OperadorGestor.objects.create(
            nome="Comum", senha="segura", papel=PapelOperador.USUARIO
        )
        self.entrar(operador)

        response = self.client.get("/sincronizacao/estacoes/")

        self.assertEqual(response.status_code, 403)

    def test_wrong_reauthentication_creates_nothing(self):
        operador = OperadorGestor.objects.create(
            nome="Admin Errado", senha="segura", papel=PapelOperador.ADMIN
        )
        self.entrar(operador)

        response = self.client.post(
            "/sincronizacao/estacoes/", {"nome": "Balcao", "senha_atual": "errada"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Senha atual incorreta")
        self.assertFalse(EstacaoCliente.objects.exists())

    def test_reauthenticated_admin_receives_secret_once_without_auditing_it(self):
        operador = OperadorGestor.objects.create(
            nome="Admin Correto", senha="segura", papel=PapelOperador.ADMIN
        )
        self.entrar(operador)

        response = self.client.post(
            "/sincronizacao/estacoes/", {"nome": "Balcao 1", "senha_atual": "segura"}
        )

        self.assertEqual(response.status_code, 200)
        segredo = response.context["segredo_novo"]
        estacao = EstacaoCliente.objects.get()
        self.assertTrue(segredo)
        self.assertNotEqual(estacao.segredo_hash, segredo)
        self.assertTrue(estacao.verifica_segredo(segredo))
        evento = EventoOperacional.objects.get(tipo="EstacaoProvisionada")
        self.assertNotIn(segredo, json.dumps(evento.valores_posteriores))
        self.assertNotIn(segredo, json.dumps(evento.metadados))


@override_settings(
    MHEIBOS_RUNTIME_ROLE="client_offline",
    MHEIBOS_STATION_ID="11111111-1111-1111-1111-111111111111",
    MHEIBOS_POLICY_VERSION="politica-teste",
)
class ModoOfflineRestritoTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operadora Local",
            senha="segura",
            papel=PapelOperador.USUARIO,
            codigo_origem_offline="OL",
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()

    def dados_pedido(self):
        return {
            "nome_cliente": "Cliente do Balcao",
            "tema": "Tema offline",
            "data_entrega": "2026-08-03",
            "valor_pago": "0.00",
            "forma_pagamento": "PIX",
            "desconto_ajuste": "0.00",
            "prioridade": "NORMAL",
            "canal_atendimento": "PRESENCIAL",
            "aguardar_arte": "on",
            "usuario_cadastro": self.operador.nome,
            "item_nome_1": "Caneca",
            "item_qtd_1": "1",
            "item_preco_1": "25.00",
        }

    def test_normal_order_form_persists_order_queue_and_offline_events_atomically(self):
        response = self.client.post("/pedidos/novo/", self.dados_pedido())

        self.assertEqual(response.status_code, 302)
        pedido = Pedido.objects.get()
        unidade = UnidadeSincronizacao.objects.get()
        self.assertTrue(pedido.origem_offline)
        self.assertEqual(pedido.codigo_visivel_offline, "OL1")
        self.assertEqual(unidade.pedido_local, pedido)
        self.assertEqual(unidade.versao_politica, "politica-teste")
        self.assertEqual(EventoOperacional.objects.filter(origem_offline=True).count(), 1)

    @override_settings(MHEIBOS_STATION_ID="invalida")
    def test_invalid_station_identity_rolls_back_entire_creation(self):
        response = self.client.post("/pedidos/novo/", self.dados_pedido())

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Pedido.objects.exists())
        self.assertFalse(UnidadeSincronizacao.objects.exists())
        self.assertFalse(EventoOperacional.objects.exists())

    def test_existing_global_order_cannot_be_changed_offline(self):
        pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Global"),
            usuario_cadastro=self.operador.nome,
        )

        response = self.client.post(
            f"/pedidos/{pedido.pk}/status/", {"status": "EM_PRODUCAO"}
        )

        self.assertEqual(response.status_code, 409)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, "AGUARDANDO_ARTE")

    def test_logout_is_blocked_while_local_queue_is_pending(self):
        pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Local"),
            usuario_cadastro=self.operador.nome,
        )
        enfileirar_pedido_local(
            pedido=pedido,
            operador=self.operador,
            estacao_id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
            versao_politica="politica-teste",
        )

        response = self.client.get("/sair/")

        self.assertRedirects(response, "/sincronizacao/", fetch_redirect_response=False)
        self.assertEqual(self.client.session["operador_id"], self.operador.pk)

from unittest.mock import patch
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, override_settings
from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from .models import (
    EstadoMissao,
    EstadoParticipacao,
    Missao,
    OrigemMissao,
    PapelParticipacao,
    ParticipacaoMissao,
    TipoManifestacaoConvite,
    TipoMissao,
)
from .services import (
    TransicaoMissaoInvalida,
    bloquear_missao,
    concluir_missao,
    convidar_participante,
    criar_missao_coletiva_espontanea,
    criar_missao_individual_voluntaria,
    iniciar_missao,
    manifestar_convite,
    pausar_missao,
    retomar_missao,
    responder_convite,
    sair_missao_espontanea,
)


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


class CicloVidaMissaoTests(TestCase):
    def setUp(self):
        self.dona = OperadorGestor.objects.create(nome="Responsável Ciclo", senha="segura", papel=PapelOperador.USUARIO)
        self.outra = OperadorGestor.objects.create(nome="Sem Autoridade", senha="segura", papel=PapelOperador.ADMIN)
        self.missao = criar_missao_individual_voluntaria(operador=self.dona, titulo="Executar ciclo", objetivo="Entregar resultado", criterio_conclusao="Resultado validado")

    def _entrar(self, operador):
        session = self.client.session
        session["operador_id"] = operador.pk
        session.save()

    def test_iniciar_pausar_retomar_e_concluir_preserva_tempos_e_eventos(self):
        self.missao = iniciar_missao(missao=self.missao, operador=self.dona)
        self.missao = pausar_missao(missao=self.missao, operador=self.dona, motivo="Aguardar material")
        self.missao.pausada_em = self.missao.pausada_em - __import__("datetime").timedelta(minutes=5)
        self.missao.save(update_fields=["pausada_em"])
        self.missao = retomar_missao(missao=self.missao, operador=self.dona, atualizacao="Material chegou")
        self.missao = concluir_missao(missao=self.missao, operador=self.dona, resultado_alcancado="Entrega validada")
        self.missao.refresh_from_db()
        self.assertEqual(self.missao.estado, EstadoMissao.CONCLUIDA)
        self.assertGreaterEqual(self.missao.tempo_total_pausa.total_seconds(), 300)
        self.assertEqual(self.missao.concluida_por, self.dona)
        self.assertEqual(self.missao.pendencias_remanescentes, "")
        self.assertEqual(set(EventoOperacional.objects.filter(alvo_id=str(self.missao.pk)).values_list("tipo", flat=True)), {"MissaoCriada", "MissaoIniciada", "MissaoPausada", "MissaoRetomada", "MissaoConcluida"})

    def test_bloqueio_exige_contexto_completo_e_retomada_limpa_estado_atual(self):
        iniciar_missao(missao=self.missao, operador=self.dona)
        with self.assertRaises(ValidationError):
            bloquear_missao(missao=self.missao, operador=self.dona, motivo="Falta aprovação", dependencia="", impacto="Atrasa", ajuda_necessaria="Decisão", urgencia="Alta")
        self.missao = bloquear_missao(missao=self.missao, operador=self.dona, motivo="Falta aprovação", dependencia="Cliente", impacto="Atrasa entrega", ajuda_necessaria="Contato comercial", urgencia="Alta")
        self.assertEqual(self.missao.estado, EstadoMissao.BLOQUEADA)
        self.missao = retomar_missao(missao=self.missao, operador=self.dona, atualizacao="Cliente aprovou")
        self.assertEqual(self.missao.estado, EstadoMissao.ATIVA)
        self.assertEqual(self.missao.motivo_bloqueio, "")
        evento = EventoOperacional.objects.get(tipo="MissaoBloqueada")
        self.assertEqual(evento.metadados["dependencia"], "Cliente")

    def test_transicao_invalida_e_admin_sem_autoridade_sao_recusados(self):
        with self.assertRaises(TransicaoMissaoInvalida):
            concluir_missao(missao=self.missao, operador=self.dona, resultado_alcancado="Ainda não iniciou")
        with self.assertRaises(PermissionDenied):
            iniciar_missao(missao=self.missao, operador=self.outra)
        self.assertEqual(self.missao.estado, EstadoMissao.PLANEJADA)

    def test_conclusao_nao_enterra_obrigacao_remanescente_em_texto(self):
        iniciar_missao(missao=self.missao, operador=self.dona)
        with self.assertRaises(ValidationError):
            concluir_missao(missao=self.missao, operador=self.dona, resultado_alcancado="Resultado parcial", pendencias_remanescentes="Ainda falta aprovação")
        self.missao.refresh_from_db()
        self.assertEqual(self.missao.estado, EstadoMissao.ATIVA)

    def test_repeticao_da_mesma_transicao_e_idempotente(self):
        iniciar_missao(missao=self.missao, operador=self.dona)
        iniciar_missao(missao=self.missao, operador=self.dona)
        self.assertEqual(EventoOperacional.objects.filter(tipo="MissaoIniciada", alvo_id=str(self.missao.pk)).count(), 1)

    @patch("apps.missoes.services.registrar_evento", side_effect=RuntimeError("falha"))
    def test_falha_de_evento_reverte_transicao(self, _evento):
        with self.assertRaises(RuntimeError):
            iniciar_missao(missao=self.missao, operador=self.dona)
        self.missao.refresh_from_db()
        self.assertEqual(self.missao.estado, EstadoMissao.PLANEJADA)
        self.assertIsNone(self.missao.iniciada_em)

    def test_interface_executa_transicao_e_offline_a_recusa(self):
        self._entrar(self.dona)
        response = self.client.post(f"/missoes/{self.missao.pk}/iniciar/")
        self.assertEqual(response.status_code, 302)
        self.missao.refresh_from_db()
        self.assertEqual(self.missao.estado, EstadoMissao.ATIVA)
        with self.settings(MHEIBOS_RUNTIME_ROLE="client_offline"):
            response = self.client.post(f"/missoes/{self.missao.pk}/pausar/", {"motivo": "Offline"})
        self.assertEqual(response.status_code, 409)
        self.missao.refresh_from_db()
        self.assertEqual(self.missao.estado, EstadoMissao.ATIVA)


class ParticipacaoEspontaneaTests(TestCase):
    def setUp(self):
        self.lider = OperadorGestor.objects.create(nome="Líder Coletiva", senha="segura", papel=PapelOperador.USUARIO)
        self.convidada = OperadorGestor.objects.create(nome="Pessoa Convidada", senha="segura", papel=PapelOperador.USUARIO)
        self.outra = OperadorGestor.objects.create(nome="Pessoa Alheia", senha="segura", papel=PapelOperador.USUARIO)

    def _criar(self):
        return criar_missao_coletiva_espontanea(
            operador=self.lider,
            titulo="Preparar ação coletiva",
            objetivo="Entregar ação em grupo",
            criterio_conclusao="Ação validada",
            convidados=[self.convidada],
        )

    def _entrar(self, operador):
        session = self.client.session
        session["operador_id"] = operador.pk
        session.save()

    def test_criacao_coletiva_preserva_lider_e_convite_sem_obrigacao(self):
        missao = self._criar()
        self.assertEqual(missao.tipo, TipoMissao.COLETIVA_ESPONTANEA)
        self.assertEqual(missao.estado, EstadoMissao.AGUARDANDO_ACEITE)
        lider = missao.participacoes.get(operador=self.lider)
        convite = missao.participacoes.get(operador=self.convidada)
        self.assertEqual((lider.papel, lider.estado_participacao), (PapelParticipacao.LIDER, EstadoParticipacao.ACEITO))
        self.assertEqual(convite.estado_participacao, EstadoParticipacao.CONVIDADO)
        self.assertTrue(EventoOperacional.objects.filter(tipo="ParticipanteConvidado", alvo_id=str(missao.pk)).exists())

    def test_aceite_ativa_participacao_e_torna_missao_planejada(self):
        missao = self._criar()
        convite = missao.participacoes.get(operador=self.convidada)
        resposta = responder_convite(participacao=convite, operador=self.convidada, aceitar=True)
        missao.refresh_from_db()
        self.assertEqual(resposta.estado_participacao, EstadoParticipacao.ACEITO)
        self.assertEqual(missao.estado, EstadoMissao.PLANEJADA)
        self.assertTrue(EventoOperacional.objects.filter(tipo="ConviteAceito", alvo_id=str(missao.pk)).exists())

    def test_recusa_encerra_convite_sem_apagar_historico_e_permite_novo_convite(self):
        missao = self._criar()
        convite = missao.participacoes.get(operador=self.convidada)
        recusado = responder_convite(participacao=convite, operador=self.convidada, aceitar=False)
        self.assertEqual(recusado.estado_participacao, EstadoParticipacao.RECUSADO)
        self.assertIsNotNone(recusado.encerrado_em)
        novo = convidar_participante(missao=missao, convidado=self.convidada, operador=self.lider)
        self.assertNotEqual(novo.pk, recusado.pk)
        self.assertEqual(missao.participacoes.filter(operador=self.convidada).count(), 2)

    def test_manifestacao_nao_aceita_convite_e_preserva_pedido(self):
        missao = self._criar()
        convite = missao.participacoes.get(operador=self.convidada)
        convite = manifestar_convite(participacao=convite, operador=self.convidada, tipo=TipoManifestacaoConvite.MAIS_INFORMACOES, texto="Qual é o prazo?")
        self.assertEqual(convite.estado_participacao, EstadoParticipacao.CONVIDADO)
        self.assertEqual(convite.manifestacao_texto, "Qual é o prazo?")
        self.assertTrue(EventoOperacional.objects.filter(tipo="ConviteManifestado").exists())

    def test_pessoa_alheia_nao_responde_convite_e_repeticao_e_idempotente(self):
        missao = self._criar()
        convite = missao.participacoes.get(operador=self.convidada)
        with self.assertRaises(PermissionDenied):
            responder_convite(participacao=convite, operador=self.outra, aceitar=True)
        responder_convite(participacao=convite, operador=self.convidada, aceitar=True)
        responder_convite(participacao=convite, operador=self.convidada, aceitar=True)
        self.assertEqual(EventoOperacional.objects.filter(tipo="ConviteAceito", alvo_id=str(missao.pk)).count(), 1)

    def test_saida_voluntaria_preserva_registro_e_lider_nao_sai_sem_transferir(self):
        missao = self._criar()
        convite = responder_convite(participacao=missao.participacoes.get(operador=self.convidada), operador=self.convidada, aceitar=True)
        saida = sair_missao_espontanea(participacao=convite, operador=self.convidada, confirmacao="SAIR", motivo="Mudança de disponibilidade")
        self.assertEqual(saida.estado_participacao, EstadoParticipacao.SAIU)
        self.assertTrue(saida.impacto_saida_confirmado)
        with self.assertRaises(ValidationError):
            sair_missao_espontanea(participacao=missao.participacoes.get(operador=self.lider), operador=self.lider, confirmacao="SAIR", motivo="Teste")

    @patch("apps.missoes.services.registrar_evento", side_effect=RuntimeError("falha"))
    def test_falha_de_auditoria_reverte_missao_e_convites(self, _evento):
        with self.assertRaises(RuntimeError):
            self._criar()
        self.assertFalse(Missao.objects.exists())
        self.assertFalse(ParticipacaoMissao.objects.exists())

    def test_visibilidade_acompanha_convite_aceite_e_saida(self):
        missao = self._criar()
        convite = missao.participacoes.get(operador=self.convidada)
        self._entrar(self.convidada)
        self.assertContains(self.client.get("/missoes/"), missao.titulo)
        responder_convite(participacao=convite, operador=self.convidada, aceitar=True)
        self.assertContains(self.client.get("/missoes/"), missao.titulo)
        sair_missao_espontanea(participacao=convite, operador=self.convidada, confirmacao="SAIR", motivo="Sem disponibilidade")
        self.assertNotContains(self.client.get("/missoes/"), missao.titulo)

    def test_interface_cria_responde_e_offline_bloqueia_convite(self):
        self._entrar(self.lider)
        response = self.client.post("/missoes/nova-coletiva/", {"titulo": "Coletiva Web", "objetivo": "Objetivo comum", "criterio_conclusao": "Entrega pronta", "resultado_esperado": "", "convidados": [self.convidada.pk]})
        self.assertEqual(response.status_code, 302)
        missao = Missao.objects.get(titulo="Coletiva Web")
        convite = missao.participacoes.get(operador=self.convidada)
        self._entrar(self.convidada)
        response = self.client.post(f"/missoes/participacoes/{convite.pk}/aceitar/")
        self.assertEqual(response.status_code, 302)
        convite.refresh_from_db()
        self.assertEqual(convite.estado_participacao, EstadoParticipacao.ACEITO)
        with self.settings(MHEIBOS_RUNTIME_ROLE="client_offline"):
            response = self.client.post(f"/missoes/{missao.pk}/convidar/", {"operador": self.outra.pk, "papel": PapelParticipacao.PARTICIPANTE})
        self.assertEqual(response.status_code, 409)

    def test_convite_pendente_impede_conclusao_e_missao_final_nao_muda_participacao(self):
        missao = criar_missao_coletiva_espontanea(
            operador=self.lider,
            titulo="Fechar coletivamente",
            objetivo="Entregar em grupo",
            criterio_conclusao="Entrega pronta",
            convidados=[self.convidada, self.outra],
        )
        aceita = responder_convite(
            participacao=missao.participacoes.get(operador=self.convidada),
            operador=self.convidada,
            aceitar=True,
        )
        missao = iniciar_missao(missao=missao, operador=self.lider)
        with self.assertRaises(ValidationError):
            concluir_missao(
                missao=missao,
                operador=self.lider,
                resultado_alcancado="Resultado",
            )
        responder_convite(
            participacao=missao.participacoes.get(operador=self.outra),
            operador=self.outra,
            aceitar=False,
        )
        missao = concluir_missao(
            missao=missao,
            operador=self.lider,
            resultado_alcancado="Resultado",
        )
        with self.assertRaises(ValidationError):
            sair_missao_espontanea(
                participacao=aceita,
                operador=self.convidada,
                confirmacao="SAIR",
                motivo="Tarde demais",
            )
        with self.assertRaises(ValidationError):
            convidar_participante(
                missao=missao,
                convidado=self.outra,
                operador=self.lider,
            )

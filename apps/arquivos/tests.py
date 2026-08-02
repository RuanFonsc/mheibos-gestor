from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.db import models
from django.test import TestCase

from apps.arquivos.models import ArquivoOficialArte
from apps.arquivos.services import (
    ArquivoOficialInvalido,
    TemaPedidoImutavel,
    reconhecer_alerta_arquivo,
    validar_alteracao_tema,
    verificar_arquivo_oficial,
    vincular_arquivo_oficial,
)
from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido


class ArquivoOficialArteTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Designer Arquivos", senha="segura", papel=PapelOperador.USUARIO
        )
        self.pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Arquivos"),
            tema="Tema inicial",
            usuario_cadastro=self.operador.nome,
        )

    def entrar(self, operador=None):
        session = self.client.session
        session["operador_id"] = (operador or self.operador).pk
        session.save()

    def test_multiplos_vinculos_guardam_metadados_sem_binario(self):
        primeiro = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"\\SERVIDOR\Artes\2026\arte-1.cdr",
            operador=self.operador,
        )
        segundo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"C:\Artes\arte-2.svg",
            operador=self.operador,
        )

        self.assertEqual(self.pedido.arquivos_oficiais_arte.count(), 2)
        self.assertEqual(primeiro.nome_oficial, "arte-1.cdr")
        self.assertEqual(segundo.extensao, "svg")
        campos = ArquivoOficialArte._meta.get_fields()
        self.assertFalse(any(isinstance(campo, (models.FileField, models.BinaryField)) for campo in campos))

    def test_mesmo_caminho_e_idempotente(self):
        primeiro = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"\\SERVIDOR\Artes\arte.cdr",
            operador=self.operador,
        )
        segundo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"\\servidor\artes\ARTE.cdr",
            operador=self.operador,
        )
        self.assertEqual(primeiro.pk, segundo.pk)
        self.assertEqual(EventoOperacional.objects.filter(tipo="ArquivoOficialArteVinculado").count(), 1)

    def test_identidade_fisica_nao_pode_ser_reescrita_ou_excluida(self):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"\\SERVIDOR\Artes\arte.cdr",
            operador=self.operador,
        )
        arquivo.caminho_oficial = r"\\SERVIDOR\Outro\renomeada.cdr"
        with self.assertRaisesMessage(ValueError, "imutavel"):
            arquivo.save()
        with self.assertRaisesMessage(ValueError, "nunca apagado"):
            arquivo.delete()

    @patch("apps.arquivos.services.registrar_evento", side_effect=RuntimeError)
    def test_falha_de_auditoria_reverte_vinculo(self, _evento):
        with self.assertRaises(RuntimeError):
            vincular_arquivo_oficial(
                pedido=self.pedido,
                caminho=r"\\SERVIDOR\Artes\arte.cdr",
                operador=self.operador,
            )
        self.assertFalse(ArquivoOficialArte.objects.exists())

    def test_caminho_relativo_e_recusado(self):
        with self.assertRaises(ArquivoOficialInvalido):
            vincular_arquivo_oficial(
                pedido=self.pedido,
                caminho="Artes/arte.cdr",
                operador=self.operador,
            )

    def test_tema_fica_imutavel_com_arquivo_ou_pagamento(self):
        vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"\\SERVIDOR\Artes\arte.cdr",
            operador=self.operador,
        )
        with self.assertRaises(TemaPedidoImutavel):
            validar_alteracao_tema(pedido=self.pedido, novo_tema="Outro tema")

        outro = Pedido.objects.create(
            cliente=self.pedido.cliente,
            tema="Tema pago",
            valor_total=Decimal("20.00"),
            valor_pago_legado=Decimal("5.00"),
        )
        with self.assertRaises(TemaPedidoImutavel):
            validar_alteracao_tema(pedido=outro, novo_tema="Outro tema")

    def test_rota_exige_autoria_do_pedido_e_exibe_vinculo(self):
        outro = OperadorGestor.objects.create(
            nome="Outro Designer", senha="segura", papel=PapelOperador.USUARIO
        )
        self.entrar(outro)
        response = self.client.post(
            f"/pedidos/{self.pedido.pk}/arquivos-oficiais/vincular/",
            {"caminho_oficial": r"\\SERVIDOR\Artes\negado.cdr"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ArquivoOficialArte.objects.exists())

        self.entrar()
        self.client.post(
            f"/pedidos/{self.pedido.pk}/arquivos-oficiais/vincular/",
            {"caminho_oficial": r"\\SERVIDOR\Artes\oficial.cdr"},
        )
        response = self.client.get(f"/pedidos/{self.pedido.pk}/")
        self.assertContains(response, "oficial.cdr")
        self.assertContains(response, "nenhum binario no banco")

    @patch("apps.arquivos.services.os.stat", return_value=SimpleNamespace(st_size=321))
    def test_verificacao_integra_registra_tamanho_e_auditoria(self, _stat):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido, caminho=r"C:\Artes\oficial.cdr", operador=self.operador
        )
        verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
        arquivo.refresh_from_db()
        self.assertEqual(arquivo.estado_integridade, "INTEGRO")
        self.assertEqual(arquivo.tamanho_bytes, 321)
        self.assertEqual(arquivo.discrepancias, [])
        self.assertTrue(EventoOperacional.objects.filter(tipo="ArquivoOficialArteVerificado").exists())

    @patch("apps.arquivos.services.os.stat", side_effect=FileNotFoundError)
    def test_arquivo_ausente_exige_eu_entendi_auditado(self, _stat):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido, caminho=r"C:\Artes\ausente.cdr", operador=self.operador
        )
        verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
        self.assertEqual(arquivo.estado_integridade, "ALERTA")
        self.assertEqual(arquivo.discrepancias[0]["codigo"], "ARQUIVO_NAO_ENCONTRADO")

        reconhecer_alerta_arquivo(arquivo=arquivo, operador=self.operador)
        arquivo.refresh_from_db()
        self.assertEqual(arquivo.alerta_reconhecido_por, self.operador)
        evento = EventoOperacional.objects.get(tipo="AlertaArquivoOficialReconhecido")
        self.assertEqual(evento.acao, "eu_entendi_alerta_arquivo")

    @patch("apps.arquivos.services.os.stat", side_effect=FileNotFoundError)
    def test_rotas_verificam_e_reconhecem_alerta(self, _stat):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido, caminho=r"C:\Artes\ausente.cdr", operador=self.operador
        )
        self.entrar()
        self.client.post(f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/verificar/")
        response = self.client.get(f"/pedidos/{self.pedido.pk}/")
        self.assertContains(response, "O arquivo nao foi encontrado")
        self.assertContains(response, "Eu entendi")
        self.client.post(f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/reconhecer-alerta/")
        arquivo.refresh_from_db()
        self.assertIsNotNone(arquivo.alerta_reconhecido_em)

from decimal import Decimal
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

from django.db import models
from django.test import TestCase
from PIL import Image, UnidentifiedImageError

from apps.arquivos.models import ArquivoOficialArte
from apps.arquivos.services import (
    ArquivoOficialInvalido,
    EncerramentoArquivoInvalido,
    TemaPedidoImutavel,
    criar_arquivo_oficial,
    encerrar_vinculo_arquivo_oficial,
    reconhecer_alerta_arquivo,
    validar_alteracao_tema,
    verificar_arquivo_oficial,
    vincular_arquivo_oficial,
)
from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador, PerfilEmpresa
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

    def test_cria_arquivo_vazio_na_estrutura_oficial(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )

            caminho = Path(arquivo.caminho_oficial)
            self.assertTrue(caminho.exists())
            self.assertEqual(caminho.stat().st_size, 0)
            self.assertEqual(caminho.suffix, ".cdr")
            self.assertIn(self.operador.nome, caminho.parts)
            self.assertIn("Cliente Arquivos", caminho.name)
            self.assertEqual(arquivo.origem, "CRIADO_MHEIBOS")
            self.assertEqual(
                EventoOperacional.objects.filter(tipo="ArquivoOficialArteCriado").count(), 1
            )

    def test_criacoes_repetidas_recebem_numeracao(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            primeiro = criar_arquivo_oficial(
                pedido=self.pedido, programa="pdf", operador=self.operador
            )
            segundo = criar_arquivo_oficial(
                pedido=self.pedido, programa="pdf", operador=self.operador
            )

            self.assertTrue(primeiro.nome_oficial.endswith(".pdf"))
            self.assertTrue(segundo.nome_oficial.endswith(" - 02.pdf"))

    def test_criacao_exige_raiz_compartilhada_configurada(self):
        PerfilEmpresa.objects.update_or_create(
            chave="global", defaults={"diretorio_artes_raiz": ""}
        )
        with self.assertRaisesMessage(ArquivoOficialInvalido, "pasta compartilhada"):
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )

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

    def test_verificacao_extrai_dimensoes_proporcao_formato_e_dpi(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "arte-raster.png"
            Image.new("RGB", (1600, 900), color="white").save(caminho, dpi=(300, 300))
            arquivo = vincular_arquivo_oficial(
                pedido=self.pedido,
                caminho=str(caminho),
                operador=self.operador,
            )
            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
            arquivo.refresh_from_db()
            self.assertEqual(arquivo.estado_integridade, "INTEGRO")
            self.assertEqual((arquivo.largura_px, arquivo.altura_px), (1600, 900))
            self.assertEqual(arquivo.resolucao_dpi, Decimal("300.00"))
            self.assertEqual(
                arquivo.propriedades_tecnicas["leitura_raster"]["proporcao"],
                "16:9",
            )
            self.assertEqual(
                arquivo.propriedades_tecnicas["leitura_raster"]["formato"],
                "PNG",
            )
            self.entrar()
            response = self.client.get(f"/pedidos/{self.pedido.pk}/")
            self.assertContains(response, "1600 × 900 px")
            self.assertContains(response, "16:9")

    @patch("apps.arquivos.services.os.stat", return_value=SimpleNamespace(st_size=12))
    @patch("apps.arquivos.metadados.Image.open", side_effect=UnidentifiedImageError)
    def test_raster_invalido_gera_discrepancia_sem_quebrar_verificacao(self, _open, _stat):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"C:\Artes\conteudo-invalido.png",
            operador=self.operador,
        )
        verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
        arquivo.refresh_from_db()
        self.assertEqual(arquivo.estado_integridade, "ALERTA")
        self.assertEqual(
            arquivo.discrepancias[0]["codigo"],
            "PROPRIEDADES_TECNICAS_INDISPONIVEIS",
        )

    @patch("apps.arquivos.services.os.stat", return_value=SimpleNamespace(st_size=321))
    def test_formato_nao_suportado_preserva_metadados_existentes(self, _stat):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"C:\Artes\oficial.cdr",
            operador=self.operador,
        )
        arquivo.largura_px = 900
        arquivo.altura_px = 600
        arquivo.propriedades_tecnicas = {"origem": "leitura_especializada"}
        arquivo.save()
        verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
        arquivo.refresh_from_db()
        self.assertEqual((arquivo.largura_px, arquivo.altura_px), (900, 600))
        self.assertEqual(arquivo.propriedades_tecnicas["origem"], "leitura_especializada")
        self.assertFalse(arquivo.propriedades_tecnicas["leitura_raster"]["suportado"])

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

    def test_encerramento_preserva_fisico_identidade_metadados_e_auditoria(self):
        administrador = OperadorGestor.objects.create(
            nome="Admin Revisao", senha="segura", papel=PapelOperador.ADMIN
        )
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "arte-preservada.cdr"
            caminho.write_bytes(b"conteudo-fisico-preservado")
            arquivo = vincular_arquivo_oficial(
                pedido=self.pedido,
                caminho=str(caminho),
                operador=self.operador,
            )
            arquivo.propriedades_tecnicas = {"perfil": "CMYK"}
            arquivo.largura_px = 1200
            arquivo.altura_px = 800
            arquivo.save()
            encerrar_vinculo_arquivo_oficial(
                arquivo=arquivo,
                operador=administrador,
                observacao="Revisao anual concluida",
                backup_previo_confirmado=True,
            )
            arquivo.refresh_from_db()
            self.assertEqual(arquivo.estado_vinculo, "ENCERRADO")
            self.assertEqual(arquivo.encerrado_por, administrador)
            self.assertEqual(arquivo.nome_oficial, "arte-preservada.cdr")
            self.assertEqual(arquivo.propriedades_tecnicas, {"perfil": "CMYK"})
            self.assertEqual((arquivo.largura_px, arquivo.altura_px), (1200, 800))
            self.assertEqual(caminho.read_bytes(), b"conteudo-fisico-preservado")
            evento = EventoOperacional.objects.get(tipo="VinculoArquivoOficialEncerrado")
            self.assertFalse(evento.valores_posteriores["arquivo_fisico_alterado"])
            self.assertTrue(evento.valores_posteriores["metadados_preservados"])
            encerrar_vinculo_arquivo_oficial(
                arquivo=arquivo,
                operador=administrador,
            )
            self.assertEqual(
                EventoOperacional.objects.filter(tipo="VinculoArquivoOficialEncerrado").count(),
                1,
            )

    def test_encerramento_exige_administrador_no_servico(self):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"C:\Artes\restrito.cdr",
            operador=self.operador,
        )
        with self.assertRaises(EncerramentoArquivoInvalido):
            encerrar_vinculo_arquivo_oficial(
                arquivo=arquivo,
                operador=self.operador,
            )

    def test_falha_de_auditoria_reverte_encerramento(self):
        administrador = OperadorGestor.objects.create(
            nome="Admin Rollback Revisao", senha="segura", papel=PapelOperador.ADMIN
        )
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"C:\Artes\rollback.cdr",
            operador=self.operador,
        )
        with patch("apps.arquivos.services.registrar_evento", side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                encerrar_vinculo_arquivo_oficial(
                    arquivo=arquivo,
                    operador=administrador,
                )
        arquivo.refresh_from_db()
        self.assertEqual(arquivo.estado_vinculo, "ATIVO")
        self.assertIsNone(arquivo.encerrado_em)

    def test_rota_exige_confirmacao_e_exibe_historico_encerrado(self):
        administrador = OperadorGestor.objects.create(
            nome="Admin Interface Revisao", senha="segura", papel=PapelOperador.ADMIN
        )
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"C:\Artes\interface-revisao.cdr",
            operador=self.operador,
        )
        self.entrar(administrador)
        url = f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/encerrar/"
        self.client.post(url, {"confirmacao": "nao"})
        arquivo.refresh_from_db()
        self.assertEqual(arquivo.estado_vinculo, "ATIVO")
        self.client.post(
            url,
            {
                "confirmacao": "ENCERRAR",
                "observacao": "Ano revisado",
                "backup_previo_confirmado": "1",
            },
        )
        response = self.client.get(f"/pedidos/{self.pedido.pk}/")
        self.assertContains(response, "Encerrado por Admin Interface Revisao")
        self.assertContains(response, "Backup prévio declarado")
        self.assertNotContains(response, "Verificar agora")

    def test_cancelar_pedido_nao_altera_vinculo_oficial(self):
        administrador = OperadorGestor.objects.create(
            nome="Admin Cancelamento Arquivo", senha="segura", papel=PapelOperador.ADMIN
        )
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido,
            caminho=r"C:\Artes\cancelamento-preserva.cdr",
            operador=self.operador,
        )
        identidade = (arquivo.caminho_oficial, arquivo.nome_oficial)
        self.entrar(administrador)
        self.client.post(
            f"/pedidos/{self.pedido.pk}/status/",
            {"status": "CANCELADO"},
        )
        arquivo.refresh_from_db()
        self.assertEqual(arquivo.estado_vinculo, "ATIVO")
        self.assertEqual((arquivo.caminho_oficial, arquivo.nome_oficial), identidade)

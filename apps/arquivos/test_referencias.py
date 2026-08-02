import hashlib
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.deletion import ProtectedError
from django.test import TestCase, override_settings

from apps.arquivos.referencias import (
    ArteReferenciaNaoAutorizada,
    adicionar_arte_referencia,
    desvincular_arte_referencia,
)
from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import ArtePedido, Pedido


class ArteReferenciaTests(TestCase):
    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.operador = OperadorGestor.objects.create(
            nome="Designer Referencia", senha="segura", papel=PapelOperador.USUARIO
        )
        self.pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Referencia"),
            usuario_cadastro=self.operador.nome,
        )

    def upload(self, nome="referencia.png", conteudo=b"imagem-referencia"):
        return SimpleUploadedFile(nome, conteudo, content_type="image/png")

    def test_inclusao_registra_hash_autoria_e_evento(self):
        conteudo = b"imagem-da-ordem"
        arte = adicionar_arte_referencia(
            pedido=self.pedido,
            upload=self.upload(conteudo=conteudo),
            operador=self.operador,
            ordem=0,
        )
        self.assertEqual(arte.conteudo_sha256, hashlib.sha256(conteudo).hexdigest())
        self.assertEqual(arte.criado_por, self.operador)
        self.assertTrue(arte.arquivo.storage.exists(arte.arquivo.name))
        evento = EventoOperacional.objects.get(tipo="ArteReferenciaVinculada")
        self.assertEqual(evento.valores_posteriores["finalidade"], "REFERENCIA_VISUAL")

    def test_desvinculo_preserva_fisico_historico_e_protege_pedido(self):
        arte = adicionar_arte_referencia(
            pedido=self.pedido,
            upload=self.upload(),
            operador=self.operador,
            ordem=0,
        )
        nome_armazenado = arte.arquivo.name
        administrador = OperadorGestor.objects.create(
            nome="Admin Historico Referencia", senha="segura", papel=PapelOperador.ADMIN
        )
        desvincular_arte_referencia(
            arte_id=arte.pk, pedido=self.pedido, operador=administrador
        )
        self.assertFalse(self.pedido.artes_ativas.filter(pk=arte.pk).exists())
        historico = ArtePedido.todos_vinculos.get(pk=arte.pk)
        self.assertEqual(historico.desvinculado_por, administrador)
        self.assertTrue(historico.arquivo.storage.exists(nome_armazenado))
        self.assertTrue(EventoOperacional.objects.filter(tipo="ArteReferenciaDesvinculada").exists())
        with self.assertRaises(ProtectedError):
            self.pedido.delete()

    @patch("apps.arquivos.referencias.registrar_evento", side_effect=RuntimeError)
    def test_falha_de_auditoria_reverte_e_remove_copia_orfa(self, _evento):
        with self.assertRaises(RuntimeError):
            adicionar_arte_referencia(
                pedido=self.pedido,
                upload=self.upload(),
                operador=self.operador,
                ordem=0,
            )
        self.assertFalse(ArtePedido.todos_vinculos.exists())
        self.assertEqual([item for item in Path(self.media.name).rglob("*") if item.is_file()], [])

    def test_rota_de_remocao_mantem_arquivo_e_oculta_referencia(self):
        arte = adicionar_arte_referencia(
            pedido=self.pedido,
            upload=self.upload(),
            operador=self.operador,
            ordem=0,
        )
        administrador = OperadorGestor.objects.create(
            nome="Administrador Referencia", senha="segura", papel=PapelOperador.ADMIN
        )
        session = self.client.session
        session["operador_id"] = administrador.pk
        session.save()
        response = self.client.post(
            f"/pedidos/{self.pedido.pk}/editar/",
            {"acao": "remover_arte", "arte_id": arte.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/pedidos/{self.pedido.pk}/editar/")
        self.assertFalse(self.pedido.artes_ativas.exists())
        arte = ArtePedido.todos_vinculos.get(pk=arte.pk)
        self.assertTrue(arte.arquivo.storage.exists(arte.arquivo.name))

    def test_servico_aplica_autorizacao_sem_depender_da_interface(self):
        outro = OperadorGestor.objects.create(
            nome="Outro Designer Referencia", senha="segura", papel=PapelOperador.USUARIO
        )
        with self.assertRaises(ArteReferenciaNaoAutorizada):
            adicionar_arte_referencia(
                pedido=self.pedido,
                upload=self.upload(),
                operador=outro,
                ordem=0,
            )
        arte = adicionar_arte_referencia(
            pedido=self.pedido,
            upload=self.upload(),
            operador=self.operador,
            ordem=0,
        )
        with self.assertRaises(ArteReferenciaNaoAutorizada):
            desvincular_arte_referencia(
                arte_id=arte.pk, pedido=self.pedido, operador=self.operador
            )

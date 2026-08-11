import tempfile
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
from django.db.models.deletion import ProtectedError
from django.test import TestCase, override_settings

from apps.arquivos.anexos import (
    AnexoDuplicado,
    AnexoNaoAutorizado,
    adicionar_anexo,
    desvincular_anexo,
)
from apps.arquivos.models import AnexoPedido
from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido


class AnexoPedidoTests(TestCase):
    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        campo_arquivo = AnexoPedido._meta.get_field("arquivo")
        armazenamento_original = campo_arquivo.storage
        self.armazenamento_privado = armazenamento_original
        campo_arquivo.storage = FileSystemStorage(location=self.media.name)
        self.addCleanup(setattr, campo_arquivo, "storage", armazenamento_original)
        self.operador = OperadorGestor.objects.create(
            nome="Responsavel Anexos", senha="segura", papel=PapelOperador.USUARIO
        )
        self.admin = OperadorGestor.objects.create(
            nome="Admin Anexos", senha="segura", papel=PapelOperador.ADMIN
        )
        self.pedido = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Anexos"),
            usuario_cadastro=self.operador.nome,
        )

    def upload(self, nome="documento.dat", conteudo=b"conteudo-opaco"):
        return SimpleUploadedFile(nome, conteudo, content_type="application/octet-stream")

    def entrar(self, operador):
        session = self.client.session
        session["operador_id"] = operador.pk
        session.save()

    def test_anexo_guarda_metadados_sem_interpretar_conteudo(self):
        anexo = adicionar_anexo(
            pedido=self.pedido,
            upload=self.upload(nome="arquivo-protegido.xyz"),
            operador=self.operador,
            manter_duplicado=False,
        )
        self.assertEqual(anexo.nome_original, "arquivo-protegido.xyz")
        self.assertEqual(len(anexo.conteudo_sha256), 64)
        self.assertTrue(anexo.arquivo.storage.exists(anexo.arquivo.name))
        with self.assertRaises(ValueError):
            self.armazenamento_privado.url("qualquer-arquivo")
        evento = EventoOperacional.objects.get(tipo="AnexoPedidoVinculado")
        self.assertFalse(evento.valores_posteriores["conteudo_interpretado"])

    def test_duplicidade_exige_decisao_humana_explicita(self):
        adicionar_anexo(
            pedido=self.pedido,
            upload=self.upload(nome="primeiro.dat"),
            operador=self.operador,
            manter_duplicado=False,
        )
        with self.assertRaises(AnexoDuplicado):
            adicionar_anexo(
                pedido=self.pedido,
                upload=self.upload(nome="segundo.dat"),
                operador=self.operador,
                manter_duplicado=False,
            )
        segundo = adicionar_anexo(
            pedido=self.pedido,
            upload=self.upload(nome="segundo.dat"),
            operador=self.operador,
            manter_duplicado=True,
        )
        self.assertEqual(AnexoPedido.objects.count(), 2)
        evento = EventoOperacional.objects.get(alvo_id=str(segundo.pk))
        self.assertTrue(evento.valores_posteriores["duplicado_mantido_por_decisao_humana"])

    def test_desvinculo_preserva_fisico_historico_e_pedido(self):
        anexo = adicionar_anexo(
            pedido=self.pedido,
            upload=self.upload(),
            operador=self.operador,
            manter_duplicado=False,
        )
        desvincular_anexo(anexo_id=anexo.pk, pedido=self.pedido, operador=self.admin)
        anexo.refresh_from_db()
        self.assertIsNotNone(anexo.desvinculado_em)
        self.assertTrue(anexo.arquivo.storage.exists(anexo.arquivo.name))
        self.assertTrue(EventoOperacional.objects.filter(tipo="AnexoPedidoDesvinculado").exists())
        with self.assertRaises(ProtectedError):
            self.pedido.delete()

    def test_autorizacao_esta_no_servico(self):
        outro = OperadorGestor.objects.create(
            nome="Outro Anexos", senha="segura", papel=PapelOperador.USUARIO
        )
        with self.assertRaises(AnexoNaoAutorizado):
            adicionar_anexo(
                pedido=self.pedido,
                upload=self.upload(),
                operador=outro,
                manter_duplicado=False,
            )
        anexo = adicionar_anexo(
            pedido=self.pedido,
            upload=self.upload(),
            operador=self.operador,
            manter_duplicado=False,
        )
        with self.assertRaises(AnexoNaoAutorizado):
            desvincular_anexo(anexo_id=anexo.pk, pedido=self.pedido, operador=self.operador)

    @patch("apps.arquivos.anexos.registrar_evento", side_effect=RuntimeError)
    def test_falha_de_auditoria_nao_deixa_registro_ou_copia_orfa(self, _evento):
        with self.assertRaises(RuntimeError):
            adicionar_anexo(
                pedido=self.pedido,
                upload=self.upload(),
                operador=self.operador,
                manter_duplicado=False,
            )
        self.assertFalse(AnexoPedido.objects.exists())
        self.assertEqual([item for item in Path(self.media.name).rglob("*") if item.is_file()], [])

    def test_interface_adiciona_detecta_duplicado_e_desvincula(self):
        self.entrar(self.operador)
        url = f"/pedidos/{self.pedido.pk}/anexos/adicionar/"
        self.client.post(url, {"anexos": self.upload(nome="interface.dat")})
        response = self.client.get(f"/pedidos/{self.pedido.pk}/")
        self.assertContains(response, "interface.dat")
        anexo_inicial = AnexoPedido.objects.get()
        download = self.client.get(
            f"/pedidos/{self.pedido.pk}/anexos/{anexo_inicial.pk}/baixar/"
        )
        self.assertTrue(download["Content-Disposition"].startswith("attachment;"))
        self.assertEqual(b"".join(cast(Any, download).streaming_content), b"conteudo-opaco")
        download.close()
        sem_acesso = OperadorGestor.objects.create(
            nome="Sem Acesso Anexo", senha="segura", papel=PapelOperador.USUARIO
        )
        self.entrar(sem_acesso)
        negado = self.client.get(
            f"/pedidos/{self.pedido.pk}/anexos/{anexo_inicial.pk}/baixar/"
        )
        self.assertEqual(negado.status_code, 404)
        self.entrar(self.operador)
        self.client.post(url, {"anexos": self.upload(nome="copia.dat")})
        self.assertEqual(AnexoPedido.objects.count(), 1)
        self.client.post(
            url,
            {"anexos": self.upload(nome="copia.dat"), "manter_duplicados": "1"},
        )
        self.assertEqual(AnexoPedido.objects.count(), 2)
        anexo = AnexoPedido.objects.first()
        self.assertIsNotNone(anexo)
        anexo = cast(Any, anexo)
        self.entrar(self.admin)
        self.client.post(f"/pedidos/{self.pedido.pk}/anexos/{anexo.pk}/desvincular/")
        anexo.refresh_from_db()
        self.assertIsNotNone(anexo.desvinculado_em)

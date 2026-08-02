import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.arquivos.models import (
    ArquivoOficialArte,
    EstadoVinculoArquivo,
    OrigemArquivoOficial,
)
from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.clientes.models import Cliente
from apps.pedidos.models import ArtePedido, Pedido, PedidoItem


class PesquisaArtesTests(TestCase):
    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.operador = OperadorGestor.objects.create(
            nome="Pesquisador Artes", senha="segura", papel=PapelOperador.ADMIN
        )
        session = self.client.session
        session["operador_id"] = self.operador.pk
        session.save()
        cliente = Cliente.objects.create(
            nome="Cliente Pesquisa Aurora",
            telefone_principal="11987654321",
        )
        self.pedido = Pedido.objects.create(
            cliente=cliente,
            legado_id=4501,
            tema="Tema Aurora",
            descricao_legada="acabamento fosco especial",
            usuario_cadastro=self.operador.nome,
        )
        PedidoItem.objects.create(
            pedido=self.pedido,
            nome="Produto Solar",
            descricao="impressao dourada",
            quantidade=1,
            preco_unitario=10,
        )
        ArquivoOficialArte.objects.create(
            pedido=self.pedido,
            caminho_oficial=r"\\SERVIDOR\Artes\#4501 - Caneca Solar.cdr",
            nome_oficial="#4501 - Caneca Solar.cdr",
            extensao="cdr",
            origem=OrigemArquivoOficial.VINCULADO_MANUAL,
            largura_px=3840,
            altura_px=2160,
            resolucao_dpi=300,
            propriedades_tecnicas={
                "perfil_cor": "CMYK Especial",
                "material": "ceramica",
            },
            criado_por=self.operador,
        )
        ArtePedido.objects.create(
            pedido=self.pedido,
            arquivo=SimpleUploadedFile(
                "mockup-frente.png", b"referencia", content_type="image/png"
            ),
            nome_original="mockup-frente.png",
            tamanho_bytes=10,
            criado_por=self.operador,
        )

    def test_todos_os_criterios_normativos_localizam_a_arte(self):
        criterios = (
            "4501",
            "Cliente Pesquisa",
            "11987654321",
            "Produto Solar",
            "Tema Aurora",
            "acabamento fosco",
            "Caneca Solar.cdr",
            "CMYK Especial",
            "3840",
            "mockup-frente.png",
        )
        for criterio in criterios:
            with self.subTest(criterio=criterio):
                response = self.client.get("/pedidos/", {"q": criterio})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Cliente Pesquisa Aurora")
                self.assertContains(response, "#4501 - Caneca Solar.cdr")

    def test_vinculos_encerrados_nao_aparecem_na_pesquisa_operacional(self):
        outro = Pedido.objects.create(
            cliente=Cliente.objects.create(nome="Cliente Arquivo Encerrado"),
            tema="Tema sem correspondencia",
        )
        ArquivoOficialArte.objects.create(
            pedido=outro,
            caminho_oficial=r"\\SERVIDOR\Arquivo\somente-encerrado.ai",
            nome_oficial="somente-encerrado.ai",
            extensao="ai",
            origem=OrigemArquivoOficial.LEGADO,
            estado_vinculo=EstadoVinculoArquivo.ENCERRADO,
        )
        response = self.client.get("/pedidos/", {"q": "somente-encerrado.ai"})
        self.assertNotContains(response, "Cliente Arquivo Encerrado")
        self.assertContains(response, "Nenhum pedido encontrado")

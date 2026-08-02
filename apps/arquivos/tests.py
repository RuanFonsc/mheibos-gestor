from decimal import Decimal
from datetime import timedelta
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

from django.db import models
from django.test import TestCase, override_settings
from django.utils import timezone
from PIL import Image, UnidentifiedImageError

from apps.arquivos.models import ArquivoOficialArte, EstadoPreparacaoArte, PreparacaoArtePedido
from apps.arquivos.services import (
    AcaoInatividadeArteInvalida,
    ArquivoOficialInvalido,
    AlertaArquivoInvalido,
    EncerramentoArquivoInvalido,
    PreparacaoArteInvalida,
    RestauracaoArquivoInvalida,
    TransferenciaResponsabilidadeArteInvalida,
    TemaPedidoImutavel,
    concluir_arte_pedido,
    criar_arquivo_oficial,
    avaliar_alerta_inatividade_arte,
    decidir_alteracao_pos_conclusao,
    decidir_copia_local_transferida,
    encerrar_vinculo_arquivo_oficial,
    reconhecer_alerta_arquivo,
    responder_alerta_inatividade_arte,
    transferir_responsabilidade_arte,
    transferir_arquivo_provisorio,
    validar_alteracao_tema,
    verificar_arquivo_oficial,
    vincular_arquivo_oficial,
    vincular_arquivo_restaurado,
)
from apps.auditoria.models import EventoOperacional
from apps.catalogo.models import (
    CategoriaServico,
    OperadorGestor,
    PapelOperador,
    PerfilEmpresa,
)
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido, PedidoItem


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

    def preparar_alerta_critico(self):
        categoria = CategoriaServico.objects.create(
            nome="Critica transferencia", alerta_dias_uteis=2
        )
        self.pedido.data_entrega = timezone.localdate() + timedelta(days=1)
        self.pedido.save(update_fields=["data_entrega"])
        PedidoItem.objects.create(
            pedido=self.pedido,
            nome="Item critico transferencia",
            categoria_servico=categoria,
        )
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
        agora = timezone.now()
        preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
        preparacao.proximo_alerta_em = agora - timedelta(seconds=1)
        preparacao.save(update_fields=["proximo_alerta_em"])
        return agora, preparacao

    def test_transferencia_gerencial_preserva_criador_pasta_e_troca_responsavel(self):
        agora, preparacao = self.preparar_alerta_critico()
        arquivo = ArquivoOficialArte.objects.get(pedido=self.pedido)
        caminho_original = arquivo.caminho_oficial
        criador_original = arquivo.criado_por
        novo = OperadorGestor.objects.create(
            nome="Designer substituto", senha="segura", papel=PapelOperador.USUARIO
        )
        gerente = OperadorGestor.objects.create(
            nome="Gerente da arte", senha="senha-gerente", papel=PapelOperador.ADMIN
        )

        preparacao = transferir_responsabilidade_arte(
            pedido=self.pedido,
            solicitante=self.operador,
            novo_responsavel=novo,
            gerente=gerente,
            senha="senha-gerente",
            agora=agora,
        )

        arquivo.refresh_from_db()
        self.assertEqual(preparacao.responsavel, novo)
        self.assertEqual(preparacao.proximo_alerta_em, agora + timedelta(hours=2))
        self.assertEqual(arquivo.caminho_oficial, caminho_original)
        self.assertEqual(arquivo.criado_por, criador_original)
        evento = EventoOperacional.objects.get(tipo="ResponsabilidadeArteTransferida")
        self.assertEqual(evento.operador, gerente)
        self.assertTrue(evento.valores_posteriores["pasta_do_criador_preservada"])

        alerta_futuro = avaliar_alerta_inatividade_arte(
            pedido=self.pedido, agora=agora + timedelta(hours=2, seconds=1)
        )
        self.assertTrue(alerta_futuro.ativo)
        responder_alerta_inatividade_arte(
            pedido=self.pedido,
            operador=novo,
            acao="AINDA_TRABALHANDO",
            agora=agora + timedelta(hours=2, seconds=1),
        )

    def test_transferencia_recusa_senha_invalida_e_reverte_falha_de_auditoria(self):
        agora, preparacao = self.preparar_alerta_critico()
        novo = OperadorGestor.objects.create(
            nome="Designer destino", senha="segura", papel=PapelOperador.USUARIO
        )
        gerente = OperadorGestor.objects.create(
            nome="Gerente seguranca", senha="senha-gerente", papel=PapelOperador.ADMIN
        )
        with self.assertRaises(TransferenciaResponsabilidadeArteInvalida):
            transferir_responsabilidade_arte(
                pedido=self.pedido,
                solicitante=self.operador,
                novo_responsavel=novo,
                gerente=gerente,
                senha="errada",
                agora=agora,
            )
        with patch("apps.arquivos.services.registrar_evento", side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                transferir_responsabilidade_arte(
                    pedido=self.pedido,
                    solicitante=self.operador,
                    novo_responsavel=novo,
                    gerente=gerente,
                    senha="senha-gerente",
                    agora=agora,
                )
        preparacao.refresh_from_db()
        self.assertEqual(preparacao.responsavel, self.operador)

    def test_interface_transfere_responsabilidade_com_senha_gerencial(self):
        self.preparar_alerta_critico()
        novo = OperadorGestor.objects.create(
            nome="Designer pela interface", senha="segura", papel=PapelOperador.USUARIO
        )
        gerente = OperadorGestor.objects.create(
            nome="Gerente pela interface", senha="senha-gerente", papel=PapelOperador.ADMIN
        )
        self.entrar()
        resposta = self.client.get(f"/pedidos/{self.pedido.pk}/")
        self.assertContains(
            resposta, "Transferir responsabilidade com autorização gerencial"
        )
        resposta = self.client.post(
            f"/pedidos/{self.pedido.pk}/arte/transferir-responsabilidade/",
            {
                "novo_responsavel": novo.pk,
                "gerente_autorizador": gerente.pk,
                "senha_gerente": "senha-gerente",
            },
        )
        self.assertEqual(resposta.status_code, 302)
        preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
        self.assertEqual(preparacao.responsavel, novo)
        self.entrar(novo)
        resposta = self.client.get(f"/pedidos/{self.pedido.pk}/")
        self.assertContains(resposta, "Marcar arte do Pedido como concluida")
        self.assertContains(resposta, "Criar arquivo oficial")

    def test_ausencia_critica_persiste_ate_vinculo_explicito_da_restauracao(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            Path(arquivo.caminho_oficial).write_bytes(b"arte original")
            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
            Path(arquivo.caminho_oficial).unlink()

            arquivo = verificar_arquivo_oficial(
                arquivo=arquivo, operador=self.operador
            )
            self.assertTrue(arquivo.ausencia_critica_ativa)
            with self.assertRaises(AlertaArquivoInvalido):
                reconhecer_alerta_arquivo(
                    arquivo=arquivo, operador=self.operador
                )

            Path(arquivo.caminho_oficial).write_bytes(b"arte original")
            arquivo = verificar_arquivo_oficial(
                arquivo=arquivo, operador=self.operador
            )
            self.assertTrue(arquivo.ausencia_critica_ativa)
            self.assertIn(
                "RESTAURACAO_NAO_CONFIRMADA",
                {item["codigo"] for item in arquivo.discrepancias},
            )

            arquivo = vincular_arquivo_restaurado(
                arquivo=arquivo,
                caminho=arquivo.caminho_oficial,
                operador=self.operador,
            )
            self.assertFalse(arquivo.ausencia_critica_ativa)
            self.assertEqual(arquivo.restaurado_por, self.operador)

    def test_restauracao_divergente_exige_decisao_e_pode_reabrir_arte(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="pdf", operador=self.operador
            )
            Path(arquivo.caminho_oficial).write_bytes(b"versao original")
            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
            concluir_arte_pedido(pedido=self.pedido, operador=self.operador)
            Path(arquivo.caminho_oficial).unlink()
            arquivo = verificar_arquivo_oficial(
                arquivo=arquivo, operador=self.operador
            )
            Path(arquivo.caminho_oficial).write_bytes(b"versao restaurada diferente")

            with self.assertRaisesMessage(
                RestauracaoArquivoInvalida, "conteudo restaurado diverge"
            ):
                vincular_arquivo_restaurado(
                    arquivo=arquivo,
                    caminho=arquivo.caminho_oficial,
                    operador=self.operador,
                )

            arquivo = vincular_arquivo_restaurado(
                arquivo=arquivo,
                caminho=arquivo.caminho_oficial,
                operador=self.operador,
                decisao="VOLTAR_PREPARACAO",
            )
            preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
            self.assertTrue(arquivo.restauracao_conteudo_divergente)
            self.assertEqual(preparacao.estado, EstadoPreparacaoArte.EM_PREPARACAO)

    def test_restauracao_recusa_outro_caminho_mesmo_com_nome_semelhante(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
            Path(arquivo.caminho_oficial).unlink()
            arquivo = verificar_arquivo_oficial(
                arquivo=arquivo, operador=self.operador
            )
            alternativo = Path(raiz) / arquivo.nome_oficial
            alternativo.write_bytes(b"")

            with self.assertRaisesMessage(
                RestauracaoArquivoInvalida, "caminho oficial original"
            ):
                vincular_arquivo_restaurado(
                    arquivo=arquivo,
                    caminho=str(alternativo),
                    operador=self.operador,
                )

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

    def test_falha_do_compartilhamento_cria_arte_provisoria_controlada(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("nao e uma pasta", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=base / "dados-locais"):
                arquivo = criar_arquivo_oficial(
                    pedido=self.pedido, programa="coreldraw", operador=self.operador
                )

            self.assertTrue(arquivo.provisoria_local)
            self.assertTrue(Path(arquivo.caminho_oficial).is_file())
            self.assertEqual(arquivo.caminho_local_origem, arquivo.caminho_oficial)
            self.assertIn("artes_provisorias", arquivo.caminho_oficial)
            self.assertTrue(arquivo.caminho_destino_pendente.endswith(arquivo.nome_oficial))

    def test_transferencia_valida_integridade_e_preserva_copia_ate_decisao(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=base / "dados-locais"):
                arquivo = criar_arquivo_oficial(
                    pedido=self.pedido, programa="pdf", operador=self.operador
                )
                origem = Path(arquivo.caminho_oficial)
                origem.write_bytes(b"arte pronta")
                destino = base / "servidor-restaurado" / arquivo.nome_oficial
                ArquivoOficialArte.objects.filter(pk=arquivo.pk).update(
                    caminho_destino_pendente=str(destino)
                )
                arquivo.refresh_from_db()
                arquivo = transferir_arquivo_provisorio(
                    arquivo=arquivo, operador=self.operador
                )

                self.assertFalse(arquivo.provisoria_local)
                self.assertEqual(Path(arquivo.caminho_oficial).read_bytes(), b"arte pronta")
                self.assertTrue(origem.exists())
                self.assertEqual(arquivo.copia_local_preservada_em, str(origem))
                self.assertEqual(arquivo.estado_integridade, "INTEGRO")

                decidir_copia_local_transferida(
                    arquivo=arquivo, operador=self.operador, decisao="REMOVER"
                )
                arquivo.refresh_from_db()
                self.assertFalse(origem.exists())
                self.assertIsNotNone(arquivo.copia_local_removida_em)
                self.assertTrue(destino.exists())

    @patch("apps.arquivos.services.registrar_evento", side_effect=RuntimeError)
    def test_falha_de_auditoria_reverte_transferencia_e_preserva_local(self, _evento):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=base / "dados-locais"):
                # A criacao precisa ocorrer antes de ativar a falha causal da transferencia.
                with patch("apps.arquivos.services.registrar_evento"):
                    arquivo = criar_arquivo_oficial(
                        pedido=self.pedido, programa="gimp", operador=self.operador
                    )
                origem = Path(arquivo.caminho_oficial)
                destino = base / "servidor-restaurado" / arquivo.nome_oficial
                ArquivoOficialArte.objects.filter(pk=arquivo.pk).update(
                    caminho_destino_pendente=str(destino)
                )
                arquivo.refresh_from_db()

                with self.assertRaises(RuntimeError):
                    transferir_arquivo_provisorio(
                        arquivo=arquivo, operador=self.operador
                    )

            arquivo.refresh_from_db()
            self.assertTrue(arquivo.provisoria_local)
            self.assertTrue(origem.exists())
            self.assertFalse(destino.exists())

    def test_dupla_indisponibilidade_recusa_criacao(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            dados_locais_inacessiveis = base / "dados-locais.txt"
            dados_locais_inacessiveis.write_text("nao e pasta", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=dados_locais_inacessiveis):
                with self.assertRaisesMessage(
                    ArquivoOficialInvalido,
                    "Nem a pasta compartilhada nem a area provisoria local estao acessiveis.",
                ):
                    criar_arquivo_oficial(
                        pedido=self.pedido, programa="pdf", operador=self.operador
                    )

    def test_colisao_no_destino_preserva_provisorio(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=base / "dados-locais"):
                arquivo = criar_arquivo_oficial(
                    pedido=self.pedido, programa="pdf", operador=self.operador
                )
                origem = Path(arquivo.caminho_oficial)
                destino = base / "servidor-restaurado" / arquivo.nome_oficial
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(b"colisao")
                ArquivoOficialArte.objects.filter(pk=arquivo.pk).update(
                    caminho_destino_pendente=str(destino)
                )
                arquivo.refresh_from_db()

                with self.assertRaisesMessage(
                    ArquivoOficialInvalido,
                    "O destino oficial ja contem um arquivo com este nome.",
                ):
                    transferir_arquivo_provisorio(
                        arquivo=arquivo, operador=self.operador
                    )

            arquivo.refresh_from_db()
            self.assertTrue(arquivo.provisoria_local)
            self.assertTrue(origem.exists())
            self.assertEqual(destino.read_bytes(), b"colisao")

    def test_corrupcao_durante_copia_reverte_transferencia(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=base / "dados-locais"):
                arquivo = criar_arquivo_oficial(
                    pedido=self.pedido, programa="pdf", operador=self.operador
                )
                origem = Path(arquivo.caminho_oficial)
                origem.write_bytes(b"conteudo integro")
                destino = base / "servidor-restaurado" / arquivo.nome_oficial
                ArquivoOficialArte.objects.filter(pk=arquivo.pk).update(
                    caminho_destino_pendente=str(destino)
                )
                arquivo.refresh_from_db()

                with patch(
                    "apps.arquivos.services._sha256_arquivo",
                    side_effect=["hash-origem", "hash-diferente"],
                ):
                    with self.assertRaisesMessage(
                        ArquivoOficialInvalido,
                        "A copia para o servidor falhou na validacao de integridade.",
                    ):
                        transferir_arquivo_provisorio(
                            arquivo=arquivo, operador=self.operador
                        )

            arquivo.refresh_from_db()
            self.assertTrue(arquivo.provisoria_local)
            self.assertTrue(origem.exists())
            self.assertFalse(destino.exists())

    def test_decisao_mover_arquiva_copia_local_sem_afetar_oficial(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=base / "dados-locais"):
                arquivo = criar_arquivo_oficial(
                    pedido=self.pedido, programa="pdf", operador=self.operador
                )
                origem = Path(arquivo.caminho_oficial)
                origem.write_bytes(b"arte pronta")
                destino = base / "servidor-restaurado" / arquivo.nome_oficial
                ArquivoOficialArte.objects.filter(pk=arquivo.pk).update(
                    caminho_destino_pendente=str(destino)
                )
                arquivo.refresh_from_db()
                arquivo = transferir_arquivo_provisorio(
                    arquivo=arquivo, operador=self.operador
                )
                decidir_copia_local_transferida(
                    arquivo=arquivo, operador=self.operador, decisao="MOVER"
                )
                arquivo.refresh_from_db()

                self.assertFalse(origem.exists())
                self.assertEqual(Path(arquivo.caminho_oficial).read_bytes(), b"arte pronta")
                self.assertTrue(Path(arquivo.copia_local_preservada_em).is_file())
                self.assertIn("artes_copias_locais", arquivo.copia_local_preservada_em)

    def test_preferencia_retencao_copias_locais_persiste_sem_scheduler(self):
        perfil, _ = PerfilEmpresa.objects.update_or_create(
            chave="global", defaults={"retencao_copias_locais_dias": 45}
        )
        self.assertEqual(perfil.retencao_copias_locais_dias, 45)
        self.assertFalse(
            EventoOperacional.objects.filter(
                tipo__icontains="RetencaoCopiaLocal"
            ).exists()
        )

    def test_interface_fluxo_provisorio_transferencia_e_decisao(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            self.entrar()
            with override_settings(DATA_DIR=base / "dados-locais"):
                resposta = self.client.post(
                    f"/pedidos/{self.pedido.pk}/arquivos-oficiais/criar/",
                    {"programa_arte": "pdf"},
                )
                self.assertEqual(resposta.status_code, 302)
                arquivo = ArquivoOficialArte.objects.get(pedido=self.pedido)
                origem = Path(arquivo.caminho_oficial)
                origem.write_bytes(b"via interface")
                destino = base / "servidor-restaurado" / arquivo.nome_oficial
                ArquivoOficialArte.objects.filter(pk=arquivo.pk).update(
                    caminho_destino_pendente=str(destino)
                )

                resposta = self.client.get(f"/pedidos/{self.pedido.pk}/")
                self.assertContains(resposta, "Copia provisoria local")
                self.assertContains(resposta, "Transferir e validar agora")

                resposta = self.client.post(
                    f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/transferir-provisorio/"
                )
                self.assertEqual(resposta.status_code, 302)
                resposta = self.client.get(f"/pedidos/{self.pedido.pk}/")
                self.assertContains(resposta, "Transferencia concluida")
                self.assertContains(resposta, "Mover para copias locais")

                resposta = self.client.post(
                    f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/decidir-copia-local/",
                    {"decisao_copia_local": "REMOVER"},
                )
                self.assertEqual(resposta.status_code, 302)
                arquivo.refresh_from_db()
                self.assertFalse(origem.exists())
                self.assertTrue(destino.exists())

    def test_interface_nega_transferencia_sem_autorizacao(self):
        with tempfile.TemporaryDirectory() as raiz:
            base = Path(raiz)
            compartilhamento_inacessivel = base / "servidor-indisponivel"
            compartilhamento_inacessivel.write_text("fora", encoding="utf-8")
            PerfilEmpresa.objects.update_or_create(
                chave="global",
                defaults={"diretorio_artes_raiz": str(compartilhamento_inacessivel)},
            )
            with override_settings(DATA_DIR=base / "dados-locais"):
                arquivo = criar_arquivo_oficial(
                    pedido=self.pedido, programa="pdf", operador=self.operador
                )
            intruso = OperadorGestor.objects.create(
                nome="Profissional sem acesso",
                senha="segura",
                papel=PapelOperador.USUARIO,
            )
            self.entrar(intruso)
            resposta = self.client.post(
                f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/transferir-provisorio/"
            )
            self.assertEqual(resposta.status_code, 302)
            arquivo.refresh_from_db()
            self.assertTrue(arquivo.provisoria_local)

    def test_criacao_inicia_agregado_sem_concluir_automaticamente(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )

            preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
            self.assertEqual(preparacao.estado, EstadoPreparacaoArte.NAO_INICIADA)
            self.assertEqual(preparacao.responsavel, self.operador)

    def test_conclusao_humana_bloqueia_novos_arquivos(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            preparacao = concluir_arte_pedido(pedido=self.pedido, operador=self.operador)

            self.assertEqual(preparacao.estado, EstadoPreparacaoArte.CONCLUIDA)
            with self.assertRaisesMessage(PreparacaoArteInvalida, "concluida"):
                criar_arquivo_oficial(
                    pedido=self.pedido, programa="photoshop", operador=self.operador
                )

    def test_modificacao_pos_conclusao_exige_decisao_e_pode_reabrir(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
            concluir_arte_pedido(pedido=self.pedido, operador=self.operador)
            Path(arquivo.caminho_oficial).write_bytes(b"conteudo da arte")

            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
            arquivo.refresh_from_db()
            self.assertTrue(arquivo.alteracao_pos_conclusao_pendente)
            self.assertEqual(arquivo.ultima_modificacao_por, self.operador)

            preparacao = decidir_alteracao_pos_conclusao(
                arquivo=arquivo, operador=self.operador, manter_concluida=False
            )
            self.assertEqual(preparacao.estado, EstadoPreparacaoArte.EM_PREPARACAO)
            arquivo.refresh_from_db()
            self.assertFalse(arquivo.alteracao_pos_conclusao_pendente)

    def test_modificacao_confirmada_pode_manter_conclusao(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="pdf", operador=self.operador
            )
            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
            concluir_arte_pedido(pedido=self.pedido, operador=self.operador)
            Path(arquivo.caminho_oficial).write_bytes(b"pdf atualizado")
            verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)

            preparacao = decidir_alteracao_pos_conclusao(
                arquivo=arquivo, operador=self.operador, manter_concluida=True
            )
            self.assertEqual(preparacao.estado, EstadoPreparacaoArte.CONCLUIDA)

    def test_conclusao_sem_verificacao_previa_cria_linha_de_base(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            concluir_arte_pedido(pedido=self.pedido, operador=self.operador)

            Path(arquivo.caminho_oficial).write_text(
                "primeira alteracao", encoding="utf-8"
            )
            arquivo.refresh_from_db()
            arquivo = verificar_arquivo_oficial(
                arquivo=arquivo, operador=self.operador
            )

            self.assertTrue(arquivo.alteracao_pos_conclusao_pendente)

    def test_alerta_de_duas_horas_lembra_e_limita_adiamento_a_dois_alertas(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            agora = timezone.now()
            preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
            preparacao.proximo_alerta_em = agora - timedelta(seconds=1)
            preparacao.save(update_fields=["proximo_alerta_em"])

            alerta = avaliar_alerta_inatividade_arte(
                pedido=self.pedido, agora=agora
            )
            self.assertTrue(alerta.ativo)
            self.assertEqual(alerta.numero, 1)
            self.assertTrue(alerta.pode_adiar_amanha)

            preparacao = responder_alerta_inatividade_arte(
                pedido=self.pedido,
                operador=self.operador,
                acao="LEMBRAR_DEPOIS",
                agora=agora,
            )
            self.assertEqual(preparacao.proximo_alerta_em, agora + timedelta(minutes=30))
            preparacao.proximo_alerta_em = agora - timedelta(seconds=1)
            preparacao.save(update_fields=["proximo_alerta_em"])
            responder_alerta_inatividade_arte(
                pedido=self.pedido,
                operador=self.operador,
                acao="AINDA_TRABALHANDO",
                agora=agora,
            )
            preparacao.refresh_from_db()
            preparacao.proximo_alerta_em = agora - timedelta(seconds=1)
            preparacao.save(update_fields=["proximo_alerta_em"])
            terceiro = avaliar_alerta_inatividade_arte(
                pedido=self.pedido, agora=agora
            )
            self.assertEqual(terceiro.numero, 3)
            self.assertFalse(terceiro.pode_adiar_amanha)

    def test_adiar_para_amanha_exige_senha_do_responsavel(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            agora = timezone.now()
            preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
            preparacao.proximo_alerta_em = agora - timedelta(seconds=1)
            preparacao.save(update_fields=["proximo_alerta_em"])

            with self.assertRaisesMessage(AcaoInatividadeArteInvalida, "senha"):
                responder_alerta_inatividade_arte(
                    pedido=self.pedido,
                    operador=self.operador,
                    acao="ADIAR_AMANHA",
                    senha="errada",
                    agora=agora,
                )
            preparacao = responder_alerta_inatividade_arte(
                pedido=self.pedido,
                operador=self.operador,
                acao="ADIAR_AMANHA",
                senha="segura",
                agora=agora,
            )
            self.assertEqual(
                preparacao.adiado_para_data,
                timezone.localtime(agora).date() + timedelta(days=1),
            )
            self.assertFalse(
                avaliar_alerta_inatividade_arte(
                    pedido=self.pedido, agora=agora
                ).ativo
            )

    def test_prazo_critico_bloqueia_adiamento_e_oferece_ajuda(self):
        categoria = CategoriaServico.objects.create(
            nome="Critica", alerta_dias_uteis=2
        )
        self.pedido.data_entrega = timezone.localdate() + timedelta(days=1)
        self.pedido.save(update_fields=["data_entrega"])
        PedidoItem.objects.create(
            pedido=self.pedido, nome="Item critico", categoria_servico=categoria
        )
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            agora = timezone.now()
            preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
            preparacao.proximo_alerta_em = agora - timedelta(seconds=1)
            preparacao.save(update_fields=["proximo_alerta_em"])

            alerta = avaliar_alerta_inatividade_arte(
                pedido=self.pedido, agora=agora
            )
            self.assertTrue(alerta.prazo_critico)
            self.assertFalse(alerta.pode_adiar_amanha)
            with self.assertRaisesMessage(AcaoInatividadeArteInvalida, "prazo critico"):
                responder_alerta_inatividade_arte(
                    pedido=self.pedido,
                    operador=self.operador,
                    acao="ADIAR_AMANHA",
                    senha="segura",
                    agora=agora,
                )
            preparacao = responder_alerta_inatividade_arte(
                pedido=self.pedido,
                operador=self.operador,
                acao="AJUDA_URGENTE",
                agora=agora,
            )
            self.assertEqual(preparacao.ajuda_urgente_solicitada_em, agora)
            self.assertTrue(
                EventoOperacional.objects.filter(
                    tipo="AlertaInatividadeArteRespondido"
                ).exists()
            )

    def test_alerta_aparece_no_detalhe_e_lembrete_persiste(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
            preparacao.proximo_alerta_em = timezone.now() - timedelta(seconds=1)
            preparacao.save(update_fields=["proximo_alerta_em"])
            self.entrar()

            resposta = self.client.get(f"/pedidos/{self.pedido.pk}/")
            self.assertContains(resposta, "sem modificacoes ha mais de duas horas")
            self.assertContains(resposta, "Ainda estou trabalhando")
            self.assertContains(resposta, "Deixar a arte para amanha")

            fila = self.client.get("/preparacao-arte/")
            self.assertContains(fila, "Artes sem atualizacao ha mais de duas horas")
            self.assertContains(fila, self.pedido.cliente.nome)
            notificacao = self.client.get("/api/notificacoes/assistencia/").json()
            self.assertEqual(notificacao["total"], 1)
            self.assertEqual(notificacao["url"], "/preparacao-arte/")

            resposta = self.client.post(
                f"/pedidos/{self.pedido.pk}/arte/responder-inatividade/",
                {"acao": "LEMBRAR_DEPOIS"},
            )
            self.assertEqual(resposta.status_code, 302)
            preparacao.refresh_from_db()
            self.assertEqual(preparacao.alertas_inatividade_respondidos, 1)
            self.assertGreater(preparacao.proximo_alerta_em, timezone.now())

    def test_falha_de_auditoria_reverte_resposta_de_inatividade(self):
        with tempfile.TemporaryDirectory() as raiz:
            PerfilEmpresa.objects.update_or_create(
                chave="global", defaults={"diretorio_artes_raiz": raiz}
            )
            arquivo = criar_arquivo_oficial(
                pedido=self.pedido, programa="coreldraw", operador=self.operador
            )
            self.assertIsNotNone(arquivo.pk)
            preparacao = PreparacaoArtePedido.objects.get(pedido=self.pedido)
            preparacao.proximo_alerta_em = timezone.now() - timedelta(seconds=1)
            preparacao.save(update_fields=["proximo_alerta_em"])
            anterior = preparacao.proximo_alerta_em

            with patch(
                "apps.arquivos.services.registrar_evento", side_effect=RuntimeError
            ):
                with self.assertRaises(RuntimeError):
                    responder_alerta_inatividade_arte(
                        pedido=self.pedido,
                        operador=self.operador,
                        acao="LEMBRAR_DEPOIS",
                    )
            preparacao.refresh_from_db()
            self.assertEqual(preparacao.proximo_alerta_em, anterior)
            self.assertEqual(preparacao.alertas_inatividade_respondidos, 0)

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
    def test_arquivo_ausente_nao_pode_ser_dispensado(self, _stat):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido, caminho=r"C:\Artes\ausente.cdr", operador=self.operador
        )
        verificar_arquivo_oficial(arquivo=arquivo, operador=self.operador)
        self.assertEqual(arquivo.estado_integridade, "ALERTA")
        self.assertEqual(arquivo.discrepancias[0]["codigo"], "ARQUIVO_NAO_ENCONTRADO")

        self.assertTrue(arquivo.ausencia_critica_ativa)
        with self.assertRaises(AlertaArquivoInvalido):
            reconhecer_alerta_arquivo(arquivo=arquivo, operador=self.operador)
        self.assertFalse(
            EventoOperacional.objects.filter(
                tipo="AlertaArquivoOficialReconhecido"
            ).exists()
        )

    @patch("apps.arquivos.services.os.stat", side_effect=FileNotFoundError)
    def test_rota_exibe_alerta_critico_sem_acao_de_dispensa(self, _stat):
        arquivo = vincular_arquivo_oficial(
            pedido=self.pedido, caminho=r"C:\Artes\ausente.cdr", operador=self.operador
        )
        self.entrar()
        self.client.post(f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/verificar/")
        response = self.client.get(f"/pedidos/{self.pedido.pk}/")
        self.assertContains(response, "O arquivo nao foi encontrado")
        self.assertContains(
            response,
            f"ALERTA CRITICO - AUSENCIA DE ARTE OFICIAL DO PEDIDO #{self.pedido.pk}",
        )
        self.assertContains(response, "Vincular arquivo restaurado")
        self.assertNotContains(response, "Eu entendi")
        fila = self.client.get("/preparacao-arte/")
        self.assertContains(fila, "Arquivos oficiais ausentes")
        self.assertContains(fila, self.pedido.cliente.nome)
        notificacao = self.client.get("/api/notificacoes/assistencia/").json()
        self.assertEqual(notificacao["total"], 1)
        self.assertEqual(
            notificacao["por_categoria"][0]["id"],
            "ausencia-arquivo-oficial",
        )
        self.client.post(f"/pedidos/{self.pedido.pk}/arquivos-oficiais/{arquivo.pk}/reconhecer-alerta/")
        arquivo.refresh_from_db()
        self.assertIsNone(arquivo.alerta_reconhecido_em)
        self.assertTrue(arquivo.ausencia_critica_ativa)

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

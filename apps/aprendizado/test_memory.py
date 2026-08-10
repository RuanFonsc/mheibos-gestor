from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.utils import timezone

from apps.aprendizado.knowledge_services import guardar_memoria, recuperar_contexto, recuperar_memorias
from apps.aprendizado.models import CamadaConhecimento, Conhecimento, EstadoConhecimento, MemoriaOperacional
from apps.catalogo.models import OperadorGestor, PapelOperador


class MemoriaOperacionalServiceTests(TestCase):
    def setUp(self):
        self.operador = OperadorGestor.objects.create(
            nome="Operador de memória", papel=PapelOperador.ADMIN, ativo=True,
        )
        self.outro_operador = OperadorGestor.objects.create(
            nome="Outro operador", papel=PapelOperador.USUARIO, ativo=True,
        )

    def test_guardar_e_recuperar_memoria_curta_vigente(self):
        memoria = guardar_memoria(
            operador=self.operador,
            chave="pedido:42",
            conteudo={"etapa": "arte"},
            expira_em=timezone.now() + timedelta(hours=1),
        )

        memorias = list(recuperar_memorias(operador=self.operador, curta=True))

        self.assertEqual(memorias, [memoria])
        self.assertEqual(memorias[0].conteudo["etapa"], "arte")

    def test_memoria_expirada_nao_e_recuperada(self):
        guardar_memoria(
            operador=self.operador,
            chave="pedido:expirado",
            conteudo={"estado": "aberto"},
            expira_em=timezone.now() - timedelta(minutes=1),
        )

        self.assertEqual(list(recuperar_memorias(operador=self.operador)), [])

    def test_memoria_de_longo_prazo_sem_expiracao_permanece_disponivel(self):
        guardar_memoria(
            operador=self.operador,
            chave="preferencia:formato",
            conteudo={"formato": "PDF"},
            curta=False,
        )

        memorias = list(recuperar_memorias(operador=self.operador, curta=False))

        self.assertEqual(len(memorias), 1)
        self.assertEqual(memorias[0].conteudo, {"formato": "PDF"})

    def test_memoria_e_isolada_por_operador(self):
        guardar_memoria(
            operador=self.operador,
            chave="privada",
            conteudo={"valor": "somente um operador"},
        )

        self.assertEqual(list(recuperar_memorias(operador=self.outro_operador)), [])

    def test_operador_inativo_nao_pode_guardar_memoria(self):
        self.operador.ativo = False
        self.operador.save(update_fields=["ativo"])

        with self.assertRaises(PermissionDenied):
            guardar_memoria(operador=self.operador, chave="bloqueada", conteudo={})

    def test_mesma_chave_atualiza_a_memoria_sem_duplicar(self):
        guardar_memoria(operador=self.operador, chave="sessao", conteudo={"n": 1})
        guardar_memoria(operador=self.operador, chave="sessao", conteudo={"n": 2})

        self.assertEqual(MemoriaOperacional.objects.filter(operador=self.operador).count(), 1)
        self.assertEqual(
            recuperar_memorias(operador=self.operador, chave="sessao").get().conteudo,
            {"n": 2},
        )

    def test_contexto_transversal_reune_conhecimento_memoria_e_contexto_atual(self):
        item = Conhecimento.objects.create(
            titulo="Regra de arte",
            conteudo="Conferir dimensões antes da produção",
            camada=CamadaConhecimento.OPERACIONAL,
            estado=EstadoConhecimento.APROVADO,
            fonte="teste",
        )
        memoria = guardar_memoria(
            operador=self.operador,
            chave="pedido:42",
            conteudo={"pedido": 42, "etapa": "arte"},
        )

        contexto = recuperar_contexto(
            operador=self.operador,
            consulta="dimensões arte",
            contexto_atual={"pedido_id": 42},
        )

        self.assertEqual(contexto["conhecimento"], [item])
        self.assertEqual(contexto["memorias"], [memoria])
        self.assertEqual(contexto["contexto_atual"], {"pedido_id": 42})
        self.assertFalse(contexto["ia_necessaria"])
        self.assertEqual({fonte["id"] for fonte in contexto["fontes"]}, {item.pk, memoria.pk})

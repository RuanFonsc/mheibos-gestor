from django.test import TestCase

from apps.catalogo.models import OperadorGestor, PapelOperador
from .models import Missao
from .services import criar_missao_atribuida


class WorkspaceMissaoInterfaceTests(TestCase):
    def setUp(self):
        self.gerente = OperadorGestor.objects.create(nome="Gerente Workspace", senha="segura", papel=PapelOperador.ADMIN)
        self.responsavel = OperadorGestor.objects.create(nome="Responsável Workspace", senha="segura", papel=PapelOperador.USUARIO)
        self.missao = criar_missao_atribuida(
            gerente=self.gerente, responsavel=self.responsavel,
            titulo="Workspace", objetivo="Executar", criterio_conclusao="Validar",
        )
        session = self.client.session
        session["operador_id"] = self.responsavel.pk
        session.save()

    def test_workspace_expoe_tarefas_notas_e_chat(self):
        response = self.client.get(f"/missoes/{self.missao.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarefas")
        self.assertContains(response, "Notas")
        self.assertContains(response, "Chat da missão")

    def test_workspace_registra_tarefa_nota_e_mensagem(self):
        base = f"/missoes/{self.missao.pk}"
        self.client.post(f"{base}/tarefas/adicionar/", {"titulo": "Executar etapa", "descricao": "Detalhar", "responsavel": self.responsavel.pk})
        self.client.post(f"{base}/notas/adicionar/", {"titulo": "Registro", "conteudo": "Andamento"})
        self.client.post(f"{base}/chat/enviar/", {"conteudo": "Atualização"})
        self.missao.refresh_from_db()
        self.assertEqual(self.missao.tarefas.count(), 1)
        self.assertEqual(self.missao.notas.count(), 1)
        self.assertEqual(self.missao.mensagens_chat.count(), 1)

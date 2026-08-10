from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.catalogo.models import OperadorGestor, PapelOperador
from .knowledge_services import aprovar_conhecimento, buscar_conhecimento, registrar_conhecimento
from .models import CamadaConhecimento, EstadoConhecimento


class ConhecimentoDeterministicoTests(TestCase):
    def setUp(self):
        self.admin = OperadorGestor.objects.create(nome="Admin Conhecimento", senha="1234", papel=PapelOperador.ADMIN)
        self.usuario = OperadorGestor.objects.create(nome="Usuario Conhecimento", senha="1234", papel=PapelOperador.USUARIO)

    def test_registro_comeca_pendente_e_aprovacao_exige_admin(self):
        item = registrar_conhecimento(
            operador=self.usuario, titulo="Procedimento", conteudo="Sempre conferir a arte", camada=CamadaConhecimento.OPERACIONAL, fonte="manual interno",
        )
        self.assertEqual(item.estado, EstadoConhecimento.PENDENTE)
        with self.assertRaises(PermissionDenied):
            aprovar_conhecimento(conhecimento=item, operador=self.usuario)
        item = aprovar_conhecimento(conhecimento=item, operador=self.admin)
        self.assertEqual(item.estado, EstadoConhecimento.APROVADO)

    def test_busca_retorna_somente_aprovado_e_respeita_camadas(self):
        pendente = registrar_conhecimento(operador=self.usuario, titulo="Pendente", conteudo="arte oficial", camada=CamadaConhecimento.OPERACIONAL, fonte="teste")
        aprovado = registrar_conhecimento(operador=self.usuario, titulo="Arte oficial", conteudo="Conferir dimensões", camada=CamadaConhecimento.OPERACIONAL, fonte="teste")
        aprovar_conhecimento(conhecimento=aprovado, operador=self.admin)
        resultado = buscar_conhecimento(consulta="arte oficial", camadas=[CamadaConhecimento.OPERACIONAL])
        self.assertEqual([item.pk for item in resultado], [aprovado.pk])
        self.assertNotIn(pendente.pk, [item.pk for item in resultado])

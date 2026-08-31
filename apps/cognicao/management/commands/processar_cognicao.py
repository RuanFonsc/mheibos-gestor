from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import time

from apps.catalogo.models import OperadorGestor
from apps.cognicao.alertas import encaminhar_alertas_para_ia
from apps.cognicao.gateway import SolicitacaoCognitiva, gateway_configurado
from apps.cognicao.models import EstadoTarefaCognitiva, TarefaCognitiva
from apps.cognicao.tools import executar_ferramenta


class Command(BaseCommand):
    help = "Processa tarefas cognitivas pendentes sem bloquear a requisição web."

    def add_arguments(self, parser):
        parser.add_argument("--limite", type=int, default=10)
        parser.add_argument("--loop", action="store_true", help="Mantém o worker processando novas tarefas.")
        parser.add_argument("--intervalo", type=float, default=1.0, help="Intervalo entre ciclos do worker, em segundos.")
        parser.add_argument("--alerta-intervalo", type=float, default=15.0, help="Intervalo entre verificações de alertas acionáveis, em segundos.")

    def handle(self, *args, **options):
        if not options["loop"]:
            encaminhadas = self._encaminhar_alertas()
            processadas = self._processar_lote(options["limite"])
            self.stdout.write(self.style.SUCCESS(f"{processadas} tarefa(s) cognitiva(s) processada(s); {encaminhadas} alerta(s) encaminhado(s)."))
            return

        intervalo = max(0.1, options["intervalo"])
        alerta_intervalo = max(1.0, options["alerta_intervalo"])
        proxima_verificacao_alertas = 0.0
        self.stdout.write(self.style.SUCCESS("Worker cognitivo ativo."))
        while True:
            agora = time.monotonic()
            if agora >= proxima_verificacao_alertas:
                self._encaminhar_alertas()
                proxima_verificacao_alertas = agora + alerta_intervalo
            processadas = self._processar_lote(options["limite"])
            if not processadas:
                time.sleep(intervalo)

    def _processar_lote(self, limite):
        processadas = 0
        for _ in range(max(0, limite)):
            tarefa = self._reservar()
            if tarefa is None:
                break
            processadas += 1
            self._processar(tarefa)
        return processadas

    @staticmethod
    def _reservar():
        with transaction.atomic():
            tarefa = (
                TarefaCognitiva.objects.select_for_update()
                .filter(estado=EstadoTarefaCognitiva.PENDENTE)
                .order_by("criada_em", "id")
                .first()
            )
            if tarefa is None:
                return None
            tarefa.estado = EstadoTarefaCognitiva.PROCESSANDO
            tarefa.iniciada_em = timezone.now()
            tarefa.save(update_fields=["estado", "iniciada_em"])
            return tarefa

    @staticmethod
    def _encaminhar_alertas():
        encaminhadas = 0
        for operador in OperadorGestor.objects.filter(ativo=True).iterator():
            encaminhadas += len(encaminhar_alertas_para_ia(operador=operador))
        return encaminhadas

    @staticmethod
    def _processar(tarefa):
        try:
            proposta = _proposta_deterministica(tarefa.contexto.get("texto", ""), tarefa)
            if proposta is not None:
                tarefa.estado = EstadoTarefaCognitiva.CONCLUIDA
                tarefa.resultado = proposta
                tarefa.concluida_em = timezone.now()
                tarefa.save(update_fields=["estado", "resultado", "concluida_em"])
                return
            contexto_modelo = {
                "solicitacao": tarefa.contexto.get("texto", ""),
                "interface_visivel": tarefa.contexto.get("interface", {}),
            }
            if tarefa.contexto.get("tipo") == "gatilho_alerta":
                contexto_modelo["alerta_operacional"] = tarefa.contexto.get("alerta", {})
            solicitacao = SolicitacaoCognitiva(
                capacidade="assistente_operacional",
                contexto=__import__("json").dumps(contexto_modelo, ensure_ascii=False),
            )
            resposta = gateway_configurado().solicitar(solicitacao)
            tarefa.estado = EstadoTarefaCognitiva.CONCLUIDA
            tarefa.resultado = {
                "texto": resposta.texto,
                "disponivel": resposta.disponivel,
                "provider": resposta.provider,
                "modelo": resposta.modelo,
                "codigo": resposta.codigo,
                "comandos": resposta.comandos,
            }
            tarefa.concluida_em = timezone.now()
            tarefa.save(update_fields=["estado", "resultado", "concluida_em"])
        except Exception as exc:  # pragma: no cover - última barreira do worker
            tarefa.estado = EstadoTarefaCognitiva.FALHOU
            tarefa.erro = str(exc)
            tarefa.concluida_em = timezone.now()
            tarefa.save(update_fields=["estado", "erro", "concluida_em"])


def _proposta_deterministica(texto, tarefa):
    """Comando explícito e seguro enquanto o provedor não devolve ferramentas estruturadas."""
    import re

    consulta_alertas = re.search(r"\b(alertas?|pend(?:ê|e)ncias?)\b", texto, re.IGNORECASE) and re.search(r"\b(mostr|list|quais|consult|ver|abrir)\w*", texto, re.IGNORECASE)
    if consulta_alertas:
        somente_criticos = bool(re.search(r"\b(crític|critic)\w*", texto, re.IGNORECASE))
        resultado = executar_ferramenta(
            nome="consultar_alertas",
            parametros={"somente_criticos": somente_criticos},
            operador=tarefa.conversa.operador,
        )
        if not resultado.sucesso:
            return {"texto": resultado.erro, "disponivel": True, "comandos": []}
        alertas = resultado.dados.get("alertas", [])
        if not alertas:
            return {"texto": "Não há alertas operacionais no seu escopo autorizado.", "disponivel": True, "comandos": []}
        linhas = [f"{item.get('pedido_label', 'Pedido')}: {item.get('titulo', 'Alerta')} — {item.get('mensagem', '')}" for item in alertas[:8]]
        comandos = [{
            "comando": "navegar",
            "parametros": {"tela": "pedido_detalhe", "pedido_id": alertas[0]["pedido_id"]},
            "rotulo": "Abrir o alerta mais urgente",
        }]
        return {
            "texto": f"Encontrei {len(alertas)} alerta(s) no seu escopo.\n" + "\n".join(linhas),
            "disponivel": True,
            "comandos": comandos,
            "alertas": alertas,
        }

    busca_pedido = re.search(r"(?:busque|pesquise|procure|localize)\s+pedidos?\s+(?:de|por)\s+(.+)", texto, re.IGNORECASE)
    if busca_pedido:
        termo = busca_pedido.group(1).strip()[:100]
        return {"texto": f"Vou abrir a lista de pedidos filtrada por: {termo}.", "disponivel": True, "comandos": [{"comando": "pesquisar_pedidos", "parametros": {"termo": termo}, "rotulo": f"Pesquisar pedidos por {termo}"}]}

    preencher_entrega = re.search(r"preencha.*?(?:data de entrega).*?(\d{4}-\d{2}-\d{2})", texto, re.IGNORECASE)
    if preencher_entrega:
        data_entrega = preencher_entrega.group(1)
        return {"texto": "Vou abrir Novo Pedido e preencher a Data de Entrega como proposta. Nada será salvo automaticamente.", "disponivel": True, "comandos": [{"comando": "navegar", "parametros": {"tela": "novo_pedido", "rota": "/pedidos/novo/", "campo": "data_entrega", "valores": {"data_entrega": data_entrega}}, "rotulo": "Abrir e preencher Data de Entrega"}] }

    encontrado = re.search(r"(?:pedido|ordem)\s+#?(\d+).*?status\s+(?:para|como)\s+([A-Za-z_ -]+)", texto, re.IGNORECASE)
    if not encontrado:
        return None
    pedido_id, status = encontrado.groups()
    status = status.strip().upper().replace(" ", "_")
    resultado = executar_ferramenta(
        nome="propor_alteracao_status",
        parametros={"pedido_id": int(pedido_id), "novo_status": status, "motivo": texto},
        operador=tarefa.conversa.operador,
    )
    if not resultado.sucesso:
        return {"texto": resultado.erro, "disponivel": True, "acao": None}
    return {"texto": "Encontrei uma alteração que precisa da sua confirmação.", "disponivel": True, "acao": resultado.dados}

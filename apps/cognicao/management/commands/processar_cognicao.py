from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import time

from apps.catalogo.models import OperadorGestor
from apps.cognicao.alertas import encaminhar_alertas_para_ia
from apps.cognicao.gateway import RespostaCognitiva, SolicitacaoCognitiva, gateway_configurado
from apps.cognicao.models import AlertaCognitiva, EstadoIntervencaoIA, EstadoTarefaCognitiva, IntervencaoIA, TarefaCognitiva
from apps.cognicao.tools import executar_ferramenta
from apps.cognicao.monitoramento import fingerprint_contexto, orçamento_disponivel


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
            if tarefa.contexto.get("tipo") == "gatilho_alerta":
                resposta, triagem = _avaliar_alertas(tarefa)
            else:
                resposta = _solicitar(tarefa, workload=tarefa.workload or "assistant")
                triagem = None
            tarefa.estado = EstadoTarefaCognitiva.CONCLUIDA
            tarefa.resultado = {
                "texto": resposta.texto,
                "disponivel": resposta.disponivel,
                "provider": resposta.provider,
                "modelo": resposta.modelo,
                "codigo": resposta.codigo,
                "comandos": resposta.comandos,
                "estrategia": resposta.estrategia,
                "intervir": resposta.intervir,
                "motivo": resposta.motivo,
                "intervencao": bool(resposta.intervir) if resposta.estrategia == "intervention" else False,
            }
            tarefa.provider = resposta.provider
            tarefa.modelo = resposta.modelo
            tarefa.tokens_input = resposta.tokens_input
            tarefa.tokens_output = resposta.tokens_output
            tarefa.thinking_tokens = resposta.thinking_tokens
            tarefa.duracao_ms = resposta.duracao_ms
            tarefa.custo_estimado = resposta.custo_estimado
            tarefa.concluida_em = timezone.now()
            campos = ["estado", "resultado", "provider", "modelo", "tokens_input", "tokens_output", "thinking_tokens", "duracao_ms", "custo_estimado", "concluida_em"]
            tarefa.save(update_fields=campos)
            if tarefa.contexto.get("tipo") == "gatilho_alerta":
                AlertaCognitiva.objects.filter(
                    operador=tarefa.conversa.operador,
                    chave__in=tarefa.contexto.get("alerta_chaves") or [],
                ).update(ultima_avaliacao_em=timezone.now())
            if tarefa.contexto.get("tipo") == "gatilho_alerta" and resposta.intervir is not True:
                tarefa.notificado_em = timezone.now()
                tarefa.save(update_fields=["notificado_em"])
        except Exception as exc:  # pragma: no cover - última barreira do worker
            tarefa.estado = EstadoTarefaCognitiva.FALHOU
            tarefa.erro = str(exc)
            tarefa.concluida_em = timezone.now()
            tarefa.save(update_fields=["estado", "erro", "concluida_em"])


def _resposta_orcamento_bloqueado(*, workload: str, motivo: str) -> RespostaCognitiva:
    return RespostaCognitiva(
        "A assistência generativa foi reduzida por limite local. Os alertas determinísticos continuam disponíveis.",
        False,
        "none",
        "",
        motivo,
        estrategia=workload,
    )


def _solicitar(tarefa, *, workload: str) -> RespostaCognitiva:
    disponivel, motivo = orçamento_disponivel(operador=tarefa.conversa.operador, fase=workload)
    if not disponivel:
        return _resposta_orcamento_bloqueado(workload=workload, motivo=motivo)
    contexto_modelo = {
        "solicitacao": tarefa.contexto.get("texto", ""),
        "interface_visivel": tarefa.contexto.get("interface", {}),
    }
    solicitacao = SolicitacaoCognitiva(
        capacidade="assistente_operacional",
        contexto=__import__("json").dumps(contexto_modelo, ensure_ascii=False),
        workload=workload,
    )
    return gateway_configurado(workload=workload).solicitar(solicitacao)


def _avaliar_alertas(tarefa) -> tuple[RespostaCognitiva, RespostaCognitiva]:
    contexto_modelo = {
        "alertas_operacionais": tarefa.contexto.get("alertas") or [tarefa.contexto.get("alerta", {})],
        "atividade_usuario": tarefa.contexto.get("atividade", {}),
        "interface_autorizada": tarefa.contexto.get("interface", {}),
        "instrucao": tarefa.contexto.get("texto", ""),
    }
    pedidos = (tarefa.contexto.get("atividade") or {}).get("pedidos") or {}
    alertas = contexto_modelo["alertas_operacionais"]
    if alertas and all((pedidos.get(str(item.get("pedido_id"))) or {}).get("pedido_aberto_pelo_usuario") for item in alertas):
        resposta = RespostaCognitiva(
            "O pedido relacionado já está aberto e em atividade. Mantive a intervenção generativa em silêncio para não interromper o trabalho em andamento.",
            True,
            "deterministic",
            "",
            "ATIVIDADE_EM_ANDAMENTO",
            estrategia="triage",
            intervir=False,
            motivo="O usuário já está trabalhando no pedido relacionado.",
        )
        return resposta, resposta
    disponivel, motivo = orçamento_disponivel(operador=tarefa.conversa.operador, fase="triage")
    if not disponivel:
        bloqueado = _resposta_orcamento_bloqueado(workload="triage", motivo=motivo)
        return bloqueado, bloqueado
    triagem = gateway_configurado(workload="triage").solicitar(
        SolicitacaoCognitiva(
            capacidade="triagem_alertas_operacionais",
            contexto=__import__("json").dumps(contexto_modelo, ensure_ascii=False),
            workload="triage",
        )
    )
    if not triagem.disponivel or not triagem.intervir:
        return triagem, triagem
    contexto_modelo["decisao_triagem"] = {"motivo": triagem.motivo, "texto": triagem.texto}
    disponivel, motivo = orçamento_disponivel(operador=tarefa.conversa.operador, fase="intervention")
    if not disponivel:
        return _resposta_orcamento_bloqueado(workload="intervention", motivo=motivo), triagem
    intervencao = gateway_configurado(workload="intervention").solicitar(
        SolicitacaoCognitiva(
            capacidade="intervencao_contextual_alertas",
            contexto=__import__("json").dumps(contexto_modelo, ensure_ascii=False),
            workload="intervention",
        )
    )
    if not intervencao.disponivel:
        return intervencao, triagem
    total_input = _somar_metricas(triagem.tokens_input, intervencao.tokens_input)
    total_output = _somar_metricas(triagem.tokens_output, intervencao.tokens_output)
    total_thinking = _somar_metricas(triagem.thinking_tokens, intervencao.thinking_tokens)
    total_duration = _somar_metricas(triagem.duracao_ms, intervencao.duracao_ms)
    total_cost = (triagem.custo_estimado or 0) + (intervencao.custo_estimado or 0)
    resposta = RespostaCognitiva(
        intervencao.texto,
        intervencao.disponivel,
        intervencao.provider,
        intervencao.modelo,
        intervencao.codigo,
        intervencao.comandos,
        estrategia="intervention",
        intervir=True,
        motivo=triagem.motivo,
        tokens_input=total_input,
        tokens_output=total_output,
        thinking_tokens=total_thinking,
        duracao_ms=total_duration,
        custo_estimado=total_cost,
    )
    _registrar_intervencao(tarefa, resposta)
    return resposta, triagem


def _somar_metricas(*valores):
    presentes = [valor for valor in valores if valor is not None]
    return sum(presentes) if presentes else None


def _registrar_intervencao(tarefa, resposta: RespostaCognitiva):
    alertas = tarefa.contexto.get("alertas") or [tarefa.contexto.get("alerta", {})]
    principal_chave = str((alertas[0] or {}).get("id") or "")
    principal = tarefa.conversa.operador.alertacognitiva_set.filter(chave=principal_chave).first()
    IntervencaoIA.objects.update_or_create(
        tarefa=tarefa,
        defaults={
            "operador": tarefa.conversa.operador,
            "alerta_principal": principal,
            "alertas": alertas,
            "provider": resposta.provider,
            "modelo": resposta.modelo,
            "estrategia": resposta.estrategia,
            "mensagem": resposta.texto,
            "acoes_disponiveis": resposta.comandos,
            "contexto_hash": fingerprint_contexto({"alertas": alertas, "atividade": tarefa.contexto.get("atividade", {})}),
            "estado": EstadoIntervencaoIA.GERADA,
            "resultado": {"codigo": resposta.codigo, "motivo": resposta.motivo},
            "tokens_input": resposta.tokens_input,
            "tokens_output": resposta.tokens_output,
            "thinking_tokens": resposta.thinking_tokens,
            "duracao_ms": resposta.duracao_ms,
            "custo_estimado": resposta.custo_estimado,
        },
    )


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

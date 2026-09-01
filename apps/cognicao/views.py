import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from apps.auditoria.services import registrar_evento
from apps.catalogo.permissions import operador_atual, pode_editar_pedido
from apps.aprendizado.models import ConversaAprendizado, DirecaoMensagem, EtiquetaConversaWhatsApp
from apps.operacao.projections import queryset_com_projecao
from apps.pedidos.models import Pedido

from .gateway import gateway_configurado
from .interface_viva import INTERFACE_INVENTARIO
from .models import EstadoIntervencaoIA, ConversaCognitiva, EstadoTarefaCognitiva, IntervencaoIA, MensagemCognitiva, TarefaCognitiva
from .monitoramento import auditar_intervencao, registrar_atividade
from .services import resumir_pedido
from apps.pedidos.use_cases import alterar_status_pedido


@require_POST
def resumo_pedido(request, pk):
    pedido = get_object_or_404(
        queryset_com_projecao(Pedido.objects.select_related("cliente")), pk=pk
    )
    operador = operador_atual(request)
    resposta = resumir_pedido(pedido=pedido, gateway=gateway_configurado())
    try:
        registrar_evento(
            tipo="AssistenciaCognitivaSolicitada",
            operador=operador,
            origem="gestor_web",
            alvo_tipo="Pedido",
            alvo_id=str(pedido.pk),
            acao="consultar_resumo_assistido",
            valores_anteriores={},
            valores_posteriores={"disponivel": resposta.disponivel},
            metadados={
                "provider": resposta.provider,
                "modelo": resposta.modelo,
                "codigo": resposta.codigo,
            },
        )
    except Exception:
        # Uma falha auxiliar de auditoria nao pode transformar IA em bloqueio operacional.
        pass
    return render(
        request,
        "cognicao/resumo_pedido.html",
        {"pedido": pedido, "resposta": resposta},
    )


@require_http_methods(["GET"])
def interface_inventario(request):
    return JsonResponse(INTERFACE_INVENTARIO)

def assistente(request):
    operador = operador_atual(request)
    conversa = (
        ConversaCognitiva.objects.filter(operador=operador, ativa=True)
        .prefetch_related("mensagens")
        .first()
    )
    return render(request, "cognicao/assistente.html", {"conversa": conversa, "active": "cognicao"})


def whatsapp(request):
    termo = str(request.GET.get("q") or "").strip()[:100]
    caixa = str(request.GET.get("caixa") or "principal").strip()
    arquivadas = caixa == "arquivadas"
    conversas_queryset = (
        ConversaAprendizado.objects.filter(origem="WHATSAPP", arquivada=arquivadas)
        .prefetch_related("mensagens", "etiquetas")
    )
    if termo:
        conversas_queryset = conversas_queryset.filter(
            Q(nome_contato__icontains=termo)
            | Q(telefone__icontains=termo)
            | Q(contato_id__icontains=termo)
        )
    conversas = list(conversas_queryset.order_by("-ultima_mensagem_em", "-atualizado_em")[:80])
    for item in conversas:
        mensagens = list(item.mensagens.all())
        ultima_mensagem = mensagens[-1] if mensagens else None
        etiquetas = list(item.etiquetas.all())
        setattr(item, "ultima_mensagem", ultima_mensagem)
        setattr(item, "etiquetas_exibicao", etiquetas)
        setattr(item, "etiquetas_filtro", "|".join(etiqueta.nome.casefold() for etiqueta in etiquetas))
        setattr(
            item,
            "nao_lida",
            bool(
                ultima_mensagem
                and ultima_mensagem.direcao == DirecaoMensagem.CLIENTE
                and (not item.lida_em or not ultima_mensagem.enviada_em or item.lida_em < ultima_mensagem.enviada_em)
            ),
        )
        setattr(item, "eh_grupo", item.contato_id.endswith("@g.us"))
    selected_id = str(request.GET.get("conversa") or "").strip()
    selected = next((item for item in conversas if str(item.pk) == selected_id), None) if selected_id else None
    selected = selected or (conversas[0] if conversas else None)
    selected_messages = list(selected.mensagens.all()) if selected else []
    whatsapp_context = {
        "conversa_id": selected.pk if selected else None,
        "nome": selected.nome_contato if selected else "",
        "telefone": selected.telefone if selected else "",
        "mensagens": [
            {
                "direcao": mensagem.direcao,
                "texto": mensagem.texto,
                "tipo": mensagem.tipo,
                "enviada_em": mensagem.enviada_em.isoformat() if mensagem.enviada_em else "",
            }
            for mensagem in selected_messages[-120:]
            if mensagem.texto
        ],
    }
    etiquetas = list(EtiquetaConversaWhatsApp.objects.order_by("nome", "id")[:40])
    return render(
        request,
        "cognicao/whatsapp.html",
        {
            "active": "whatsapp",
            "conversas": conversas,
            "conversa_selecionada": selected,
            "mensagens_selecionadas": selected_messages,
            "termo": termo,
            "caixa": caixa,
            "arquivadas_total": ConversaAprendizado.objects.filter(origem="WHATSAPP", arquivada=True).count(),
            "etiquetas": etiquetas,
            "whatsapp_context": whatsapp_context,
            "filtros_operacionais": {
                "lead": sum(1 for item in conversas if item.tem_lead),
                "pedido": sum(1 for item in conversas if item.tem_sinal_pedido),
                "atencao": sum(1 for item in conversas if item.tem_reclamacao),
            },
            "direcao_cliente": DirecaoMensagem.CLIENTE,
            "direcao_empresa": DirecaoMensagem.EMPRESA,
        },
    )
@require_POST
def whatsapp_etiqueta(request):
    try:
        payload = json.loads(request.body or "{}")
        conversa_id = int(payload.get("conversa_id"))
        nome = str(payload.get("nome") or "").strip()[:48]
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({"erro": "Dados inválidos para a etiqueta."}, status=400)
    conversa = get_object_or_404(ConversaAprendizado, pk=conversa_id, origem="WHATSAPP")
    if not nome:
        return JsonResponse({"erro": "Informe um nome para a etiqueta."}, status=400)
    etiqueta, _ = EtiquetaConversaWhatsApp.objects.get_or_create(conversa=conversa, nome=nome)
    return JsonResponse({"sucesso": True, "etiqueta": {"id": etiqueta.pk, "nome": etiqueta.nome}})

@require_POST
def enviar_mensagem(request):
    operador = operador_atual(request)
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"erro": "Mensagem inválida."}, status=400)
    texto = str(payload.get("texto") or "").strip()
    if not texto or len(texto) > 4000:
        return JsonResponse({"erro": "Informe uma mensagem entre 1 e 4000 caracteres."}, status=400)
    conversa = None
    if payload.get("conversa_id"):
        conversa = ConversaCognitiva.objects.filter(
            pk=payload["conversa_id"], operador=operador, ativa=True
        ).first()
    if conversa is None:
        conversa = ConversaCognitiva.objects.create(operador=operador, titulo=texto[:80])
    mensagem = MensagemCognitiva.objects.create(conversa=conversa, papel="USUARIO", texto=texto)
    contexto_raw = payload.get("interface_context") if isinstance(payload.get("interface_context"), dict) else {}
    campos_visiveis = [{"nome": str(item.get("nome") or "")[:120], "id": str(item.get("id") or "")[:120], "rotulo": str(item.get("rotulo") or "")[:180], "tipo": str(item.get("tipo") or "")[:40], "obrigatorio": bool(item.get("obrigatorio"))} for item in contexto_raw.get("campos", [])[:100] if isinstance(item, dict)]
    acoes_visiveis = [{"texto": str(item.get("texto") or "")[:180], "tipo": str(item.get("tipo") or "")[:20], "href": str(item.get("href") or "")[:240]} for item in contexto_raw.get("acoes", [])[:120] if isinstance(item, dict)]
    whatsapp_raw = contexto_raw.get("whatsapp") if isinstance(contexto_raw.get("whatsapp"), dict) else None
    whatsapp_visivel = None
    if whatsapp_raw is not None:
        whatsapp_visivel = {
            "conversa_id": str(whatsapp_raw.get("conversa_id") or "")[:40],
            "nome": str(whatsapp_raw.get("nome") or "")[:160],
            "telefone": str(whatsapp_raw.get("telefone") or "")[:32],
            "mensagens": [
                {
                    "direcao": str(item.get("direcao") or "")[:16],
                    "texto": str(item.get("texto") or "")[:2000],
                    "tipo": str(item.get("tipo") or "")[:80],
                    "enviada_em": str(item.get("enviada_em") or "")[:48],
                }
                for item in whatsapp_raw.get("mensagens", [])[:120]
                if isinstance(item, dict) and str(item.get("texto") or "").strip()
            ],
        }
    interface_context = {"rota": str(contexto_raw.get("rota") or "")[:240], "titulo": str(contexto_raw.get("titulo") or "")[:240], "campos": campos_visiveis, "acoes": acoes_visiveis, "whatsapp": whatsapp_visivel}

    tarefa = TarefaCognitiva.objects.create(
        conversa=conversa,
        mensagem_usuario=mensagem,
        contexto={"texto": texto, "operador_id": operador.pk, "rota": request.headers.get("Referer", ""), "interface": interface_context},
    )
    return JsonResponse({"conversa_id": conversa.pk, "tarefa_id": tarefa.pk, "estado": tarefa.estado})


@require_http_methods(["GET"])
def tarefa_status(request, pk):
    operador = operador_atual(request)
    tarefa = get_object_or_404(TarefaCognitiva, pk=pk, conversa__operador=operador)
    if tarefa.estado == EstadoTarefaCognitiva.CONCLUIDA and tarefa.resultado:
        MensagemCognitiva.objects.get_or_create(
            conversa=tarefa.conversa,
            papel="MHEIBOS",
            texto=tarefa.resultado.get("texto", ""),
            defaults={"metadados": tarefa.resultado},
        )
    return JsonResponse({"tarefa_id": tarefa.pk, "estado": tarefa.estado, "resultado": tarefa.resultado, "erro": tarefa.erro})


@require_http_methods(["GET"])
def notificacoes_alertas(request):
    operador = operador_atual(request)
    tarefas = list(
        TarefaCognitiva.objects.filter(
            conversa__operador=operador,
            contexto__tipo="gatilho_alerta",
            estado__in=(EstadoTarefaCognitiva.CONCLUIDA, EstadoTarefaCognitiva.FALHOU),
            notificado_em__isnull=True,
        )
        .order_by("concluida_em", "id")[:5]
    )
    if tarefas:
        agora = timezone.now()
        TarefaCognitiva.objects.filter(pk__in=[tarefa.pk for tarefa in tarefas]).update(notificado_em=agora)
    notificacoes = []
    for tarefa in tarefas:
        resultado = tarefa.resultado or {}
        intervencao = getattr(tarefa, "intervencao", None)
        if intervencao is not None:
            if intervencao.estado == EstadoIntervencaoIA.GERADA:
                intervencao.estado = EstadoIntervencaoIA.EXIBIDA
                intervencao.exibida_em = timezone.now()
                intervencao.save(update_fields=["estado", "exibida_em"])
            intervencao_id = intervencao.pk
            resposta_intervencao = intervencao.resposta_usuario
        else:
            intervencao_id = None
            resposta_intervencao = ""
        notificacoes.append({
            "tarefa_id": tarefa.pk,
            "texto": resultado.get("texto") or "A IA não conseguiu concluir a análise deste alerta.",
            "disponivel": bool(resultado.get("disponivel", False)),
            "comandos": resultado.get("comandos") or [],
            "alerta": tarefa.contexto.get("alerta") or {},
            "alertas": tarefa.contexto.get("alertas") or [],
            "intervencao_id": intervencao_id,
            "resposta_intervencao": resposta_intervencao,
            "modelo": resultado.get("modelo") or tarefa.modelo,
            "estrategia": resultado.get("estrategia") or tarefa.workload,
        })
    return JsonResponse({"notificacoes": notificacoes})


@require_POST
def registrar_atividade_view(request):
    operador = operador_atual(request)
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"sucesso": False, "erro": "Atividade inválida."}, status=400)
    tipo = str(payload.get("tipo") or "")[:48]
    alvo_tipo = str(payload.get("alvo_tipo") or "")[:48]
    alvo_id = str(payload.get("alvo_id") or "")[:80]
    dados = payload.get("dados") if isinstance(payload.get("dados"), dict) else {}
    dados = {
        "rota": str(dados.get("rota") or "")[:240],
        "titulo": str(dados.get("titulo") or "")[:180],
    }
    if alvo_tipo == "Pedido" and alvo_id:
        try:
            pedido = Pedido.objects.get(pk=int(alvo_id))
        except (Pedido.DoesNotExist, TypeError, ValueError):
            return JsonResponse({"sucesso": False, "erro": "Pedido não encontrado."}, status=404)
        if not operador.is_admin and not pode_editar_pedido(pedido, operador):
            return JsonResponse({"sucesso": False, "erro": "Pedido fora do escopo autorizado."}, status=403)
    evento = registrar_atividade(operador=operador, tipo=tipo, alvo_tipo=alvo_tipo, alvo_id=alvo_id, dados=dados)
    if evento is None:
        return JsonResponse({"sucesso": False, "erro": "Tipo de atividade não permitido."}, status=400)
    return JsonResponse({"sucesso": True, "evento_id": evento.pk})


@require_POST
def responder_intervencao(request, pk):
    operador = operador_atual(request)
    intervencao = get_object_or_404(IntervencaoIA, pk=pk, operador=operador)
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"sucesso": False, "erro": "Resposta inválida."}, status=400)
    aliases = {"aceitar": "ACEITA", "aceita": "ACEITA", "recusar": "RECUSADA", "recusada": "RECUSADA", "ignorar": "IGNORADA", "ignorada": "IGNORADA", "resolver": "RESOLVIDA", "resolvida": "RESOLVIDA"}
    resposta = aliases.get(str(payload.get("resposta") or "").strip().casefold(), "")
    if resposta not in {item.value for item in EstadoIntervencaoIA}:
        return JsonResponse({"sucesso": False, "erro": "Resposta de intervenção não permitida."}, status=400)
    if intervencao.respondida_em and intervencao.estado != resposta:
        return JsonResponse({"sucesso": False, "erro": "Esta intervenção já recebeu uma resposta."}, status=409)
    agora = timezone.now()
    intervencao.estado = resposta
    intervencao.resposta_usuario = resposta
    intervencao.respondida_em = agora
    intervencao.save(update_fields=["estado", "resposta_usuario", "respondida_em"])
    registrar_atividade(operador=operador, tipo="intervencao_resposta", alvo_tipo="IntervencaoIA", alvo_id=str(intervencao.pk), dados={"resposta": resposta})
    auditar_intervencao(intervencao=intervencao, operador=operador, acao="responder", resultado=resposta)
    return JsonResponse({"sucesso": True, "estado": intervencao.estado})


@require_POST
def confirmar_alteracao_status(request):
    operador = operador_atual(request)
    try:
        payload = json.loads(request.body or "{}")
        pedido = Pedido.objects.get(pk=payload["pedido_id"])
        resultado = alterar_status_pedido(
            pedido=pedido,
            novo_status=payload["novo_status"],
            operador=operador,
            observacao=str(payload.get("motivo") or "Assistência confirmada pelo usuário"),
        )
    except (json.JSONDecodeError, KeyError, TypeError, ValueError, Pedido.DoesNotExist):
        return JsonResponse({"sucesso": False, "erro": "Dados inválidos para a ação."}, status=400)
    except Exception as exc:
        return JsonResponse({"sucesso": False, "erro": str(exc)}, status=409)
    return JsonResponse({"sucesso": True, "alterado": resultado.alterado, "status": resultado.status_novo})

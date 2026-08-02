from decimal import Decimal
import uuid

from django.contrib import messages
from django.conf import settings
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.db.models import Prefetch, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.catalogo.assistencia import pedido_em_alerta, preparar_categorias_pedidos
from apps.auditoria.services import registrar_evento
from apps.arquivos.services import (
    AlertaArquivoInvalido,
    ArquivoOficialInvalido,
    EncerramentoArquivoInvalido,
    TemaPedidoImutavel,
    encerrar_vinculo_arquivo_oficial,
    reconhecer_alerta_arquivo,
    validar_alteracao_tema,
    verificar_arquivo_oficial,
    vincular_arquivo_oficial,
)
from apps.arquivos.referencias import (
    ArteReferenciaInvalida,
    adicionar_arte_referencia,
    desvincular_arte_referencia,
)
from apps.arquivos.anexos import (
    AnexoInvalido,
    adicionar_anexo,
    desvincular_anexo,
)
from apps.arquivos.models import AnexoPedido
from apps.arquivos.models import ArquivoOficialArte, EstadoVinculoArquivo
from apps.arquivos.pesquisa import pesquisar_pedidos_por_artes
from apps.catalogo.models import CategoriaServico, OperadorGestor, PerfilEmpresa, ProdutoServico
from apps.catalogo.os_config import css_linha_cabecalho, normalizar_campos_os
from apps.catalogo.permissions import operador_atual, pode_editar_pedido
from apps.clientes.models import Cliente, StatusCadastroCliente
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.pedidos.forms import PedidoCreateForm, PedidoEditForm, PedidoStatusForm
from apps.pedidos.models import (
    PagamentoPedido,
    Pedido,
    PedidoItem,
    HistoricoStatusPedido,
    PrioridadePedido,
    STATUS_ENTREGA,
    STATUS_ASSISTENCIA,
    STATUS_FUNIL_GESTOR,
    STATUS_PRE_PRODUCAO,
    StatusPagamento,
    StatusPedido,
)
from apps.pedidos.use_cases import (
    AlteracaoStatusNegada,
    EntregaComSaldoNegada,
    alterar_status_pedido,
)
from apps.operacao.services import ProcessoEncerrado
from apps.operacao.projections import projetar_lista, projetar_pedido, queryset_com_projecao
from apps.sincronizacao.services import SincronizacaoInvalida, enfileirar_pedido_local


def pedido_list(request):
    operador = operador_atual(request)
    busca = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    modo_visualizacao = request.GET.get("visualizacao", "grade").strip()
    if modo_visualizacao not in {"grade", "lista"}:
        modo_visualizacao = "grade"
    itens_prefetch = Prefetch(
        "itens",
        queryset=PedidoItem.objects.select_related("produto__categoria_servico", "categoria_servico"),
    )
    arquivos_prefetch = Prefetch(
        "arquivos_oficiais_arte",
        queryset=ArquivoOficialArte.objects.filter(
            estado_vinculo=EstadoVinculoArquivo.ATIVO
        ),
        to_attr="arquivos_oficiais_ativos",
    )
    pedidos = queryset_com_projecao(
        Pedido.objects.select_related("cliente").prefetch_related(
            itens_prefetch, "artes", arquivos_prefetch
        )
    )

    if busca:
        pedidos = pesquisar_pedidos_por_artes(pedidos, busca)
    if status == StatusPedido.EM_PRODUCAO:
        pedidos = pedidos.filter(status__in=STATUS_FUNIL_GESTOR)
    elif status:
        pedidos = pedidos.filter(status=status)
    if categoria:
        pedidos = pedidos.filter(
            Q(itens__categoria_servico_id=categoria) | Q(itens__produto__categoria_servico_id=categoria)
        ).distinct()

    pedidos_lista = projetar_lista(preparar_categorias_pedidos(pedidos[:80]))
    for pedido in pedidos_lista:
        pedido.alerta_prazo = pedido_em_alerta(pedido)

    contexto = {
        "active": "pedidos",
        "pedidos": pedidos_lista,
        "busca": busca,
        "status_atual": status,
        "categoria_atual": categoria,
        "modo_visualizacao": modo_visualizacao,
        "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        "status_choices": StatusPedido.choices,
        "prioridade_choices": PrioridadePedido.choices,
        "total": Pedido.objects.count(),
        "pre_producao": Pedido.objects.filter(status__in=STATUS_PRE_PRODUCAO).count(),
        "em_producao": Pedido.objects.filter(status__in=STATUS_FUNIL_GESTOR).count(),
        "prontos": Pedido.objects.filter(status=StatusPedido.PRONTO).count(),
        "cancelados": Pedido.objects.filter(status=StatusPedido.CANCELADO).count(),
        "pode_acoes_admin": operador.is_admin,
    }
    return render(request, "pedidos/list.html", contexto)


def atendimento_list(request):
    operador = operador_atual(request)
    busca = request.GET.get("q", "").strip()
    pedidos = Pedido.objects.select_related("cliente").prefetch_related("itens", "artes").filter(status=StatusPedido.EM_ATENDIMENTO)
    if busca:
        filtros_busca = (
            Q(cliente__nome__icontains=busca)
            | Q(tema__icontains=busca)
            | Q(usuario_cadastro__icontains=busca)
            | Q(itens__nome__icontains=busca)
        )
        if busca.isdigit():
            filtros_busca |= Q(pk=int(busca)) | Q(legado_id=int(busca))
        pedidos = pedidos.filter(filtros_busca).distinct()
    return render(
        request,
        "pedidos/atendimento.html",
        {
            "active": "atendimento",
            "pedidos": pedidos.order_by("data_entrega", "id")[:120],
            "busca": busca,
            "total_atendimento": Pedido.objects.filter(status=StatusPedido.EM_ATENDIMENTO).count(),
            "meus_atendimento": Pedido.objects.filter(status=StatusPedido.EM_ATENDIMENTO, usuario_cadastro__iexact=operador.nome).count(),
        },
    )


def entrega_list(request):
    operador = operador_atual(request)
    itens_prefetch = Prefetch(
        "itens",
        queryset=PedidoItem.objects.select_related("produto__categoria_servico", "categoria_servico"),
    )
    pedidos = Pedido.objects.select_related("cliente").prefetch_related(itens_prefetch, "pagamentos", "artes").filter(
        status__in=STATUS_ENTREGA
    )
    pedidos_lista = preparar_categorias_pedidos(pedidos.order_by("data_entrega", "id")[:120])
    for pedido in pedidos_lista:
        pedido.alerta_prazo = pedido_em_alerta(pedido)
    contexto = {
        "active": "entrega",
        "pedidos": pedidos_lista,
        "prontos": pedidos.count(),
        "entregues": Pedido.objects.filter(status=StatusPedido.ENTREGUE).count(),
        "pode_acoes_admin": operador.is_admin,
    }
    return render(request, "pedidos/entrega.html", contexto)


def pedido_detail(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related(
            "itens", "artes", "anexos", "arquivos_oficiais_arte", "pagamentos", "processos__etapas__responsavel"
        ),
        pk=pk,
    )
    operador = operador_atual(request)
    return render(
        request,
        "pedidos/detail.html",
        {
            "active": "pedidos",
            "pedido": pedido,
            "pode_editar": pode_editar_pedido(pedido, operador),
            "pode_cancelar": operador.pode_cancelar_pedido,
            "pode_desvincular_anexo": operador.is_admin,
            "pode_encerrar_arquivo_oficial": operador.is_admin,
            "arquivos_oficiais": pedido.arquivos_oficiais_arte.all(),
            "anexos_ativos": pedido.anexos.filter(desvinculado_em__isnull=True),
            "status_form": PedidoStatusForm(initial={"status": pedido.status}),
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        },
    )


def pedido_ordem_servico(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes", "pagamentos"),
        pk=pk,
    )
    perfil_empresa, _ = PerfilEmpresa.objects.get_or_create(chave="global")
    campos = normalizar_campos_os(perfil_empresa.os_campos)
    artes = list(pedido.artes_ativas.order_by("ordem", "id"))
    arte = artes[0] if artes else None
    itens = list(pedido.itens.all())
    descricao = pedido.descricao_legada or " | ".join(str(item) for item in itens)
    designer_nome = (pedido.designer or pedido.usuario_cadastro or "").strip()
    designer_foto = None
    if designer_nome:
        operador_designer = OperadorGestor.objects.filter(nome__iexact=designer_nome).first()
        if operador_designer and operador_designer.foto:
            designer_foto = operador_designer.foto
    contexto = {
        "pedido": pedido,
        "perfil_empresa": perfil_empresa,
        "campos": campos,
        "arte": arte,
        "artes": artes,
        "itens": itens,
        "descricao_os": descricao,
        "designer_foto": designer_foto,
        "os_header_line_css": css_linha_cabecalho(perfil_empresa.os_linha_cabecalho),
    }
    return render(request, "pedidos/ordem_servico.html", contexto)


def pedido_edit(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes"),
        pk=pk,
    )
    operador = operador_atual(request)
    if not pode_editar_pedido(pedido, operador):
        messages.error(request, "Seu perfil só permite editar pedidos cadastrados por você.")
        return redirect("pedido_detail", pk=pedido.pk)
    cliente = pedido.cliente
    initial = {
        "nome_cliente": cliente.nome,
        "data_pedido": pedido.data_pedido,
        "tema": pedido.tema,
        "telefone_1": cliente.telefone_principal,
        "telefone_2": cliente.telefone_secundario,
        "data_entrega": pedido.data_entrega,
        "hora_entrega": pedido.hora_entrega,
        "observacoes": pedido.observacoes,
        "caminho_arquivo_corel": pedido.caminho_arquivo_corel,
        "valor_pago": pedido.valor_pago_legado,
        "forma_pagamento": pedido.forma_pagamento_legada,
        "desconto_ajuste": pedido.desconto_ajuste,
        "prioridade": pedido.prioridade,
        "canal_atendimento": pedido.canal_atendimento,
        "status": pedido.status,
        "usuario_cadastro": pedido.usuario_cadastro or "",
    }

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "remover_arte":
            if not operador.is_admin:
                messages.error(request, "Seu perfil não tem permissão para excluir informações do pedido.")
                return redirect("pedido_edit", pk=pedido.pk)
            try:
                desvincular_arte_referencia(
                    arte_id=request.POST.get("arte_id"),
                    pedido=pedido,
                    operador=operador,
                )
            except ArteReferenciaInvalida as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, "Vinculo da arte de referencia removido; arquivo fisico preservado.")
            return redirect("pedido_edit", pk=pedido.pk)

        form = PedidoEditForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                _atualizar_pedido(
                    pedido, form, request.FILES.getlist("artes"), operador
                )
            except TemaPedidoImutavel as exc:
                messages.error(request, str(exc))
                return redirect("pedido_edit", pk=pedido.pk)
            except (EntregaComSaldoNegada, ProcessoEncerrado):
                messages.error(
                    request,
                    "A entrega nao pode ser concluida enquanto houver saldo aberto.",
                )
                return redirect("pedido_edit", pk=pedido.pk)
            messages.success(request, "Pedido atualizado.")
            return redirect("pedido_detail", pk=pedido.pk)
        messages.error(request, "Não foi possível salvar o pedido. Confira os campos destacados.")
    else:
        form = PedidoEditForm(initial=initial)

    produtos = ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True).order_by("nome")
    itens = list(pedido.itens.all())
    itens_rows = (itens + [None] * 5)[:5]
    operadores = OperadorGestor.objects.filter(ativo=True).order_by("nome")
    return render(
        request,
        "pedidos/edit.html",
        {
            "active": "pedidos",
            "pedido": pedido,
            "form": form,
            "produtos": produtos,
            "operadores": operadores,
            "categorias_servico": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
            "itens_rows": itens_rows,
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        },
    )


def pedido_update_status(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    retorno = request.POST.get("next")
    if not (retorno and retorno.startswith("/") and not retorno.startswith("//")):
        retorno = None
    form = PedidoStatusForm(request.POST)
    if form.is_valid():
        novo_status = form.cleaned_data["status"]
        origem_producao = bool(retorno and retorno.startswith("/producao/"))
        try:
            alterar_status_pedido(
                pedido=pedido,
                novo_status=novo_status,
                operador=operador,
                origem_operacional=origem_producao,
            )
        except (AlteracaoStatusNegada, EntregaComSaldoNegada, ProcessoEncerrado):
            messages.error(request, "Seu perfil não tem permissão para alterar este pedido.")
            if retorno:
                return redirect(retorno)
            return redirect("pedido_detail", pk=pedido.pk)
        messages.success(request, "Status atualizado.")
    if retorno:
        return redirect(retorno)
    return redirect("pedido_detail", pk=pedido.pk)


def pedido_bulk_action(request):
    if request.method != "POST":
        return redirect("pedido_list")

    operador = operador_atual(request)
    retorno = request.POST.get("next")
    if not (retorno and retorno.startswith("/") and not retorno.startswith("//")):
        retorno = None
    acao = request.POST.get("acao", "").strip()
    ids = [valor for valor in request.POST.getlist("pedido_ids") if valor.isdigit()]
    pedidos = list(Pedido.objects.select_related("cliente").filter(pk__in=ids))

    if not pedidos:
        messages.warning(request, "Selecione pelo menos um pedido.")
        return redirect(retorno or "pedido_list")

    status_por_acao = {
        "marcar_pronto": StatusPedido.PRONTO,
        "enviar_producao": StatusPedido.EM_PRODUCAO,
        "marcar_entregue": StatusPedido.ENTREGUE,
        "cancelar": StatusPedido.CANCELADO,
    }

    if acao == "excluir":
        if not operador.is_admin:
            messages.error(request, "Somente administradores podem excluir pedidos.")
            return redirect(retorno or "pedido_list")
        excluidos = 0
        protegidos = 0
        for pedido in pedidos:
            try:
                pedido.delete()
                excluidos += 1
            except ProtectedError:
                protegidos += 1
        if excluidos:
            messages.success(request, f"{excluidos} pedido(s) excluido(s).")
        if protegidos:
            messages.warning(request, f"{protegidos} pedido(s) possuem vinculos protegidos e nao foram excluidos.")
        return redirect(retorno or "pedido_list")

    novo_status = status_por_acao.get(acao)
    if not novo_status:
        messages.error(request, "Acao em massa invalida.")
        return redirect(retorno or "pedido_list")

    origem_operacional = bool(
        retorno
        and (
            retorno.startswith("/producao/")
            or retorno.startswith("/assistencia-envio/")
            or retorno.startswith("/pedidos/entrega/")
        )
    )
    atualizados = 0
    bloqueados = 0
    for pedido in pedidos:
        try:
            resultado = alterar_status_pedido(
                pedido=pedido,
                novo_status=novo_status,
                operador=operador,
                origem_operacional=origem_operacional,
            )
        except (AlteracaoStatusNegada, EntregaComSaldoNegada, ProcessoEncerrado):
            bloqueados += 1
            continue
        atualizados += int(resultado.alterado)

    if atualizados:
        messages.success(request, f"{atualizados} pedido(s) atualizado(s).")
    if bloqueados:
        messages.warning(request, f"{bloqueados} pedido(s) ignorado(s) por permissao.")
    if not atualizados and not bloqueados:
        messages.info(request, "Nenhum pedido precisou ser alterado.")
    return redirect(retorno or "pedido_list")


def pedido_rejeitar_producao(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    retorno = request.POST.get("next")
    if not (retorno and retorno.startswith("/") and not retorno.startswith("//")):
        retorno = "producao_home"
    motivo = (request.POST.get("motivo") or "").strip()
    if request.method != "POST":
        return redirect(retorno)
    if not motivo:
        messages.error(request, "Informe o motivo para devolver o pedido aos designers.")
        return redirect(retorno)
    if pedido.status != StatusPedido.EM_PRODUCAO:
        messages.error(request, "Somente pedidos em producao podem ser rejeitados.")
        return redirect(retorno)
    operador = operador_atual(request)
    pedido.projecao = projetar_pedido(pedido)
    alterar_status_pedido(
        pedido=pedido,
        novo_status=StatusPedido.AGUARDANDO_ARTE,
        operador=operador,
        origem_operacional=True,
        observacao=f"Rejeitado pela produção: {motivo}",
    )


    messages.warning(request, f"Pedido #{pedido.pk} devolvido para os designers.")
    return redirect(retorno)


def pedido_vincular_arquivo_oficial(request, pk):
    if request.method != "POST":
        return redirect("pedido_detail", pk=pk)
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    if not pode_editar_pedido(pedido, operador):
        messages.error(request, "Seu perfil nao pode vincular arquivos a este Pedido.")
        return redirect("pedido_detail", pk=pk)
    try:
        vincular_arquivo_oficial(
            pedido=pedido,
            caminho=request.POST.get("caminho_oficial", ""),
            operador=operador,
        )
    except ArquivoOficialInvalido as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Arquivo oficial de arte vinculado.")
    return redirect("pedido_detail", pk=pk)


def pedido_verificar_arquivo_oficial(request, pk, arquivo_id):
    if request.method != "POST":
        return redirect("pedido_detail", pk=pk)
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    if not pode_editar_pedido(pedido, operador):
        messages.error(request, "Seu perfil nao pode verificar arquivos deste Pedido.")
        return redirect("pedido_detail", pk=pk)
    arquivo = get_object_or_404(pedido.arquivos_oficiais_arte, pk=arquivo_id)
    verificar_arquivo_oficial(arquivo=arquivo, operador=operador)
    if arquivo.estado_integridade == "ALERTA":
        messages.warning(request, "A verificacao encontrou discrepancias no arquivo oficial.")
    else:
        messages.success(request, "Arquivo oficial verificado sem discrepancias.")
    return redirect("pedido_detail", pk=pk)


def pedido_reconhecer_alerta_arquivo(request, pk, arquivo_id):
    if request.method != "POST":
        return redirect("pedido_detail", pk=pk)
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    if not pode_editar_pedido(pedido, operador):
        messages.error(request, "Seu perfil nao pode reconhecer alertas deste Pedido.")
        return redirect("pedido_detail", pk=pk)
    arquivo = get_object_or_404(pedido.arquivos_oficiais_arte, pk=arquivo_id)
    try:
        reconhecer_alerta_arquivo(arquivo=arquivo, operador=operador)
    except AlertaArquivoInvalido as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Confirmacao 'Eu entendi' registrada na auditoria.")
    return redirect("pedido_detail", pk=pk)


def pedido_adicionar_anexos(request, pk):
    if request.method != "POST":
        return redirect("pedido_detail", pk=pk)
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    if not pode_editar_pedido(pedido, operador):
        messages.error(request, "Seu perfil nao pode adicionar anexos a este Pedido.")
        return redirect("pedido_detail", pk=pk)
    uploads = request.FILES.getlist("anexos")
    if not uploads:
        messages.error(request, "Selecione pelo menos um arquivo para anexar.")
        return redirect("pedido_detail", pk=pk)
    manter_duplicados = request.POST.get("manter_duplicados") == "1"
    adicionados = 0
    for upload in uploads:
        try:
            adicionar_anexo(
                pedido=pedido,
                upload=upload,
                operador=operador,
                manter_duplicado=manter_duplicados,
            )
        except AnexoInvalido as exc:
            messages.warning(request, str(exc))
        else:
            adicionados += 1
    if adicionados:
        messages.success(request, f"{adicionados} anexo(s) vinculado(s) sem interpretar o conteudo.")
    return redirect("pedido_detail", pk=pk)


def pedido_desvincular_anexo(request, pk, anexo_id):
    if request.method != "POST":
        return redirect("pedido_detail", pk=pk)
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    try:
        desvincular_anexo(anexo_id=anexo_id, pedido=pedido, operador=operador)
    except AnexoInvalido as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Vinculo do anexo removido; arquivo fisico preservado.")
    return redirect("pedido_detail", pk=pk)


def pedido_baixar_anexo(request, pk, anexo_id):
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    if not pode_editar_pedido(pedido, operador):
        raise Http404
    anexo = get_object_or_404(
        AnexoPedido,
        pk=anexo_id,
        pedido=pedido,
        desvinculado_em__isnull=True,
    )
    return FileResponse(
        anexo.arquivo.open("rb"),
        as_attachment=True,
        filename=anexo.nome_original,
    )


def pedido_encerrar_arquivo_oficial(request, pk, arquivo_id):
    if request.method != "POST":
        return redirect("pedido_detail", pk=pk)
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    arquivo = get_object_or_404(pedido.arquivos_oficiais_arte, pk=arquivo_id)
    if request.POST.get("confirmacao", "").strip().upper() != "ENCERRAR":
        messages.error(request, "Digite ENCERRAR para confirmar a revisao do vinculo.")
        return redirect("pedido_detail", pk=pk)
    try:
        encerrar_vinculo_arquivo_oficial(
            arquivo=arquivo,
            operador=operador,
            observacao=request.POST.get("observacao", ""),
            backup_previo_confirmado=request.POST.get("backup_previo_confirmado") == "1",
        )
    except EncerramentoArquivoInvalido as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Vinculo oficial encerrado; arquivo e historico preservados.")
    return redirect("pedido_detail", pk=pk)


def pedido_create(request):
    operador = operador_atual(request)
    hoje = timezone.localdate()
    cliente_prefill = Cliente.objects.filter(pk=request.GET.get("cliente")).first()
    if request.method == "POST":
        dados_post = request.POST.copy()
        dados_post["data_pedido"] = hoje.isoformat()
        form = PedidoCreateForm(dados_post, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    offline = settings.MHEIBOS_RUNTIME_ROLE == "client_offline"
                    pedido = _criar_pedido(
                        form,
                        request.FILES.getlist("artes"),
                        operador,
                        origem_offline=offline,
                    )
                    if offline:
                        try:
                            estacao_id = uuid.UUID(settings.MHEIBOS_STATION_ID)
                        except (TypeError, ValueError) as exc:
                            raise SincronizacaoInvalida(
                                "Esta estacao offline ainda nao possui identidade valida."
                            ) from exc
                        enfileirar_pedido_local(
                            pedido=pedido,
                            operador=operador,
                            estacao_id=estacao_id,
                            versao_politica=settings.MHEIBOS_POLICY_VERSION,
                        )
            except SincronizacaoInvalida as exc:
                messages.error(request, str(exc))
            else:
                identificador = pedido.codigo_visivel_offline or pedido.pk
                messages.success(request, f"Pedido #{identificador} criado com sucesso.")
                return redirect("pedido_detail", pk=pedido.pk)
        messages.error(request, "Não foi possível criar o pedido. Confira os campos destacados.")
    else:
        initial = {
            "data_pedido": hoje,
            "data_entrega": hoje,
            "forma_pagamento": "PIX",
            "valor_pago": Decimal("0.00"),
            "desconto_ajuste": Decimal("0.00"),
            "prioridade": PrioridadePedido.NORMAL,
            "canal_atendimento": operador.canal_atendimento_padrao,
        }
        if cliente_prefill:
            initial.update(
                {
                    "nome_cliente": cliente_prefill.nome,
                    "telefone_1": cliente_prefill.telefone_principal,
                    "telefone_2": cliente_prefill.telefone_secundario,
                }
            )
        form = PedidoCreateForm(initial=initial)

    recentes = Pedido.objects.select_related("cliente").order_by("-id")[:6]
    prioridades = Pedido.objects.select_related("cliente").filter(
        status__in=STATUS_PRE_PRODUCAO
    ).order_by("data_entrega", "id")[:8]
    produtos = ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True).order_by("nome")
    clientes_autocomplete = Cliente.objects.filter(
        status_cadastro=StatusCadastroCliente.CADASTRADO
    ).order_by("nome")[:400]
    return render(
        request,
        "pedidos/create.html",
        {
            "active": "novo_pedido",
            "form": form,
            "recentes": recentes,
            "prioridades": prioridades,
            "produtos": produtos,
            "clientes_autocomplete": clientes_autocomplete,
            "categorias_servico": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
            "operador_atual": operador,
        },
    )


@transaction.atomic
def _criar_pedido(form, arquivos, operador, *, origem_offline=False):
    dados = form.cleaned_data
    caminho_oficial = (dados.get("caminho_arquivo_corel") or "").strip()
    if origem_offline and caminho_oficial:
        raise SincronizacaoInvalida(
            "Arquivos fisicos nao podem ser vinculados no modo offline restrito."
        )
    cliente, _ = Cliente.objects.get_or_create(
        nome=dados["nome_cliente"].upper(),
        defaults={
            "telefone_principal": dados.get("telefone_1", ""),
            "telefone_secundario": dados.get("telefone_2", ""),
        },
    )

    itens = []
    subtotal = Decimal("0.00")
    for index in range(1, 6):
        nome = form.data.get(f"item_nome_{index}", "").strip()
        if not nome:
            continue
        produto = ProdutoServico.objects.filter(nome__iexact=nome).first()
        categoria = produto.categoria_servico if produto else CategoriaServico.objects.filter(pk=form.data.get(f"item_categoria_{index}") or None).first()
        quantidade = Decimal(form.data.get(f"item_qtd_{index}") or "1")
        preco = Decimal(str(form.data.get(f"item_preco_{index}") or "0").replace(",", "."))
        descricao = form.data.get(f"item_desc_{index}", "").strip()
        subtotal += quantidade * preco
        itens.append((index, nome, quantidade, preco, descricao, produto, categoria))

    valor_total = subtotal + dados["desconto_ajuste"]
    if dados["marcar_pronto"]:
        status = StatusPedido.PRONTO
    elif dados["aguardar_arte"]:
        status = StatusPedido.AGUARDANDO_ARTE
    else:
        status = StatusPedido.ARTE_EM_PREPARO
    pedido = Pedido.objects.create(
        cliente=cliente,
        tema=dados["tema"].upper(),
        data_pedido=dados["data_pedido"],
        data_entrega=dados["data_entrega"],
        hora_entrega=dados.get("hora_entrega"),
        observacoes=dados.get("observacoes", ""),
        caminho_arquivo_corel="",
        valor_total=valor_total,
        valor_pago_legado=dados["valor_pago"],
        desconto_ajuste=dados["desconto_ajuste"],
        forma_pagamento_legada=dados["forma_pagamento"],
        prioridade=dados["prioridade"],
        canal_atendimento=dados["canal_atendimento"],
        status=status,
        estado_entrega=(
            "PRONTO" if status == StatusPedido.PRONTO else "PENDENTE"
        ),
        origem="BALCAO",
        usuario_cadastro=(form.data.get("usuario_cadastro") or "").strip() or "Usuario Temporario",
        data_registro=timezone.now(),
    )

    for ordem, nome, quantidade, preco, descricao, produto, categoria in itens:
        PedidoItem.objects.create(
            pedido=pedido,
            produto=produto,
            categoria_servico=categoria,
            ordem=ordem,
            nome=nome,
            quantidade=quantidade,
            preco_unitario=preco,
            custo_unitario_estimado=produto.custo_estimado if produto else Decimal("0.00"),
            descricao=descricao,
        )

    _sincronizar_pagamento_informado(pedido, dados["valor_pago"], dados["forma_pagamento"], dados["data_pedido"])

    for ordem, arquivo in enumerate(arquivos):
        adicionar_arte_referencia(
            pedido=pedido,
            upload=arquivo,
            operador=operador,
            ordem=ordem,
        )

    sincronizar_financeiro_pedido(pedido)
    if caminho_oficial:
        vincular_arquivo_oficial(
            pedido=pedido, caminho=caminho_oficial, operador=operador
        )
    if not origem_offline:
        registrar_evento(tipo="PedidoCriado", operador=operador, origem="gestor_web", alvo_tipo="Pedido", alvo_id=str(pedido.pk), acao="criar", valores_anteriores={}, valores_posteriores={"status_legado": pedido.status, "estado_comercial": pedido.estado_comercial, "estado_entrega": pedido.estado_entrega, "origem": pedido.origem, "valor_total": str(pedido.valor_total)})
    return pedido


def _sincronizar_pagamento_informado(pedido, valor_pago, forma_pagamento, data_pagamento):
    valor_pago = valor_pago or Decimal("0.00")
    pagamentos = pedido.pagamentos.all()
    pagamento = pagamentos.filter(observacoes="Valor pago informado no pedido").first()
    if not pagamento and pagamentos.count() <= 1:
        pagamento = pagamentos.first()

    if valor_pago <= 0:
        if pagamento and pagamentos.count() <= 1:
            pagamento.delete()
        return

    dados = {
        "valor": valor_pago,
        "forma": forma_pagamento,
        "data_pagamento": data_pagamento,
        "status": StatusPagamento.CONFIRMADO,
        "observacoes": "Valor pago informado no pedido",
    }
    if pagamento:
        for campo, valor in dados.items():
            setattr(pagamento, campo, valor)
        pagamento.save(update_fields=list(dados.keys()))
    else:
        PagamentoPedido.objects.create(pedido=pedido, **dados)


@transaction.atomic
def _atualizar_pedido(pedido, form, arquivos, operador):
    dados = form.cleaned_data
    validar_alteracao_tema(pedido=pedido, novo_tema=dados["tema"].upper())
    caminho_oficial = (dados.get("caminho_arquivo_corel") or "").strip()
    cliente = pedido.cliente
    cliente.nome = dados["nome_cliente"].upper()
    cliente.telefone_principal = dados.get("telefone_1", "")
    cliente.telefone_secundario = dados.get("telefone_2", "")
    cliente.save(update_fields=["nome", "telefone_principal", "telefone_secundario"])

    pedido.itens.all().delete()
    subtotal = Decimal("0.00")
    for index in range(1, 6):
        nome = form.data.get(f"item_nome_{index}", "").strip()
        if not nome:
            continue
        produto = ProdutoServico.objects.filter(nome__iexact=nome).first()
        categoria = produto.categoria_servico if produto else CategoriaServico.objects.filter(pk=form.data.get(f"item_categoria_{index}") or None).first()
        quantidade = Decimal(form.data.get(f"item_qtd_{index}") or "1")
        preco = Decimal(str(form.data.get(f"item_preco_{index}") or "0").replace(",", "."))
        descricao = form.data.get(f"item_desc_{index}", "").strip()
        subtotal += quantidade * preco
        PedidoItem.objects.create(
            pedido=pedido,
            produto=produto,
            categoria_servico=categoria,
            ordem=index,
            nome=nome,
            quantidade=quantidade,
            preco_unitario=preco,
            custo_unitario_estimado=produto.custo_estimado if produto else Decimal("0.00"),
            descricao=descricao,
        )

    pedido.tema = dados["tema"].upper()
    pedido.data_pedido = dados["data_pedido"]
    pedido.data_entrega = dados["data_entrega"]
    pedido.hora_entrega = dados.get("hora_entrega")
    pedido.observacoes = dados.get("observacoes", "")
    pedido.prioridade = dados["prioridade"]
    pedido.canal_atendimento = dados["canal_atendimento"]
    pedido.valor_total = subtotal + dados["desconto_ajuste"]
    pedido.valor_pago_legado = dados["valor_pago"]
    pedido.desconto_ajuste = dados["desconto_ajuste"]
    pedido.forma_pagamento_legada = dados["forma_pagamento"]
    novo_status = dados["status"]
    pedido.usuario_cadastro = dados.get("usuario_cadastro", "").strip()
    pedido.save()
    if caminho_oficial:
        vincular_arquivo_oficial(
            pedido=pedido, caminho=caminho_oficial, operador=operador
        )
    _sincronizar_pagamento_informado(pedido, dados["valor_pago"], dados["forma_pagamento"], dados["data_pedido"])

    if novo_status != pedido.status:
        alterar_status_pedido(
            pedido=pedido,
            novo_status=novo_status,
            operador=operador,
        )

    ordem_base = pedido.artes.count()
    for offset, arquivo in enumerate(arquivos):
        adicionar_arte_referencia(
            pedido=pedido,
            upload=arquivo,
            operador=operador,
            ordem=ordem_base + offset,
        )

    sincronizar_financeiro_pedido(pedido)
    return pedido

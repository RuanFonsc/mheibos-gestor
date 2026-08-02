import json
import hashlib
from collections import defaultdict

from django.contrib import messages
from django.conf import settings
from django.db import connections
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.catalogo.assistencia import categorias_do_pedido, dias_uteis_restantes, pedido_em_alerta, pedidos_assistencia, preparar_categorias_pedidos
from apps.catalogo.authentication import (
    autenticar_operador,
    definir_senha_operador,
    iniciar_sessao_operador,
    sessao_possui_operador,
    validar_senha_operador,
)
from apps.catalogo.bootstrap import primeiro_admin_pendente
from apps.catalogo.forms import (
    CategoriaServicoForm,
    CategoriaUsuarioForm,
    OperadorGestorForm,
    OperadorPerfilForm,
    OperadorSenhaForm,
    PerfilEmpresaForm,
    ProdutoServicoForm,
    senha_operador_valida,
)
from apps.catalogo.licensing import activate_online, install_offline_license, machine_fingerprint, verify_license
from apps.catalogo.models import (
    CategoriaServico,
    CategoriaUsuario,
    ChaveRecuperacaoSenha,
    OperadorGestor,
    PapelOperador,
    PerfilEmpresa,
    ProdutoServico,
)
from apps.catalogo.os_config import cores_linha_cabecalho_form, lista_campos_os, normalizar_linha_cabecalho, salvar_campos_os, salvar_linha_cabecalho
from apps.catalogo.permissions import operador_atual
from apps.catalogo.ui_prefs import carregar_preferencias, garantir_operadores_padrao, salvar_preferencias
from apps.catalogo.widget_data import pedidos_para_widget, resumo_assistencia_envio
from apps.pedidos.models import Pedido, PedidoItem, PrioridadePedido, StatusPedido
from apps.operacao.projections import projetar_lista, queryset_com_projecao, queryset_fila_producao
from apps.pedidos.use_cases import (
    AlteracaoStatusNegada,
    ArteNecessariaParaProducao,
    alterar_status_pedido,
)


def _destino_seguro(request, padrao):
    proximo = request.GET.get("next") or request.POST.get("next") or ""
    if proximo.startswith("/") and not proximo.startswith("//"):
        return proximo
    return reverse(padrao)


def licenca_ativar(request):
    status = verify_license()
    next_url = request.GET.get("next") or request.POST.get("next") or reverse("home")
    if status.ok and request.method == "GET":
        return redirect(_destino_seguro(request, "home"))

    erro_middleware = request.session.pop("licenca_erro", "")
    if erro_middleware:
        messages.error(request, erro_middleware)

    if request.method == "POST":
        acao = request.POST.get("acao")
        try:
            if acao == "ativar_online":
                activate_online(request.POST.get("license_key", ""))
            elif acao == "instalar_offline":
                install_offline_license(request.POST.get("license_token", ""))
            else:
                raise ValueError("Acao de licenca invalida.")
            messages.success(request, "Licenca ativada com sucesso.")
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect("home")
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(
        request,
        "catalogo/licenca.html",
        {
            "machine_id": machine_fingerprint(),
            "status": status,
            "next": next_url,
        },
    )


def login_operador(request):
    garantir_operadores_padrao()
    if sessao_possui_operador(request):
        return redirect("home")
    if request.method == "POST":
        nome = request.POST.get("usuario", "").strip()
        senha = request.POST.get("senha", "")
        operador = autenticar_operador(nome, senha, origem="gestor_web")
        if operador:
            iniciar_sessao_operador(request, operador)
            salvar_preferencias({"usuario": operador.nome}, request=request)
            return redirect(_destino_seguro(request, "home"))
        messages.error(request, "Usuario ou senha invalidos.")
    return render(
        request,
        "catalogo/login.html",
        {
            "titulo": "Mheibos Gestor",
            "subtitulo": "Acesse o sistema administrativo.",
            "usuarios": OperadorGestor.objects.filter(ativo=True).order_by("nome"),
            "next": request.GET.get("next", ""),
            "producao": False,
        },
    )


def login_producao(request):
    garantir_operadores_padrao()
    if sessao_possui_operador(request):
        return redirect("producao_home")
    if request.method == "POST":
        nome = request.POST.get("usuario", "").strip()
        senha = request.POST.get("senha", "")
        operador = autenticar_operador(nome, senha, origem="producao_web")
        if operador:
            iniciar_sessao_operador(request, operador)
            salvar_preferencias({"usuario": operador.nome}, request=request)
            return redirect(_destino_seguro(request, "producao_home"))
        messages.error(request, "Usuario ou senha invalidos.")
    return render(
        request,
        "catalogo/login.html",
        {
            "titulo": "Mheibos Producao",
            "subtitulo": "Acesse a fila de producao.",
            "usuarios": OperadorGestor.objects.filter(ativo=True).order_by("nome"),
            "next": request.GET.get("next", ""),
            "producao": True,
        },
    )


def login_vendas(request):
    garantir_operadores_padrao()
    if sessao_possui_operador(request):
        return redirect("vendas_home")
    if request.method == "POST":
        nome = request.POST.get("usuario", "").strip()
        senha = request.POST.get("senha", "")
        operador = autenticar_operador(nome, senha, origem="vendas_web")
        if operador:
            iniciar_sessao_operador(request, operador)
            salvar_preferencias({"usuario": operador.nome}, request=request)
            return redirect(_destino_seguro(request, "vendas_home"))
        messages.error(request, "Usuario ou senha invalidos.")
    return render(
        request,
        "catalogo/login.html",
        {
            "titulo": "Mheibos Vendas",
            "subtitulo": "Atendimento rapido para loja, balcao e WhatsApp.",
            "usuarios": OperadorGestor.objects.filter(ativo=True).order_by("nome"),
            "next": request.GET.get("next", ""),
            "producao": False,
            "vendas": True,
        },
    )


def logout_operador(request):
    request.session.flush()
    destino = request.GET.get("app")
    if destino == "producao":
        return redirect("producao_login")
    if destino == "vendas":
        return redirect("vendas_login")
    return redirect("login")


def primeiro_admin(request):
    if not primeiro_admin_pendente():
        return redirect("home")
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        senha = request.POST.get("senha", "")
        confirmar = request.POST.get("confirmar_senha", "")
        if not nome:
            messages.error(request, "Informe o nome do primeiro administrador.")
        elif len(senha) < 4:
            messages.error(request, "A senha precisa ter pelo menos 4 caracteres.")
        elif senha != confirmar:
            messages.error(request, "As senhas nao conferem.")
        else:
            operador = OperadorGestor(
                nome=nome,
                papel=PapelOperador.ADMIN_GERAL,
                ativo=True,
            )
            definir_senha_operador(operador, senha, salvar=False)
            operador.save()
            salvar_preferencias({"usuario": operador.nome}, request=request)
            messages.success(request, "Administrador geral criado. Faca login no launcher.")
            return redirect("home")
    return render(request, "catalogo/primeiro_admin.html")


def produtos(request):
    operador = operador_atual()
    categoria_form = CategoriaServicoForm(prefix="categoria")
    produto_form = ProdutoServicoForm(prefix="produto")

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "categoria":
            if not operador.pode_criar_categoria_servico:
                messages.error(request, "Seu perfil não tem permissão para criar categorias de serviço.")
                return redirect("produtos")
            categoria_form = CategoriaServicoForm(request.POST, prefix="categoria")
            if categoria_form.is_valid():
                categoria_form.save()
                messages.success(request, "Categoria criada.")
                return redirect("produtos")
        if acao == "produto":
            produto_form = ProdutoServicoForm(request.POST, prefix="produto")
            if produto_form.is_valid():
                produto_form.save()
                messages.success(request, "Produto criado.")
                return redirect("produtos")

    return render(
        request,
        "catalogo/produtos.html",
        {
            "active": "produtos",
            "categorias": CategoriaServico.objects.all(),
            "produtos": ProdutoServico.objects.select_related("categoria_servico").order_by("categoria_servico__ordem", "nome"),
            "categoria_form": categoria_form,
            "produto_form": produto_form,
            "pode_criar_categoria": operador.pode_criar_categoria_servico,
            "pode_excluir_categoria": operador.pode_excluir_categoria_servico,
            "pode_excluir_produto": operador.pode_excluir_produto,
        },
    )


def produto_editar(request, pk):
    operador = operador_atual()
    produto = get_object_or_404(ProdutoServico, pk=pk)
    categoria_form = CategoriaServicoForm(prefix="categoria")
    produto_form = ProdutoServicoForm(request.POST or None, instance=produto, prefix="produto")

    if request.method == "POST" and produto_form.is_valid():
        produto_form.save()
        messages.success(request, "Produto atualizado.")
        return redirect("produtos")

    return render(
        request,
        "catalogo/produtos.html",
        {
            "active": "produtos",
            "categorias": CategoriaServico.objects.all(),
            "produtos": ProdutoServico.objects.select_related("categoria_servico").order_by("categoria_servico__ordem", "nome"),
            "categoria_form": categoria_form,
            "produto_form": produto_form,
            "produto_editando": produto,
            "pode_criar_categoria": operador.pode_criar_categoria_servico,
            "pode_excluir_categoria": operador.pode_excluir_categoria_servico,
            "pode_excluir_produto": operador.pode_excluir_produto,
        },
    )


def produto_excluir(request, pk):
    operador = operador_atual()
    if not operador.pode_excluir_produto:
        messages.error(request, "Seu perfil não tem permissão para excluir produtos.")
        return redirect("produtos")
    produto = get_object_or_404(ProdutoServico, pk=pk)
    try:
        produto.delete()
        messages.success(request, "Produto excluído.")
    except Exception:
        produto.ativo = False
        produto.save(update_fields=["ativo"])
        messages.warning(request, "Produto vinculado a pedidos. Ele foi marcado como inativo.")
    return redirect("produtos")


def categoria_excluir(request, pk):
    operador = operador_atual()
    if not operador.pode_excluir_categoria_servico:
        messages.error(request, "Seu perfil não tem permissão para excluir categorias de serviço.")
        return redirect("produtos")
    categoria = get_object_or_404(CategoriaServico, pk=pk)
    try:
        categoria.delete()
        messages.success(request, "Categoria excluída.")
    except Exception:
        categoria.ativa = False
        categoria.save(update_fields=["ativa"])
        messages.warning(request, "Categoria vinculada a produtos/pedidos. Ela foi marcada como inativa.")
    return redirect("produtos")


def preparacao_arte(request):
    aguardando_arte = (
        Pedido.objects.filter(status=StatusPedido.AGUARDANDO_ARTE)
        .select_related("cliente")
        .prefetch_related("itens", "artes")
        .order_by("data_entrega", "id")[:120]
    )
    return render(
        request,
        "catalogo/preparacao_arte.html",
        {
            "active": "preparacao_arte",
            "aguardando_arte": aguardando_arte,
            "total_aguardando_arte": Pedido.objects.filter(
                status=StatusPedido.AGUARDANDO_ARTE
            ).count(),
        },
    )


def assistencia_envio(request):
    operador = operador_atual(request)
    busca = request.GET.get("q", "").strip()
    categorias_ids = request.GET.getlist("categorias")
    usuarios = request.GET.getlist("usuarios")
    grupos = pedidos_assistencia(busca, categorias_ids, usuarios)
    return render(
        request,
        "catalogo/assistencia_envio.html",
        {
            "active": "assistencia",
            "grupos": grupos,
            "busca": busca,
            "categorias": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
            "categorias_selecionadas": [str(item) for item in categorias_ids],
            "usuarios": OperadorGestor.objects.filter(ativo=True).order_by("nome"),
            "usuarios_selecionados": usuarios,
            "dias_uteis_restantes": dias_uteis_restantes,
            "pode_acoes_admin": operador.is_admin,
        },
    )


def assistencia_marcar_enviado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual(request)
    try:
        alterar_status_pedido(
            pedido=pedido,
            novo_status=StatusPedido.EM_PRODUCAO,
            operador=operador,
        )
    except ArteNecessariaParaProducao:
        messages.error(
            request,
            f"Pedido #{pedido.pk} continua aguardando arte. Adicione a referencia antes de prosseguir.",
        )
    except AlteracaoStatusNegada:
        messages.error(request, "Seu perfil nao pode alterar este Pedido.")
    else:
        messages.success(request, f"Pedido #{pedido.pk} enviado para producao.")
    return redirect("assistencia_envio")


def configuracoes(request):
    garantir_operadores_padrao()
    operador = operador_atual(request)
    perfil_empresa, _ = PerfilEmpresa.objects.get_or_create(chave="global")
    operador_editando = None
    operador_id_edicao = request.GET.get("operador_id")
    if operador.is_admin_geral and operador_id_edicao:
        operador_editando = OperadorGestor.objects.filter(pk=operador_id_edicao).first()
    operador_form = OperadorGestorForm(prefix="operador", instance=operador_editando)
    perfil_form = OperadorPerfilForm(prefix="perfil", instance=operador)
    senha_form = OperadorSenhaForm(prefix="senha")
    perfil_empresa_form = PerfilEmpresaForm(prefix="empresa", instance=perfil_empresa)
    categoria_usuario_form = CategoriaUsuarioForm(prefix="categoria_usuario")
    linha_cabecalho_cores = cores_linha_cabecalho_form(perfil_empresa.os_linha_cabecalho)

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "testar_banco":
            if not operador.pode_gerenciar_usuarios:
                messages.error(request, "Somente administradores podem testar a conexao com o banco.")
                return redirect("configuracoes")
            try:
                with connections["default"].cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
                messages.success(request, "Conexao com o banco local realizada com sucesso.")
            except Exception as exc:
                messages.error(request, f"Nao foi possivel conectar ao banco: {exc}")
            return redirect(f"{reverse('configuracoes')}?aba=banco")
        if acao == "salvar_perfil":
            nome_anterior = operador.nome
            perfil_form = OperadorPerfilForm(request.POST, request.FILES, prefix="perfil", instance=operador)
            senha_atual = (request.POST.get("senha_atual") or "").strip()
            if not senha_operador_valida(operador, senha_atual):
                messages.error(request, "Senha incorreta. Informe sua senha atual para salvar o perfil.")
            elif perfil_form.is_valid():
                perfil_form.save()
                if operador.nome != nome_anterior:
                    salvar_preferencias({"usuario": operador.nome}, request=request)
                messages.success(request, "Perfil salvo.")
                return redirect("configuracoes")
            else:
                messages.error(request, "Nao foi possivel salvar seu perfil. Confira os campos.")
        if acao == "trocar_senha":
            senha_form = OperadorSenhaForm(request.POST, prefix="senha")
            if senha_form.is_valid():
                dados = senha_form.cleaned_data
                if not senha_operador_valida(operador, dados["senha_atual"]):
                    senha_form.add_error("senha_atual", "Senha atual incorreta.")
                else:
                    definir_senha_operador(operador, dados["senha_nova"])
                    messages.success(request, "Senha alterada com sucesso.")
                    return redirect("configuracoes")
            if not senha_form.errors:
                messages.error(request, "Nao foi possivel alterar a senha. Confira os campos.")
        if acao == "salvar_operador":
            if not operador.is_admin_geral:
                messages.error(request, "Somente administradores gerais gerenciam usuarios.")
                return redirect("configuracoes")
                messages.error(request, "Somente administradores cadastram novos usuários.")
                return redirect("configuracoes")
            operador_id = request.POST.get("operador_id")
            senha_admin = (request.POST.get("senha_admin") or "").strip()
            if not senha_operador_valida(operador, senha_admin):
                messages.error(request, "Senha do administrador incorreta. Informe sua senha para salvar usuarios.")
                if operador_id:
                    return redirect(f"{reverse('configuracoes')}?aba=usuarios&operador_id={operador_id}")
                return redirect(f"{reverse('configuracoes')}?aba=usuarios")
            instance = OperadorGestor.objects.filter(pk=operador_id).first() if operador_id else None
            operador_form = OperadorGestorForm(request.POST, request.FILES, prefix="operador", instance=instance)
            if operador_form.is_valid():
                usuario = operador_form.save()
                messages.success(request, f"Usuário {usuario.nome} salvo.")
            else:
                messages.error(request, "Não foi possível salvar o usuário. Confira os campos.")
            return redirect("configuracoes")
        if acao == "salvar_categoria_usuario":
            if not operador.is_admin_geral:
                messages.error(request, "Somente administradores gerais configuram categorias de usuarios.")
                return redirect("configuracoes")
            categoria_usuario_form = CategoriaUsuarioForm(request.POST, prefix="categoria_usuario")
            if categoria_usuario_form.is_valid():
                categoria_usuario_form.save()
                messages.success(request, "Categoria de usuario salva.")
                return redirect(f"{reverse('configuracoes')}?aba=usuarios_config")
            messages.error(request, "Nao foi possivel salvar a categoria. Confira os campos.")
        if acao == "salvar_categorias_usuarios":
            if not operador.is_admin_geral:
                messages.error(request, "Somente administradores gerais configuram categorias de usuarios.")
                return redirect("configuracoes")
            atualizados = 0
            for usuario_id in request.POST.getlist("usuario_categoria_ids"):
                usuario = OperadorGestor.objects.filter(pk=usuario_id).first()
                if not usuario:
                    continue
                categoria_id = request.POST.get(f"usuario_categoria_{usuario.pk}") or ""
                usuario.categoria_usuario = CategoriaUsuario.objects.filter(pk=categoria_id, ativa=True).first() if categoria_id else None
                usuario.save(update_fields=["categoria_usuario", "atualizado_em"])
                atualizados += 1
            messages.success(request, f"Categorias atualizadas para {atualizados} usuario(s).")
            return redirect(f"{reverse('configuracoes')}?aba=usuarios_config")
        if acao == "excluir_operador":
            if not operador.is_admin_geral:
                messages.error(request, "Somente administradores gerais excluem usuarios.")
                return redirect("configuracoes")
            alvo = OperadorGestor.objects.filter(pk=request.POST.get("operador_id")).first()
            if not alvo:
                messages.error(request, "Usuario nao encontrado.")
                return redirect("configuracoes")
            if alvo.pk == operador.pk:
                messages.error(request, "Voce nao pode excluir o seu proprio usuario.")
                return redirect("configuracoes")
            if alvo.is_admin_geral and OperadorGestor.objects.filter(papel=PapelOperador.ADMIN_GERAL, ativo=True).count() <= 1:
                messages.error(request, "Mantenha pelo menos um administrador geral ativo.")
                return redirect("configuracoes")
            nome = alvo.nome
            foto = alvo.foto
            alvo.delete()
            if foto:
                foto.delete(save=False)
            messages.success(request, f"Usuario {nome} excluido.")
            return redirect("configuracoes")
        if acao == "salvar_empresa":
            if not operador.pode_gerenciar_usuarios:
                messages.error(request, "Somente administradores alteram o perfil da empresa.")
                return redirect("configuracoes")
            perfil_empresa_form = PerfilEmpresaForm(request.POST, request.FILES, prefix="empresa", instance=perfil_empresa)
            if perfil_empresa_form.is_valid():
                perfil_empresa_form.save()
                messages.success(request, "Perfil da empresa salvo.")
                return redirect(f"{reverse('configuracoes')}?aba=empresa")
            messages.error(request, "Nao foi possivel salvar o perfil da empresa. Confira os campos.")
        if acao == "salvar_ordem_servico":
            if not operador.pode_gerenciar_usuarios:
                messages.error(request, "Somente administradores alteram a ordem de servico.")
                return redirect("configuracoes")
            perfil_empresa.os_campos = salvar_campos_os(request.POST)
            layout = request.POST.get("os_layout")
            layouts_validos = {choice[0] for choice in PerfilEmpresa.LayoutOrdemServico.choices}
            if layout in layouts_validos:
                perfil_empresa.os_layout = layout
            for campo_cor in ("os_cor_linhas", "os_cor_textos", "os_cor_legendas"):
                valor = (request.POST.get(campo_cor) or "").strip()
                if len(valor) == 7 and valor.startswith("#"):
                    setattr(perfil_empresa, campo_cor, valor)
            perfil_empresa.os_linha_cabecalho = salvar_linha_cabecalho(request.POST)
            perfil_empresa.save(
                update_fields=[
                    "os_campos",
                    "os_layout",
                    "os_cor_linhas",
                    "os_cor_textos",
                    "os_cor_legendas",
                    "os_linha_cabecalho",
                    "atualizado_em",
                ]
            )
            messages.success(request, "Configuracoes da ordem de servico salvas.")
            return redirect("configuracoes")
        if acao == "salvar_alertas":
            if not operador.pode_gerenciar_usuarios:
                messages.error(request, "Somente administradores alteram alertas.")
                return redirect("configuracoes")
            for categoria in CategoriaServico.objects.all():
                prefixo = f"categoria_{categoria.pk}"
                categoria.alerta_prazo_ativo = request.POST.get(f"{prefixo}_ativo") == "on"
                try:
                    categoria.alerta_dias_uteis = max(0, int(request.POST.get(f"{prefixo}_dias") or 0))
                except ValueError:
                    categoria.alerta_dias_uteis = 2
                categoria.alerta_mesmo_dia_apos_14h = request.POST.get(f"{prefixo}_mesmo_dia") == "on"
                categoria.save(update_fields=["alerta_prazo_ativo", "alerta_dias_uteis", "alerta_mesmo_dia_apos_14h"])
            messages.success(request, "Regras de notificacoes e alertas salvas.")
            return redirect(f"{reverse('configuracoes')}?aba=widgets")
        if acao == "trocar_perfil_proprio":
            if not operador.is_admin_geral:
                messages.error(request, "Somente administradores gerais acessam outros usuarios.")
                return redirect("configuracoes")
            alvo_nome = request.POST.get("usuario_ativo", "").strip()
            alvo = OperadorGestor.objects.filter(nome=alvo_nome, ativo=True).first()
            if alvo:
                iniciar_sessao_operador(request, alvo)
                salvar_preferencias({"usuario": alvo.nome}, request=request)
                messages.success(request, f"Usuário ativo: {alvo.nome}.")
            return redirect("configuracoes")

    db = settings.DATABASES["default"]
    legacy_db = settings.DATABASES.get("legacy", {})
    todos_operadores_qs = OperadorGestor.objects.all() if operador.pode_gerenciar_usuarios else OperadorGestor.objects.filter(pk=operador.pk)
    operadores_ativos_qs = OperadorGestor.objects.filter(ativo=True) if operador.pode_gerenciar_usuarios else OperadorGestor.objects.filter(pk=operador.pk)
    categorias_usuario = CategoriaUsuario.objects.filter(ativa=True).order_by("ordem", "nome")
    contexto = {
        "active": "configuracoes",
        "categorias": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
        "operadores": operadores_ativos_qs,
        "todos_operadores": todos_operadores_qs,
        "categorias_usuario": categorias_usuario,
        "categoria_usuario_form": categoria_usuario_form,
        "operador_form": operador_form,
        "perfil_form": perfil_form,
        "senha_form": senha_form,
        "perfil_empresa_form": perfil_empresa_form,
        "perfil_empresa": perfil_empresa,
        "linha_cabecalho_cores": linha_cabecalho_cores,
        "linha_cabecalho_css": normalizar_linha_cabecalho(perfil_empresa.os_linha_cabecalho),
        "ordem_servico_campos": lista_campos_os(perfil_empresa.os_campos),
        "layouts_ordem_servico": PerfilEmpresa.LayoutOrdemServico.choices,
        "papeis_operador": PapelOperador.choices,
        "pode_gerenciar_usuarios": operador.pode_gerenciar_usuarios,
        "pode_gerenciar_usuarios_geral": operador.is_admin_geral,
        "operador_editando": operador_editando,
        "preferencias": carregar_preferencias(operador=operador, request=request),
        "db": db,
        "legacy_db": legacy_db,
        "zoom_opcoes": [85, 90, 95, 100, 110, 125, 150, 175],
        "intervalo_opcoes": [5, 10, 15, 30, 60],
        "visivel_opcoes": [30, 60, 120, 300],
    }
    return render(request, "catalogo/configuracoes.html", contexto)

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "criar_operador":
            nome = request.POST.get("nome_operador", "").strip()
            if nome:
                OperadorGestor.objects.get_or_create(nome=nome, defaults={"ativo": True})
                messages.success(request, f"Usuário {nome} criado.")
            else:
                messages.error(request, "Informe o nome do novo usuário.")
            return redirect("configuracoes")

    db = settings.DATABASES["default"]
    legacy_db = settings.DATABASES.get("legacy", {})
    contexto = {
        "active": "configuracoes",
        "categorias": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
        "operadores": OperadorGestor.objects.filter(ativo=True),
        "preferencias": carregar_preferencias(operador=operador, request=request),
        "db": db,
        "legacy_db": legacy_db,
        "zoom_opcoes": [85, 90, 95, 100, 110, 125, 150, 175],
        "intervalo_opcoes": [5, 10, 15, 30, 60],
        "visivel_opcoes": [30, 60, 120, 300],
    }
    return render(request, "catalogo/configuracoes.html", contexto)


def _salvar_regras_alerta(request):
    for categoria in CategoriaServico.objects.all():
        prefixo = f"categoria_{categoria.pk}"
        categoria.alerta_prazo_ativo = request.POST.get(f"{prefixo}_ativo") == "on"
        try:
            categoria.alerta_dias_uteis = max(0, int(request.POST.get(f"{prefixo}_dias") or 0))
        except ValueError:
            categoria.alerta_dias_uteis = 2
        categoria.alerta_mesmo_dia_apos_14h = request.POST.get(f"{prefixo}_mesmo_dia") == "on"
        categoria.save(update_fields=["alerta_prazo_ativo", "alerta_dias_uteis", "alerta_mesmo_dia_apos_14h"])


def producao_home(request):
    operador = operador_atual(request)
    status = request.GET.get("status", "").strip()
    prioridade = request.GET.get("prioridade", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    ordem = request.GET.get("ordem", "asc").strip()
    if ordem not in {"asc", "desc"}:
        ordem = "asc"

    itens_prefetch = Prefetch(
        "itens",
        queryset=PedidoItem.objects.select_related("produto__categoria_servico", "categoria_servico"),
    )
    mostrando_prontos = status == StatusPedido.PRONTO
    status_base = StatusPedido.PRONTO if mostrando_prontos else StatusPedido.EM_PRODUCAO
    pedidos = queryset_com_projecao(
        queryset_fila_producao(prontos=mostrando_prontos)
        .select_related("cliente")
        .prefetch_related(itens_prefetch, "artes")
    )
    if prioridade:
        pedidos = pedidos.filter(prioridade=prioridade)
    if categoria:
        pedidos = pedidos.filter(
            Q(itens__categoria_servico_id=categoria) | Q(itens__produto__categoria_servico_id=categoria)
        ).distinct()

    categorias = list(CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"))
    pedidos_lista = projetar_lista(
        preparar_categorias_pedidos(
            pedidos.order_by("data_entrega" if ordem == "asc" else "-data_entrega", "id")[:180]
        )
    )
    grupos_map = defaultdict(list)
    sem_categoria = []
    for pedido in pedidos_lista:
        pedido.alerta_prazo = pedido_em_alerta(pedido)
        categorias_pedido = sorted(categorias_do_pedido(pedido), key=lambda item: (item.ordem, item.nome))
        if not categorias_pedido:
            sem_categoria.append(pedido)
            continue
        for categoria_pedido in categorias_pedido:
            grupos_map[categoria_pedido.id].append(pedido)

    grupos = [
        {"categoria": categoria_item, "pedidos": grupos_map.get(categoria_item.id, [])}
        for categoria_item in categorias
        if grupos_map.get(categoria_item.id)
    ]
    if sem_categoria:
        grupos.append({"categoria": None, "pedidos": sem_categoria})

    contexto = {
        "active": "producao",
        "modo_producao": True,
        "grupos": grupos,
        "status_atual": status_base,
        "prioridade_atual": prioridade,
        "categoria_atual": categoria,
        "ordem": ordem,
        "ordem_inversa": "desc" if ordem == "asc" else "asc",
        "categorias_tabs": categorias,
        "prioridade_choices": PrioridadePedido.choices,
        "liberados": queryset_fila_producao().count(),
        "produzindo": queryset_fila_producao().count(),
        "prontos": queryset_fila_producao(prontos=True).count(),
        "urgentes": queryset_fila_producao().filter(prioridade=PrioridadePedido.URGENTE).count(),
        "pode_acoes_admin": operador.is_admin,
    }
    return render(request, "pedidos/producao.html", contexto)


def producao_configuracoes(request):
    operador = operador_atual(request)
    contexto = {
        "active": "producao_configuracoes",
        "modo_producao": True,
        "preferencias": carregar_preferencias(operador=operador, request=request),
        "db": settings.DATABASES["default"],
        "pode_ver_banco": bool(operador and operador.is_admin_geral),
        "zoom_opcoes": [85, 90, 95, 100, 110, 125, 150, 175],
        "intervalo_opcoes": [5, 10, 15, 30, 60],
        "visivel_opcoes": [30, 60, 120, 300],
        "posicao_opcoes": [
            ("inferior_centro", "Inferior centro"),
            ("inferior_direita", "Inferior direita"),
            ("inferior_esquerda", "Inferior esquerda"),
            ("superior_direita", "Superior direita"),
            ("superior_esquerda", "Superior esquerda"),
            ("centro", "Centro"),
        ],
        "operador": operador,
    }
    return render(request, "catalogo/producao_configuracoes.html", contexto)


def _categorias_da_requisicao(request):
    valor = request.GET.get("categorias", "")
    if not valor.strip():
        return None
    return [item.strip() for item in valor.split(",") if item.strip()]


def api_widget_prazos(request):
    pedidos = pedidos_para_widget(_categorias_da_requisicao(request))
    for pedido in pedidos:
        pedido["url"] = reverse("pedido_detail", args=[pedido["id"]])
    return JsonResponse({"pedidos": pedidos, "total": len(pedidos)})


def api_notificacao_assistencia(request):
    resumo = resumo_assistencia_envio(_categorias_da_requisicao(request))
    resumo["url"] = reverse("assistencia_envio")
    return JsonResponse(resumo)


@require_http_methods(["GET", "POST"])
def api_preferencias(request):
    if request.method == "GET":
        return JsonResponse(carregar_preferencias(request=request))
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    return JsonResponse(salvar_preferencias(payload, request=request))


def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return None


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_launcher_login(request):
    if request.method == "GET":
        garantir_operadores_padrao()
        usuarios = OperadorGestor.objects.filter(ativo=True).order_by("nome").values("nome", "papel")
        return JsonResponse({"usuarios": list(usuarios), "primeiro_admin_pendente": primeiro_admin_pendente()})

    payload = _json_body(request)
    if payload is None:
        return JsonResponse({"ok": False, "erro": "JSON invalido."}, status=400)
    nome = str(payload.get("usuario") or "").strip()
    senha = str(payload.get("senha") or "")
    operador = autenticar_operador(nome, senha, origem="launcher_api")
    if not operador:
        return JsonResponse({"ok": False, "erro": "Usuario ou senha invalidos."}, status=403)
    iniciar_sessao_operador(request, operador)
    salvar_preferencias({"usuario": operador.nome}, request=request)
    return JsonResponse(
        {
            "ok": True,
            "usuario": operador.nome,
            "papel": operador.papel,
            "pode_recuperar_senha": operador.is_admin,
        }
    )


@csrf_exempt
@require_http_methods(["POST"])
def api_launcher_trocar_senha(request):
    payload = _json_body(request)
    if payload is None:
        return JsonResponse({"ok": False, "erro": "JSON invalido."}, status=400)
    nome = str(payload.get("usuario") or "").strip()
    senha_atual = str(payload.get("senha_atual") or "")
    nova_senha = str(payload.get("nova_senha") or "")
    if len(nova_senha) < 4:
        return JsonResponse({"ok": False, "erro": "A nova senha precisa ter pelo menos 4 caracteres."}, status=400)
    operador = OperadorGestor.objects.filter(nome=nome, ativo=True).first()
    if not operador or not validar_senha_operador(operador, senha_atual):
        return JsonResponse({"ok": False, "erro": "Senha atual invalida."}, status=403)
    definir_senha_operador(operador, nova_senha)
    return JsonResponse({"ok": True})


@csrf_exempt
@require_http_methods(["POST"])
def api_launcher_recuperar_senha(request):
    payload = _json_body(request)
    if payload is None:
        return JsonResponse({"ok": False, "erro": "JSON invalido."}, status=400)
    alvo_nome = str(payload.get("usuario") or "").strip()
    chave = str(payload.get("chave") or "").strip().upper()
    nova_senha = str(payload.get("nova_senha") or "")
    if len(nova_senha) < 4:
        return JsonResponse({"ok": False, "erro": "A nova senha precisa ter pelo menos 4 caracteres."}, status=400)
    chave_hash = hashlib.sha256(chave.encode("utf-8")).hexdigest()
    chave_registro = ChaveRecuperacaoSenha.objects.filter(chave_hash=chave_hash, usada_em__isnull=True).first()
    if not chave_registro:
        return JsonResponse({"ok": False, "erro": "Chave de recuperacao invalida ou ja utilizada."}, status=403)
    alvo = OperadorGestor.objects.filter(nome=alvo_nome, ativo=True).first()
    if not alvo:
        return JsonResponse({"ok": False, "erro": "Usuario nao encontrado."}, status=404)
    definir_senha_operador(alvo, nova_senha)
    chave_registro.usada_em = timezone.now()
    chave_registro.save(update_fields=["usada_em"])
    return JsonResponse({"ok": True})

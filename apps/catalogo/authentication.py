from django.contrib.auth.hashers import check_password, identify_hasher, make_password
from django.utils.crypto import constant_time_compare

from apps.catalogo.models import OperadorGestor


SESSION_OPERATOR_ID = "operador_id"
SESSION_OPERATOR_NAME = "operador_nome"


def senha_esta_protegida(valor: str) -> bool:
    try:
        identify_hasher(valor)
    except ValueError:
        return False
    return True


def definir_senha_operador(operador: OperadorGestor, senha: str, *, salvar: bool = True) -> None:
    operador.senha = make_password(senha)
    if salvar:
        operador.save(update_fields=["senha", "atualizado_em"])


def validar_senha_operador(
    operador: OperadorGestor,
    senha: str,
    *,
    atualizar_legado: bool = True,
) -> bool:
    armazenada = operador.senha or ""
    if senha_esta_protegida(armazenada):
        return check_password(senha, armazenada)

    valida = constant_time_compare(senha or "", armazenada)
    if valida and atualizar_legado:
        definir_senha_operador(operador, senha)
    return valida


def autenticar_operador(nome: str, senha: str) -> OperadorGestor | None:
    operador = OperadorGestor.objects.filter(nome=nome.strip(), ativo=True).first()
    if operador and validar_senha_operador(operador, senha):
        return operador
    return None


def iniciar_sessao_operador(request, operador: OperadorGestor) -> None:
    request.session[SESSION_OPERATOR_ID] = operador.pk
    request.session[SESSION_OPERATOR_NAME] = operador.nome


def operador_da_sessao(request) -> OperadorGestor | None:
    operador_id = request.session.get(SESSION_OPERATOR_ID)
    if operador_id:
        operador = OperadorGestor.objects.filter(pk=operador_id, ativo=True).first()
        if operador:
            request.session[SESSION_OPERATOR_NAME] = operador.nome
            return operador

    nome = (request.session.get(SESSION_OPERATOR_NAME) or "").strip()
    if not nome:
        return None
    operador = OperadorGestor.objects.filter(nome__iexact=nome, ativo=True).first()
    if operador:
        iniciar_sessao_operador(request, operador)
    return operador


def sessao_possui_operador(request) -> bool:
    return bool(
        request.session.get(SESSION_OPERATOR_ID)
        or request.session.get(SESSION_OPERATOR_NAME)
    )

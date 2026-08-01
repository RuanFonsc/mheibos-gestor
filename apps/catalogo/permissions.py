from apps.catalogo.models import OperadorGestor, PapelOperador
from apps.catalogo.authentication import operador_da_sessao
from apps.catalogo.ui_prefs import carregar_preferencias


def operador_padrao():
    if not OperadorGestor.objects.exists():
        return None
    operador, _ = OperadorGestor.objects.get_or_create(
        nome="Usuario Temporario",
        defaults={"papel": PapelOperador.TEMPORARIO, "ativo": True},
    )
    return operador


def operador_atual(request=None):
    if request is not None:
        operador = operador_da_sessao(request)
        if operador:
            return operador
    nome = ""
    if not nome:
        nome = (carregar_preferencias().get("usuario") or "").strip()
    if nome:
        operador = OperadorGestor.objects.filter(nome__iexact=nome, ativo=True).first()
        if operador:
            return operador
    return operador_padrao()


def mesmo_operador(nome, operador):
    return (nome or "").strip().casefold() == (operador.nome or "").strip().casefold()


def pode_editar_pedido(pedido, operador):
    if operador.is_admin:
        return True
    if operador.papel == PapelOperador.TEMPORARIO:
        return False
    return mesmo_operador(pedido.usuario_cadastro, operador)

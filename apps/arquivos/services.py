import re
from pathlib import PureWindowsPath

from django.db import transaction

from apps.auditoria.services import registrar_evento

from .models import ArquivoOficialArte, OrigemArquivoOficial


class ArquivoOficialInvalido(Exception):
    pass


class TemaPedidoImutavel(Exception):
    pass


def normalizar_caminho_oficial(valor: str) -> tuple[str, str, str]:
    caminho = (valor or "").strip().replace("/", "\\")
    if "\x00" in caminho or len(caminho) > 1000:
        raise ArquivoOficialInvalido("O caminho do arquivo oficial e invalido ou excessivo.")
    if not caminho or not (caminho.startswith("\\\\") or re.match(r"^[A-Za-z]:\\", caminho)):
        raise ArquivoOficialInvalido("Informe um caminho absoluto do Windows para o arquivo oficial.")
    nome = PureWindowsPath(caminho).name
    if not nome or len(nome) > 255:
        raise ArquivoOficialInvalido("O caminho nao contem um nome de arquivo valido.")
    extensao = PureWindowsPath(nome).suffix.lower().lstrip(".")
    return caminho, nome, extensao


@transaction.atomic
def vincular_arquivo_oficial(*, pedido, caminho: str, operador) -> ArquivoOficialArte:
    caminho, nome, extensao = normalizar_caminho_oficial(caminho)
    existente = ArquivoOficialArte.objects.filter(
        pedido=pedido, caminho_oficial__iexact=caminho, estado_vinculo="ATIVO"
    ).first()
    if existente:
        return existente
    arquivo = ArquivoOficialArte.objects.create(
        pedido=pedido,
        caminho_oficial=caminho,
        nome_oficial=nome,
        extensao=extensao,
        origem=OrigemArquivoOficial.VINCULADO_MANUAL,
        criado_por=operador,
    )
    registrar_evento(
        tipo="ArquivoOficialArteVinculado",
        operador=operador,
        origem="gestor_web",
        alvo_tipo="ArquivoOficialArte",
        alvo_id=str(arquivo.pk),
        acao="vincular_arquivo_oficial",
        valores_anteriores={},
        valores_posteriores={
            "pedido_id": pedido.pk,
            "nome_oficial": nome,
            "caminho_oficial": caminho,
            "estado_integridade": arquivo.estado_integridade,
        },
        chave_idempotencia=f"arquivo-oficial-vincular:{arquivo.pk}",
    )
    return arquivo


def validar_alteracao_tema(*, pedido, novo_tema: str) -> None:
    if (pedido.tema or "").strip() == (novo_tema or "").strip():
        return
    if pedido.total_pago > 0 or pedido.arquivos_oficiais_arte.exists():
        raise TemaPedidoImutavel(
            "O tema nao pode ser alterado depois do primeiro pagamento ou vinculo de arte oficial."
        )

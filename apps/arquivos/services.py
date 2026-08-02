import os
import re
from pathlib import PureWindowsPath

from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento

from .models import ArquivoOficialArte, EstadoIntegridadeArquivo, OrigemArquivoOficial


class ArquivoOficialInvalido(Exception):
    pass


class TemaPedidoImutavel(Exception):
    pass


class AlertaArquivoInvalido(Exception):
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


@transaction.atomic
def verificar_arquivo_oficial(*, arquivo: ArquivoOficialArte, operador) -> ArquivoOficialArte:
    discrepancias = []
    tamanho = None
    try:
        dados = os.stat(arquivo.caminho_oficial)
    except (FileNotFoundError, NotADirectoryError):
        discrepancias.append({"codigo": "ARQUIVO_NAO_ENCONTRADO", "mensagem": "O arquivo nao foi encontrado no caminho oficial."})
    except OSError as exc:
        discrepancias.append({"codigo": "CAMINHO_INACESSIVEL", "mensagem": "O caminho oficial nao pode ser acessado.", "detalhe": str(exc)})
    else:
        tamanho = dados.st_size
        if os.path.basename(arquivo.caminho_oficial).casefold() != arquivo.nome_oficial.casefold():
            discrepancias.append({"codigo": "NOME_DIVERGENTE", "mensagem": "O nome encontrado diverge da identidade oficial."})

    estado_anterior = arquivo.estado_integridade
    arquivo.estado_integridade = EstadoIntegridadeArquivo.ALERTA if discrepancias else EstadoIntegridadeArquivo.INTEGRO
    arquivo.discrepancias = discrepancias
    arquivo.tamanho_bytes = tamanho
    arquivo.verificado_em = timezone.now()
    arquivo.alerta_reconhecido_em = None
    arquivo.alerta_reconhecido_por = None
    arquivo.save(update_fields=["estado_integridade", "discrepancias", "tamanho_bytes", "verificado_em", "alerta_reconhecido_em", "alerta_reconhecido_por", "atualizado_em"])
    registrar_evento(
        tipo="ArquivoOficialArteVerificado", operador=operador, origem="gestor_web",
        alvo_tipo="ArquivoOficialArte", alvo_id=str(arquivo.pk), acao="verificar_integridade_arquivo",
        valores_anteriores={"estado_integridade": estado_anterior},
        valores_posteriores={"estado_integridade": arquivo.estado_integridade, "discrepancias": discrepancias, "tamanho_bytes": tamanho},
    )
    return arquivo


@transaction.atomic
def reconhecer_alerta_arquivo(*, arquivo: ArquivoOficialArte, operador) -> ArquivoOficialArte:
    verificacao = arquivo.verificado_em
    if (
        arquivo.estado_integridade != EstadoIntegridadeArquivo.ALERTA
        or not arquivo.discrepancias
        or verificacao is None
    ):
        raise AlertaArquivoInvalido("Nao existe alerta de arquivo pendente para reconhecer.")
    if arquivo.alerta_reconhecido_em:
        return arquivo
    arquivo.alerta_reconhecido_em = timezone.now()
    arquivo.alerta_reconhecido_por = operador
    arquivo.save(update_fields=["alerta_reconhecido_em", "alerta_reconhecido_por", "atualizado_em"])
    registrar_evento(
        tipo="AlertaArquivoOficialReconhecido", operador=operador, origem="gestor_web",
        alvo_tipo="ArquivoOficialArte", alvo_id=str(arquivo.pk), acao="eu_entendi_alerta_arquivo",
        valores_anteriores={"alerta_reconhecido": False},
        valores_posteriores={"alerta_reconhecido": True, "discrepancias": arquivo.discrepancias},
        chave_idempotencia=f"arquivo-alerta-reconhecer:{arquivo.pk}:{verificacao.isoformat()}",
    )
    return arquivo

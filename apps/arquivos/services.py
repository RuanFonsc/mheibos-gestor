import os
import re
from pathlib import Path
from pathlib import PureWindowsPath

from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento

from .metadados import extrair_metadados_graficos
from .models import (
    ArquivoOficialArte,
    EstadoIntegridadeArquivo,
    EstadoVinculoArquivo,
    OrigemArquivoOficial,
)

from apps.catalogo.models import PerfilEmpresa
from apps.catalogo.ui_prefs import PROGRAMAS_ARTE


MESES_PT_BR = (
    "", "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
)


class ArquivoOficialInvalido(Exception):
    pass


class TemaPedidoImutavel(Exception):
    pass


class AlertaArquivoInvalido(Exception):
    pass


class EncerramentoArquivoInvalido(Exception):
    pass


def _componente_seguro(valor: str, *, padrao: str) -> str:
    limpo = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", str(valor or ""))
    limpo = re.sub(r"\s+", " ", limpo).strip(" .")
    return (limpo or padrao)[:80]


def _proximo_caminho_oficial(*, pasta: Path, base: str, extensao: str) -> Path:
    candidato = pasta / f"{base}.{extensao}"
    indice = 2
    while candidato.exists():
        candidato = pasta / f"{base} - {indice:02d}.{extensao}"
        indice += 1
    return candidato


@transaction.atomic
def criar_arquivo_oficial(*, pedido, programa: str, operador) -> ArquivoOficialArte:
    if programa not in PROGRAMAS_ARTE:
        raise ArquivoOficialInvalido("Selecione um programa ou formato oficial valido.")
    perfil_empresa, _ = PerfilEmpresa.objects.get_or_create(chave="global")
    raiz = (perfil_empresa.diretorio_artes_raiz or "").strip()
    if not raiz:
        raise ArquivoOficialInvalido(
            "Configure a pasta compartilhada de artes em Perfil da Empresa antes de criar o arquivo."
        )
    agora = timezone.localtime()
    pasta = (
        Path(raiz)
        / _componente_seguro(operador.nome, padrao="Usuario")
        / str(agora.year)
        / MESES_PT_BR[agora.month]
        / f"{agora.day:02d}"
    )
    nome_programa, extensao = PROGRAMAS_ARTE[programa]
    numero = pedido.legado_id or pedido.pk
    base = " - ".join(
        (
            f"#{numero}",
            _componente_seguro(pedido.cliente.nome, padrao="Cliente"),
            _componente_seguro(pedido.tema, padrao="Sem tema"),
        )
    )
    try:
        pasta.mkdir(parents=True, exist_ok=True)
        caminho = _proximo_caminho_oficial(pasta=pasta, base=base, extensao=extensao)
        with caminho.open("xb"):
            pass
    except OSError as exc:
        raise ArquivoOficialInvalido(
            "Nao foi possivel criar o arquivo na pasta compartilhada. Verifique acesso e conexao."
        ) from exc
    try:
        arquivo = ArquivoOficialArte.objects.create(
            pedido=pedido,
            caminho_oficial=str(caminho),
            nome_oficial=caminho.name,
            extensao=extensao,
            origem=OrigemArquivoOficial.CRIADO_MHEIBOS,
            criado_por=operador,
            propriedades_tecnicas={"programa": programa, "programa_nome": nome_programa},
        )
        registrar_evento(
            tipo="ArquivoOficialArteCriado",
            operador=operador,
            origem="gestor_web",
            alvo_tipo="ArquivoOficialArte",
            alvo_id=str(arquivo.pk),
            acao="criar_arquivo_oficial",
            valores_anteriores={},
            valores_posteriores={
                "pedido_id": pedido.pk,
                "nome_oficial": arquivo.nome_oficial,
                "caminho_oficial": arquivo.caminho_oficial,
                "programa": programa,
                "arquivo_vazio": True,
            },
            chave_idempotencia=f"arquivo-oficial-criar:{arquivo.pk}",
        )
    except Exception:
        caminho.unlink(missing_ok=True)
        raise
    return arquivo


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
    largura_px = arquivo.largura_px
    altura_px = arquivo.altura_px
    resolucao_dpi = arquivo.resolucao_dpi
    propriedades_tecnicas = dict(arquivo.propriedades_tecnicas or {})
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
        leitura = extrair_metadados_graficos(
            arquivo.caminho_oficial,
            arquivo.extensao,
        )
        propriedades_tecnicas["leitura_raster"] = leitura.propriedades
        if leitura.aplicavel and leitura.discrepancia is None:
            largura_px = leitura.largura_px
            altura_px = leitura.altura_px
            resolucao_dpi = leitura.resolucao_dpi
        if leitura.discrepancia:
            discrepancias.append(leitura.discrepancia)

    estado_anterior = arquivo.estado_integridade
    arquivo.estado_integridade = EstadoIntegridadeArquivo.ALERTA if discrepancias else EstadoIntegridadeArquivo.INTEGRO
    arquivo.discrepancias = discrepancias
    arquivo.tamanho_bytes = tamanho
    arquivo.largura_px = largura_px
    arquivo.altura_px = altura_px
    arquivo.resolucao_dpi = resolucao_dpi
    arquivo.propriedades_tecnicas = propriedades_tecnicas
    arquivo.verificado_em = timezone.now()
    arquivo.alerta_reconhecido_em = None
    arquivo.alerta_reconhecido_por = None
    arquivo.save(update_fields=["estado_integridade", "discrepancias", "tamanho_bytes", "largura_px", "altura_px", "resolucao_dpi", "propriedades_tecnicas", "verificado_em", "alerta_reconhecido_em", "alerta_reconhecido_por", "atualizado_em"])
    registrar_evento(
        tipo="ArquivoOficialArteVerificado", operador=operador, origem="gestor_web",
        alvo_tipo="ArquivoOficialArte", alvo_id=str(arquivo.pk), acao="verificar_integridade_arquivo",
        valores_anteriores={"estado_integridade": estado_anterior},
        valores_posteriores={"estado_integridade": arquivo.estado_integridade, "discrepancias": discrepancias, "tamanho_bytes": tamanho, "largura_px": largura_px, "altura_px": altura_px, "resolucao_dpi": str(resolucao_dpi) if resolucao_dpi else None, "propriedades_tecnicas": propriedades_tecnicas},
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


@transaction.atomic
def encerrar_vinculo_arquivo_oficial(
    *,
    arquivo: ArquivoOficialArte,
    operador,
    observacao: str = "",
    backup_previo_confirmado: bool = False,
) -> ArquivoOficialArte:
    if not operador.is_admin:
        raise EncerramentoArquivoInvalido(
            "Somente administradores podem encerrar vinculos de arquivos oficiais."
        )
    arquivo = ArquivoOficialArte.objects.select_for_update().get(pk=arquivo.pk)
    if arquivo.estado_vinculo == EstadoVinculoArquivo.ENCERRADO:
        return arquivo
    arquivo.estado_vinculo = EstadoVinculoArquivo.ENCERRADO
    arquivo.encerrado_em = timezone.now()
    arquivo.encerrado_por = operador
    arquivo.encerramento_observacao = (observacao or "").strip()
    arquivo.backup_previo_confirmado = bool(backup_previo_confirmado)
    arquivo.save(
        update_fields=[
            "estado_vinculo",
            "encerrado_em",
            "encerrado_por",
            "encerramento_observacao",
            "backup_previo_confirmado",
            "atualizado_em",
        ]
    )
    registrar_evento(
        tipo="VinculoArquivoOficialEncerrado",
        operador=operador,
        origem="gestor_web",
        alvo_tipo="ArquivoOficialArte",
        alvo_id=str(arquivo.pk),
        acao="encerrar_vinculo_arquivo_oficial",
        valores_anteriores={"estado_vinculo": EstadoVinculoArquivo.ATIVO},
        valores_posteriores={
            "estado_vinculo": EstadoVinculoArquivo.ENCERRADO,
            "pedido_id": arquivo.pedido_id,
            "nome_oficial": arquivo.nome_oficial,
            "caminho_oficial": arquivo.caminho_oficial,
            "arquivo_fisico_alterado": False,
            "metadados_preservados": True,
            "backup_previo_confirmado": arquivo.backup_previo_confirmado,
            "observacao": arquivo.encerramento_observacao,
        },
        chave_idempotencia=f"arquivo-oficial-encerrar:{arquivo.pk}",
    )
    return arquivo

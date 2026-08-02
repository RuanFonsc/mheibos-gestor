import os
import re
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from pathlib import PureWindowsPath

from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento

from .metadados import extrair_metadados_graficos
from .models import (
    ArquivoOficialArte,
    EstadoIntegridadeArquivo,
    EstadoPreparacaoArte,
    EstadoVinculoArquivo,
    OrigemArquivoOficial,
    PreparacaoArtePedido,
)

from apps.catalogo.models import PerfilEmpresa
from apps.catalogo.assistencia import pedido_em_alerta
from apps.catalogo.authentication import validar_senha_operador
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


class PreparacaoArteInvalida(Exception):
    pass


class AcaoInatividadeArteInvalida(Exception):
    pass


@dataclass(frozen=True)
class AlertaInatividadeArte:
    ativo: bool
    numero: int = 0
    prazo_critico: bool = False
    pode_adiar_amanha: bool = False
    responsavel_nome: str = ""


def avaliar_alerta_inatividade_arte(*, pedido, agora=None) -> AlertaInatividadeArte:
    agora = agora or timezone.now()
    preparacao = PreparacaoArtePedido.objects.select_related("responsavel").filter(
        pedido=pedido
    ).first()
    if preparacao is None or preparacao.estado == EstadoPreparacaoArte.CONCLUIDA:
        return AlertaInatividadeArte(ativo=False)
    if not ArquivoOficialArte.objects.filter(
        pedido=pedido, estado_vinculo=EstadoVinculoArquivo.ATIVO
    ).exists():
        return AlertaInatividadeArte(ativo=False)
    hoje = timezone.localtime(agora).date()
    if preparacao.adiado_para_data and hoje < preparacao.adiado_para_data:
        return AlertaInatividadeArte(ativo=False)
    referencia = (
        preparacao.proximo_alerta_em
        or preparacao.ultima_atividade_em
        or preparacao.iniciado_em
        or preparacao.criado_em
    )
    if preparacao.proximo_alerta_em is None:
        referencia += timedelta(hours=2)
    if agora < referencia:
        return AlertaInatividadeArte(ativo=False)
    prazo_critico = bool(
        pedido.data_entrega
        and pedido_em_alerta(pedido, timezone.localtime(agora))
    )
    numero = preparacao.alertas_inatividade_respondidos + 1
    return AlertaInatividadeArte(
        ativo=True,
        numero=numero,
        prazo_critico=prazo_critico,
        pode_adiar_amanha=numero <= 2 and not prazo_critico,
        responsavel_nome=preparacao.responsavel.nome if preparacao.responsavel else "",
    )


@transaction.atomic
def responder_alerta_inatividade_arte(
    *, pedido, operador, acao: str, senha: str = "", agora=None
) -> PreparacaoArtePedido:
    agora = agora or timezone.now()
    preparacao = PreparacaoArtePedido.objects.select_for_update().select_related(
        "responsavel"
    ).get(pedido=pedido)
    alerta = avaliar_alerta_inatividade_arte(pedido=pedido, agora=agora)
    if not alerta.ativo:
        raise AcaoInatividadeArteInvalida("O alerta de inatividade nao esta ativo.")
    if preparacao.responsavel_id and preparacao.responsavel_id != operador.pk:
        raise AcaoInatividadeArteInvalida(
            "Somente o responsavel atual pode responder ao alerta de inatividade."
        )
    acoes = {"AINDA_TRABALHANDO", "LEMBRAR_DEPOIS", "ADIAR_AMANHA", "AJUDA_URGENTE"}
    if acao not in acoes:
        raise AcaoInatividadeArteInvalida("Selecione uma resposta valida.")
    if acao == "ADIAR_AMANHA":
        if not alerta.pode_adiar_amanha:
            raise AcaoInatividadeArteInvalida(
                "A arte nao pode ser adiada neste alerta ou dentro do prazo critico."
            )
        responsavel = preparacao.responsavel or operador
        if not validar_senha_operador(responsavel, senha):
            raise AcaoInatividadeArteInvalida("A senha do responsavel e invalida.")
        preparacao.adiado_para_data = timezone.localtime(agora).date() + timedelta(days=1)
        preparacao.proximo_alerta_em = None
    elif acao == "AJUDA_URGENTE":
        if not alerta.prazo_critico:
            raise AcaoInatividadeArteInvalida(
                "Ajuda urgente e oferecida quando o Pedido esta no prazo critico."
            )
        preparacao.ajuda_urgente_solicitada_em = agora
        preparacao.proximo_alerta_em = agora + timedelta(minutes=30)
    else:
        minutos = 120 if acao == "AINDA_TRABALHANDO" else 30
        preparacao.proximo_alerta_em = agora + timedelta(minutes=minutos)
        preparacao.adiado_para_data = None
    preparacao.alertas_inatividade_respondidos += 1
    preparacao.save(
        update_fields=[
            "proximo_alerta_em",
            "adiado_para_data",
            "alertas_inatividade_respondidos",
            "ajuda_urgente_solicitada_em",
            "atualizado_em",
        ]
    )
    registrar_evento(
        tipo="AlertaInatividadeArteRespondido",
        operador=operador,
        origem="gestor_web",
        alvo_tipo="PreparacaoArtePedido",
        alvo_id=str(preparacao.pk),
        acao="responder_alerta_inatividade_arte",
        valores_anteriores={"numero_alerta": alerta.numero},
        valores_posteriores={
            "resposta": acao,
            "prazo_critico": alerta.prazo_critico,
            "proximo_alerta_em": (
                preparacao.proximo_alerta_em.isoformat()
                if preparacao.proximo_alerta_em
                else None
            ),
            "adiado_para_data": (
                preparacao.adiado_para_data.isoformat()
                if preparacao.adiado_para_data
                else None
            ),
        },
        chave_idempotencia=(
            f"arte-inatividade:{preparacao.pk}:{alerta.numero}:{acao}"
        ),
    )
    return preparacao


def obter_preparacao_arte(*, pedido, operador=None) -> PreparacaoArtePedido:
    preparacao, criada = PreparacaoArtePedido.objects.get_or_create(
        pedido=pedido,
        defaults={"responsavel": operador},
    )
    if not criada and operador and preparacao.responsavel_id is None:
        preparacao.responsavel = operador
        preparacao.save(update_fields=["responsavel", "atualizado_em"])
    return preparacao


def _iniciar_monitoramento_inatividade(
    preparacao: PreparacaoArtePedido, *, agora=None
) -> None:
    agora = agora or timezone.now()
    preparacao.iniciado_em = preparacao.iniciado_em or agora
    preparacao.ultima_atividade_em = agora
    preparacao.proximo_alerta_em = agora + timedelta(hours=2)
    preparacao.adiado_para_data = None
    preparacao.save(
        update_fields=[
            "iniciado_em",
            "ultima_atividade_em",
            "proximo_alerta_em",
            "adiado_para_data",
            "atualizado_em",
        ]
    )


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
    preparacao = obter_preparacao_arte(pedido=pedido, operador=operador)
    if preparacao.estado == EstadoPreparacaoArte.CONCLUIDA:
        raise PreparacaoArteInvalida(
            "A arte do Pedido esta concluida. Reabra a preparacao antes de criar outro arquivo oficial."
        )
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
        _iniciar_monitoramento_inatividade(preparacao)
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
    preparacao = obter_preparacao_arte(pedido=pedido, operador=operador)
    if preparacao.estado == EstadoPreparacaoArte.CONCLUIDA:
        raise PreparacaoArteInvalida(
            "A arte do Pedido esta concluida. Novos arquivos oficiais nao podem ser vinculados."
        )
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
    _iniciar_monitoramento_inatividade(preparacao)
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
    modificado_em_ns = None
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
        modificado_em_ns = getattr(
            dados,
            "st_mtime_ns",
            int(getattr(dados, "st_mtime", 0) * 1_000_000_000),
        )
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
    tamanho_anterior = arquivo.tamanho_bytes
    modificado_anterior = arquivo.modificado_em_ns
    mudanca_conteudo = (
        modificado_anterior is not None
        and (modificado_anterior != modificado_em_ns or tamanho_anterior != tamanho)
    )
    preparacao = obter_preparacao_arte(pedido=arquivo.pedido, operador=operador)
    if tamanho and preparacao.estado == EstadoPreparacaoArte.NAO_INICIADA:
        preparacao.estado = EstadoPreparacaoArte.EM_PREPARACAO
        preparacao.iniciado_em = preparacao.iniciado_em or timezone.now()
    if mudanca_conteudo:
        atividade_em = timezone.now()
        preparacao.ultima_atividade_em = atividade_em
        preparacao.proximo_alerta_em = atividade_em + timedelta(hours=2)
        preparacao.adiado_para_data = None
        arquivo.ultima_modificacao_por = operador
        arquivo.modificacao_detectada_em = atividade_em
        if preparacao.estado == EstadoPreparacaoArte.CONCLUIDA:
            arquivo.alteracao_pos_conclusao_pendente = True
    preparacao.save(
        update_fields=[
            "estado",
            "iniciado_em",
            "ultima_atividade_em",
            "proximo_alerta_em",
            "adiado_para_data",
            "atualizado_em",
        ]
    )
    arquivo.estado_integridade = EstadoIntegridadeArquivo.ALERTA if discrepancias else EstadoIntegridadeArquivo.INTEGRO
    arquivo.discrepancias = discrepancias
    arquivo.tamanho_bytes = tamanho
    arquivo.modificado_em_ns = modificado_em_ns
    arquivo.largura_px = largura_px
    arquivo.altura_px = altura_px
    arquivo.resolucao_dpi = resolucao_dpi
    arquivo.propriedades_tecnicas = propriedades_tecnicas
    arquivo.verificado_em = timezone.now()
    arquivo.alerta_reconhecido_em = None
    arquivo.alerta_reconhecido_por = None
    arquivo.save(update_fields=["estado_integridade", "discrepancias", "tamanho_bytes", "modificado_em_ns", "modificacao_detectada_em", "alteracao_pos_conclusao_pendente", "ultima_modificacao_por", "largura_px", "altura_px", "resolucao_dpi", "propriedades_tecnicas", "verificado_em", "alerta_reconhecido_em", "alerta_reconhecido_por", "atualizado_em"])
    registrar_evento(
        tipo="ArquivoOficialArteVerificado", operador=operador, origem="gestor_web",
        alvo_tipo="ArquivoOficialArte", alvo_id=str(arquivo.pk), acao="verificar_integridade_arquivo",
        valores_anteriores={"estado_integridade": estado_anterior},
        valores_posteriores={"estado_integridade": arquivo.estado_integridade, "discrepancias": discrepancias, "tamanho_bytes": tamanho, "modificacao_conteudo": mudanca_conteudo, "alteracao_pos_conclusao_pendente": arquivo.alteracao_pos_conclusao_pendente, "largura_px": largura_px, "altura_px": altura_px, "resolucao_dpi": str(resolucao_dpi) if resolucao_dpi else None, "propriedades_tecnicas": propriedades_tecnicas},
    )
    return arquivo


@transaction.atomic
def concluir_arte_pedido(*, pedido, operador) -> PreparacaoArtePedido:
    arquivos = list(
        ArquivoOficialArte.objects.filter(
            pedido=pedido, estado_vinculo=EstadoVinculoArquivo.ATIVO
        )
    )
    if not arquivos:
        raise PreparacaoArteInvalida("Crie ou vincule pelo menos um arquivo oficial antes de concluir a arte.")
    for arquivo in arquivos:
        if not os.path.isfile(arquivo.caminho_oficial):
            raise PreparacaoArteInvalida(
                f"O arquivo oficial {arquivo.nome_oficial} nao esta acessivel."
            )
        if os.path.basename(arquivo.caminho_oficial).casefold() != arquivo.nome_oficial.casefold():
            raise PreparacaoArteInvalida(
                f"O arquivo oficial {arquivo.nome_oficial} apresenta nome divergente."
            )
        if arquivo.alteracao_pos_conclusao_pendente:
            raise PreparacaoArteInvalida(
                "Resolva as modificacoes posteriores antes de confirmar a conclusao."
            )
        dados = os.stat(arquivo.caminho_oficial)
        arquivo.tamanho_bytes = dados.st_size
        arquivo.modificado_em_ns = getattr(
            dados,
            "st_mtime_ns",
            int(getattr(dados, "st_mtime", 0) * 1_000_000_000),
        )
        arquivo.save(
            update_fields=["tamanho_bytes", "modificado_em_ns", "atualizado_em"]
        )
    preparacao = PreparacaoArtePedido.objects.select_for_update().filter(pedido=pedido).first()
    if preparacao is None:
        preparacao = PreparacaoArtePedido.objects.create(pedido=pedido, responsavel=operador)
    if preparacao.estado == EstadoPreparacaoArte.CONCLUIDA:
        return preparacao
    estado_anterior = preparacao.estado
    preparacao.estado = EstadoPreparacaoArte.CONCLUIDA
    preparacao.concluido_em = timezone.now()
    preparacao.concluido_por = operador
    preparacao.responsavel = preparacao.responsavel or operador
    preparacao.proximo_alerta_em = None
    preparacao.adiado_para_data = None
    preparacao.save(update_fields=["estado", "concluido_em", "concluido_por", "responsavel", "proximo_alerta_em", "adiado_para_data", "atualizado_em"])
    registrar_evento(
        tipo="ArtePedidoConcluida", operador=operador, origem="gestor_web",
        alvo_tipo="PreparacaoArtePedido", alvo_id=str(preparacao.pk), acao="concluir_arte_pedido",
        valores_anteriores={"estado": estado_anterior},
        valores_posteriores={"estado": preparacao.estado, "pedido_id": pedido.pk, "arquivos_oficiais": len(arquivos)},
        chave_idempotencia=f"arte-pedido-concluir:{preparacao.pk}:{preparacao.concluido_em.isoformat()}",
    )
    return preparacao


@transaction.atomic
def decidir_alteracao_pos_conclusao(*, arquivo: ArquivoOficialArte, operador, manter_concluida: bool) -> PreparacaoArtePedido:
    arquivo = ArquivoOficialArte.objects.select_for_update().get(pk=arquivo.pk)
    if not arquivo.alteracao_pos_conclusao_pendente:
        raise PreparacaoArteInvalida("Nao existe modificacao posterior pendente para este arquivo.")
    preparacao = PreparacaoArtePedido.objects.select_for_update().get(pedido=arquivo.pedido)
    estado_anterior = preparacao.estado
    arquivo.alteracao_pos_conclusao_pendente = False
    arquivo.save(update_fields=["alteracao_pos_conclusao_pendente", "atualizado_em"])
    if not manter_concluida:
        preparacao.estado = EstadoPreparacaoArte.EM_PREPARACAO
        preparacao.concluido_em = None
        preparacao.concluido_por = None
        preparacao.ultima_atividade_em = timezone.now()
        preparacao.save(update_fields=["estado", "concluido_em", "concluido_por", "ultima_atividade_em", "atualizado_em"])
    registrar_evento(
        tipo="AlteracaoArteConcluidaConfirmada", operador=operador, origem="gestor_web",
        alvo_tipo="ArquivoOficialArte", alvo_id=str(arquivo.pk), acao="decidir_alteracao_pos_conclusao",
        valores_anteriores={"estado_arte": estado_anterior, "pendente": True},
        valores_posteriores={"estado_arte": preparacao.estado, "pendente": False, "manter_concluida": manter_concluida},
    )
    return preparacao


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

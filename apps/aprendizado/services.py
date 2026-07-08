import re
import json
import unicodedata
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from apps.aprendizado.models import (
    AmostraTreinamento,
    ConversaAprendizado,
    DirecaoMensagem,
    MensagemAprendizado,
    OrigemConversa,
    TipoAmostraTreinamento,
)

EXPORT_DIR = Path(settings.BASE_DIR) / "exports" / "aprendizado"
EXPORT_CONVERSAS_FILE = EXPORT_DIR / "conversas_uteis.json"
EXPORT_INDIVIDUAL_DIR = EXPORT_DIR / "conversas"


RECLAMACAO_TERMOS = (
    "reclam",
    "problema",
    "atras",
    "demor",
    "errado",
    "erro",
    "defeito",
    "nao gostei",
    "não gostei",
    "cancelar",
    "devol",
)

LEAD_TERMOS = (
    "orcamento",
    "orçamento",
    "quanto fica",
    "valor",
    "preco",
    "preço",
    "fazer",
    "pedido",
    "quero",
    "preciso",
    "tem como",
)

PEDIDO_TERMOS = (
    "unidade",
    "unidades",
    "quantidade",
    "arte",
    "tema",
    "medida",
    "tamanho",
    "entrega",
    "prazo",
    "nome",
)


def telefone_de_jid(jid):
    texto = str(jid or "")
    numero = texto.split("@", 1)[0]
    return re.sub(r"\D+", "", numero)[:32]


def texto_da_mensagem(data):
    message = data.get("message") or {}
    if isinstance(message.get("conversation"), str):
        return message["conversation"]
    extended = message.get("extendedTextMessage") or {}
    if isinstance(extended.get("text"), str):
        return extended["text"]
    image = message.get("imageMessage") or {}
    if isinstance(image.get("caption"), str):
        return image["caption"]
    document = message.get("documentMessage") or {}
    if isinstance(document.get("caption"), str):
        return document["caption"]
    return ""


def enviada_em(data):
    raw = data.get("messageTimestamp")
    try:
        return datetime.fromtimestamp(int(raw), tz=timezone.get_current_timezone())
    except (TypeError, ValueError, OSError):
        return timezone.now()


def _contem(texto, termos):
    base = _normalizar_busca(texto)
    return any(_normalizar_busca(termo) in base for termo in termos)


def _normalizar_busca(texto):
    sem_acento = unicodedata.normalize("NFKD", str(texto or ""))
    return "".join(char for char in sem_acento if not unicodedata.combining(char)).casefold()


def _conteudo_treinamento(conversa):
    mensagens = list(conversa.mensagens.order_by("enviada_em").values("direcao", "texto", "tipo", "enviada_em"))
    return {
        "origem": conversa.origem,
        "instancia": conversa.instancia,
        "contato": {
            "nome": conversa.nome_contato,
            "telefone": conversa.telefone,
        },
        "sinais": {
            "lead": conversa.tem_lead,
            "reclamacao": conversa.tem_reclamacao,
            "pedido": conversa.tem_sinal_pedido,
        },
        "mensagens": [
            {
                "direcao": item["direcao"],
                "tipo": item["tipo"],
                "texto": item["texto"],
                "enviada_em": item["enviada_em"].isoformat() if item["enviada_em"] else "",
            }
            for item in mensagens
            if item["texto"]
        ],
    }


def _amostra_payload(amostra):
    return {
        "id": amostra.pk,
        "conversa_id": amostra.conversa_id,
        "tipo": amostra.tipo,
        "qualidade": amostra.qualidade,
        "pronta": amostra.pronta,
        "conteudo": amostra.conteudo,
        "atualizada_em": amostra.atualizada_em.isoformat() if amostra.atualizada_em else "",
    }


def exportar_conversas_uteis_json():
    EXPORT_INDIVIDUAL_DIR.mkdir(parents=True, exist_ok=True)
    amostras = list(
        AmostraTreinamento.objects.filter(conversa__util_para_treinamento=True, pronta=True)
        .select_related("conversa")
        .order_by("conversa_id", "tipo")
    )
    payload = {
        "projeto": "Mheibos Aprendizado",
        "meta_conversas": 1000,
        "total_conversas_uteis": ConversaAprendizado.objects.filter(util_para_treinamento=True).count(),
        "total_amostras": len(amostras),
        "gerado_em": timezone.now().isoformat(),
        "amostras": [_amostra_payload(amostra) for amostra in amostras],
    }
    EXPORT_CONVERSAS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    for amostra in amostras:
        destino = EXPORT_INDIVIDUAL_DIR / f"conversa_{amostra.conversa_id}_{amostra.tipo.lower()}.json"
        destino.write_text(json.dumps(_amostra_payload(amostra), ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def atualizar_sinais(conversa):
    mensagens = list(conversa.mensagens.values("direcao", "texto"))
    textos = [str(item["texto"] or "").strip() for item in mensagens if str(item["texto"] or "").strip()]
    texto_total = "\n".join(textos)
    conversa.total_mensagens = conversa.mensagens.count()
    conversa.total_cliente = conversa.mensagens.filter(direcao=DirecaoMensagem.CLIENTE).count()
    conversa.total_empresa = conversa.mensagens.filter(direcao=DirecaoMensagem.EMPRESA).count()
    conversa.tem_reclamacao = _contem(texto_total, RECLAMACAO_TERMOS)
    conversa.tem_lead = _contem(texto_total, LEAD_TERMOS)
    conversa.tem_sinal_pedido = _contem(texto_total, PEDIDO_TERMOS)
    cliente_com_texto = sum(
        1
        for item in mensagens
        if item["direcao"] == DirecaoMensagem.CLIENTE and str(item["texto"] or "").strip()
    )
    empresa_com_texto = sum(
        1
        for item in mensagens
        if item["direcao"] == DirecaoMensagem.EMPRESA and str(item["texto"] or "").strip()
    )
    tem_sinal_util = conversa.tem_reclamacao or conversa.tem_lead or conversa.tem_sinal_pedido
    conversa.util_para_treinamento = bool(textos) and (
        (cliente_com_texto >= 2 and empresa_com_texto >= 1)
        or (cliente_com_texto >= 2 and tem_sinal_util)
    )
    primeira = conversa.mensagens.order_by("enviada_em").first()
    ultima = conversa.mensagens.order_by("-enviada_em").first()
    conversa.primeira_mensagem_em = primeira.enviada_em if primeira else None
    conversa.ultima_mensagem_em = ultima.enviada_em if ultima else None
    conversa.save(
        update_fields=[
            "total_mensagens",
            "total_cliente",
            "total_empresa",
            "tem_reclamacao",
            "tem_lead",
            "tem_sinal_pedido",
            "util_para_treinamento",
            "primeira_mensagem_em",
            "ultima_mensagem_em",
            "atualizado_em",
        ]
    )
    if conversa.util_para_treinamento:
        tipo = TipoAmostraTreinamento.CONVERSA
        if conversa.tem_reclamacao:
            tipo = TipoAmostraTreinamento.RECLAMACAO
        elif conversa.tem_sinal_pedido:
            tipo = TipoAmostraTreinamento.PEDIDO
        elif conversa.tem_lead:
            tipo = TipoAmostraTreinamento.LEAD
        pronta = len(textos) >= 4 and (empresa_com_texto >= 1 or tem_sinal_util)
        AmostraTreinamento.objects.update_or_create(
            conversa=conversa,
            tipo=tipo,
            defaults={
                "conteudo": _conteudo_treinamento(conversa),
                "qualidade": 2 if len(textos) >= 6 and empresa_com_texto >= 1 else 1,
                "pronta": pronta,
            },
        )
        exportar_conversas_uteis_json()
    else:
        conversa.amostras.update(pronta=False)


def registrar_evento_evolution(payload):
    data = payload.get("data") or payload
    key = data.get("key") or {}
    remote_jid = key.get("remoteJid") or key.get("remoteJidAlt") or payload.get("sender") or ""
    instancia = payload.get("instance") or data.get("instanceName") or ""
    mensagem_id = key.get("id") or data.get("id") or f"sem-id-{timezone.now().timestamp()}"
    from_me = bool(key.get("fromMe"))
    direcao = DirecaoMensagem.EMPRESA if from_me else DirecaoMensagem.CLIENTE
    nome = data.get("pushName") or ""
    telefone = telefone_de_jid(remote_jid)
    texto = texto_da_mensagem(data)

    conversa, _ = ConversaAprendizado.objects.get_or_create(
        origem=OrigemConversa.WHATSAPP,
        instancia=instancia,
        contato_id=remote_jid,
        defaults={
            "telefone": telefone,
            "nome_contato": nome,
        },
    )
    atualizou = False
    if nome and conversa.nome_contato != nome:
        conversa.nome_contato = nome
        atualizou = True
    if telefone and conversa.telefone != telefone:
        conversa.telefone = telefone
        atualizou = True
    if atualizou:
        conversa.save(update_fields=["nome_contato", "telefone", "atualizado_em"])

    MensagemAprendizado.objects.get_or_create(
        conversa=conversa,
        mensagem_id=mensagem_id,
        defaults={
            "direcao": direcao,
            "tipo": data.get("messageType") or "",
            "texto": texto,
            "enviada_em": enviada_em(data),
            "payload": payload,
        },
    )
    atualizar_sinais(conversa)
    return conversa

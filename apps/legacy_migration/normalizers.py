import base64
import binascii
import hashlib
import json
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def texto_limpo(valor):
    return str(valor or "").strip()


def decimal_br(valor):
    if valor is None:
        return Decimal("0.00")
    if isinstance(valor, Decimal):
        return valor
    texto = str(valor).strip().replace("R$", "").replace(" ", "")
    if not texto:
        return Decimal("0.00")
    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    else:
        texto = texto.replace(",", ".")
    try:
        return Decimal(texto).quantize(Decimal("0.01"))
    except InvalidOperation:
        return Decimal("0.00")


def parse_data(valor):
    texto = texto_limpo(valor)
    if not texto:
        return None
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S"):
        try:
            parsed = datetime.strptime(texto[: len(formato)], formato)
            return parsed.date()
        except ValueError:
            continue
    return None


def parse_datetime(valor):
    texto = texto_limpo(valor)
    if not texto:
        return None
    for formato in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto[: len(formato)], formato)
        except ValueError:
            continue
    parsed_date = parse_data(texto)
    if parsed_date:
        return datetime.combine(parsed_date, datetime.min.time())
    return None


def parse_hora(valor):
    texto = texto_limpo(valor)
    if not texto:
        return None
    for formato in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(texto[: len(formato)], formato).time()
        except ValueError:
            continue
    return None


def normalizar_status(valor):
    texto = texto_limpo(valor).lower()
    if "cancel" in texto:
        return "CANCELADO"
    if "aguard" in texto and "arte" in texto:
        return "AGUARDANDO_ARTE"
    if "entreg" in texto:
        return "ENTREGUE"
    if "pronto" in texto or "finaliz" in texto:
        return "PRONTO"
    return "EM_PRODUCAO"


def normalizar_forma_pagamento(valor):
    texto = texto_limpo(valor).lower()
    if "pix" in texto:
        return "PIX"
    if "vista" in texto or "dinheiro" in texto:
        return "DINHEIRO"
    if "cart" in texto:
        return "CARTAO"
    if "cheque" in texto:
        return "CHEQUE"
    if "transfer" in texto:
        return "TRANSFERENCIA"
    if texto:
        return "OUTRO"
    return "NAO_INFORMADO"


def normalizar_origem(valor):
    texto = texto_limpo(valor).lower()
    if "whats" in texto:
        return "WHATSAPP"
    if "ia" in texto or "bot" in texto:
        return "IA"
    if texto:
        return "OUTRO"
    return "LEGADO"


def parse_itens_descricao(descricao):
    itens = []
    blocos = re.split(r"\n(?=\d+(?:[,.]\d+)?x\s)", texto_limpo(descricao))
    padrao = re.compile(
        r"^(?P<qtd>\d+(?:[,.]\d+)?)x\s+(?P<nome>.+?)\s+-\s+R\$\s*(?P<preco>\d+(?:[,.]\d+)?)\s*un\.?",
        re.I | re.S,
    )
    for ordem, bloco in enumerate(blocos):
        bloco = bloco.strip()
        if not bloco:
            continue
        match = padrao.search(bloco)
        if not match:
            continue
        descricao_item = ""
        if "Descricao:" in bloco:
            descricao_item = bloco.split("Descricao:", 1)[1].strip()
        if "Descrição:" in bloco:
            descricao_item = bloco.split("Descrição:", 1)[1].strip()
        itens.append(
            {
                "ordem": ordem,
                "quantidade": decimal_br(match.group("qtd")),
                "nome": match.group("nome").strip(),
                "preco_unitario": decimal_br(match.group("preco")),
                "descricao": descricao_item,
            }
        )
    return itens


def imagens_base64(arte_data):
    texto = texto_limpo(arte_data)
    if len(texto) < 80:
        return []
    if texto.startswith("{"):
        try:
            obj = json.loads(texto)
            imagens = obj.get("images") or obj.get("imagens") or []
            return [str(item) for item in imagens if len(str(item)) > 80]
        except (json.JSONDecodeError, TypeError):
            return []
    return [texto]


def decodificar_imagem_base64(valor):
    texto = texto_limpo(valor)
    if "," in texto and texto.lower().startswith("data:"):
        texto = texto.split(",", 1)[1]
    try:
        dados = base64.b64decode(texto, validate=True)
    except (binascii.Error, ValueError):
        return None, ""
    return dados, hashlib.sha256(dados).hexdigest()


def data_competencia_padrao(*datas):
    for valor in datas:
        if isinstance(valor, datetime):
            return valor.date()
        if isinstance(valor, date):
            return valor
    return date.today()

from copy import deepcopy


ORDEM_SERVICO_CAMPOS = [
    ("cliente", "Cliente", True),
    ("data_pedido", "Data do pedido", True),
    ("tema", "Tema", False),
    ("telefone_1", "Telefone 1", False),
    ("telefone_2", "Telefone 2", False),
    ("descricao", "Descricao", False),
    ("data_entrega", "Data da entrega", True),
    ("hora_entrega", "Hora da entrega", False),
    ("pagamento", "Pagamento", False),
    ("valor_total", "Valor total", True),
    ("pago", "Pago", False),
    ("resta", "Resta", False),
    ("observacoes", "Observacoes", False),
    ("designer", "Designer", False),
]


def campos_os_padrao():
    return {
        chave: {"rotulo": rotulo, "obrigatorio": obrigatorio}
        for chave, rotulo, obrigatorio in ORDEM_SERVICO_CAMPOS
    }


def normalizar_campos_os(dados):
    campos = campos_os_padrao()
    if not isinstance(dados, dict):
        return campos
    for chave, config in dados.items():
        if chave not in campos or not isinstance(config, dict):
            continue
        rotulo = str(config.get("rotulo") or campos[chave]["rotulo"]).strip()
        campos[chave]["rotulo"] = rotulo[:80] or campos[chave]["rotulo"]
        campos[chave]["obrigatorio"] = bool(config.get("obrigatorio"))
    return campos


def lista_campos_os(dados):
    normalizados = normalizar_campos_os(dados)
    return [
        {
            "chave": chave,
            "rotulo": normalizados[chave]["rotulo"],
            "obrigatorio": normalizados[chave]["obrigatorio"],
        }
        for chave, _, _ in ORDEM_SERVICO_CAMPOS
    ]


def salvar_campos_os(post):
    campos = deepcopy(campos_os_padrao())
    for chave in campos:
        campos[chave]["rotulo"] = str(post.get(f"os_rotulo_{chave}") or campos[chave]["rotulo"]).strip()[:80]
        campos[chave]["obrigatorio"] = post.get(f"os_obrigatorio_{chave}") == "on"
    return campos


def linha_cabecalho_padrao():
    return {"cores": ["#00a8e0", "#d966b3", "#f5d547"]}


def normalizar_linha_cabecalho(dados):
    if not isinstance(dados, dict):
        return linha_cabecalho_padrao()
    cores = []
    for cor in dados.get("cores", []):
        valor = str(cor).strip().lower()
        if len(valor) == 7 and valor.startswith("#"):
            cores.append(valor)
    if not cores:
        return linha_cabecalho_padrao()
    return {"cores": cores[:3]}


def css_linha_cabecalho(dados):
    cores = normalizar_linha_cabecalho(dados)["cores"]
    if len(cores) == 1:
        return cores[0]
    return f"linear-gradient(90deg, {', '.join(cores)})"


def salvar_linha_cabecalho(post):
    cores = []
    for indice in (1, 2, 3):
        valor = (post.get(f"os_header_cor_{indice}") or "").strip().lower()
        if len(valor) == 7 and valor.startswith("#"):
            cores.append(valor)
    return {"cores": cores or linha_cabecalho_padrao()["cores"]}


def cores_linha_cabecalho_form(dados):
    cores = normalizar_linha_cabecalho(dados)["cores"]
    while len(cores) < 3:
        cores.append("")
    return cores[:3]

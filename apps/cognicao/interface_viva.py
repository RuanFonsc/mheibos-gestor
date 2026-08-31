"""Inventário oficial da Interface Viva e comandos executáveis pelo cliente web."""

from typing import Any

INTERFACE_INVENTARIO: dict[str, Any] = {
    "versao": "1.0",
    "telas": {
        "novo_pedido": {
            "rota": "/pedidos/novo/",
            "nome": "Novo Pedido",
            "campos": {
                "nome_cliente": {"rotulo": "Nome do Cliente", "tipo": "texto", "obrigatorio": True},
                "tema": {"rotulo": "Tema", "tipo": "texto", "obrigatorio": True},
                "data_entrega": {"rotulo": "Data de Entrega", "tipo": "data", "obrigatorio": True},
                "hora_entrega": {"rotulo": "Hora da Entrega", "tipo": "hora", "obrigatorio": False},
                "observacoes": {"rotulo": "Observações", "tipo": "texto_longo", "obrigatorio": False},
                "prioridade": {"rotulo": "Prioridade", "tipo": "selecao", "obrigatorio": True},
                "canal_atendimento": {"rotulo": "Canal de atendimento", "tipo": "selecao", "obrigatorio": True},
                "valor_pago": {"rotulo": "Valor Pago", "tipo": "decimal", "obrigatorio": True},
                "forma_pagamento": {"rotulo": "Forma de Pagamento", "tipo": "selecao", "obrigatorio": True},
                "desconto_ajuste": {"rotulo": "Desconto / Acréscimo", "tipo": "decimal", "obrigatorio": True},
                "aguardar_arte": {"rotulo": "Aguardando arte", "tipo": "booleano", "obrigatorio": False},
                "marcar_pronto": {"rotulo": "Marcar como pronto imediatamente", "tipo": "booleano", "obrigatorio": False},
            },
            "acoes": {"salvar": {"requer_confirmacao": True, "persistente": True}},
        },
        "pedidos": {"rota": "/pedidos/", "nome": "Gestor de Pedidos", "acoes": {"pesquisar": {"requer_confirmacao": False}}},
        "pedido_detalhe": {"rota": "/pedidos/{pedido_id}/", "nome": "Detalhe do Pedido", "acoes": {"alterar_status": {"requer_confirmacao": True, "persistente": True}}},
        "dashboard": {"rota": "/dashboard/", "nome": "Dashboard"},
        "assistencia_impressao": {"rota": "/assistencia-envio/", "nome": "Assistência de Impressão"},
        "entregas": {"rota": "/pedidos/entrega/", "nome": "Entregas"},
        "clientes": {"rota": "/clientes/", "nome": "Clientes"},
        "produtos": {"rota": "/produtos/", "nome": "Produtos"},
        "whatsapp": {"rota": "/cognicao/whatsapp/", "nome": "WhatsApp", "acoes": {"selecionar_conversa": {"requer_confirmacao": False}, "preparar_resposta": {"requer_confirmacao": False}}},
    },
    "comandos": {
        "navegar": {"descricao": "Abrir uma tela registrada; pode receber campo para destaque após a navegação", "confirmacao": False},
        "destacar_campo": {"descricao": "Focar e destacar um campo registrado", "confirmacao": False},
        "destacar_acao": {"descricao": "Destacar um botão registrado", "confirmacao": False},
        "preencher_campos": {"descricao": "Preencher valores propostos em formulário", "confirmacao": True},
        "abrir_pedido": {"descricao": "Abrir um pedido autorizado", "confirmacao": False},
        "pesquisar_pedidos": {"descricao": "Pesquisar pedidos no escopo do usuário", "confirmacao": False},
    },
}


def inventario_para_modelo() -> str:
    import json
    return json.dumps(INTERFACE_INVENTARIO, ensure_ascii=False, separators=(",", ":"))
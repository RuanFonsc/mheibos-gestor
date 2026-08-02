from django.db.models import Q, TextField
from django.db.models.functions import Cast

from .models import EstadoVinculoArquivo


def pesquisar_pedidos_por_artes(pedidos, termo: str):
    termo = str(termo or "").strip()
    if not termo:
        return pedidos

    pedidos = pedidos.alias(
        _metadados_arquivo_texto=Cast(
            "arquivos_oficiais_arte__propriedades_tecnicas",
            output_field=TextField(),
        ),
        _discrepancias_arquivo_texto=Cast(
            "arquivos_oficiais_arte__discrepancias",
            output_field=TextField(),
        ),
    )
    filtro_pedido = (
        Q(cliente__nome__icontains=termo)
        | Q(cliente__telefone_principal__icontains=termo)
        | Q(cliente__telefone_secundario__icontains=termo)
        | Q(tema__icontains=termo)
        | Q(descricao_legada__icontains=termo)
        | Q(itens__nome__icontains=termo)
        | Q(itens__descricao__icontains=termo)
        | Q(itens__produto__nome__icontains=termo)
    )
    filtro_arquivo_oficial = Q(
        arquivos_oficiais_arte__estado_vinculo=EstadoVinculoArquivo.ATIVO
    ) & (
        Q(arquivos_oficiais_arte__nome_oficial__icontains=termo)
        | Q(arquivos_oficiais_arte__caminho_oficial__icontains=termo)
        | Q(arquivos_oficiais_arte__extensao__icontains=termo)
        | Q(arquivos_oficiais_arte__estado_integridade__icontains=termo)
        | Q(_metadados_arquivo_texto__icontains=termo)
        | Q(_discrepancias_arquivo_texto__icontains=termo)
    )
    filtro_referencia = Q(artes__desvinculado_em__isnull=True) & (
        Q(artes__nome_original__icontains=termo)
        | Q(artes__conteudo_sha256__icontains=termo)
    )
    filtros = filtro_pedido | filtro_arquivo_oficial | filtro_referencia

    if termo.isdigit():
        numero = int(termo)
        filtros |= (
            Q(pk=numero)
            | Q(legado_id=numero)
            | (
                Q(arquivos_oficiais_arte__estado_vinculo=EstadoVinculoArquivo.ATIVO)
                & (
                    Q(arquivos_oficiais_arte__tamanho_bytes=numero)
                    | Q(arquivos_oficiais_arte__largura_px=numero)
                    | Q(arquivos_oficiais_arte__altura_px=numero)
                    | Q(arquivos_oficiais_arte__resolucao_dpi=numero)
                )
            )
        )
    return pedidos.filter(filtros).distinct()

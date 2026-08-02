import hashlib

from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.permissions import pode_editar_pedido

from .models import AnexoPedido


class AnexoInvalido(Exception):
    pass


class AnexoNaoAutorizado(AnexoInvalido):
    pass


class AnexoDuplicado(AnexoInvalido):
    pass


def _hash_upload(upload) -> str:
    digest = hashlib.sha256()
    for bloco in upload.chunks():
        digest.update(bloco)
    upload.seek(0)
    return digest.hexdigest()


def adicionar_anexo(*, pedido, upload, operador, manter_duplicado: bool) -> AnexoPedido:
    if not pode_editar_pedido(pedido, operador):
        raise AnexoNaoAutorizado("Seu perfil nao pode adicionar anexos a este Pedido.")
    conteudo_sha256 = _hash_upload(upload)
    duplicado = AnexoPedido.objects.filter(
        pedido=pedido, conteudo_sha256=conteudo_sha256
    ).first()
    if duplicado and not manter_duplicado:
        raise AnexoDuplicado(
            f"O conteudo ja esta vinculado como '{duplicado.nome_original}'. "
            "Marque a decisao de manter duplicados para adicionar outra copia."
        )

    anexo = None
    try:
        with transaction.atomic():
            anexo = AnexoPedido.objects.create(
                pedido=pedido,
                arquivo=upload,
                nome_original=upload.name[:255],
                tamanho_bytes=upload.size,
                conteudo_sha256=conteudo_sha256,
                criado_por=operador,
            )
            registrar_evento(
                tipo="AnexoPedidoVinculado",
                operador=operador,
                origem="gestor_web",
                alvo_tipo="AnexoPedido",
                alvo_id=str(anexo.pk),
                acao="vincular_anexo",
                valores_anteriores={},
                valores_posteriores={
                    "pedido_id": pedido.pk,
                    "nome_original": anexo.nome_original,
                    "tamanho_bytes": anexo.tamanho_bytes,
                    "conteudo_sha256": conteudo_sha256,
                    "duplicado_mantido_por_decisao_humana": bool(duplicado),
                    "conteudo_interpretado": False,
                },
                chave_idempotencia=f"anexo-vincular:{anexo.pk}",
            )
    except Exception:
        if anexo and anexo.arquivo.name:
            anexo.arquivo.storage.delete(anexo.arquivo.name)
        raise
    return anexo


@transaction.atomic
def desvincular_anexo(*, anexo_id, pedido, operador) -> AnexoPedido:
    if not operador.is_admin:
        raise AnexoNaoAutorizado("Somente administradores podem desvincular anexos.")
    anexo = AnexoPedido.objects.select_for_update().filter(
        pk=anexo_id, pedido=pedido
    ).first()
    if anexo is None:
        raise AnexoInvalido("O anexo nao pertence a este Pedido.")
    if anexo.desvinculado_em:
        return anexo
    anexo.desvinculado_em = timezone.now()
    anexo.desvinculado_por = operador
    anexo.save(update_fields=["desvinculado_em", "desvinculado_por"])
    registrar_evento(
        tipo="AnexoPedidoDesvinculado",
        operador=operador,
        origem="gestor_web",
        alvo_tipo="AnexoPedido",
        alvo_id=str(anexo.pk),
        acao="desvincular_anexo",
        valores_anteriores={"vinculo_ativo": True},
        valores_posteriores={
            "vinculo_ativo": False,
            "arquivo_fisico_preservado": True,
            "nome_original": anexo.nome_original,
        },
        chave_idempotencia=f"anexo-desvincular:{anexo.pk}",
    )
    return anexo

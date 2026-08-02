import hashlib

from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.permissions import pode_editar_pedido
from apps.pedidos.models import ArtePedido


class ArteReferenciaInvalida(Exception):
    pass


class ArteReferenciaNaoAutorizada(ArteReferenciaInvalida):
    pass


def _hash_upload(upload) -> str:
    digest = hashlib.sha256()
    for bloco in upload.chunks():
        digest.update(bloco)
    upload.seek(0)
    return digest.hexdigest()


def adicionar_arte_referencia(*, pedido, upload, operador, ordem: int) -> ArtePedido:
    if not pode_editar_pedido(pedido, operador):
        raise ArteReferenciaNaoAutorizada(
            "Seu perfil nao pode adicionar arte de referencia a este Pedido."
        )
    conteudo_sha256 = _hash_upload(upload)
    arte = None
    try:
        with transaction.atomic():
            arte = ArtePedido.todos_vinculos.create(
                pedido=pedido,
                arquivo=upload,
                nome_original=upload.name,
                tamanho_bytes=upload.size,
                ordem=ordem,
                conteudo_sha256=conteudo_sha256,
                criado_por=operador,
            )
            registrar_evento(
                tipo="ArteReferenciaVinculada",
                operador=operador,
                origem="gestor_web",
                alvo_tipo="ArtePedido",
                alvo_id=str(arte.pk),
                acao="vincular_arte_referencia",
                valores_anteriores={},
                valores_posteriores={
                    "pedido_id": pedido.pk,
                    "nome_original": arte.nome_original,
                    "tamanho_bytes": arte.tamanho_bytes,
                    "conteudo_sha256": conteudo_sha256,
                    "finalidade": "REFERENCIA_VISUAL",
                },
                chave_idempotencia=f"arte-referencia-vincular:{arte.pk}",
            )
    except Exception:
        if arte and arte.arquivo.name:
            arte.arquivo.storage.delete(arte.arquivo.name)
        raise
    return arte


@transaction.atomic
def desvincular_arte_referencia(*, arte_id: int, pedido, operador) -> ArtePedido:
    if not operador.is_admin:
        raise ArteReferenciaNaoAutorizada(
            "Somente administradores podem desvincular arte de referencia."
        )
    arte = ArtePedido.todos_vinculos.select_for_update().filter(
        pk=arte_id, pedido=pedido
    ).first()
    if arte is None:
        raise ArteReferenciaInvalida("A arte de referencia nao pertence a este Pedido.")
    if arte.desvinculado_em:
        return arte
    arte.desvinculado_em = timezone.now()
    arte.desvinculado_por = operador
    arte.save(update_fields=["desvinculado_em", "desvinculado_por"])
    registrar_evento(
        tipo="ArteReferenciaDesvinculada",
        operador=operador,
        origem="gestor_web",
        alvo_tipo="ArtePedido",
        alvo_id=str(arte.pk),
        acao="desvincular_arte_referencia",
        valores_anteriores={"vinculo_ativo": True},
        valores_posteriores={
            "vinculo_ativo": False,
            "arquivo_fisico_preservado": True,
            "nome_original": arte.nome_original,
        },
        chave_idempotencia=f"arte-referencia-desvincular:{arte.pk}",
    )
    return arte

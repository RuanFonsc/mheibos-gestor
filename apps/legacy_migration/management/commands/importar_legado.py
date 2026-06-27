from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import connections, transaction

from apps.clientes.models import Cliente
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.legacy_migration.normalizers import (
    data_competencia_padrao,
    decodificar_imagem_base64,
    decimal_br,
    imagens_base64,
    normalizar_forma_pagamento,
    normalizar_origem,
    normalizar_status,
    parse_data,
    parse_datetime,
    parse_hora,
    parse_itens_descricao,
    texto_limpo,
)
from apps.pedidos.models import (
    ArtePedido,
    PagamentoPedido,
    Pedido,
    PedidoItem,
    StatusPedido,
)


class Command(BaseCommand):
    help = "Importa pedidos do banco PostgreSQL legado para o schema Django novo."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        limite = options["limit"]
        dry_run = options["dry_run"]

        sql = "SELECT * FROM pedidos ORDER BY id ASC"
        if limite:
            sql += f" LIMIT {int(limite)}"

        with connections["legacy"].cursor() as cursor:
            cursor.execute(sql)
            colunas = [coluna[0] for coluna in cursor.description]
            linhas = [dict(zip(colunas, row)) for row in cursor.fetchall()]

        if dry_run:
            self.stdout.write(self.style.WARNING(f"Dry-run: {len(linhas)} pedidos seriam importados."))
            return

        importados = 0
        atualizados = 0

        for row in linhas:
            criado = self._importar_pedido(row)
            if criado:
                importados += 1
            else:
                atualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Importacao concluida: {importados} criados, {atualizados} atualizados."
            )
        )

    @transaction.atomic
    def _importar_pedido(self, row):
        nome_cliente = texto_limpo(row.get("nome_do_cliente")) or "Cliente sem nome"
        cliente, _ = Cliente.objects.get_or_create(
            nome=nome_cliente,
            defaults={
                "email": texto_limpo(row.get("email_do_cliente")),
                "telefone_principal": self._normalizar_telefone(row.get("numero_1")),
                "telefone_secundario": self._normalizar_telefone(row.get("numero_2")),
            },
        )

        data_registro = parse_datetime(row.get("data_registro"))
        data_pedido = parse_data(row.get("data_do_pedido")) or data_competencia_padrao(data_registro)
        data_entrega = parse_data(row.get("data_de_entrega"))
        valor_total = decimal_br(row.get("valor_total"))
        valor_pago = decimal_br(row.get("valor_pago"))

        pedido, criado = Pedido.objects.update_or_create(
            legado_id=row["id"],
            defaults={
                "cliente": cliente,
                "designer": texto_limpo(row.get("designer")),
                "tema": texto_limpo(row.get("tema")),
                "descricao_legada": texto_limpo(row.get("descricao")),
                "data_registro": data_registro,
                "data_pedido": data_pedido,
                "data_entrega": data_entrega,
                "hora_entrega": parse_hora(row.get("hora_da_entrega")),
                "observacoes": texto_limpo(row.get("observacoes")),
                "valor_total": valor_total,
                "valor_pago_legado": valor_pago,
                "desconto_ajuste": decimal_br(row.get("desconto")),
                "forma_pagamento_legada": normalizar_forma_pagamento(row.get("forma_de_pagamento")),
                "status": normalizar_status(row.get("status")),
                "origem": normalizar_origem(row.get("origem")),
                "pdf_gerado_por": texto_limpo(row.get("pdf_gerado_por")),
            },
        )

        self._importar_itens(pedido, row)
        self._importar_pagamento(pedido, row, valor_pago, data_pedido)
        self._importar_artes(pedido, row)
        sincronizar_financeiro_pedido(pedido)
        return criado

    def _importar_itens(self, pedido, row):
        if pedido.itens.exists():
            return

        itens = parse_itens_descricao(row.get("descricao"))
        if not itens:
            PedidoItem.objects.create(
                pedido=pedido,
                nome=texto_limpo(row.get("tema")) or "Item legado",
                descricao=texto_limpo(row.get("descricao")),
                quantidade=1,
                preco_unitario=pedido.valor_total,
                ordem=0,
            )
            return

        for item in itens:
            PedidoItem.objects.create(pedido=pedido, **item)

    def _importar_pagamento(self, pedido, row, valor_pago, data_pedido):
        if valor_pago <= 0 or pedido.pagamentos.exists():
            return
        PagamentoPedido.objects.create(
            pedido=pedido,
            valor=valor_pago,
            forma=normalizar_forma_pagamento(row.get("forma_de_pagamento")),
            data_pagamento=data_pedido,
            observacoes="Importado do campo valor_pago do legado.",
        )

    def _importar_artes(self, pedido, row):
        if pedido.artes.exists():
            return

        for ordem, imagem in enumerate(imagens_base64(row.get("arte"))):
            dados, digest = decodificar_imagem_base64(imagem)
            if not dados:
                continue
            nome = f"pedido_{pedido.legado_id}_arte_{ordem + 1}.jpg"
            arte = ArtePedido(
                pedido=pedido,
                nome_original=nome,
                tamanho_bytes=len(dados),
                ordem=ordem,
                legado_base64_hash=digest,
            )
            arte.arquivo.save(Path(nome).name, ContentFile(dados), save=True)

    def _limitar_texto(self, valor, limite):
        return texto_limpo(valor)[:limite]

    def _normalizar_telefone(self, valor):
        texto = texto_limpo(valor)
        if not texto:
            return ""
        texto_lower = texto.lower()
        if "imagem anexada" in texto_lower or texto_lower.startswith("[imagem"):
            return ""
        return texto[:32]

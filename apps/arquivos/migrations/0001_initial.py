import uuid

import django.db.models.deletion
from django.db import migrations, models


def importar_caminhos_legados(apps, schema_editor):
    Pedido = apps.get_model("pedidos", "Pedido")
    Arquivo = apps.get_model("arquivos", "ArquivoOficialArte")
    registros = []
    for pedido in Pedido.objects.exclude(caminho_arquivo_corel="").iterator():
        caminho = pedido.caminho_arquivo_corel.strip().replace("/", "\\")
        nome = caminho.rsplit("\\", 1)[-1] or "arquivo-legado"
        extensao = nome.rsplit(".", 1)[-1].lower() if "." in nome else ""
        registros.append(
            Arquivo(
                pedido_id=pedido.pk,
                caminho_oficial=caminho,
                nome_oficial=nome[:255],
                extensao=extensao[:32],
                origem="LEGADO",
                estado_integridade="NAO_VERIFICADO",
                estado_vinculo="ATIVO",
            )
        )
        if len(registros) >= 500:
            Arquivo.objects.bulk_create(registros)
            registros.clear()
    if registros:
        Arquivo.objects.bulk_create(registros)


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("catalogo", "0016_operadorgestor_codigo_origem_offline"),
        ("pedidos", "0010_pedido_codigo_visivel_offline_and_more"),
    ]
    operations = [
        migrations.CreateModel(
            name="ArquivoOficialArte",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("caminho_oficial", models.CharField(max_length=1000)),
                ("nome_oficial", models.CharField(max_length=255)),
                ("extensao", models.CharField(blank=True, max_length=32)),
                ("origem", models.CharField(choices=[("CRIADO_MHEIBOS", "Criado pelo Mheibos"), ("VINCULADO_MANUAL", "Vinculado manualmente"), ("LEGADO", "Compatibilidade legada")], max_length=24)),
                ("estado_integridade", models.CharField(choices=[("NAO_VERIFICADO", "Nao verificado"), ("INTEGRO", "Integro"), ("ALERTA", "Alerta de integridade")], default="NAO_VERIFICADO", max_length=24)),
                ("estado_vinculo", models.CharField(choices=[("ATIVO", "Ativo"), ("ENCERRADO", "Encerrado")], default="ATIVO", max_length=16)),
                ("tamanho_bytes", models.PositiveBigIntegerField(blank=True, null=True)),
                ("largura_px", models.PositiveIntegerField(blank=True, null=True)),
                ("altura_px", models.PositiveIntegerField(blank=True, null=True)),
                ("resolucao_dpi", models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ("propriedades_tecnicas", models.JSONField(blank=True, default=dict)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("criado_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="arquivos_oficiais_criados", to="catalogo.operadorgestor")),
                ("pedido", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="arquivos_oficiais_arte", to="pedidos.pedido")),
            ],
            options={"ordering": ["criado_em", "nome_oficial"]},
        ),
        migrations.AddIndex(model_name="arquivooficialarte", index=models.Index(fields=["pedido", "estado_vinculo"], name="arquivos_ar_pedido__01b705_idx")),
        migrations.AddIndex(model_name="arquivooficialarte", index=models.Index(fields=["nome_oficial"], name="arquivos_ar_nome_of_595afa_idx")),
        migrations.AddIndex(model_name="arquivooficialarte", index=models.Index(fields=["estado_integridade"], name="arquivos_ar_estado__b4ea7b_idx")),
        migrations.RunPython(importar_caminhos_legados, migrations.RunPython.noop),
    ]

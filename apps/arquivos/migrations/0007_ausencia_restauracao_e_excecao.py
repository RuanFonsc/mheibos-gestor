import django.db.models.deletion
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("arquivos", "0006_alertas_inatividade_arte"),
        ("catalogo", "0017_perfilempresa_diretorio_artes_e_retencao"),
        ("pedidos", "0011_artepedido_conteudo_sha256_artepedido_criado_por_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="arquivooficialarte",
            name="ausencia_critica_ativa",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="ausencia_detectada_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="conteudo_sha256",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="restauracao_conteudo_divergente",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="restaurado_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="restaurado_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="arquivos_oficiais_restaurados",
                to="catalogo.operadorgestor",
            ),
        ),
        migrations.CreateModel(
            name="ExcecaoAusenciaArquivoOficial",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("acao", models.CharField(max_length=120)),
                ("justificativa", models.TextField()),
                ("arquivos_ausentes", models.JSONField(default=list)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "autorizador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="excecoes_arquivo_autorizadas",
                        to="catalogo.operadorgestor",
                    ),
                ),
                (
                    "pedido",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="excecoes_ausencia_arquivo",
                        to="pedidos.pedido",
                    ),
                ),
                (
                    "solicitante",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="excecoes_arquivo_solicitadas",
                        to="catalogo.operadorgestor",
                    ),
                ),
            ],
            options={
                "ordering": ["-criado_em"],
                "indexes": [
                    models.Index(
                        fields=["pedido", "acao", "criado_em"],
                        name="arquivos_ex_pedido__c84b63_idx",
                    )
                ],
            },
        ),
    ]

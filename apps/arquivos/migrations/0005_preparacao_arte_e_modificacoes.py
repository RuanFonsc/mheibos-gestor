import django.db.models.deletion
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalogo", "0017_perfilempresa_diretorio_artes_e_retencao"),
        ("pedidos", "0011_artepedido_conteudo_sha256_artepedido_criado_por_and_more"),
        ("arquivos", "0004_arquivooficialarte_backup_previo_confirmado_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PreparacaoArtePedido",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("estado", models.CharField(choices=[("NAO_INICIADA", "Arte nao iniciada"), ("EM_PREPARACAO", "Arte em preparacao"), ("CONCLUIDA", "Arte concluida")], default="NAO_INICIADA", max_length=24)),
                ("iniciado_em", models.DateTimeField(blank=True, null=True)),
                ("ultima_atividade_em", models.DateTimeField(blank=True, null=True)),
                ("concluido_em", models.DateTimeField(blank=True, null=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("concluido_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="preparacoes_arte_concluidas", to="catalogo.operadorgestor")),
                ("pedido", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="preparacao_arte", to="pedidos.pedido")),
                ("responsavel", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="preparacoes_arte_responsavel", to="catalogo.operadorgestor")),
            ],
            options={"ordering": ["-atualizado_em"]},
        ),
        migrations.AddField(model_name="arquivooficialarte", name="alteracao_pos_conclusao_pendente", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="arquivooficialarte", name="modificacao_detectada_em", field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name="arquivooficialarte", name="modificado_em_ns", field=models.PositiveBigIntegerField(blank=True, null=True)),
        migrations.AddField(model_name="arquivooficialarte", name="ultima_modificacao_por", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="arquivos_oficiais_modificados", to="catalogo.operadorgestor")),
    ]

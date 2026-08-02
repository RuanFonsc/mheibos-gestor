import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("arquivos", "0001_initial"),
        ("catalogo", "0016_operadorgestor_codigo_origem_offline"),
    ]

    operations = [
        migrations.AddField(
            model_name="arquivooficialarte",
            name="alerta_reconhecido_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="alerta_reconhecido_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="alertas_arquivo_reconhecidos",
                to="catalogo.operadorgestor",
            ),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="discrepancias",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="verificado_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

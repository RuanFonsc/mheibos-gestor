from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("sincronizacao", "0002_estacaocliente")]

    operations = [
        migrations.AddField(
            model_name="unidadesincronizacao",
            name="codigo_confirmacao",
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name="unidadesincronizacao",
            name="incorporada_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="unidadesincronizacao",
            name="pedido_global_id_confirmado",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("catalogo", "0016_operadorgestor_codigo_origem_offline")]

    operations = [
        migrations.AddField(
            model_name="perfilempresa",
            name="diretorio_artes_raiz",
            field=models.CharField(
                blank=True,
                help_text="Pasta compartilhada usada pelas instancias do Mheibos para as artes oficiais.",
                max_length=1000,
            ),
        ),
        migrations.AddField(
            model_name="perfilempresa",
            name="retencao_copias_locais_dias",
            field=models.PositiveSmallIntegerField(default=30),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogo", "0008_perfilempresa_os_cor_legendas"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfilempresa",
            name="os_linha_cabecalho",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]

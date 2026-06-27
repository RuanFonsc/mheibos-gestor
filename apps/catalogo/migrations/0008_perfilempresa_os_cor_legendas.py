from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogo", "0007_perfilempresa_os_cor_linhas_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfilempresa",
            name="os_cor_legendas",
            field=models.CharField(default="#06143d", max_length=7),
        ),
    ]

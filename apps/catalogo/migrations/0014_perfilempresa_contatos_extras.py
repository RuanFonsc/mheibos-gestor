from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogo", "0013_categoriausuario_operadorgestor_categoria_usuario"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfilempresa",
            name="instagram_secundario",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="perfilempresa",
            name="telefone_terciario",
            field=models.CharField(blank=True, max_length=32),
        ),
    ]

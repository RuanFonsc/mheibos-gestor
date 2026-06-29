from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="cpf_cnpj",
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name="cliente",
            name="endereco",
            field=models.TextField(blank=True),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0005_pedido_caminho_arquivo_corel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="origem",
            field=models.CharField(
                choices=[
                    ("BALCAO", "Balcao"),
                    ("VENDAS", "Mheibos Vendas"),
                    ("WHATSAPP", "WhatsApp"),
                    ("IA", "IA"),
                    ("LEGADO", "Legado"),
                    ("OUTRO", "Outro"),
                ],
                default="LEGADO",
                max_length=24,
            ),
        ),
    ]

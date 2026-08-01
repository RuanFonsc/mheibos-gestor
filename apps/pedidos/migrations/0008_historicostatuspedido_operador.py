from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalogo", "0015_operadorgestor_canal_atendimento_padrao"),
        ("pedidos", "0007_pedido_canal_atendimento"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicostatuspedido",
            name="operador",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="historicos_status_pedido",
                to="catalogo.operadorgestor",
            ),
        ),
    ]

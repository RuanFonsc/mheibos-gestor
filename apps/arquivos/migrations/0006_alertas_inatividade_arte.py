from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("arquivos", "0005_preparacao_arte_e_modificacoes"),
    ]

    operations = [
        migrations.AddField(
            model_name="preparacaoartepedido",
            name="adiado_para_data",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="preparacaoartepedido",
            name="ajuda_urgente_solicitada_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="preparacaoartepedido",
            name="alertas_inatividade_respondidos",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="preparacaoartepedido",
            name="proximo_alerta_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

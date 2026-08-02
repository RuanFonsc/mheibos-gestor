from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("arquivos", "0007_ausencia_restauracao_e_excecao")]

    operations = [
        migrations.AddField(
            model_name="arquivooficialarte",
            name="provisoria_local",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="caminho_destino_pendente",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="caminho_local_origem",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="transferido_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="transferido_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="arquivos_oficiais_transferidos",
                to="catalogo.operadorgestor",
            ),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="copia_local_preservada_em",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name="arquivooficialarte",
            name="copia_local_removida_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

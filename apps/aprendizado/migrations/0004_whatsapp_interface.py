from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aprendizado", "0003_memoriaoperacional"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversaaprendizado",
            name="favorita",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="conversaaprendizado",
            name="arquivada",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="conversaaprendizado",
            name="lida_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="EtiquetaConversaWhatsApp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=48)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                (
                    "conversa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="etiquetas",
                        to="aprendizado.conversaaprendizado",
                    ),
                ),
            ],
            options={
                "ordering": ["nome", "id"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("conversa", "nome"),
                        name="aprendizado_etiqueta_conversa_nome_uniq",
                    )
                ],
            },
        ),
    ]
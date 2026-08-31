from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cognicao", "0002_conversacognitiva_origem_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tarefacognitiva",
            name="notificado_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="AlertaCognitiva",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("chave", models.CharField(max_length=200)),
                ("dados", models.JSONField(blank=True, default=dict)),
                ("ativa", models.BooleanField(default=True)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("atualizada_em", models.DateTimeField(auto_now=True)),
                ("ultima_tarefa_em", models.DateTimeField(blank=True, null=True)),
                ("operador", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="catalogo.operadorgestor")),
            ],
            options={
                "indexes": [
                    models.Index(fields=["operador", "ativa"], name="cognicao_al_operado_8b2b1f_idx"),
                ],
                "constraints": [
                    models.UniqueConstraint(fields=("operador", "chave"), name="cognicao_alerta_operador_chave_uniq"),
                ],
            },
        ),
    ]

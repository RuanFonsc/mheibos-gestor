import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("catalogo", "0015_operadorgestor_canal_atendimento_padrao")]
    operations = [
        migrations.CreateModel(
            name="EventoOperacional",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("tipo", models.CharField(max_length=120)),
                ("versao_esquema", models.PositiveSmallIntegerField(default=1)),
                ("ocorrido_em", models.DateTimeField()),
                ("registrado_em", models.DateTimeField(auto_now_add=True)),
                ("origem", models.CharField(max_length=80)),
                ("origem_offline", models.BooleanField(default=False)),
                ("alvo_tipo", models.CharField(max_length=80)),
                ("alvo_id", models.CharField(max_length=80)),
                ("acao", models.CharField(max_length=120)),
                ("valores_anteriores", models.JSONField(default=dict)),
                ("valores_posteriores", models.JSONField(default=dict)),
                ("correlacao_id", models.UUIDField(default=uuid.uuid4)),
                ("chave_idempotencia", models.CharField(blank=True, max_length=180, null=True, unique=True)),
                ("resultado", models.CharField(choices=[("CONCLUIDO", "Concluído"), ("REJEITADO", "Rejeitado"), ("PENDENTE", "Pendente"), ("FALHA", "Falha")], default="CONCLUIDO", max_length=24)),
                ("metadados", models.JSONField(default=dict)),
                ("operador", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="eventos_operacionais", to="catalogo.operadorgestor")),
            ],
            options={"ordering": ["-ocorrido_em", "-registrado_em"]},
        ),
        migrations.AddIndex(model_name="eventooperacional", index=models.Index(fields=["alvo_tipo", "alvo_id", "ocorrido_em"], name="auditoria_e_alvo_ti_560ca9_idx")),
        migrations.AddIndex(model_name="eventooperacional", index=models.Index(fields=["tipo", "ocorrido_em"], name="auditoria_e_tipo_81b640_idx")),
        migrations.AddIndex(model_name="eventooperacional", index=models.Index(fields=["correlacao_id"], name="auditoria_e_correla_a528ce_idx")),
    ]

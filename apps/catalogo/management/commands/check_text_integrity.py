import re
from pathlib import Path
from typing import Any, cast

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import models


BAD_FRAGMENTS = (
    "Gr?fica",
    "r?pida",
    "Comunica??o",
    "Pain?is",
    "Cart?o",
    "couch?",
    "Descri??o",
    "padr?o",
    "produ??o",
    "confer?ncia",
)
SUSPICIOUS_RE = re.compile(r"[A-Za-z]\?[A-Za-z]|\?\?")
TEXT_EXTENSIONS = {".py", ".html", ".js", ".css", ".txt", ".md", ".json", ".toml", ".yml", ".yaml"}
IGNORED_DIRS = {".git", ".venv", "__pycache__", "node_modules", "staticfiles", "media"}
IGNORED_FILES = {"package-lock.json", "check_text_integrity.py"}


def texto_suspeito(value):
    return bool(value and (SUSPICIOUS_RE.search(value) or any(fragment in value for fragment in BAD_FRAGMENTS)))


def linha_suspeita(value):
    if "http://" in value or "https://" in value:
        return False
    if " ?? " in value and not any(fragment in value for fragment in BAD_FRAGMENTS):
        return False
    return texto_suspeito(value)


class Command(BaseCommand):
    help = "Verifica textos corrompidos por perda de acento, como Gr?fica ou Descri??o."

    def add_arguments(self, parser):
        parser.add_argument("--skip-files", action="store_true", help="Nao verifica arquivos do projeto.")
        parser.add_argument("--skip-db", action="store_true", help="Nao verifica campos de texto do banco.")

    def handle(self, *args, **options):
        achados = []
        if not options["skip_files"]:
            achados.extend(self._verificar_arquivos())
        if not options["skip_db"]:
            achados.extend(self._verificar_banco())

        if achados:
            for item in achados[:100]:
                self.stderr.write(item)
            if len(achados) > 100:
                self.stderr.write(f"... mais {len(achados) - 100} achado(s)")
            raise CommandError(f"Encontrados {len(achados)} texto(s) suspeito(s).")
        self.stdout.write(self.style.SUCCESS("Nenhum texto suspeito encontrado."))

    def _verificar_arquivos(self):
        raiz = Path.cwd()
        achados = []
        for path in raiz.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if path.name in IGNORED_FILES:
                continue
            if any(part in IGNORED_DIRS for part in path.parts):
                continue
            try:
                texto = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                achados.append(f"arquivo:{path}: nao esta em UTF-8")
                continue
            for numero, linha in enumerate(texto.splitlines(), start=1):
                if linha_suspeita(linha):
                    achados.append(f"arquivo:{path}:{numero}: {linha.strip()[:180]}")
        return achados

    def _verificar_banco(self):
        achados = []
        for model in apps.get_models():
            campos = [
                field
                for field in model._meta.fields
                if isinstance(field, (models.CharField, models.TextField))
            ]
            if not campos:
                continue
            for obj in cast(Any, model).objects.all().iterator():
                for field in campos:
                    value = getattr(obj, field.name, "") or ""
                    if texto_suspeito(str(value)):
                        trecho = str(value).replace("\n", " ")[:180]
                        achados.append(f"banco:{model._meta.label}:{obj.pk}:{field.name}: {trecho}")
        return achados

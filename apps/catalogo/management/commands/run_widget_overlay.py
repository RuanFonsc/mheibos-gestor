import subprocess
import sys
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Inicia o widget flutuante do Windows (sobrepõe qualquer programa)."

    def add_arguments(self, parser):
        parser.add_argument("--url", default="http://127.0.0.1:8000", help="URL base do Gestor web")

    def handle(self, *args, **options):
        script = Path(__file__).resolve().parents[4] / "tools" / "widget_overlay.py"
        subprocess.Popen([sys.executable, str(script), options["url"]])
        self.stdout.write(self.style.SUCCESS(f"Widget overlay iniciado ({options['url']})."))

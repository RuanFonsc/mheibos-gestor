from django.core.management.base import BaseCommand

from apps.catalogo.integrity import MANIFEST_FILE, build_manifest, save_manifest


class Command(BaseCommand):
    help = "Gera o manifesto de integridade dos arquivos principais."

    def handle(self, *args, **options):
        manifest = build_manifest()
        save_manifest()
        self.stdout.write(self.style.SUCCESS(f"Manifesto gerado em {MANIFEST_FILE} ({len(manifest)} arquivos)."))

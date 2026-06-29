import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.catalogo.licensing import _b64url_encode, canonical_payload


class Command(BaseCommand):
    help = "Emite uma licenca offline assinada."

    def add_arguments(self, parser):
        parser.add_argument("--private-key", required=True, help="Arquivo PEM com a chave privada.")
        parser.add_argument("--license-id", required=True)
        parser.add_argument("--customer", required=True)
        parser.add_argument("--machine", action="append", default=[], help="ID da maquina autorizada. Pode repetir.")
        parser.add_argument("--expires-at", default="", help="Validade em YYYY-MM-DD. Vazio significa sem validade.")
        parser.add_argument("--max-machines", type=int, default=1)

    def handle(self, *args, **options):
        private_path = Path(options["private_key"])
        if not private_path.exists():
            raise CommandError("Arquivo de chave privada nao encontrado.")
        private_key = serialization.load_pem_private_key(private_path.read_bytes(), password=None)
        if not isinstance(private_key, Ed25519PrivateKey):
            raise CommandError("A chave privada precisa ser Ed25519.")
        expires_at = options["expires_at"].strip()
        if expires_at:
            try:
                timezone.datetime.fromisoformat(expires_at)
            except ValueError as exc:
                raise CommandError("Use validade no formato YYYY-MM-DD.") from exc

        payload = {
            "license_id": options["license_id"],
            "customer": options["customer"],
            "machines": sorted(set(options["machine"])),
            "max_machines": options["max_machines"],
            "issued_at": timezone.localdate().isoformat(),
            "expires_at": expires_at,
            "revoked": False,
        }
        payload_bytes = canonical_payload(payload)
        signature = private_key.sign(payload_bytes)
        token = f"{_b64url_encode(payload_bytes)}.{_b64url_encode(signature)}"
        self.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False))
        self.stdout.write("LICENSE_TOKEN:")
        self.stdout.write(token)

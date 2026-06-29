import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from django.core.management.base import BaseCommand


def b64url(value):
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


class Command(BaseCommand):
    help = "Gera um par de chaves Ed25519 para licenciamento."

    def handle(self, *args, **options):
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_raw = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        self.stdout.write("CHAVE PRIVADA, guarde fora do app:")
        self.stdout.write(private_pem.decode("ascii"))
        self.stdout.write("MHEIBOS_LICENSE_PUBLIC_KEY:")
        self.stdout.write(b64url(public_raw))

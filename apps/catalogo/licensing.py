import base64
import hashlib
import json
import os
import platform
import socket
import uuid
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from urllib import error, request

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from django.conf import settings
from django.utils import timezone


LICENSE_DIR = Path(settings.DATA_DIR) / "license"
LICENSE_FILE = LICENSE_DIR / "activation.json"


@dataclass
class LicenseStatus:
    ok: bool
    message: str
    payload: dict | None = None
    source: str = "local"
    offline_allowed: bool = True


def _b64url_decode(value):
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def _b64url_encode(value):
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def canonical_payload(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def machine_fingerprint():
    parts = [
        platform.system(),
        platform.node(),
        platform.machine(),
        str(uuid.getnode()),
        os.environ.get("COMPUTERNAME", ""),
        os.environ.get("USERNAME", ""),
    ]
    if platform.system().lower() == "windows":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography") as key:
                parts.append(winreg.QueryValueEx(key, "MachineGuid")[0])
        except OSError:
            pass
    raw = "|".join(str(part or "") for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def public_key_configured():
    return bool(getattr(settings, "MHEIBOS_LICENSE_PUBLIC_KEY", ""))


def enforced():
    return bool(getattr(settings, "MHEIBOS_LICENSE_ENFORCED", False))


def load_license_token():
    try:
        data = json.loads(LICENSE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return ""
    return str(data.get("license") or "")


def save_license_token(token):
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps({"license": token}, indent=2), encoding="utf-8")


def decode_license(token):
    if not token or "." not in token:
        raise ValueError("Licenca vazia ou em formato invalido.")
    payload_b64, signature_b64 = token.split(".", 1)
    payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    signature = _b64url_decode(signature_b64)
    return payload, signature


def verify_license(token=None):
    if token is None and not enforced():
        return LicenseStatus(True, "Licenciamento desativado neste ambiente.", source="disabled")
    if not public_key_configured():
        return LicenseStatus(False, "Chave publica de licenca nao configurada.")

    token = token or load_license_token()
    if not token:
        return LicenseStatus(False, "Este computador ainda nao foi ativado.")

    try:
        payload, signature = decode_license(token)
        public_key = Ed25519PublicKey.from_public_bytes(_b64url_decode(settings.MHEIBOS_LICENSE_PUBLIC_KEY))
        public_key.verify(signature, canonical_payload(payload))
    except (ValueError, json.JSONDecodeError, InvalidSignature):
        return LicenseStatus(False, "Licenca invalida ou adulterada.")

    machine_id = machine_fingerprint()
    allowed_machines = payload.get("machines") or []
    if allowed_machines and machine_id not in allowed_machines:
        return LicenseStatus(False, "Esta licenca pertence a outro computador.", payload=payload)

    expires_at = payload.get("expires_at")
    if expires_at:
        try:
            expires_date = timezone.datetime.fromisoformat(str(expires_at)).date()
        except ValueError:
            return LicenseStatus(False, "Data de validade da licenca invalida.", payload=payload)
        if expires_date < timezone.localdate():
            return LicenseStatus(False, "Licenca expirada.", payload=payload)

    revoked = bool(payload.get("revoked"))
    if revoked:
        return LicenseStatus(False, "Licenca revogada.", payload=payload)

    return LicenseStatus(True, "Licenca valida.", payload=payload)


def activate_online(license_key):
    url = str(getattr(settings, "MHEIBOS_LICENSE_SERVER_URL", "") or "").strip()
    if not url:
        raise ValueError("Central de licencas nao configurada.")
    payload = {
        "license_key": license_key.strip(),
        "machine_id": machine_fingerprint(),
        "hostname": socket.gethostname(),
        "app_version": getattr(settings, "MHEIBOS_APP_VERSION", "dev"),
    }
    req = request.Request(
        url.rstrip("/") + "/activate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        try:
            data = json.loads(exc.read().decode("utf-8"))
            detail = data.get("error") or data.get("message") or str(exc)
        except Exception:
            detail = str(exc)
        raise ValueError(detail) from exc
    except Exception as exc:
        raise ValueError(f"Nao foi possivel falar com a central: {exc}") from exc

    token = data.get("license") or data.get("token")
    if not token:
        raise ValueError("A central nao retornou uma licenca assinada.")
    status = verify_license(token)
    if not status.ok:
        raise ValueError(status.message)
    save_license_token(token)
    return status


def install_offline_license(token):
    status = verify_license(token)
    if not status.ok:
        raise ValueError(status.message)
    save_license_token(token)
    return status


def grace_limit():
    return timezone.localdate() + timedelta(days=int(getattr(settings, "MHEIBOS_LICENSE_OFFLINE_DAYS", 30)))

import hashlib
import json
from pathlib import Path

from django.conf import settings


MANIFEST_FILE = Path(settings.RESOURCE_DIR) / "config" / "integrity_manifest.json"
CHECK_EXTENSIONS = {".py", ".html", ".js", ".css", ".json"}
CHECK_DIRS = ("apps", "config", "templates", "static", "electron")
IGNORED_PARTS = {"__pycache__", ".git", ".venv", "node_modules"}


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_manifest_files():
    root = Path(settings.RESOURCE_DIR)
    for dirname in CHECK_DIRS:
        base = root / dirname
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in CHECK_EXTENSIONS:
                continue
            if any(part in IGNORED_PARTS for part in path.parts):
                continue
            if path == MANIFEST_FILE:
                continue
            yield path


def build_manifest():
    root = Path(settings.RESOURCE_DIR)
    return {
        str(path.relative_to(root)).replace("\\", "/"): file_hash(path)
        for path in iter_manifest_files()
    }


def save_manifest():
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(build_manifest(), indent=2, sort_keys=True), encoding="utf-8")


def check_integrity():
    if not MANIFEST_FILE.exists():
        return False, "Manifesto de integridade nao encontrado."
    expected = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    current = build_manifest()
    missing = sorted(set(expected) - set(current))
    changed = sorted(path for path, digest in expected.items() if current.get(path) and current[path] != digest)
    extra = sorted(set(current) - set(expected))
    if missing or changed or extra:
        detail = []
        if missing:
            detail.append(f"ausentes: {', '.join(missing[:5])}")
        if changed:
            detail.append(f"alterados: {', '.join(changed[:5])}")
        if extra:
            detail.append(f"novos: {', '.join(extra[:5])}")
        return False, "; ".join(detail)
    return True, "Arquivos principais integres."

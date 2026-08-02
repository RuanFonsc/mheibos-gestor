#!/usr/bin/env python3
"""Reporta valores visuais arbitrários em arquivos de interface alterados."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ALLOWED_PX = {0, 1, 2, 4, 8, 10, 11, 12, 13, 14, 15, 16, 18, 20, 24, 28, 30, 32, 36, 38, 40, 42, 44, 48, 52, 56, 60, 64, 68, 72, 216, 248, 320, 400, 440, 520, 560, 720, 800, 1040}
PX = re.compile(r"(?<![-\w])(?P<value>\d+)px")
INLINE = re.compile(r"\sstyle\s*=", re.IGNORECASE)


def audit(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    issues = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if INLINE.search(line):
            issues.append(f"{path}:{line_no}: estilo inline")
        for match in PX.finditer(line):
            value = int(match.group("value"))
            if value not in ALLOWED_PX:
                issues.append(f"{path}:{line_no}: {value}px fora da escala")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    issues = [issue for path in args.paths if path.is_file() for issue in audit(path)]
    print("\n".join(issues) if issues else "PASS: tokens e estilos inline")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

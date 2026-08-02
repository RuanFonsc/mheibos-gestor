#!/usr/bin/env python3
"""Executa as verificações estáticas reproduzíveis da Skill de UI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    skill = Path(__file__).resolve().parent
    paths = args.paths or ["templates/base.html"]
    command = [sys.executable, str(skill / "validate_design_tokens.py"), *paths]
    result = subprocess.run(command, cwd=args.root, check=False)
    print("Navegador real, overflow e screenshots permanecem gates bloqueantes separados.")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

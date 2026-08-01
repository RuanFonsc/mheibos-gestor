#!/usr/bin/env python3
"""Validate expected ENG documents and operational progress."""
import argparse, json, re, sys
from pathlib import Path

EXPECTED={f"{n:04d}" for n in range(11)}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path.cwd()); args=ap.parse_args(); root=args.root.resolve()
    errors=[]; warnings=[]; found={}
    for path in root.rglob("*.md"):
        m=re.search(r"(?i)(?:^|[^A-Z])ENG[- _]?(\d{4})",path.name)
        if m and "SERIES-PLAN" not in path.name.upper():
            num=m.group(1); found.setdefault(num,[]).append(path)
            if path.stat().st_size==0: errors.append(f"vazio: {path}")
            text=path.read_text(encoding="utf-8")
            if not re.search(r"(?m)^#.+",text): errors.append(f"sem título: {path}")
            if not re.search(r"(?i)RFC|Manifesto|Inventário",text): warnings.append(f"sem referência normativa explícita: {path}")
            if re.search(r"DECISAO_HUMANA_NECESSARIA|TODO|TBD",text,re.I): warnings.append(f"decisão pendente: {path}")
    for num,paths in found.items():
        if len(paths)>1: errors.append(f"responsabilidade possivelmente duplicada ENG-{num}: {len(paths)} arquivos")
    missing=sorted(EXPECTED-set(found))
    progress=root/"engineering/ENG-PROGRESS.json"
    if not progress.is_file(): warnings.append("ENG-PROGRESS.json ausente")
    else:
        try:
            data=json.loads(progress.read_text(encoding="utf-8"))
            if "documents" not in data: errors.append("progresso sem documents")
        except (OSError,json.JSONDecodeError) as exc: errors.append(f"progresso inválido: {exc}")
    for msg in warnings: print("WARN:",msg)
    for msg in errors: print("ERROR:",msg)
    print("FOUND:",",".join(sorted(found)) or "none"); print("MISSING:",",".join(missing) or "none")
    print(f"RESULT: {'FAIL' if errors else 'PASS_WITH_GAPS' if warnings or missing else 'PASS'}")
    return 1 if errors else 0
if __name__=="__main__": sys.exit(main())

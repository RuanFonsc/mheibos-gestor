#!/usr/bin/env python3
"""Validate the repository-local Mheibos skill using only stdlib."""
import argparse, re, sys
from difflib import SequenceMatcher
from pathlib import Path

REQUIRED_REFS={"AGENTS-FULL.md","SOURCE-HIERARCHY.md","RFC-ROUTING.md","ENGINEERING-GATES.md","TERMINOLOGY.md","MIGRATION-RULES.md","ENG-SERIES-PLAN.md","STOP-CONDITIONS.md"}
REQUIRED_SCRIPTS={"discover_sources.py","validate_skill.py","validate_eng_series.py","update_eng_progress.py"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path.cwd()); args=ap.parse_args()
    root=args.root.resolve(); skill=root/".agents/skills/mheibos-engineering"; errors=[]; warnings=[]
    md=skill/"SKILL.md"
    if not md.is_file(): errors.append("SKILL.md ausente"); text=""
    else: text=md.read_text(encoding="utf-8")
    match=re.match(r"\A---\n(.*?)\n---\n",text,re.S)
    if not match: errors.append("frontmatter YAML delimitado inválido")
    else:
        fm=match.group(1)
        if not re.search(r"(?m)^name:\s*mheibos-engineering\s*$",fm): errors.append("name ausente/incorreto")
        if not re.search(r"(?m)^description:\s*(?:>|\S)",fm): errors.append("description ausente")
    for name in REQUIRED_REFS:
        if not (skill/"references"/name).is_file(): errors.append(f"referência ausente: {name}")
    for name in REQUIRED_SCRIPTS:
        path=skill/"scripts"/name
        if not path.is_file(): errors.append(f"script ausente: {name}")
        elif not path.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3"): errors.append(f"script não invocável: {name}")
    for target in re.findall(r"`((?:references|scripts)/[^ `]+)`", text):
        if not (skill/target).exists(): errors.append(f"link interno quebrado: {target}")
    if "docs/ENG-SERIES-PLAN.md" in text and not (root/"docs/ENG-SERIES-PLAN.md").is_file(): errors.append("plano ENG externo quebrado")
    for path in skill.rglob("*"):
        if path.is_file() and path.stat().st_size > 200_000: warnings.append(f"arquivo grande: {path.relative_to(root)}")
    agents=next((p for p in (root/"AGENTS.md",root/"docs/AGENTS.md") if p.is_file()),None)
    if agents and text:
        ratio=SequenceMatcher(None,agents.read_text(encoding="utf-8").lower(),text.lower()).ratio()
        if ratio > .55: errors.append(f"duplicação evidente AGENTS/SKILL: {ratio:.2f}")
    if skill.parent.name!="skills" or skill.parent.parent.name!=".agents": errors.append("estrutura local incompatível")
    for msg in warnings: print("WARN:",msg)
    for msg in errors: print("ERROR:",msg)
    print(f"RESULT: {'FAIL' if errors else 'PASS'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 1 if errors else 0
if __name__=="__main__": sys.exit(main())

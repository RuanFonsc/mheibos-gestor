#!/usr/bin/env python3
"""Discover Mheibos sources without changing the repository."""
import argparse, json, re
from collections import defaultdict
from pathlib import Path

PATTERNS = [
 ("RFC", re.compile(r"(?i)(?:^|[^a-z])RFC[- _]?(\d{4})")),
 ("MANIFESTO", re.compile(r"(?i)manifesto")),
 ("PRINCIPLES", re.compile(r"(?i)princ[ií]p")),
 ("INVENTORY", re.compile(r"(?i)invent[aá]rio")),
 ("DIAGNOSTIC", re.compile(r"(?i)diagn[oó]stico")),
 ("FUNCTIONAL_REPORT", re.compile(r"(?i)relat[oó]rio.*funcional")),
 ("ENG_PLAN", re.compile(r"(?i)ENG[- _]SERIES[- _]PLAN")),
 ("ENG", re.compile(r"(?i)(?:^|[^a-z])ENG[- _]?(\d{4})")),
]
SKIP = {".git", ".agents", ".venv", "node_modules", "__pycache__"}

def discover(root):
    items = []
    for path in root.rglob("*"):
        if not path.is_file() or any(p in SKIP for p in path.parts):
            continue
        name = path.name
        kind, number = None, None
        for label, regex in PATTERNS:
            match = regex.search(name)
            if match:
                kind = label
                number = match.group(1) if match.lastindex else None
                break
        if kind:
            items.append({"type": kind, "number": number, "path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size})
    groups = defaultdict(list)
    for item in items:
        groups[(item["type"], item["number"])].append(item["path"])
    duplicates = [{"type": k[0], "number": k[1], "paths": v} for k, v in groups.items() if len(v) > 1]
    return {"root": str(root.resolve()), "sources": sorted(items, key=lambda x: x["path"].lower()), "duplicates_or_versions": duplicates}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("text","json"), default="text")
    args=parser.parse_args()
    data=discover(args.root)
    if args.format=="json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for item in data["sources"]:
            suffix=f" {item['number']}" if item["number"] else ""
            print(f"{item['type']}{suffix}: {item['path']} ({item['bytes']} bytes)")
        for group in data["duplicates_or_versions"]:
            print("DUPLICATE_OR_VERSION:", ", ".join(group["paths"]))
if __name__=="__main__": main()

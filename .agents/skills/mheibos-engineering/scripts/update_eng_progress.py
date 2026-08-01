#!/usr/bin/env python3
"""Safely initialize or explicitly update engineering/ENG-PROGRESS.json."""
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

STATES={"PENDING","IN_PROGRESS","COMPLETED","COMPLETED_WITH_GAPS","BLOCKED"}
def fresh():
    return {"schema_version":1,"documents":{f"ENG-{n:04d}":{"status":"PENDING","history":[]} for n in range(11)}}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path.cwd()); ap.add_argument("--document"); ap.add_argument("--status",choices=sorted(STATES)); ap.add_argument("--note"); ap.add_argument("--validated",action="store_true"); args=ap.parse_args()
    path=args.root.resolve()/"engineering/ENG-PROGRESS.json"
    try: data=json.loads(path.read_text(encoding="utf-8")) if path.exists() else fresh()
    except json.JSONDecodeError as exc: print(f"ERROR: JSON inválido: {exc}"); return 1
    if bool(args.document)!=bool(args.status): print("ERROR: use --document e --status juntos"); return 1
    if args.document:
        if args.document not in data.get("documents",{}): print("ERROR: documento desconhecido"); return 1
        if args.status in {"COMPLETED","COMPLETED_WITH_GAPS"} and not args.validated:
            print("ERROR: conclusão exige --validated após validação humana/externa"); return 1
        item=data["documents"][args.document]; old=item["status"]
        event={"at":datetime.now(timezone.utc).isoformat(),"from":old,"to":args.status,"note":args.note or ""}
        item.setdefault("history",[]).append(event); item["history"]=item["history"][-20:]; item["status"]=args.status
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(".json.tmp"); temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); temp.replace(path)
    print(path); return 0
if __name__=="__main__": sys.exit(main())

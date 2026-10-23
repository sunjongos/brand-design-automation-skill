#!/usr/bin/env python3
"""Create and validate auditable multi-tool brand automation receipts."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

STAGES = ["planner", "brand_anchor", "landing", "figma_design", "social", "slides", "video", "qa", "delivery"]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init"); init.add_argument("receipt", type=Path); init.add_argument("--brand", required=True)
    update = sub.add_parser("set"); update.add_argument("receipt", type=Path); update.add_argument("stage", choices=STAGES); update.add_argument("status", choices=["passed", "blocked", "failed"]); update.add_argument("--artifact", action="append", default=[]); update.add_argument("--note", action="append", default=[])
    check = sub.add_parser("check"); check.add_argument("receipt", type=Path); check.add_argument("--allow-blocked", action="store_true")
    args = parser.parse_args()
    now = datetime.now(timezone.utc).isoformat()
    if args.cmd == "init":
        save(args.receipt, {"schema": 1, "brand": args.brand, "created_at": now, "stages": {s: {"status": "pending", "artifacts": [], "notes": []} for s in STAGES}})
        print(f"INITIALIZED: {args.receipt}"); return 0
    data = load(args.receipt)
    if args.cmd == "set":
        data["stages"][args.stage] = {"status": args.status, "artifacts": args.artifact, "notes": args.note, "updated_at": now}
        save(args.receipt, data); print(f"UPDATED: {args.stage}={args.status}"); return 0
    missing = [s for s in STAGES if s not in data.get("stages", {})]
    bad = [s for s in STAGES if data.get("stages", {}).get(s, {}).get("status") not in ({"passed", "blocked"} if args.allow_blocked else {"passed"})]
    if missing or bad:
        print("INCOMPLETE");
        if missing: print("- missing: " + ", ".join(missing))
        if bad: print("- not passed: " + ", ".join(bad))
        return 1
    print("COMPLETE: all pipeline stages have acceptable receipts"); return 0


if __name__ == "__main__":
    raise SystemExit(main())

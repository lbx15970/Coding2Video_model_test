#!/usr/bin/env python3
"""新建一次测试任务：生成带时间戳的 run 目录并自动登记到 runs/RUNS.md。

用法：
    python3 scripts/new_run.py --model seed-evolving --case case-001 --note "首测：柱状图动画"
    python3 scripts/new_run.py --model claude-opus-5.5 --case case-001 --refs assets/refs/images/a.png
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS_MD = ROOT / "runs" / "RUNS.md"
OUTPUTS = ROOT / "outputs"
RUN_SUBDIRS = ("videos", "code", "logs")


def slug(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z_.-]+", "-", text.strip()).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="模型 key，与 models/registry.yaml 一致")
    ap.add_argument("--case", required=True, help="用例 id，如 case-001")
    ap.add_argument("--note", default="", help="任务说明")
    ap.add_argument("--refs", default="", help="输入素材相对路径，逗号分隔")
    ap.add_argument("--params", default="", help='覆盖参数 JSON，如 \'{"temperature":0.3}\'')
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    now = datetime.now()
    run_id = f"{now:%Y%m%d-%H%M%S}_{slug(args.model)}_{slug(args.case)}"
    run_dir = OUTPUTS / run_id
    refs = [r.strip() for r in args.refs.split(",") if r.strip()]
    override = json.loads(args.params) if args.params else {}

    meta = {
        "run_id": run_id,
        "created_at": now.isoformat(timespec="seconds"),
        "model": args.model,
        "case": args.case,
        "note": args.note,
        "params_override": override,
        "inputs": refs,
        "outputs": {"videos": [], "code": []},
        "model_version_reported": None,
        "status": "created",
        "conclusion": "",
    }

    if args.dry_run:
        print(json.dumps({"run_id": run_id, "run_dir": str(run_dir), "meta": meta},
                         ensure_ascii=False, indent=2))
        return 0

    if run_dir.exists():
        print(f"run 目录已存在，拒绝覆盖：{run_dir}", file=sys.stderr)
        return 1

    run_dir.mkdir(parents=True)
    for sub in RUN_SUBDIRS:
        (run_dir / sub).mkdir()
    (run_dir / "run_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    row = (f"| {now:%Y-%m-%d %H:%M:%S} | {run_id} | {args.model} | {args.case} | "
           f"{', '.join(refs) or '-'} | outputs/{run_id}/ | created | {args.note or '-'} |\n")
    with RUNS_MD.open("a", encoding="utf-8") as f:
        f.write(row)

    print(f"run_id: {run_id}")
    print(f"目录:   outputs/{run_id}/")
    print("下一步: python3 scripts/ark_client.py --run "
          f"{run_id} --prompt-file cases/{args.case}/prompt.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""校验 README 的目录树与实际目录是否一致。

- 只比较目录与 README 树里列出的路径（`<占位符>` 自动跳过）
- outputs/<run_id>/ 内部不参与校验
- 通过退出码 0，不一致退出码 1 并打印差异，便于 CI / 规则钩子调用

用法：python3 scripts/check_tree.py [--root .]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

START = "<!-- TREE:START -->"
END = "<!-- TREE:END -->"
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def parse_readme_tree(readme: Path) -> list[str]:
    text = readme.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit("README 缺少 TREE:START / TREE:END 标记")
    block = text.split(START, 1)[1].split(END, 1)[0]

    entries: list[str] = []
    stack: list[str] = []
    for line in block.splitlines():
        if "── " not in line:
            continue
        name = line.split("── ", 1)[1].split(" #", 1)[0].strip()
        if not name or name == "/":
            continue
        depth = line.index("── ") // 4
        is_dir = name.endswith("/")
        name = name.rstrip("/")
        stack = stack[:depth]
        stack.append(name)
        if "<" in name or ">" in name:          # 占位符，如 <run_id>
            continue
        if any("<" in p or ">" in p for p in stack):   # 占位符的子级同样跳过
            continue
        if is_dir:
            entries.append("/".join(stack))
    return entries


def actual_dirs(root: Path) -> list[str]:
    dirs: list[str] = []
    for path in root.rglob("*"):
        if not path.is_dir():
            continue
        rel = path.relative_to(root).as_posix()
        parts = rel.split("/")
        if any(p in SKIP_DIRS for p in parts):
            continue
        if rel.startswith("outputs/"):   # 每次任务的动态目录，不参与校验
            continue
        dirs.append(rel)
    return dirs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args()

    root = Path(args.root).resolve()
    documented = set(parse_readme_tree(root / "README.md"))
    actual = set(actual_dirs(root))

    undocumented = sorted(actual - documented)
    ghosts = sorted(documented - actual)

    if not undocumented and not ghosts:
        print(f"OK：{len(actual)} 个目录与 README 一致")
        return 0

    for d in undocumented:
        print(f"❌ 未写入 README: {d}/   → 在目录树父级下补一行 `├── {d.split('/')[-1]}/  # 说明`")
    for d in ghosts:
        print(f"❌ README 有但磁盘没有: {d}/   → 删除该行或创建目录")
    return 1


if __name__ == "__main__":
    sys.exit(main())

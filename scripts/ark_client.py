#!/usr/bin/env python3
"""调用火山方舟 Ark Chat Completions（Doubao-Seed-Evolving），产物落到指定 run 目录。

单轮文本/图片接口客户端，不包含多轮 Agent、视频获取或渲染。
密钥从 models/.env 或环境变量读取，不写进代码。

用法：
    python3 scripts/ark_client.py --run 20261029-140000_seed-evolving_case-001 \
        --prompt-file cases/case-001/prompt.md
    python3 scripts/ark_client.py --run <run_id> --prompt "写一段 p5.js 动画" --image assets/refs/a.png
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT_MAP = {
    "python": "py", "py": "py", "javascript": "js", "js": "js", "typescript": "ts",
    "html": "html", "css": "css", "bash": "sh", "sh": "sh", "json": "json",
    "glsl": "glsl", "yaml": "yaml", "sql": "sql", "java": "java", "c": "c", "cpp": "cpp",
}


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip("'\"")
    return out


def load_model_cfg(path: Path, model: str) -> dict[str, str]:
    """解析 models/models.yaml：一级 key 是模型名，二级是 `k: v`。不引 PyYAML。"""
    cfg: dict[str, dict[str, str]] = {}
    section = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        k, _, v = raw.strip().partition(":")
        v = v.split(" #")[0].strip()
        if indent == 0:
            section = "" if v else k
            cfg.setdefault(section, {})
        elif section and v:
            cfg[section][k] = v
    return cfg.get(model, {})


def build_messages(prompt: str, images: list[Path]) -> list[dict]:
    content: list[dict] = [{"type": "text", "text": prompt}]
    for img in images:
        b64 = base64.b64encode(img.read_bytes()).decode()  # 大图建议改用对象存储 URL
        suffix = img.suffix.lstrip(".").lower() or "png"
        content.append({"type": "image_url",
                        "image_url": {"url": f"data:image/{suffix};base64,{b64}"}})
    return [{"role": "user", "content": content}]


def ssl_context() -> ssl.SSLContext:
    """macOS 自带 Python 常缺根证书，优先用 certifi。"""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def post(url: str, key: str, payload: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as resp:
        return json.loads(resp.read().decode("utf-8"))


def save_code(content: str, code_dir: Path) -> list[str]:
    saved = []
    pattern = re.compile(r"```([\w+-]*)\n(.*?)```", re.S)
    for i, (lang, body) in enumerate(pattern.findall(content), start=1):
        ext = EXT_MAP.get(lang.lower(), "txt")
        path = code_dir / f"generated_{i:02d}.{ext}"
        path.write_text(body, encoding="utf-8")
        saved.append(str(path.relative_to(ROOT)))
    if not saved:
        (code_dir / "generated_00.md").write_text(content, encoding="utf-8")
        saved.append(str((code_dir / "generated_00.md").relative_to(ROOT)))
    return saved


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="已存在的 run_id（先跑 new_run.py）")
    ap.add_argument("--model", default="seed-evolving", help="models/models.yaml 里的模型 key")
    ap.add_argument("--prompt-file", default="", help="prompt 文件路径")
    ap.add_argument("--prompt", default="", help="直接给 prompt")
    ap.add_argument("--image", action="append", default=[], help="参考图片，可多次")
    ap.add_argument("--params", default="", help='覆盖参数 JSON，如 \'{"temperature":0.3}\'')
    args = ap.parse_args()

    run_dir = ROOT / "outputs" / args.run
    if not run_dir.is_dir():
        print(f"run 目录不存在：{run_dir}（先用 scripts/new_run.py 建）", file=sys.stderr)
        return 1

    cfg_path = ROOT / "models" / "models.yaml"
    cfg = load_model_cfg(cfg_path, args.model)
    env = load_env(ROOT / "models" / ".env")

    endpoint = cfg.get("model", "")
    base_url = cfg.get("base_url", "").rstrip("/")
    key_name = cfg.get("api_key_env", "ARK_API_KEY")
    key = env.get(key_name) or os.environ.get(key_name, "")
    if not (endpoint and base_url and key):
        print(f"缺少 endpoint/base_url/api_key，检查 models/models.yaml 与 models/.env",
              file=sys.stderr)
        return 1

    prompt = args.prompt or Path(args.prompt_file).read_text(encoding="utf-8")
    images = [Path(p) for p in args.image]

    body = {
        "model": endpoint,
        "messages": build_messages(prompt, images),
        "stream": False,
    }
    for k in ("temperature", "top_p", "frequency_penalty", "presence_penalty"):
        if k in cfg:
            body[k] = float(cfg[k])
    if "max_tokens" in cfg:
        body["max_tokens"] = int(cfg["max_tokens"])
    body.update(json.loads(args.params) if args.params else {})

    timeout = int(float(cfg.get("timeout_s", 180)))
    retries = int(float(cfg.get("max_retries", 2)))

    logs = run_dir / "logs"
    (logs / "request.json").write_text(json.dumps(body, ensure_ascii=False, indent=2),
                                       encoding="utf-8")

    resp, err = None, None
    for attempt in range(retries + 1):
        try:
            resp = post(f"{base_url}/chat/completions", key, body, timeout)
            break
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:800]}"
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"
        if attempt < retries:
            time.sleep(2 * (attempt + 1))
    if resp is None:
        (logs / "error.txt").write_text(err or "unknown", encoding="utf-8")
        print(f"调用失败：{err}", file=sys.stderr)
        return 1

    (logs / "response.json").write_text(json.dumps(resp, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    (logs / "error.txt").unlink(missing_ok=True)
    content = resp["choices"][0]["message"]["content"]
    (logs / "content.md").write_text(content, encoding="utf-8")
    reasoning = resp["choices"][0]["message"].get("reasoning_content")
    if reasoning:
        (logs / "reasoning.md").write_text(reasoning, encoding="utf-8")
    codes = save_code(content, run_dir / "code")

    meta_path = run_dir / "run_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["model_version_reported"] = resp.get("model")
    meta["params_actual"] = {k: body[k] for k in body if k not in ("model", "messages")}
    meta["usage"] = resp.get("usage", {})
    meta["outputs"]["code"] = codes
    meta["status"] = "generated"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"模型回报版本: {resp.get('model')}")
    print(f"代码文件: {codes}")
    print(f"tokens: {resp.get('usage', {})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

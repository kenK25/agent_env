#!/usr/bin/env python3
"""対象ファイルの入力トークン数を計測する。
使い方: python3 estimate.py <path-or-glob> [...] [--api]
  既定: 文字数ベースの概算（ASCII 4文字≒1トークン、非ASCII 1文字≒1トークン）
  --api: ANTHROPIC_API_KEY があれば count_tokens API で計測（ファイル内容が外部送信される）
"""
import glob
import json
import os
import sys
import urllib.request

EXCLUDE_DIRS = {"build", "dist", "node_modules", "third_party", "vendor", ".git"}
EXCLUDE_EXT = {".log", ".bag", ".bin"}
API_MODEL = os.environ.get("ESTIMATE_MODEL", "claude-sonnet-5")


def iter_files(args):
    for arg in args:
        paths = glob.glob(arg, recursive=True) or [arg]
        for p in paths:
            if os.path.isdir(p):
                for root, dirs, files in os.walk(p):
                    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                    for f in files:
                        yield os.path.join(root, f)
            elif os.path.isfile(p):
                yield p


def excluded(path):
    parts = set(os.path.normpath(path).split(os.sep))
    return bool(parts & EXCLUDE_DIRS) or os.path.splitext(path)[1] in EXCLUDE_EXT


def approx_tokens(text):
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    return ascii_chars // 4 + (len(text) - ascii_chars)


def api_tokens(text, key):
    body = json.dumps({"model": API_MODEL, "messages": [{"role": "user", "content": text or " "}]}).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages/count_tokens",
        data=body,
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)["input_tokens"]


def main():
    args = [a for a in sys.argv[1:] if a != "--api"]
    if not args:
        print(__doc__)
        return 2
    key = os.environ.get("ANTHROPIC_API_KEY") if "--api" in sys.argv else None
    method = "count_tokens API" if key else "文字数ベースの概算"

    rows = []
    for path in sorted(set(iter_files(args))):
        if excluded(path):
            continue
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue  # バイナリ等は対象外
        rows.append((api_tokens(text, key) if key else approx_tokens(text), path))

    total = sum(t for t, _ in rows)
    print(f"方式: {method} / ファイル数: {len(rows)} / 合計: {total:,} tokens")
    print("上位10ファイル:")
    for t, p in sorted(rows, reverse=True)[:10]:
        print(f"  {t:>8,}  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

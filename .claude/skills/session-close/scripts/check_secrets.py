#!/usr/bin/env python3
"""ノートに書く前のテキストから秘密値らしきものを検知する。
使い方: python check_secrets.py <file>   または  echo "text" | python check_secrets.py -
終了コード: 0=検知なし, 1=検知あり
"""
import sys, re

PATTERNS = [
    (r"sk-[A-Za-z0-9_\-]{20,}", "APIキー(sk-)"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
    (r"ghp_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "秘密鍵"),
    (r"[a-z]+://[^/\s:]+:[^@\s]+@", "接続文字列(user:pass@)"),
    (r"(?i)(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*\S{6,}", "password/token/key 代入"),
    (r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{40,}={0,2}(?![A-Za-z0-9+/])", "base64風の長い文字列"),
    (r"\b[0-9a-f]{32,}\b", "16進の長い文字列(ハッシュ/鍵)"),
]

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8", errors="ignore").read()
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for pat, label in PATTERNS:
            if re.search(pat, line):
                hits.append((i, label, line.strip()[:60]))
                break
    if not hits:
        print("OK: 秘密値らしき記述は検知されませんでした"); return 0
    print(f"WARN: {len(hits)} 行に秘密値の可能性")
    for i, label, snippet in hits:
        print(f"  L{i} [{label}] {snippet}...")
    return 1

if __name__ == "__main__":
    sys.exit(main())

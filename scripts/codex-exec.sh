#!/usr/bin/env bash
# Delegate a task described in a handoff note to Codex (non-interactive).
# Usage: scripts/codex-exec.sh <handoff.md> [sandbox: read-only|workspace-write]
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

note="${1:?usage: scripts/codex-exec.sh <handoff.md> [read-only|workspace-write]}"
sandbox="${2:-read-only}"
[ -f "$note" ] || { echo "handoff note not found: $note" >&2; exit 2; }
command -v codex >/dev/null 2>&1 || { echo "codex CLI not found. Run scripts/setup.sh first." >&2; exit 2; }
[ -n "${OPENAI_API_KEY:-}" ] || { echo "OPENAI_API_KEY is not set." >&2; exit 2; }

mkdir -p .agents/reviews
out=".agents/reviews/$(date +%Y%m%d-%H%M%S)-exec-$(basename "$note" .md).md"

codex exec --sandbox "$sandbox" --output-last-message "$out" \
  "AGENTS.md に従い、次の handoff ノートのタスクを実行してください。完了後、ノートの「結果」欄に記入する内容を最終メッセージとして出力してください。

$(cat "$note")"

echo "[codex-exec] result: $out"

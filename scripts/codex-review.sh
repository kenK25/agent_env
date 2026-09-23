#!/usr/bin/env bash
# Run an independent Codex review of the current branch and save it under .agents/reviews/.
# Usage: scripts/codex-review.sh [--uncommitted | base-ref]   (default base: origin/main)
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

command -v codex >/dev/null 2>&1 || { echo "codex CLI not found. Run scripts/setup.sh first." >&2; exit 2; }
[ -n "${OPENAI_API_KEY:-}" ] || { echo "OPENAI_API_KEY is not set; cannot run Codex review." >&2; exit 2; }

# `codex review --base` rejects a custom prompt, so use `codex exec` read-only with the shared review prompt.
if [ "${1:-}" = "--uncommitted" ]; then
  target="未コミットの変更（git diff HEAD と未追跡ファイル）"
else
  base="${1:-origin/main}"
  target="git diff ${base}...HEAD"
fi

mkdir -p .agents/reviews
out=".agents/reviews/$(date +%Y%m%d-%H%M%S)-$(git rev-parse --abbrev-ref HEAD | tr '/' '_').md"

codex exec --sandbox read-only --output-last-message "$out" \
  "$(cat .agents/prompts/review.md)

レビュー対象の差分: ${target}" >/dev/null

cat "$out"
echo
echo "[codex-review] saved: $out"

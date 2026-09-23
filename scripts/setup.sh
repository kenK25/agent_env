#!/usr/bin/env bash
# Shared bootstrap for Claude Code on the web (SessionStart hook) and Codex cloud (environment setup script).
set -euo pipefail

CODEX_VERSION="${CODEX_VERSION:-latest}"

if ! command -v codex >/dev/null 2>&1; then
  if command -v npm >/dev/null 2>&1; then
    npm install -g "@openai/codex@${CODEX_VERSION}" >/dev/null 2>&1 \
      && echo "[setup] installed codex $(codex --version 2>/dev/null)" \
      || echo "[setup] WARN: failed to install @openai/codex (network policy?)"
  else
    echo "[setup] WARN: npm not found; skip codex install"
  fi
else
  echo "[setup] codex present: $(codex --version 2>/dev/null)"
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "[setup] NOTE: OPENAI_API_KEY is not set; Codex review/exec from Claude will be unavailable"
fi

# Project dependencies go below (e.g. npm ci / uv sync).

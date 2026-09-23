@AGENTS.md

# Claude Code 固有の指示

- 共通ルールは上記 `AGENTS.md` に従う。ここには Claude Code 固有の事項のみ書く。
- PR を作る前、またはまとまった実装が終わった時点で、Codex による独立レビューを取る:
  - `/codex-review` スラッシュコマンド、または `bash scripts/codex-review.sh`
  - 結果は `.agents/reviews/` に保存される。blocker / major は対応するか、対応しない理由を PR 本文に書く。
- Codex に作業を切り出す場合は `bash scripts/codex-exec.sh <handoffノートのパス>` を使う（既定は読み取り専用サンドボックス）。
- `OPENAI_API_KEY` が未設定で Codex を呼べない場合は、レビューをスキップしたことを明示して報告する（黙ってスキップしない）。

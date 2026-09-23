---
description: Codex に現在のブランチの独立レビューを依頼し、指摘を整理する
argument-hint: "[--uncommitted | base-branch]"
---

1. `bash scripts/codex-review.sh $ARGUMENTS` を実行する。
2. 失敗した場合（codex 未導入・OPENAI_API_KEY 未設定など）は、原因をそのまま報告して終了する。
3. 成功した場合、Codex の指摘を重大度順に整理し、各指摘について
   - 妥当か（コードを読んで裏を取る。Codex の指摘を鵜呑みにしない）
   - 対応方針（修正する / しない理由）
   を簡潔にまとめる。blocker / major で妥当なものは修正を提案する。

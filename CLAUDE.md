# CLAUDE.md

## トークン節約スキル（Claude Code版）
`.claude/skills/` にある4つのスキルを、次の条件のときだけ使う。

- **発火条件**: 2ファイル以上を読む調査、または2ファイル以上を生成・変更する作業
- **順序**: session-bootstrap → model-router → token-estimate → （作業）→ session-close
- **使わない**: 単発の質問、1ファイルだけの修正、対象ファイルが特定済みの小修正

記録は、リポジトリ直下の `session-notes.md`（索引）と `notes/[task].md` に残す。クラウドのセッションはコンテナが消えるため、session-close で commit・push する。

claude.ai から同期される Cowork版（`anthropic-skills:*`）は Cowork 用なので、このリポジトリではこの Code版を優先する。

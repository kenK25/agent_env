# agent_env — Claude Code × OpenAI Codex 協調クラウド環境

Claude Code（実装主担当）と OpenAI Codex（独立レビュー・並列実装）を、
**同じリポジトリ規約の上で** クラウド実行するためのテンプレートリポジトリです。

## 構成

```
AGENTS.md                      共通ルール（Codex はネイティブに読む / Claude は CLAUDE.md から import）
CLAUDE.md                      Claude Code 固有の指示
.claude/settings.json          SessionStart フック（クラウド時に scripts/setup.sh 実行）・権限
.claude/commands/codex-review.md  /codex-review スラッシュコマンド
.agents/handoff/TEMPLATE.md    エージェント間の引き継ぎノート雛形
.agents/prompts/review.md      Codex レビュー用プロンプト（ローカル・CI 共通）
scripts/setup.sh               共通ブートストラップ（Claude web / Codex cloud 両方から呼ぶ）
scripts/codex-review.sh        Claude から Codex に独立レビューを依頼
scripts/codex-exec.sh          handoff ノートを Codex に非対話実行させる
.github/workflows/codex-review.yml  PR ごとに Codex が自動レビューしてコメント
.github/workflows/claude.yml        @claude メンションで Claude が対応
```

## 協調フロー

```
[人間] Issue/依頼
   │
   ▼
[Claude Code] claude/<topic> で実装 ──(/codex-review)──▶ [Codex] ローカル独立レビュー
   │                                                         │
   │◀──────────────── 指摘（.agents/reviews/）────────────────┘
   ▼
PR 作成 ──▶ [Codex] GitHub Actions で自動レビュー → PR コメント
   │
   ▼
[人間] 指摘を見て `@claude 修正して` ──▶ [Claude] 修正 push ──▶ 再レビュー
   │
   ▼
[人間] マージ判断
```

並列化したい作業は `.agents/handoff/` にノートを書き、Codex cloud か `scripts/codex-exec.sh` に渡します（`codex/<topic>` ブランチ）。

## セットアップ

### 1. GitHub Secrets
| Secret | 用途 |
|---|---|
| `ANTHROPIC_API_KEY` | `claude.yml`（または `claude_code_oauth_token` に差し替え可） |
| `OPENAI_API_KEY` | `codex-review.yml` |

Claude 側 GitHub App は Claude Code で `/install-github-app` を実行すると導入できます。

### 2. Claude Code on the web
- 環境変数に `OPENAI_API_KEY` を設定（Claude から Codex レビューを呼ぶ場合のみ）。
- ネットワークポリシーで `registry.npmjs.org` と `api.openai.com` への到達が必要。
- セッション開始時に `scripts/setup.sh` が自動実行され、Codex CLI が導入されます。

### 3. Codex cloud
- 環境の Setup script に `bash scripts/setup.sh` を指定。
- `AGENTS.md` は自動で読み込まれます。

## 検証状況（2026-09-23 時点）

**事実（一次情報・実機で確認済み）**
- `openai/codex-action@v1` の入力（`openai-api-key` / `prompt-file` / `permission-profile` 等）と出力 `final-message` — 同リポジトリの README・`action.yml`
- `anthropics/claude-code-action@v1` の入力（`anthropic_api_key` / `additional_permissions` 等）— 同リポジトリの `docs/usage.md`
- Codex CLI 0.156.0 の `codex exec --sandbox read-only --output-last-message` が引数として受理されること — 実機で確認
- 同バージョンの `codex review --base/--uncommitted` はカスタムプロンプトと併用不可（実機でエラー確認）。そのためレビューも `codex exec` で実行する設計にしています
- `permission-profile` には Codex CLI 0.138.0 以上が必要 — codex-action README

**未検証 / 推定**
- 実 API キーを使った end-to-end 実行（本リポジトリでは未実施）
- 当初検討した「Codex を MCP サーバーとして Claude に接続」は、0.156.0 の `--help` に `mcp-server` サブコマンドが見当たらないため採用せず、CLI 直接呼び出しにしました。

## 注意
- Codex レビュー用ワークフローは fork からの PR では Secrets が渡らないため動きません（GitHub の仕様）。
- Codex のコメントは `github-actions[bot]` として投稿され、`claude-code-action` は既定で bot のコメントに反応しないため、相互起動の無限ループは起きません。

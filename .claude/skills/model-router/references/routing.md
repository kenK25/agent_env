# routing.md — モデル選定規則（Claude Code版・初期値）

> 出典: Cowork版 model-router の SKILL.md に書かれている既定割当を引き継いだ。昇格・降格の条件は本リポジトリで仮に置いたもので、実績を見て補正する。
> Cowork版の references/routing.md は claude.ai からの同期に含まれていなかったため、参照していない。

## 既定割当
| 種別 | モデル | Agent tool 指定 |
|---|---|---|
| explore | haiku | `subagent_type: "Explore"`, `model: "haiku"` |
| collect | haiku | `subagent_type: "general-purpose"`, `model: "haiku"` |
| generate | sonnet | `subagent_type: "general-purpose"`, `model: "sonnet"` |
| reason | メイン会話 | サブエージェントに出さない |

## 昇格（仮置き）
- generate → opus: セキュリティに関わるコード（認証、暗号、権限）、公開APIやスキーマの設計変更、5ファイル以上にまたがるリファクタ
- collect → sonnet: 一次情報どうしの矛盾を裁く必要がある場合、法規・知財・IPO関連で解釈を要する場合
- explore → sonnet: haiku の返却が2回続けて的外れだった場合

## 降格（仮置き）
- generate → haiku: 定型的な変換（リネーム、フォーマット、テンプレート埋め）

## 補正
- 割当の実績（過不足）は session-close で `session-notes.md` の「見積補正メモ」に1行残し、この表の見直しに使う。

# code-skills

## 目的
- Cowork用の自作スキル4つを Claude Code でも使えるようにする

## 対象パス
- .claude/skills/{session-bootstrap,model-router,token-estimate,session-close}/
- CLAUDE.md

## ADR
### ADR-001: Cowork版とCode版を二重管理にする
- 決定: Code版を `.claude/skills/` にプロジェクトスキルとして置き、発火条件を「2ファイル以上の調査・生成」に絞る
- 理由: Cowork版は description が Cowork 専用のため Code では使われない。Code では毎回使うとかえってオーバーヘッドになる
- 却下案: claude.ai 側の description を1本化する（前提ファイル問題が残り、発火条件も分けられない）

### ADR-002: estimate.py の count_tokens API 利用をオプトインにする
- 決定: `--api` を付け、かつ ANTHROPIC_API_KEY があるときだけ API で計測する。既定は文字数による概算
- 理由: ファイルの中身が外部APIへ送られるため
- 却下案: キーがあれば自動で API を使う（Cowork版の元の仕様）

## 細かい決定
- スキル名は Cowork版と同じにする（Code では接頭辞なしで呼べる。一覧に出ることは確認済み）
- routing.md と formula.md の係数・条件は仮置きと明記する（Cowork版の原本が同期されていないため）
- session-close に commit・push の手順を追加する（クラウドのコンテナは消えるため）

## 未完タスク
- [ ] PR #2 のレビューとマージ（ユーザー判断。監視は不要とのこと）
- [ ] Cowork側で付属ファイルがあるか確認する（引き継ぎプロンプトはユーザーに渡し済み）
- [ ] 新しいセッションで、2ファイル以上の作業でスキルが自動で使われるか確認する
- [ ] formula.md の係数を実績で補正する（3件たまったら「自己計測」に更新）

## 接続・参照先（値は書かない。参照名のみ）
- PR: kenK25/agent_env#2（ブランチ claude/nifty-wright-91brmg）
- 同期先: ~/.claude/skills/synced/<org>_<id>/
- 環境変数: ANTHROPIC_API_KEY（estimate.py --api のときだけ使う）、ESTIMATE_MODEL

## 見積 vs 実績
- token-estimate は使っていない（スキル作成前に始めた作業のため）

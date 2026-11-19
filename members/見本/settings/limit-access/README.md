---
name: limit-access
description: 認証情報ファイルの読み取り、または点検時の書き込みを制限する設定。
---

# 権限を絞る設定

[Claude Code 用の断片](claude-code/settings.fragment.json)は、`.env` と `.env.local` を読む `Read` ツールを制限します。本人が自分の作業フォルダの `.claude/settings.json` の `permissions.deny` に2項目を足します。シェルからの読み取り制限には別のルールが必要です。

[Codex 用の断片](codex/config.fragment.toml)は、資料を読むだけの作業でサンドボックスを書き込み不可にします。本人が信頼済みの作業フォルダの `.codex/config.toml` のトップレベルに足します。同じキーがあれば値を確認し、重ねて書かないようにします。

本人が断片の全文を確認して手で足します。戻す時は、足した項目だけを取り除くか、変更前の値に戻します。

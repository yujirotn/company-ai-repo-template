# 設定の断片

`<設定の名前>/` に、権限や作業範囲など一つの目的に絞った設定を置きます。Claude Code 用は `claude-code/settings.fragment.json`、Codex 用は `codex/config.fragment.toml` のように分けます。

各部品の `README.md` は先頭の `---` で囲んだ `name`（部品名）と `description`（何が変わるか一文）から始めます。本文には書き足す場所、権限の変化、既存の設定と重なる時の注意、戻し方を書き、名札からリンクします。

本人に設定の全文を見せてから、本人が自分の設定に手で足します。鍵、個人専用のパス、ローカル設定全体は共有しません。[権限設定の見本](../../見本/settings/limit-access/README.md)

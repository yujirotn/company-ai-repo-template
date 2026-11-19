---
name: block-inline-key
description: API キーらしい文字列をファイル編集ツールで書き込む前に止める。
---

# 鍵らしい記述を止めるフック

[共通の台本](block_inline_key.py)は、編集内容に `api_key` や `access_token` といった名前で長い値を代入する記述があれば、その値を表示せず編集を止めます。Python 3 が必要です。Claude Code は `Write` と `Edit`、Codex は `apply_patch` の追加行が対象です。シェルや別の編集ツールでの書き込みには別途対策が必要です。

1. 本人が台本と対応する設定断片の全文を読みます。[Claude Code 用](claude-code/settings.fragment.json) / [Codex 用](codex/hooks.fragment.json)
2. 本人が台本を自分の作業フォルダの `scripts/` に置き、既存の `hooks.PreToolUse` にこの項目を手で追記します。Claude Code は `.claude/settings.json`、Codex は `.codex/hooks.json` に足します。Codex の見本は Git 書庫の一番上にある `scripts/` を参照します。起動時のフック確認で内容を確かめます。
3. フックのフォルダで、次のコマンドを使って架空の値を試せます。終了コード `2` で止めた理由が出ます。無害な編集なら終了コード `0` になります。

```bash
python3 -c 'import json; print(json.dumps({"tool_name": "Write", "tool_input": {"content": "api_key = " + repr("sample" * 4)}}))' | python3 block_inline_key.py
```

戻す時は、本人が足した `PreToolUse` の項目を取り除きます。[Claude Code のフック](https://code.claude.com/docs/en/hooks) / [Codex のフック](https://learn.chatgpt.com/docs/hooks)

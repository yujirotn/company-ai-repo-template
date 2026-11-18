# Codexに同じ守りをかける方法

この書庫には、Codex（OpenAIのAIコーディングツール）用の守りが最初から入っています。

| ファイル | 何か |
|---|---|
| `.codex/config.toml` | 書けるのは書庫の中だけ（`sandbox_mode = "workspace-write"`）・囲いの外に出る前に人に確かめる（`approval_policy = "on-request"`）・AI が自分でネットにつながない |
| `.codex/rules/default.rules` | 止めるコマンド（`forbidden`）・確かめるコマンド（`prompt`）の一覧 |
| `.codex/hooks.json` | 開いた時に最新を取ってくる（`SessionStart`）・危ない操作を止める見張り番（`PreToolUse` → `scripts/guardrail.py`） |

1行ずつの説明・外したい時は `docs/おすすめの設定.md` の「6. Codex の設定」を見てください。

**`~/.codex/config.toml`（Codexを使う本人のパソコン全体の設定）は、このひな形からは書き換えません。**
他のChatGPTアプリと共用しているファイルのため、ここを書き換えると他の用途に影響が出るおそれがあるからです。
書庫の中の `.codex/` は、**この書庫だけ**に効きます。

## 効くための条件

- Codex は、この書庫を「信頼する」と答えた後にだけ `.codex/` を読みます（信頼していないと、何を書いても効きません）
- `.codex/hooks.json` は、起動時の「Hooks need review」で中身を確かめて信頼すると動きます。書き換えると、もう一度確認が出ます
- `.codex/rules/` を書き換えた後は、Codex を開き直します

## 別の書庫に入れる時

`.codex/config.toml`・`.codex/rules/default.rules`・`.codex/hooks.json`・`scripts/guardrail.py` の4つを、同じ場所に写します。
`.gitignore` で `.codex/` を除外している場合は、この3つだけ書庫に入るように `!.codex/config.toml` などを足します。

## 限界（正直に書く）

- Codex の囲い（sandbox）は「どこを書けるか」「ネットにつなげるか」を決めるもので、書庫の中を `rm -rf` で消す操作までは防げません。
  そのため、ルール（`prompt`）と見張り番で、まとめて消す操作の前に人を挟みます
- ルール（`.codex/rules/`）は、2026-11 時点で公式が「試験中（experimental）で、変わることがある」としている仕組みです
- 書庫の中の設定は、本人が書き換えれば外せます。会社として外せない形にしたい時は、管理者が
  `/etc/codex/requirements.toml`（Windows は `%ProgramData%\OpenAI\Codex\requirements.toml`）に書きます
- ガードレール（うっかり防止）であり、迂回しようとする行為まで防ぐものではありません

# Codexに同じ守りをかける方法

`templates/settings.json` はClaude Code専用の設定です。Codex（OpenAIのAIコーディングツール）には
別の仕組みで同じ趣旨の守り（秘密ファイルを読ませない・破壊的な操作をさせない）をかけます。

**`~/.codex/config.toml`（Codexを使う本人のパソコン全体の設定）は、このひな形からは書き換えません。**
他のChatGPTアプリと共用しているファイルのため、ここを書き換えると他の用途に影響が出るおそれがあるからです。
代わりに、**リポジトリ単位の設定ファイル**を使います。

## 1. リポジトリ単位の設定ファイルを置く

このリポジトリの中に `.codex/config.toml` を作ると、**このリポジトリだけ**に適用される設定になります
（2026-11-16 時点の公式ドキュメントで確認済み。本人のパソコン全体の設定は変更しません）。

```
company-ai-repo-template/
└── .codex/
    └── config.toml   ← このリポジトリ専用の設定（必要なら作る。ひな形には同梱していない）
```

**注意**: Codexはこのプロジェクト単位の設定を、**そのプロジェクトを「信頼する」と答えた後**にだけ読み込みます
（Codexを初めてこのフォルダで動かした時に出る確認への回答）。信頼していない状態では、ここに何を書いても反映されません。

## 2. 設定の例（ベータ機能）

Codexの「permission profile（権限の名前付きセット）」という仕組みを使うと、ファイルごとに
read（読む）・write（書く）・deny（拒否）を指定できます。**この機能は2026-11-16時点でベータ版**であり、
将来変わる可能性があります。使う前に、手元のCodexのバージョンで実際に動くか確認してください。

```toml
# .codex/config.toml（このリポジトリ専用）
default_permissions = "company-template"

[permissions.company-template.filesystem]
":minimal" = "read"

[permissions.company-template.filesystem.":workspace_roots"]
"." = "write"
"**/.env" = "deny"
"**/.env.*" = "deny"
"**/*.key" = "deny"
"**/*.pem" = "deny"
"**/*credentials*" = "deny"
"**/*secret*" = "deny"
"**/.aws" = "deny"
"**/.ssh" = "deny"

[permissions.company-template.network]
enabled = true
```

- `deny` は `write` より優先され、`write` は `read` より優先されます（具体的な指定が広い指定に勝ちます）。
- ドメイン単位でネットワークを絞りたい場合は `features.network_proxy = true` を加え、
  `[permissions.company-template.network.domains]` に `"送って良い先" = "allow"` のように書きます
  （書かなければ全部許可のままなので、絞りたい場合は明示する）。
- 古い書き方の `sandbox_mode`（`read-only` / `workspace-write` / `danger-full-access`）と、
  この `permissions` の書き方は**どちらか一方だけ**を使います。両方書くと `sandbox_mode` が優先されてしまいます。

## 3. その場限りで試す（`-c` フラグ）

設定ファイルを置かずに、1回の実行だけ制限をかけたい場合は `-c` で上書きできます。

```bash
codex exec -c sandbox_mode="read-only" "このリポジトリの構成を説明して"
```

## 4. `rm -rf` ・`git push --force` の防止について

Codexのpermission profileは「どのファイルを読み書きできるか」「ネットワークにつなげるか」を制御するもので、
Claude Codeの `Bash(rm -rf *)` のような**コマンド文字列そのものの拒否**とは仕組みが異なります。
`sandbox_mode` を `workspace-write` 以下に絞っておけば、このリポジトリの外のファイルを壊すことは防げますが、
**リポジトリの中身を `rm -rf` で消す操作自体は、ファイルシステム権限だけでは防げません**
（書く権限がある以上、書く操作で壊すこともできてしまうため）。
本当に消されたくない場合は、Codexの承認モード（`approval_policy`）を `on-request` 以上の厳しさにして、
破壊的な操作の前に必ず人の承認を挟む運用にしてください。

## 5. この説明の限界（正直に書く）

- ここに書いた `[permissions.*]` の構文は、公式ドキュメントの説明をもとに書いたものです。
  **このひな形自体には `.codex/config.toml` を同梱していません**（本番のキーやパスは会社ごとに違うため）。
  実際に使う前に、自分の手元のCodexで一度動作確認をしてください。
- Claude CodeのBashルールと同じく、ガードレール（うっかり防止）であり、迂回しようとする行為まで防ぐ
  ものではありません。

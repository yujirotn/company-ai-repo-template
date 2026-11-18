# SHO-SAN の道具（見本）

「SHO-SAN では、こういうスキルを全員に配って使っている」という**見本**のプラグインです。
どの会社でも使える形に書き直してあります。そのままインストールして使ってもよいし、
自社の `plugins/common/` や部署の道具を作る時の書き方の参考にしてもかまいません。

## 入っているスキル

| スキルの呼び方 | やること | 使う場面の例 |
|---|---|---|
| `/sho-san:grill` | 計画・設計・決めごとを、共通理解に達するまで1問ずつ詰める。各質問にAIの推奨を添える | 「この計画を詰めて」「グリルして」 |
| `/sho-san:handoff` | 作業の区切りで README に「最近の動き」「未解決事項」を残し、次の会話に貼れる「再開の文」を出す | 「引き継ぎを残して」「今日はここまで」 |
| `/sho-san:nihongo` | メール・お知らせ・提案書・スライド・README など、人に出す日本語を自然に整える | 「この文を nihongo で直して」 |

## インストール

```bash
claude plugin marketplace add ./<この書庫のフォルダ>
claude plugin install sho-san@company-ai-repo-template
```

Codex でも `codex plugin marketplace add ./` → `codex plugin add sho-san@company-ai-repo-template` で
読み込める（スキルだけのプラグインのため。README の「検証結果」を参照）。

## 出典とライセンス

| スキル | 出典 | ライセンス |
|---|---|---|
| `grill` | Matt Pocock の `grilling` / `grill-me`（https://github.com/mattpocock/skills）を日本語の現場向けに書き直した | MIT（`skills/grill/LICENSE`） |
| `handoff` | SHO-SAN の社内スキルを汎用に書き直した | MIT（この書庫の `LICENSE`） |
| `nihongo` | AnIT012 の `nihongo`（https://github.com/AnIT012/nihongo）v2.1.2 を取り込み、説明文だけ絞った | MIT（`skills/nihongo/LICENSE`。変えた所は `skills/nihongo/UPSTREAM.md`） |

原典があるスキルを自社用に直す時も、`LICENSE` と出典の表記は消さずに残してください。

## 要らない時

このプラグインは見本なので、使わない会社は `.claude-plugin/marketplace.json` の `sho-san` の行を消し、
このフォルダごと消してかまいません。

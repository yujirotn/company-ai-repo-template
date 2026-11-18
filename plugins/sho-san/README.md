# SHO-SAN の道具（見本）

「SHO-SAN では、こういうスキルを全員に配って使っている」という**見本**のプラグインです。
どの会社でも使える形に書き直してあります。そのままインストールして使ってもよいし、
自社の `plugins/common/` や部署の道具を作る時の書き方の参考にしてもかまいません。

## 入っているスキル（13本・3つのまとまり）

見た目（色・書体）は会社の `DESIGN.md`、置き場所は `CLAUDE.md` / `AGENTS.md` に従うように書いてあります。

### 仕事の進め方
| スキルの呼び方 | やること | 使う場面の例 |
|---|---|---|
| `/sho-san:grill` | 計画・設計・決めごとを、共通理解に達するまで1問ずつ詰める。各質問にAIの推奨を添える | 「この計画を詰めて」「グリルして」 |
| `/sho-san:handoff` | 作業の区切りで README に「最近の動き」「未解決事項」を残し、次の会話に貼れる「再開の文」を出す | 「引き継ぎを残して」「今日はここまで」 |
| `/sho-san:nihongo` | メール・お知らせ・提案書・スライド・README など、人に出す日本語を自然に整える | 「この文を nihongo で直して」 |
| `/sho-san:org-rebuild` | AI の作業環境（ハーネス）を、点検 → グリル → 移行 → 再点検の流れで作り直す。30分版もある | 「AI の環境を作り直したい」 |
| `/sho-san:proposal-duplication` | 提案の前に、相手の頭の中（悩み・信じていること・恐れていること）から構成を組む壁打ち | 「〇〇さんへの提案を組みたい」 |

### 資料作成
| スキルの呼び方 | やること | 使う場面の例 |
|---|---|---|
| `/sho-san:visual-design` | 資料・画面の見た目（文字・余白・階層・色）を作る・直す・点検する時の原則 | 「見た目を整えて」 |
| `/sho-san:explain-visual` | 仕組みや考え方を「大きな図＋少ない文字」の1枚で見せる図解 | 「これを図解して」 |
| `/sho-san:slide-deck-create` | 16:9 の横めくりのスライドを HTML 1枚で作る（見本つき） | 「研修のスライドを作って」 |
| `/sho-san:doc-kit` | 会社紹介・戦略共有・仕組みの図解を、会社の色とロゴで「縦（A4・配る）」と「横（16:9・映す）」の両方で作る（見本つき） | 「会社紹介を縦と横で作って」 |
| `/sho-san:stack-diagram` | 道具やサービスのつながりを、本物のロゴ入りの構成図で描く | 「仕組みの構成図を描いて」 |

### 画面づくり
| スキルの呼び方 | やること | 使う場面の例 |
|---|---|---|
| `/sho-san:ux-review` | 画面が人にとって分かりやすいかを、実際に操作して12の観点で点検する（設計とレビューの2つのやり方） | 「この画面、使いやすい？」 |
| `/sho-san:design-review` | 見た目を `DESIGN.md` に照らして10の観点で点検する | 「デザインを点検して」 |
| `/sho-san:web-preflight` | 公開前に、メタ情報・リンク切れ・仮の文言・画像の説明などを機械で点検する | 「公開前に点検して」 |

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
| `org-rebuild` | SHO-SAN の社内スキルを汎用に書き直した。点検には公開の道具 [harness-check](https://github.com/yujirotn/harness-check) を使う | MIT（この書庫の `LICENSE`） |
| `stack-diagram` | caru-ini の stack-diagram を日本語に書き直し、外部への投稿の機能と同梱フォントを外した | MIT（`skills/stack-diagram/LICENSE`） |
| `doc-kit` | SHO-SAN の社内の資料作成キットと図解の型を汎用に書き直した。見本のアイコンは [Lucide](https://lucide.dev) | MIT（この書庫の `LICENSE`）。アイコンは ISC（`skills/doc-kit/assets/LICENSE-lucide.txt`） |
| `visual-design`・`explain-visual`・`slide-deck-create`・`proposal-duplication`・`ux-review`・`design-review`・`web-preflight` | SHO-SAN の社内スキルを汎用に書き直した（design-review・web-preflight は一から書き直し） | MIT（この書庫の `LICENSE`） |
| `nihongo` | AnIT012 の `nihongo`（https://github.com/AnIT012/nihongo）v2.1.2 を取り込み、説明文だけ絞った | MIT（`skills/nihongo/LICENSE`。変えた所は `skills/nihongo/UPSTREAM.md`） |

原典があるスキルを自社用に直す時も、`LICENSE` と出典の表記は消さずに残してください。

## 要らない時

このプラグインは見本なので、使わない会社は `.claude-plugin/marketplace.json` の `sho-san` の行を消し、
このフォルダごと消してかまいません。

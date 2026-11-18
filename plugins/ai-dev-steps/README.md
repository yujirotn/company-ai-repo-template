# 開発の手順 1〜9（ai-dev-steps）

AI と一緒に道具やサービスを作る時の手順を、**1段1スキル**にしたプラグインです。
家づくりと同じで、先に図面（`docs/`）を描き、図面どおりに建て、建てた人とは別の目で検査します。
後から思いつきで足すと、違法建築のように、直すたびに別の所が壊れるからです。

覚えるのは入口の **`dev-start`** だけです。`docs/` の中を見て、「今どの段か・次に何をするか」を教えてくれます。

Claude Code と Codex のどちらでも使えます（スキルだけでできています）。

## 全体の図

```
 1 コンセプト ─ 2 仕様 ─ 3 画面 ─ 4 試作 ─ 5 価値の検証 ─ 6 本番の実装 ─ 7 価格 ─ 8 デザイン ─ 9 攻撃して直す
 施主の要望    要望書と   間取り図   模型      住む人に見て     1部屋ずつ施工    見積もり   内装・外観    防犯の点検
 を聞く        構造の仕様  パース              もらう          して検査
                                              (売るものだけ)                   (売るものだけ)
```

| 段 | やること | 家づくりでいうと | スキル | できるもの |
|---|---|---|---|---|
| ─ | 今どの段か・次は何かを教える | 現場の工程表 | `dev-start` | （何も作らない） |
| 1 | 誰の、どんな困りごとを、どう解くか | 施主の要望を聞く | `dev-concept` | `docs/00-コンセプト.md` |
| 2 | 戦略・要件・構造の3層で仕様を決める | 要望書・構造と設備の仕様 | `dev-spec` | `docs/01-要件.md`・`docs/03-データ.md` |
| 3 | 線だけの画面の下書きを3案並べて選ぶ | 間取り図・パース | `dev-wireframe` | `docs/02-画面.md`・`docs/wireframes/画面案.html` |
| 4 | 架空のデータで、まず一通り動くもの | 模型・モデルルーム | `dev-prototype` | 試作のコード・`docs/04-完成条件.md`（試作の分） |
| 5 | 毎日使うか・無くなったら困るかを5段階で聞く | 住む人に模型を見てもらう | `dev-validate` | `docs/05-検証.md` |
| 6 | 完成条件を先に決め、別の AI に厳しく点検させる | 1部屋ずつ施工して検査 | `dev-build` | 本番のコード・`docs/04-完成条件.md`・`docs/reviews/` |
| 7 | 費用と利益の試算・プランの配分・値段の感じ方 | 見積もり | `dev-pricing` | `docs/06-価格.md` |
| 8 | 雰囲気の見本 → 決まり → 画面 | 内装・外観 | `dev-design` | 書庫の一番上の `DESIGN.md` |
| 9 | 自分の練習環境だけを、別の AI に攻めさせて直す | 防犯の点検 | `dev-attack` | `docs/reviews/攻撃-<日付>.md` |

`docs/` の場所は、書庫に `projects/` があれば `projects/<仕事の名前>/docs/`、無ければ今のフォルダの `docs/` です。仕事の名前は、段1で自分で日本語で付けます（例: `projects/備品の貸し出し記録/docs/`）。

### 社内で使う道具なら、5 と 7 は飛ばす

5（価値の検証）と 7（価格）は、**売るもの**（社外の人がお金を払うもの）の時だけの段です。
社内で使う道具なら飛ばしてかまいません。段1で「種類」を聞かれるので、そこで「社内で使う道具」と答えれば、`dev-start` が自動で飛ばします。

## どの段でも守ること

- **設計を変える時は、先に図面（docs）を直してからコードを直す**
- **直す前に、なぜそうなったか（根本原因）を説明してから直す**
- **分からないことは作らずに聞く**。1問ずつ、AI の推奨を添えて聞く
- **鍵（パスワード・API キー・トークン・.env の中身）を docs にもコードにも書かない**。書くのは「どこに置いたか」だけ
- **攻撃（段9）は、自分で作った道具を、自分の練習環境でだけ**。最初に必ず確かめる

## 入れ方

この書庫（会社の書庫のひな形）の目録に入っています。書庫のフォルダで次を打ちます。

**Claude Code**

```bash
claude plugin marketplace add ./
claude plugin install ai-dev-steps@company-ai-repo-template
```

画面の中なら `/plugin install ai-dev-steps@company-ai-repo-template` でも入ります。入れた後は `/reload-plugins` か、開き直します。

**Codex**

```bash
codex plugin marketplace add ./
codex plugin add ai-dev-steps@company-ai-repo-template
```

新しくなった時は、`codex plugin add ai-dev-steps@company-ai-repo-template` をもう一度打つと入れ直せます。

## 呼び方

| | 呼び方 | 例 |
|---|---|---|
| Claude Code | `/ai-dev-steps:<スキル名>`、または言葉で頼む | `/ai-dev-steps:dev-start`／「新しい道具を作りたい。次は何をすればいい？」 |
| Codex | `$ai-dev-steps:<スキル名>`、または言葉で頼む | `$ai-dev-steps:dev-start`／「dev-start で今の段を教えて」 |

どちらも、言葉で頼めば合うスキルを AI が選びます。迷ったら「dev-start で、今どの段か教えて」と頼んでください。

## ほかの道具との関係

- **全社共通の `start-from-spec`**（4枚の仕様書を一気に埋める短い道）と、同じ `docs/` の見出しを使っています。どちらで作った docs も、もう一方でそのまま続けられます
- **入っていれば使う・無くても回る**もの:
  - `grill`（1問ずつ詰める）・`ux-review`・`design-review`・`visual-design`（見本の道具箱に入っている場合）
  - Claude Code の公式プラグイン `feature-dev`・`code-review`・`frontend-design`・`security-guidance`・`claude-security`、組み込みの `/code-review`・`/security-review`
  - Codex の `codex-security`
- 段6と段9の「別の目」は、専用の点検役の部品を使わず、**新しい AI を起こして読ませる**やり方で書いてあります。Claude Code ならサブエージェント、Codex ならサブエージェントか新しい `codex exec`、どちらでも新しい会話に依頼文を貼れば同じことができます

## 中身

```
ai-dev-steps/
  .claude-plugin/plugin.json
  README.md            この説明
  NOTICE.md            考え方を借りた元の一覧
  skills/
    dev-start/         入口
    dev-concept/       1 コンセプト
    dev-spec/          2 仕様
    dev-wireframe/     3 画面
    dev-prototype/     4 試作
    dev-validate/      5 価値の検証（売るものだけ）
    dev-build/         6 本番の実装
    dev-pricing/       7 価格（売るものだけ）
      scripts/price_check.py   費用と利益の試算・値段の感じ方の集計（Python だけで動き、外には何も送らない）
      assets/例_*.csv          入力の例（数字はすべて例）
    dev-design/        8 デザイン
    dev-attack/        9 攻撃して直す
```

## ライセンス

MIT（この書庫の `LICENSE`）。考え方を借りた元は `NOTICE.md` にまとめています。

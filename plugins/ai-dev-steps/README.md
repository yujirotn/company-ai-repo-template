# 開発の手順 1〜9（ai-dev-steps）

AI と一緒に道具やサービスを作る時の手順を、**1段1スキル**にしたプラグインです。
家づくりと同じで、先に図面（`docs/`）を描き、図面どおりに建て、建てた人とは別の目で検査します。
後から思いつきで足すと、違法建築のように、直すたびに別の所が壊れるからです。

覚えるのは入口の **`dev-start`** だけです。`docs/` の中を見て、「今どの段か・次に何をするか」を教えてくれます。

Claude Code と Codex のどちらでもスキルを使えます。Claude Code には、仕様とコードを読む点検役も同梱しています。

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
| 3 | 論点ごとに画面の見本を3案横に並べて選ぶ（画面えらびのページ） | 間取り図・パース | `dev-wireframe` | `docs/02-画面.md`・`docs/wireframes/画面えらび.html`・`画面案.html` |
| 4 | 架空のデータで、まず一通り動くもの | 模型・モデルルーム | `dev-prototype` | 試作のコード・`docs/04-完成条件.md`（試作の分） |
| 5 | 毎日使うか・無くなったら困るかを5段階で聞く | 住む人に模型を見てもらう | `dev-validate` | `docs/05-検証.md` |
| 6 | 完成条件を先に決め、別の AI に厳しく点検させる | 1部屋ずつ施工して検査 | `dev-build` | 本番のコード・`docs/04-完成条件.md`・`docs/reviews/` |
| 7 | 費用と利益の試算・プランの配分・値段の感じ方 | 見積もり | `dev-pricing` | `docs/06-価格.md` |
| 8 | 雰囲気の見本 → 決まり → 画面 | 内装・外観 | `dev-design` | 会社の `DESIGN.md` を当てる（無ければ `docs/デザイン.md`。会社の決まりは書き換えない） |
| 9 | 攻める側の目で仕様とコードを読み、守りを直す | 防犯の点検 | `dev-attack` | `docs/reviews/攻撃-<日付>.md` |

仕事の場所を指定した場合は、各スキルはそこを使います。新しい仕事は、段1で日本語の名前を付けて書庫の `projects/<仕事の名前>/` に作ります（例: `projects/備品の貸し出し記録/`）。その仕事の入口は `README.md` です。各スキルが今の段・進み具合・最近の動きを書き足します。仕様は `docs/`、試作は `prototype/`、本番は `app/` に置きます。

### 社内で使う道具なら、5 と 7 は飛ばす

5（価値の検証）と 7（価格）は、**売るもの**（社外の人がお金を払うもの）の時だけの段です。
社内で使う道具なら飛ばしてかまいません。段1で「種類」を聞かれるので、そこで「社内で使う道具」と答えれば、`dev-start` が自動で飛ばします。

## どの段でも守ること

- **設計を変える時は、先に図面（docs）を直してからコードを直す**
- **直す前に、なぜそうなったか（根本原因）を説明してから直す**
- **分からないことは作らずに聞く**。1問ずつ、AI の推奨を添えて聞く
- **鍵（パスワード・API キー・トークン・.env の中身）を docs にもコードにも書かない**。書くのは「どこに置いたか」だけ
- **段の終わりは、本人の OK が出るまで次へ進まない**。方向を変えたい時は、その段か前の段の docs から直す
- **段9の点検役は仕様とコードを読む**。読む点検だけの進み具合は「一部（読む点検のみ）」です

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

| 置き方 | Claude Code | Codex |
|---|---|---|
| プラグインとして入れた場合 | `/ai-dev-steps:dev-start` | `$ai-dev-steps:dev-start` |
| スキルを直接置いた場合 | `.claude/skills/` に置いて `/dev-start` | `.agents/skills/` に置いて `$dev-start` |

次の段も同じ形式で、`dev-start` をその段のスキル名に替えて呼びます。「dev-start で、今どの段か教えて」と言葉で頼むこともできます。

書庫の親フォルダで開くと、子フォルダに直接置いたスキルが見つからないことがあります。対象の書庫か仕事のフォルダで新しく開くか、同梱の `plugins/ai-dev-steps/skills/dev-start/SKILL.md` のパスを示して「この手順で進めて」と頼んでください。

## ほかの道具との関係

- **入っていれば使う・無くても回る**もの:
  - `grill`（1問ずつ詰める）・`ux-review`・`design-review`・`visual-design`（見本の道具箱に入っている場合）
  - Claude Code の公式プラグイン `feature-dev`・`code-review`・`frontend-design`・`security-guidance`・`claude-security`、組み込みの `/code-review`・`/security-review`
  - Codex の `codex-security`
- 段6と段9では、Claude Code は同梱の点検役、Codex は利用できる場合に組み込みのサブエージェントを使います。同梱の点検役やサブエージェントを使えない場合は、各スキルの依頼文で別の AI に読む点検を頼めます

## 中身

```
ai-dev-steps/
  .claude-plugin/plugin.json
  README.md            この説明
  NOTICE.md            考え方を借りた元の一覧
  agents/              Claude Code 用の読む点検役
    build-reviewer.md    段6 作りを見る
    security-reviewer.md 段6 守りを見る
    attacker.md          段9 攻める側の目で守りを見る
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

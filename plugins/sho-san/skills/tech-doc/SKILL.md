---
name: tech-doc
description: 技術の解説・研修の教材・仕組みの説明を、数式・コード・図を含むHTML1枚として作る・直すスキル。研修の教材、エンジニア向けの引き継ぎ資料、用語の定義から順に説明する文書、社内のナレッジ集に使う。「教材を作って」「仕組みを解説して」「技術資料をHTMLで」と言われた時に使う。提案書・定例報告・図解1枚もの・スライドには使わない（その会社の DESIGN.md に従って作る）。
---

# tech-doc ─ 技術解説・教材のHTML

> 原典: mathbullet/skills の `html` スキル（https://github.com/mathbullet/skills 、MIT License）。
> 「この会社での使い方」を足し、本体は原典の決まりを日本語でそのまま残した。ライセンス表記は同じフォルダの `LICENSE` を参照。

---

## この会社での使い方（本体より先に読む）

### 使う／使わない

| 使う | 使わない |
|---|---|
| 研修の教材 | 社外に出す提案書・定例資料・分析レポート（→ その会社の `DESIGN.md` に従う） |
| エンジニア向けの引き継ぎ・設計の解説 | 大きな図1枚と少ない文字の図解 |
| 用語の定義から入る、概念・仕組みの解説 | めくるスライド |
| 数式・コード・差分を含む文書 | 履歴・記録・仕事の管理（→ Markdown） |
| 社内のナレッジ集（困った時の対処集など） | |

**決め手は「読み手が社内か社外か」ではなく、「技術的な中身を、用語の定義から順に説明する文書か」。**
社内向けでも、経営層への報告や意思決定の資料は `DESIGN.md` に従って作る。

### 会社の DESIGN.md との関係

このスキルは自分専用の見た目の決まり（`design-system/`）を持つ。教材・解説の中で見た目がそろうことに価値があるため。
作り始める前に、その会社の `DESIGN.md` を読み、次のどちらかを決める。

- `DESIGN.md` に「技術解説・教材はこの見た目で」という決まりがあれば、それに従う
- 決まりが無ければ、このスキルの `design-system/` をそのまま使う。**色だけ会社の色に寄せる、などの混ぜ方はしない**（混ぜると両方が崩れる）。会社の色に合わせたい時は、`document.css` の `:root` の色の値をまとめて差し替える
- 迷ったら、作る前に担当者に聞く

どちらの場合も、次は守る。

- 絵文字・矢印の文字を図の記号に使わない（記号はインラインSVGで描く）
- 赤の強調は1ページ1か所まで
- 飾りだけのイラストを入れない
- `DESIGN.md` の言葉づかい・書いてはいけないこと（社名・人名・数字の扱いなど）

### 置き場所

- 置き場所はその会社の `CLAUDE.md`・各仕事の `README.md` に従う。決まりが無ければ、その仕事のフォルダの `docs/` に置く
- 書庫の一番上に直接置かない
- ファイル名は `{yyyymmdd}-{内容を表す英小文字とハイフン}.html`

### design-system の置き方

できあがりのHTMLと同じフォルダに `design-system/` をコピーし、相対パスで読み込む。
**同じフォルダの複数のHTMLで1組を共有してよい**。すでにあればコピーし直さない。

```bash
cp -R "<このスキルのフォルダ>/design-system" "<置き場所のフォルダ>/design-system"
```

### 確かめ方（ここで必ずつまずく）

**エディタのプレビューでは正しく表示されないことが多い。** 中身だけを読み込むため、`./design-system/document.css` の相対パスが解決せず、CSSが当たらない素のHTMLに見える。
**ブラウザで `file://` から開くか、ヘッドレスのChrome で画像にして確かめる。**

```bash
# macOS の例。Chrome の場所はパソコンに合わせて変える
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=8000 \
  --window-size=1280,5200 --screenshot="<置き場所>/check.png" \
  "file://<HTMLの絶対パス>"
```

長いページは分けて見る。**目で見るのは必須**（日本語の折り返しの崩れ・表の列落ちを見る）。確かめ用の画像は、できあがりと一緒に残さない。

### できあがる前のチェック

| # | 項目 | 確かめ方の例 |
|---|---|---|
| 1 | 赤の強調（`<em>`）は1か所だけか | `grep -o '<em>' F \| wc -l` |
| 2 | 絵文字・矢印の文字が混ざっていないか | `grep -oE '[→←↑↓⇒✅❌⚠️★●▼]' F \| wc -l` |
| 3 | 表は3列までか | 目で見る |
| 4 | 目次の `href="#..."` と h2 の `id` がそろっているか | `grep -o 'id="[a-z-]*"' F` と `grep -o 'href="#[a-z-]*"' F` |
| 5 | 用語の一覧が `aside.mb-glossary` にあるか | 目で見る |
| 6 | ブラウザで表示を目で見たか | 上のコマンド |

### 人に渡す・公開する時

**HTML1枚では完結しない**（CSS と JS が別のファイル）。

- ファイルで渡す → `design-system/` フォルダごと渡す
- URL で公開する → `design-system/` も一緒に置く。**HTMLだけ置くと素のHTMLになる**
- 公開・社外への送付は、取り消しにくい外向きの操作。**本人の指示がある時だけ行い、公開先はその会社の決まりに従う**

### PDF にする

`scripts/render-pdf.sh <html>`（ヘッドレスのChrome で印刷してPDFにする。macOS の Chrome の場所を探す。外への送信はしない）。
**本人から頼まれた時だけ実行する。**
Chrome が無い・macOS 以外の時は、ブラウザで開いて「印刷 → PDFに保存」を使う（`document.css` に印刷用の決まりが入っている）。

---

# 本体 ─ HTML による説明の文書

## 文章

説明の中身と日本語の書き方を補うため、次の併用を勧める（必須ではない）。

- `nihongo`：日本語の文章の書き方
- 用語の定義・説明の細かさ・構成をそろえる、技術文書の書き方の決まり（会社に決まりがあればそれ）

## できあがり

- HTML を作る
- ビルドなしで、ブラウザがそのまま表示できる状態にする
- 置き場所の指定があれば従う。無ければ上の「置き場所」に従う
- ファイル名は `{yyyymmdd}-{内容を表す英小文字とハイフン}.html`。既存のファイルを直す時は名前を変えない

## デザインシステム

作る前に `design-system/component-samples.html` をブラウザで開いて見る。部品の集まりは `design-system/document.css`、数式のコピー機能は `design-system/math-copy.js` を正とする。

既定では、できあがりと一緒に必要なファイルを置き、次の相対パスで読み込む。

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Ubuntu+Sans:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&family=Ubuntu+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./design-system/document.css">
<script src="./design-system/math-copy.js"></script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>
<script>document.addEventListener("DOMContentLoaded", () => hljs.highlightAll());</script>
```

> 文字・数式・コードの色付けは、ネット上の配布元（Google Fonts・jsDelivr・cdnjs）から読み込む。ネットにつながらない場所で見る時は、文字が別の書体になり、数式が `$...$` のまま見える。

主な決まりは次のとおり。

- 背景は `#FAF9F6`。部品は白地・黒の罫線・角丸を基本にする
- 文章は Ubuntu Sans と Noto Sans JP、コード・URL・日付は Ubuntu Mono
- 色はリンクの青 `#2990DA` と強調の赤 `#D63A2F` だけ
- 赤の強調は、原則1ページ1か所まで
- コードの色付けと差分の色は、意味を分けるための色なので、この制限の外
- 余白は上下左右のつり合いを保つ
- 引用は `.mb-quote` を使い、原文と訳を同じ文字の大きさ・色で上下に並べる
- `.mb-chip` は、並んだ固有名や分類名を並べる時だけ使う
- 絵文字や矢印の文字を図の記号に使わない。記号はインラインSVGで描く
- 表は短い対応関係に使い、3列までを基本にする
- 行の見出しのセルには `.mb-rowlabel` を付け、語の途中で折り返さないようにする
- コードの差分は `pre.mb-diff` を使い、変えた理由を文章で説明してから、必要な部分だけ示す
- そのページだけの `<style>` は、図の配置の調整など最小限にとどめる

## 構成と書式

説明する中身に合わせて、並べて比べる・図にする・時系列・まとめ・折りたたみを使い分ける。
一方向の単純な手順を、必要もないのに流れ図にしない。

基本の順は次のとおり。

1. 用語の一覧
2. 背景
3. 本論
4. 具体例
5. 補足・限界・関係する事柄

h1 とリード文の後に `.mb-toc` の目次を置き、各 h2 に対応する `id` を付ける。
用語の一覧は `.mb-wrap` の中の `aside.mb-glossary` に置く。
専門用語は、本文で使う前に1〜2文で定義する。

## 図

- `.mb-figure` は、画像・SVG などの資料とキャプションを1つにまとめる外枠。特定の図の形や「矢印で結んだ箱」を意味しない
- `.mb-figure-frame` は資料を見せる面、`figcaption` は図の番号・説明・出どころを書く所
- 元の資料に大事な図がある時は、出どころを書いて引用する
- 元の図があるのに、まねた図を作らない
- 自分で描く図はインラインSVGにし、記号を並べた文字の絵（アスキーアート）を使わない
- 黒一色の線画を基本にし、`.mb-figure-frame` に載せる
- 箱が多い時は縦に並べる
- 矢印が交差する形を避ける
- ただの一直線の手順は、番号つきの説明にする

## コード

- Highlight.js を必ず読み込み、言語に合わせて色を付ける
- `pre code` には `language-javascript`・`language-python`・`language-html` などの言語のクラスを必ず付ける
- 色を付けない文字には `language-plaintext` を付ける
- 自分で色を付けて飾らず、`document.css` の `.hljs-*` の決まりを使う
- `pre.mb-diff code` には `nohighlight` を付け、差分用の色と行頭の記号を使う

## 数式

- MathJax 3 を使う
- 文中の数式は `$...$`、行を分けて見せる数式は `$$...$$`
- ベクトルと行列は `\boldsymbol{...}` を使う
- スカラー・添字・集合の名前は飾らない
- 名前のついた演算は `\mathtt{...}`、標準の LaTeX のコマンドはそのまま使う
- `math-copy.js` で、すべての数式から LaTeX の元の文をコピーできるようにする
- ページの側で `window.MathJax` を定義し直さない
- 知らないコマンドを、勝手に別の書き方に置き換えない

## 印刷と PDF

印刷の見た目は `document.css` の `@media print` を使う。
PDF にするのは、本人から頼まれた時だけ `scripts/render-pdf.sh` を実行する。

# 図の型の見本帳

毎回ゼロから図を描かない。**型を6つに絞り、写して中身を差し替える**。

## 色（まず DESIGN.md に合わせる）

下の見本は、仮の色（黒・灰・強調色1つ）で書いてある。作る時は `DESIGN.md` の色に置き換える。
**SVG の `fill`・`stroke` の属性には CSS 変数が効かない**ので、色は直接の値で書く（置き換える時は、ファイル全体で一括置換する）。

| 役割 | 仮の色 | DESIGN.md のどれに当てるか |
|---|---|---|
| 文字・線・濃い塗り | `#231815` | 文字の色 |
| 補足の文字・2段目の塗り | `#655E5B` | 文字の色を薄めたもの |
| 薄い文字・3段目の塗り | `#9C9591` | 〃 |
| 強調（一番見てほしい1種類だけ） | `#C7161D` | 強調の色 |
| 罫線 | `#E7DEDA` | 線の色 |
| 薄い面 | `#FAF8F6` | 地の色に近い薄い色 |
| 終わり・うまくいった | `#15803d` | 決まりが無ければこのまま |
| 戻り・注意 | `#b45309` | 決まりが無ければこのまま |

## 図の描き方（図が主役）

- **文章で3行を超えるなら図にする**。図はページの中に書いた SVG で描く
- **強調色は「その図で一番見てほしい1種類」だけ**に使う（例: AI が受け持つ工程、一番効く制限）。ほかは黒・白抜き・灰で描き分ける
- 担い手の区別は **黒塗り／白抜き／強調色の塗り** の3つまで。補助の情報は図から外して、カードや表に回す
- 流れは**1本の線でつなぐ**（角を丸めた折れ線）。分かれ道は細い点線で控えめに
- 役割分担は、担い手ごとの横の帯（レーン）に工程を並べる**路線図の形**にする
- 判定の流れは大きなひし形を並べず、**縦の線に小さな印を並べたはしごの形**（問い → 矢印 → 右に答えの箱）
- 「A ごとに B が違う」は**一覧表**にする。当てはまらない所は薄い文字の「なし」
- 文字のカードを並べるだけにしない

## 共通の決まり（これを外すと崩れる）

| 項目 | 決まり |
|---|---|
| 入れ物 | 標準は `<div class="compare-box">`（薄い地・SVG が幅いっぱいに縮む）。横長は `<div class="roadmap-scroll">`（最小幅 860px で、狭い画面では横にスクロール） |
| viewBox | `.compare-box` → **`0 0 720 {高さ}`** ／ `.roadmap-scroll` → **`0 0 1000 {高さ}`**。この2つ以外を使わない |
| 文字の大きさ | 図の題 15 / ノード名 13 / 補足 11。**11 より小さくしない**（375px で潰れる） |
| 強調色 | 「最重要」「一番の近道」「おすすめ」だけ。3か所以上あったら使いすぎ |
| 読み上げへの配慮 | `role="img"` と `aria-label="{図の中身を文章で全部}"` が**必須**。印刷が崩れた時の保険にもなる |
| 文字数 | 1ノードは**全角8文字以内**。入らないなら考えを分ける（文字を小さくしない） |

入れ物の CSS（ページの `<style>` に入れる）:

```css
.compare-box { background:#FAF8F6; border-top:1px solid #E7DEDA; border-bottom:1px solid #E7DEDA; padding:16px; }
.compare-box svg { width:100%; height:auto; display:block; }
.roadmap-scroll { overflow-x:auto; -webkit-overflow-scrolling:touch; }
.roadmap-scroll svg { min-width:860px; width:100%; height:auto; display:block; }
.table-scroll { overflow-x:auto; }
```

---

## ① 流れ図 — 処理・データの流れ

**番号付きの箱を CSS で横一列に並べる**（罫線と矢印）。3〜5段。

分かれ道・戻り・同時に進む所があるなら、一列の箱では表せないので、**⑥状態の移り変わり**か、下の SVG 版にする。

### SVG 版（分かれ道あり）

```html
<div class="compare-box">
  <svg viewBox="0 0 720 220" role="img" aria-label="入力が判定に入り、条件を満たせば処理Aへ、満たさなければ処理Bへ分かれ、どちらも保存に合流する流れ図。">
    <defs>
      <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="#231815"/>
      </marker>
    </defs>
    <g font-size="13" font-weight="700" text-anchor="middle">
      <rect x="20" y="86" width="118" height="48" rx="8" fill="#231815"/><text x="79" y="115" fill="#fff">入力</text>
      <path d="M144 110 H188" stroke="#231815" stroke-width="2" marker-end="url(#ar)"/>
      <polygon points="256,74 322,110 256,146 190,110" fill="#fff" stroke="#231815" stroke-width="2"/>
      <text x="256" y="115" fill="#231815">判定</text>
      <path d="M256 70 V40 H452" stroke="#231815" stroke-width="2" marker-end="url(#ar)"/>
      <text x="350" y="32" font-size="11" fill="#15803d">条件を満たす</text>
      <path d="M256 150 V180 H452" stroke="#231815" stroke-width="2" marker-end="url(#ar)"/>
      <text x="350" y="196" font-size="11" fill="#b45309">満たさない</text>
      <rect x="458" y="16" width="118" height="48" rx="8" fill="#655E5B"/><text x="517" y="45" fill="#fff">処理A</text>
      <rect x="458" y="156" width="118" height="48" rx="8" fill="#9C9591"/><text x="517" y="185" fill="#fff">処理B</text>
      <path d="M582 40 H630 V104" stroke="#231815" stroke-width="2" marker-end="url(#ar)"/>
      <path d="M582 180 H630 V136" stroke="#231815" stroke-width="2" marker-end="url(#ar)"/>
      <rect x="572" y="106" width="118" height="28" rx="8" fill="#C7161D"/><text x="631" y="126" fill="#fff" font-size="12">保存</text>
    </g>
  </svg>
</div>
```

> 角を丸めるか（`rx`）は `DESIGN.md` に合わせる。決まりで角丸を使わないなら `rx` を外す。

---

## ② 層の図 — 階層・受け持ちの分担

「上から下へ」で**抽象→具体**、または**使う人→土台**の順に積む。3〜5層。
各層の右に「ここで何が起きるか」を1行添えると、ぐっと分かりやすくなる。

```html
<div class="compare-box">
  <svg viewBox="0 0 720 268" role="img" aria-label="4層の図。上から順に、使う人が触る層、判断する層、処理する層、データを置く層。右側に各層の役割を書いている。">
    <text x="360" y="20" text-anchor="middle" font-size="15" font-weight="700" fill="#231815">{{システム名}}の4層</text>
    <g font-size="13" font-weight="700">
      <rect x="40" y="36" width="360" height="46" rx="8" fill="#231815"/>
      <text x="220" y="64" fill="#fff" text-anchor="middle">{{第1層（例: 画面）}}</text>
      <text x="416" y="64" font-size="11.5" font-weight="600" fill="#655E5B">{{ここで何が起きるか}}</text>

      <rect x="40" y="92" width="360" height="46" rx="8" fill="#655E5B"/>
      <text x="220" y="120" fill="#fff" text-anchor="middle">{{第2層（例: 判断）}}</text>
      <text x="416" y="120" font-size="11.5" font-weight="600" fill="#655E5B">{{ここで何が起きるか}}</text>

      <rect x="40" y="148" width="360" height="46" rx="8" fill="#9C9591"/>
      <text x="220" y="176" fill="#fff" text-anchor="middle">{{第3層（例: 処理）}}</text>
      <text x="416" y="176" font-size="11.5" font-weight="600" fill="#655E5B">{{ここで何が起きるか}}</text>

      <rect x="40" y="204" width="360" height="46" rx="8" fill="#fff" stroke="#231815" stroke-width="2"/>
      <text x="220" y="232" fill="#231815" text-anchor="middle">{{第4層（例: 保管）}}</text>
      <text x="416" y="232" font-size="11.5" font-weight="600" fill="#655E5B">{{ここで何が起きるか}}</text>
    </g>
    <path d="M22 40 V246" stroke="#E7DEDA" stroke-width="2"/>
    <text x="14" y="60" font-size="11" fill="#655E5B" transform="rotate(-90 14 60)">近い</text>
    <text x="14" y="232" font-size="11" fill="#655E5B" transform="rotate(-90 14 232)">遠い</text>
  </svg>
</div>
```

> 濃い→薄いの段階（`#231815`→`#655E5B`→`#9C9591`→白）で**深さ**を表す。
> 一番下を白抜きにすると「ここが土台」が目で分かる。

---

## ③ 関係図 — 登場するものとつながり

真ん中に主役、まわりに関係するもの。**矢印の向き＝頼る向き・データの向き**を必ずそろえる（片方向で描けないなら、両向きの矢印にせず2本引く）。

```html
<div class="compare-box">
  <svg viewBox="0 0 720 300" role="img" aria-label="真ん中の主役と、それを取り巻く4つの関係するものの関係図。矢印はデータの流れる向きを示す。">
    <defs>
      <marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="#9C9591"/>
      </marker>
    </defs>
    <g stroke="#9C9591" stroke-width="2" marker-end="url(#ar2)" fill="none">
      <path d="M176 84 L292 132"/><path d="M544 84 L428 132"/>
      <path d="M292 176 L176 222"/><path d="M428 176 L544 222"/>
    </g>
    <circle cx="360" cy="154" r="72" fill="#231815"/>
    <text x="360" y="150" text-anchor="middle" font-size="15" font-weight="800" fill="#fff">{{主役}}</text>
    <text x="360" y="172" text-anchor="middle" font-size="11" fill="#E7DEDA">{{一言で役割}}</text>
    <g font-size="12.5" font-weight="700" text-anchor="middle">
      <rect x="40" y="42" width="140" height="44" rx="8" fill="#fff" stroke="#231815" stroke-width="2"/>
      <text x="110" y="70" fill="#231815">{{関係するものA}}</text>
      <rect x="540" y="42" width="140" height="44" rx="8" fill="#fff" stroke="#231815" stroke-width="2"/>
      <text x="610" y="70" fill="#231815">{{関係するものB}}</text>
      <rect x="40" y="220" width="140" height="44" rx="8" fill="#fff" stroke="#231815" stroke-width="2"/>
      <text x="110" y="248" fill="#231815">{{関係するものC}}</text>
      <rect x="540" y="220" width="140" height="44" rx="8" fill="#fff" stroke="#231815" stroke-width="2"/>
      <text x="610" y="248" fill="#231815">{{関係するものD}}</text>
    </g>
    <g font-size="11" fill="#655E5B" text-anchor="middle">
      <text x="222" y="100">{{何を渡す}}</text><text x="498" y="100">{{何を渡す}}</text>
      <text x="222" y="212">{{何を渡す}}</text><text x="498" y="212">{{何を渡す}}</text>
    </g>
  </svg>
</div>
```

> 関係するものが5個以上になったら、**まとめて層に落とす**（②層の図へ）。放射状は4個までが限度。

---

## ④ 比べる図 — 前と後・A案とB案

**左右2列の SVG で組む**（左＝今・A案、右＝これから・B案、真ん中に→。強調色はこの→の1か所まで）。

このスキルで使う時の注意: 提案書と違って、**おすすめを押す図ではない**。
「何がどう変わるか」を分かってもらうのが目的なので、左右の下の説明は「良い点・悪い点」ではなく「この時どうなるか」を書く。
左右の地を色で塗り分けない。両方白にして、区別は上のラベル（「今」「これから」）で示す。

---

## ⑤ 時の流れ — いきさつ・予定

**3〜5個の点を並べた横の年表、または月を横軸にした予定表を SVG で組む。**

「なぜ今この形なのか」を説明する時に効く。
各点に**日付＋そこで何が変わったか**を入れる（出来事を並べるだけにしない）。

---

## ⑥ 状態の移り変わり — ステータスの動き

「今どの状態か」「次にどこへ行けるか」「戻れるか」を示す。仕事の進み具合・承認の流れ・データの一生に向く。

```html
<div class="compare-box">
  <svg viewBox="0 0 720 210" role="img" aria-label="4つの状態の移り変わりの図。状態1から順に進み、状態3からは状態2へ戻ることもできる。状態4が終わり。">
    <defs>
      <marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="#231815"/>
      </marker>
      <marker id="ar3b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="#b45309"/>
      </marker>
    </defs>
    <g font-size="12.5" font-weight="700" text-anchor="middle">
      <rect x="24" y="86" width="132" height="46" rx="23" fill="#fff" stroke="#231815" stroke-width="2"/>
      <text x="90" y="114" fill="#231815">{{状態1}}</text>
      <rect x="204" y="86" width="132" height="46" rx="23" fill="#655E5B"/>
      <text x="270" y="114" fill="#fff">{{状態2}}</text>
      <rect x="384" y="86" width="132" height="46" rx="23" fill="#655E5B"/>
      <text x="450" y="114" fill="#fff">{{状態3}}</text>
      <rect x="564" y="86" width="132" height="46" rx="23" fill="#15803d"/>
      <text x="630" y="114" fill="#fff">{{状態4・終わり}}</text>
    </g>
    <g stroke="#231815" stroke-width="2" fill="none" marker-end="url(#ar3)">
      <path d="M160 109 H198"/><path d="M340 109 H378"/><path d="M520 109 H558"/>
    </g>
    <path d="M450 82 C450 40, 270 40, 270 80" stroke="#b45309" stroke-width="2" fill="none" marker-end="url(#ar3b)"/>
    <text x="360" y="34" text-anchor="middle" font-size="11" font-weight="700" fill="#b45309">{{差し戻す条件}}</text>
    <g font-size="11" fill="#655E5B" text-anchor="middle">
      <text x="179" y="148">{{進む条件}}</text><text x="359" y="148">{{進む条件}}</text><text x="539" y="148">{{進む条件}}</text>
    </g>
    <text x="360" y="186" text-anchor="middle" font-size="11" fill="#655E5B">終わり＝{{そこから先に進まない条件}}</text>
  </svg>
</div>
```

> 終わりの状態は緑（`#15803d`）、戻りの線は琥珀色（`#b45309`）でそろえる。
> **進む条件のラベルを省かない**。矢印だけの図は「順番」しか伝えず、肝心の「いつ動くか」が抜ける。

---

## SVG の落とし穴（実際に踏んだもの）

### 1. 分かれ道が幹の線を共有すると「全部が注意の色」になる

3方向に分かれる図で、各分かれ道を `M{分かれ元} H{分かれる点} V{行き先}` と書くと、
**幹の部分を3本が重ねて描く**。最後に描いた色（たいてい強調色）が上書きして、
幹まで強調色になり「全部が危ない」に見える。

```html
<!-- だめ: 3本が幹 176→240 を重ねて描く。最後の色が幹を塗りつぶす -->
<path d="M176 104 H240 V40 H286"  stroke="#15803d"/>
<path d="M176 104 H286"           stroke="#b45309"/>
<path d="M176 104 H240 V168 H286" stroke="#C7161D"/>

<!-- よい: 幹を1本だけ黒で引き、分かれる点から色を分ける -->
<path d="M176 104 H240"    stroke="#231815"/>
<path d="M240 104 V40 H286"  stroke="#15803d" marker-end="url(#a-g)"/>
<path d="M240 104 H286"      stroke="#b45309" marker-end="url(#a-b)"/>
<path d="M240 104 V168 H286" stroke="#C7161D" marker-end="url(#a-r)"/>
```

### 2. 合流する線に `marker-end` を付けると、線の途中に迷子の矢印が出る

2本を1点に合流させる時、片方は「合流点で終わる」線になる。
そこに `marker-end` が効いていると、**図の真ん中に行き先のない矢印**が生える。

```html
<!-- だめ: グループの marker-end が効いて、合流点(660,150)に上向きの矢印が生える -->
<g marker-end="url(#a-ink)">
  <path d="M634 118 H660 V150 H676"/>
  <path d="M634 182 H660 V150"/>
</g>

<!-- よい: 合流点で終わる線はグループから出して、矢印を付けない -->
<g marker-end="url(#a-ink)"><path d="M634 118 H660 V150 H676"/></g>
<path d="M634 182 H660 V150" stroke="#231815" stroke-width="2" fill="none"/>
```

### 3. 375px で `.compare-box` に入れた図は文字が読めなくなる

`.compare-box` は SVG を**幅いっぱいに縮める**。viewBox 720 幅の図を 375px で表示すると、
大きさ 11 の文字は実際には約 5.7px になって読めない。

→ **文字の多い図は `.roadmap-scroll` に入れる**（最小幅 860px で縮まず、横にスクロールして読める）。
`.compare-box` は「文字が少なく、縮んでも意味が分かる」図だけに使う。
横にスクロールする図には「※ スマホでは横にスクロールできます」の一文を必ず添える（気づかれないため）。

---

## 型が決まらない時

| 症状 | どうするか |
|---|---|
| どの型にも当てはまらない | 説明したいことが**2つ以上混ざっている**。分けて2枚にする |
| ノードが8個を超える | 細かすぎる。まとめて②層の図に落とす |
| 矢印が交差だらけ | 並び順が違う。**交差ゼロで描けるまで**ノードを並べ替える |
| 図にしたら情報が減って不安 | それでよい。減った分は本文の補足か、7「実物との対応」に回す |

# 確かめ方（実際のブラウザで）

ファイルの文字を検索するだけでは合格にしない。スライドの重なり・はみ出し・画像の壊れは、表示しないと分からない。

## 1. 開く

作ったHTMLを手元のブラウザで開く（ファイルをダブルクリック、または `python3 -m http.server` で手元だけに出して開く）。

## 2. 機械で点検する（Playwright を使える時）

Playwright（ブラウザを自動で動かす道具。`pip install playwright && python3 -m playwright install chromium`）で、最低限この4つを見る:

```python
# 作業用の一時フォルダに置いて動かす。手元のファイルを開くだけで、外へは何も送らない
import sys, pathlib
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()   # スクショの出力先（作業用の一時フォルダの絶対パス）
out.mkdir(parents=True, exist_ok=True)
bad = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 810})
    pg.goto(html.as_uri())
    total = pg.evaluate("document.querySelectorAll('.slide').length")
    for n in range(1, total + 1):
        pg.evaluate(f"location.hash = '#{n}'")
        pg.wait_for_timeout(80)
        # (1) いつも1枚だけ見えている（前のスライドが透けて重ならない）
        vis = pg.evaluate("[...document.querySelectorAll('.slide')].filter(s => getComputedStyle(s).display !== 'none').length")
        if vis != 1: bad.append(f"{n}枚目: 見えているスライドが {vis} 枚")
        # (2) 中身がスライドの外にはみ出していない
        over = pg.evaluate("""() => { const s = document.querySelector('.slide.is-current');
            return s.scrollHeight > s.clientHeight + 1 || s.scrollWidth > s.clientWidth + 1; }""")
        if over: bad.append(f"{n}枚目: 中身がはみ出している")
        pg.screenshot(path=str(out / f"slide-{n:02d}.png"))
    # (3) 壊れた画像がない
    broken = pg.evaluate("[...document.images].filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.src)")
    bad += [f"画像が読めない: {s}" for s in broken]
    # (4) 印刷すると全スライドが並ぶ（確かめたら必ず元に戻す）
    pg.emulate_media(media="print")
    printed = pg.evaluate("[...document.querySelectorAll('.slide')].filter(s => getComputedStyle(s).display !== 'none').length")
    if printed != total: bad.append(f"印刷で並ぶのが {printed}/{total} 枚")
    pg.emulate_media(media=None)
    b.close()
print("\n".join(bad) or "機械の点検は指摘なし。スクショを必ず目で見ること")
```

## 3. 目で見る（ここが本番）

撮ったスクショを開いて1枚ずつ見る。見る点:

| 見る点 | だめだった時 |
|---|---|
| 文字が読める大きさか（後ろの席から見えるか） | 文字を削る。文字を小さくしない |
| 語の途中で折れていないか | 改行の位置を自分で決める（`<br>`）。3列なら2列にする |
| 下の1/3が白く空いていないか | `slide-design-principles.md` の1の順でつぶす |
| 強調色が1枚に1か所か | 2つ目は黒の太字に |
| 題が体言止めか・扉と次の題が重なっていないか | 書き直す |
| 画像の文字に抜け・崩れがないか（文字入りの画像を使った時） | その1枚だけ作り直す |
| キー・クリック・スワイプでめくれるか | 見本の `<script>` を消していないか確かめる |

## はまりやすい所

1. **重なりは見た目でしか分からない**: CSS の指定がぶつかって前のスライドが透ける失敗は、ファイルを読んでも見えない。必ず2枚目以降にめくって確かめる
2. **印刷の見た目に切り替えたら必ず戻す**: `emulate_media(media="print")` のままにすると、全スライドが表示されたままになり「全部重なって見える」と見誤る
3. **スクショは作業用の一時フォルダの絶対パスに保存する**: 相対パスにすると、書庫の中に画像が散らかる
4. **直す時はファイル名を変えない**: すでに誰かにリンクを渡していると、見られなくなる

#!/usr/bin/env python3
"""doc-kit の資料（縦 A4 / 横 16:9）を1ページずつ撮り、ページの枠からのはみ出しを数える。

使い方:
    python3 shot.py <html_path> <out_dir> --kind tate   # 縦（A4。.page を1ページとして撮る）
    python3 shot.py <html_path> <out_dir> --kind yoko   # 横（16:9。.slide を1枚として撮る）

出力:
    <out_dir>/<kind>_1.png, <kind>_2.png …  … 目視用（★必ず1枚ずつ開いて見る）
    標準出力に、ページごとの「収まっている／はみ出し」

機械で拾えるのは「枠からのはみ出し」だけ。文字と線の重なり・線の交差・強調の数は、
画像を目で見て確かめる。

外部への送信はしない（手元のHTMLを手元のブラウザで開いて撮るだけ）。
依存: playwright（pip install playwright && python3 -m playwright install chromium）
"""
import argparse
import pathlib

from playwright.sync_api import sync_playwright

KINDS = {
    # 名前: (ページの要素, 画面の幅, 画面の高さ, ページの高さの上限 px)
    "tate": (".page", 900, 1300, 1123),   # A4 297mm ≒ 1122.5px
    "yoko": (".slide", 1300, 800, 720),
}

PROBE = """
(sel) => [...document.querySelectorAll(sel)].map(p => ({
  h: p.scrollHeight, w: p.scrollWidth, ch: p.clientHeight, cw: p.clientWidth
}))
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--kind", choices=KINDS.keys(), required=True)
    a = ap.parse_args()

    sel, vw, vh, limit = KINDS[a.kind]
    src = pathlib.Path(a.html).resolve()
    out = pathlib.Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=2)
        pg.goto(src.as_uri())
        pg.wait_for_timeout(1500)  # 書体の読み込みを待つ
        pages = pg.query_selector_all(sel)
        if not pages:
            print(f"ページが見つからない（{sel} が無い）。見本の型を写して作ったか確かめる")
            return
        sizes = pg.evaluate(PROBE, sel)
        bad = 0
        for i, (el, s) in enumerate(zip(pages, sizes), 1):
            path = out / f"{a.kind}_{i}.png"
            el.screenshot(path=str(path))
            over_h = s["h"] > limit + 1 or s["h"] > s["ch"] + 1
            over_w = s["w"] > s["cw"] + 1
            if over_h or over_w:
                bad += 1
                print(f"{i}: はみ出し（高さ {s['h']}px / 上限 {limit}px・幅 {s['w']}px / {s['cw']}px） → {path.name}")
            else:
                print(f"{i}: 収まっている → {path.name}")
        b.close()
    print(f"\n{len(pages)}ページ中 はみ出し {bad}。画像を1枚ずつ開いて目で確かめること。")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""explain-visual の図解HTMLを 1280px / 375px で撮影し、はみ出しを機械検出する。

使い方:
    python3 shot.py <html_path> [out_dir]

出力:
    <out_dir>/shot-1280.png / shot-375.png  … 目視用（★これを必ず見ること）
    標準出力に機械チェック結果（横スクロール発生・SVGはみ出し・画像破損）

機械チェックは「明らかな崩れ」しか拾えない。日本語の折り返し・図の意味の破綻は
必ずスクショを目視して判断する（grep や DOM チェックだけで合格にしない）。

外部への送信はしない（手元のHTMLを手元のブラウザで開いて撮るだけ）。
依存: playwright（pip install playwright && python3 -m playwright install chromium）
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

WIDTHS = (1280, 375)

# 横スクロールを許してよい容器（references/diagram-patterns.md の仕様上、意図的に min-width を持つ）
SCROLL_OK = ".roadmap-scroll, .table-scroll"

PROBE = """
() => {
  const bad = [];
  // 1. body 自体の横スクロール（= レイアウト崩れ）
  if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 1) {
    bad.push(`body横スクロール: ${document.documentElement.scrollWidth}px > ${document.documentElement.clientWidth}px`);
  }
  // 2. 許可された容器の外での要素はみ出し
  const limit = document.documentElement.clientWidth;
  for (const el of document.querySelectorAll('svg, table, pre, .compare-box, .flow, .deliv-grid')) {
    if (el.closest('%s')) continue;
    const r = el.getBoundingClientRect();
    if (r.right > limit + 1 || r.left < -1) {
      bad.push(`はみ出し: <${el.tagName.toLowerCase()} class="${el.className.baseVal ?? el.className}"> right=${Math.round(r.right)} limit=${limit}`);
    }
  }
  // 3. 画像破損
  for (const img of document.images) {
    if (!(img.complete && img.naturalWidth > 0)) bad.push(`画像破損: ${img.getAttribute('src')}`);
  }
  // 4. aria-label のない SVG（diagram-patterns.md の必須ルール）
  for (const s of document.querySelectorAll('svg')) {
    if (!s.getAttribute('aria-label')) bad.push('SVGにaria-labelが無い');
  }
  return bad;
}
""" % SCROLL_OK


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    html = pathlib.Path(sys.argv[1]).resolve()
    if not html.is_file():
        print(f"ERROR: ファイルが無い: {html}")
        return 2
    out = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else html.parent / "_shots"
    out.mkdir(parents=True, exist_ok=True)

    findings: dict[int, list[str]] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for w in WIDTHS:
                page = browser.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2)
                page.goto(html.as_uri(), wait_until="load")
                page.wait_for_timeout(300)
                page.screenshot(path=str(out / f"shot-{w}.png"), full_page=True)
                findings[w] = page.evaluate(PROBE)
                page.close()
        finally:
            browser.close()

    print(f"スクショ: {out}/shot-1280.png , {out}/shot-375.png")
    ng = False
    for w, bad in findings.items():
        if bad:
            ng = True
            print(f"\n🔴 {w}px — {len(bad)}件")
            for b in bad:
                print(f"   - {b}")
        else:
            print(f"🟢 {w}px — 機械チェックは指摘なし")
    print("\n" + json.dumps({str(k): v for k, v in findings.items()}, ensure_ascii=False))
    print("\n★ 機械チェックが緑でも、必ずスクショを Read して目視すること。")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""画面の「情報量」を計測し、スクリーンショットを撮る（ux-review 用）。

使い方:
    python3 ux_measure.py <URL か HTMLファイルのパス> <出力フォルダ> [--widths 1280,768,375] [--height 900] [--wait 800]

必要なもの:
    Playwright（pip install playwright && playwright install chromium）
    指定した URL を開く以外の通信はしない。書き込むのは <出力フォルダ> の中だけ。

出力:
    <出力フォルダ>/ux-<幅>.png       … 最初の表示範囲（スクロール前）のスクショ
    <出力フォルダ>/ux-<幅>-full.png  … ページ全体のスクショ
    <出力フォルダ>/ux-metrics.json   … 計測値
    標準出力に計測値の表

計測するもの（最初の表示範囲＝スクロール前に見えている範囲だけを数える）:
    buttons        押せる要素（button / a / role=button / input[type=submit] など）で、見えていて無効でないもの
    disabled       見えている無効な押せる要素
    emphasis       強調の印（赤系・警告系の文字色や背景、太い枠）の要素数
    text_chars     見えている文字数
    small_text     12px 未満の文字を含む要素数
    small_targets  44px 未満の押せる要素数（主に375pxで見る）
    colors         文字色・背景色の実色の種類
    first_seen     画面の左上から読んだ時に最初に目に入る見出し・強い文字（上から5つ）

数値は判定の「きっかけ」。最終判定は必ずスクショを目で見て行う（references/principles.md の「計測の目安」）。
"""
import argparse
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

PROBE = r"""
() => {
  const vw = window.innerWidth, vh = window.innerHeight;
  const inView = r => r.width > 0 && r.height > 0 && r.bottom > 0 && r.right > 0 && r.top < vh && r.left < vw;
  const visible = el => {
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) === 0) return false;
    return inView(el.getBoundingClientRect());
  };
  const clickSel = 'button, a[href], [role=button], input[type=submit], input[type=button], select, summary';
  const clickables = [...document.querySelectorAll(clickSel)].filter(visible);
  const isDisabled = el => el.disabled || el.getAttribute('aria-disabled') === 'true';
  const buttons = clickables.filter(el => !isDisabled(el));
  const disabled = clickables.filter(isDisabled);

  const parse = c => { const m = c && c.match(/\d+(\.\d+)?/g); return m ? m.map(Number) : null; };
  const isAlert = c => { const v = parse(c); if (!v) return false; const [r,g,b] = v; return r > 170 && g < 110 && b < 110; };
  const all = [...document.body.querySelectorAll('*')].filter(visible);
  let emphasis = 0, small = 0;
  const colors = new Set();
  for (const el of all) {
    const s = getComputedStyle(el);
    const ownText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (ownText) {
      colors.add(s.color);
      if (parseFloat(s.fontSize) < 12) small++;
    }
    if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent') colors.add(s.backgroundColor);
    const thick = ['Top','Right','Bottom','Left'].some(k => parseFloat(s['border'+k+'Width']) >= 2 && isAlert(s['border'+k+'Color']));
    if ((ownText && isAlert(s.color)) || isAlert(s.backgroundColor) || thick) emphasis++;
  }
  const smallTargets = buttons.filter(el => { const r = el.getBoundingClientRect(); return r.width < 44 || r.height < 44; }).length;

  // 見えている文字数（スクロール前の範囲に入る文字ノードだけ）
  let chars = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode, t = n.textContent.trim();
    if (!t || !n.parentElement || !visible(n.parentElement)) continue;
    const range = document.createRange(); range.selectNodeContents(n);
    if (inView(range.getBoundingClientRect())) chars += t.length;
  }

  // 最初に目に入りやすいもの: 大きさ×太さ×上にあるほど強い
  const cands = all.filter(el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1)).map(el => {
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    const weight = parseInt(s.fontWeight) || 400;
    const score = parseFloat(s.fontSize) * (weight >= 600 ? 1.4 : 1) * (isAlert(s.color) || isAlert(s.backgroundColor) ? 1.3 : 1) - (r.top / vh) * 4;
    return {text: el.innerText.trim().replace(/\s+/g,' ').slice(0, 40), score: Math.round(score*10)/10, top: Math.round(r.top)};
  }).sort((a,b) => b.score - a.score);
  const seen = []; for (const c of cands) { if (!seen.some(x => x.text === c.text)) seen.push(c); if (seen.length >= 5) break; }

  return {
    viewport: [vw, vh],
    buttons: buttons.length, disabled: disabled.length, emphasis, text_chars: chars,
    small_text: small, small_targets: smallTargets, colors: colors.size,
    body_scroll_x: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    first_seen: seen,
  };
}
"""


def target_url(arg: str) -> str:
    if arg.startswith(("http://", "https://", "file://")):
        return arg
    p = pathlib.Path(arg).resolve()
    if not p.is_file():
        sys.exit(f"ERROR: ファイルが見つかりません: {p}")
    return p.as_uri()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("out")
    ap.add_argument("--widths", default="1280,768,375")
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--wait", type=int, default=800, help="読み込み後に待つミリ秒（React等の描画待ち）")
    a = ap.parse_args()

    out = pathlib.Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    url = target_url(a.target)
    widths = [int(w) for w in a.widths.split(",") if w.strip()]
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for w in widths:
                page = browser.new_page(viewport={"width": w, "height": a.height}, device_scale_factor=2)
                errors = []
                page.on("pageerror", lambda e, errors=errors: errors.append(str(e)))
                page.goto(url, wait_until="load")
                page.wait_for_timeout(a.wait)
                page.screenshot(path=str(out / f"ux-{w}.png"))
                page.screenshot(path=str(out / f"ux-{w}-full.png"), full_page=True)
                m = page.evaluate(PROBE)
                m["page_errors"] = errors
                results[w] = m
                page.close()
        finally:
            browser.close()

    (out / "ux-metrics.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
    keys = ["buttons", "disabled", "emphasis", "text_chars", "small_text", "small_targets", "colors", "body_scroll_x"]
    print("| 幅 | " + " | ".join(keys) + " |")
    print("|---|" + "---|" * len(keys))
    for w, m in results.items():
        print(f"| {w} | " + " | ".join(str(m[k]) for k in keys) + " |")
    for w, m in results.items():
        print(f"\n[{w}px] 最初に目に入りやすいもの: " + " ／ ".join(f"{s['text']}" for s in m["first_seen"]))
        if m["page_errors"]:
            print(f"[{w}px] ページのエラー: {m['page_errors']}")
    print(f"\nスクショ: {out}/ux-<幅>.png（最初の表示範囲）と ux-<幅>-full.png（全体）。★必ず目で見ること")
    return 0


if __name__ == "__main__":
    sys.exit(main())

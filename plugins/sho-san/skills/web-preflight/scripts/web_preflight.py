#!/usr/bin/env python3
"""静的なHTMLのサイトを、公開前に機械的に点検する（web-preflight 用）。

使い方:
    python3 web_preflight.py <サイトのフォルダ か HTMLファイル> [--out レポート.md]

点検すること:
    要修正: <title>・meta description・viewport が無い／手元のファイルへの参照切れ／
            ダミー文字の残り／中身の無いリンク（href="" "#" javascript:）
    注意:   lang・OGP（og:title・og:image）・favicon が無い／h1 が1個でない／
            img の alt が無い・中身の無い言葉・ファイル名のまま／タイトル・説明文の長さ
    情報:   見出しの段階の飛び／外部リンクの数

終わりの番号: 0=要修正なし / 1=要修正あり・HTMLが無い / 2=使い方の間違い
標準ライブラリだけで動く。通信はしない。書き込むのは --out のファイルだけ。
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

DUMMY = [
    (re.compile(r"lorem\s+ipsum", re.I), "Lorem ipsum の残り"),
    (re.compile(r"ダミー"), "「ダミー」の残り"),
    (re.compile(r"テキストテキスト"), "流し込み前の文字の残り"),
    (re.compile(r"サンプルテキスト"), "「サンプルテキスト」の残り"),
    (re.compile(r"〇〇|○○|XX月|ＸＸ"), "伏せ字の残り"),
    (re.compile(r"\b(TODO|FIXME|TBD)\b"), "TODO などの残り"),
]
EMPTY_ALT_WORDS = {
    "image", "img", "photo", "picture", "icon", "banner", "thumbnail", "dummy",
    "sample", "alt", "test", "画像", "写真", "ダミー", "サンプル", "アイコン", "バナー",
}
FILENAME_RE = re.compile(r"^[\w./\\-]+\.(jpe?g|png|gif|webp|svg|avif)$", re.I)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")
TITLE_LEN = (10, 60)      # 目安。検索結果で切れにくい長さ
DESC_LEN = (50, 160)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = None
        self._in_title = False
        self._skip = 0           # script/style の中の文字は数えない
        self.meta = {}
        self.icons = 0
        self.headings = []       # (段階, 行)
        self.imgs = []           # (attrs, 行)
        self.refs = []           # (属性名, 値, 行)
        self.links = []          # (href, 行)
        self.text = []           # (文字, 行)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
            self.title = ""
        elif tag in ("script", "style"):
            self._skip += 1
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if "icon" in rel:
                self.icons += 1
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append((int(tag[1]), line))
        if tag == "img":
            self.imgs.append((a, line))
        if tag == "a" and "href" in a:
            self.links.append((a["href"].strip(), line))
        for k in ("src", "href", "poster"):
            if k in a and not (tag == "a" and k == "href"):
                self.refs.append((k, a[k].strip(), line))
        if "srcset" in a:
            for part in a["srcset"].split(","):
                p = part.strip().split(" ")[0]
                if p:
                    self.refs.append(("srcset", p, line))
        if "style" in a:
            for u in CSS_URL_RE.findall(a["style"]):
                self.refs.append(("style", u.strip(), line))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self._skip and data.strip():
            self.text.append((data.strip(), self.getpos()[0]))


def is_local(ref: str) -> bool:
    if not ref or ref.startswith(("#", "data:", "mailto:", "tel:", "javascript:", "//")):
        return False
    return not urlparse(ref).scheme


def exists(root: Path, page: Path, ref: str) -> bool:
    path = unquote(urlparse(ref).path)
    if not path:
        return True
    target = (root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    return target.exists()


def check_page(root: Path, f: Path, out: dict):
    rel = f.relative_to(root) if f != root else Path(f.name)
    p = Page()
    p.feed(f.read_text(encoding="utf-8", errors="replace"))

    def add(level, msg, line=None):
        out[level].append(f"`{rel}{':' + str(line) if line else ''}` {msg}")

    # 必須の設定
    if not (p.title or "").strip():
        add("要修正", "<title> が無い・空")
    else:
        n = len(p.title.strip())
        if not TITLE_LEN[0] <= n <= TITLE_LEN[1]:
            add("注意", f"タイトルが {n} 文字（目安 {TITLE_LEN[0]}〜{TITLE_LEN[1]}）")
    desc = p.meta.get("description", "").strip()
    if not desc:
        add("要修正", "meta description が無い・空")
    elif not DESC_LEN[0] <= len(desc) <= DESC_LEN[1]:
        add("注意", f"説明文が {len(desc)} 文字（目安 {DESC_LEN[0]}〜{DESC_LEN[1]}）")
    if "viewport" not in p.meta:
        add("要修正", "meta viewport が無い（スマホで縮んで表示される）")
    if not p.lang:
        add("注意", "<html lang> が無い")
    for k in ("og:title", "og:image"):
        if k not in p.meta:
            add("注意", f"{k} が無い（SNSで共有した時の表示）")
    if not p.icons:
        add("注意", "favicon（タブのアイコン）の指定が無い")

    # 見出し
    h1 = sum(1 for lv, _ in p.headings if lv == 1)
    if h1 != 1:
        add("注意", f"h1 が {h1} 個（ふつうは1個）")
    prev = 0
    for lv, line in p.headings:
        if prev and lv > prev + 1:
            add("情報", f"見出しの段階が飛んでいる h{prev} → h{lv}", line)
        prev = lv

    # 画像の alt
    for a, line in p.imgs:
        if "alt" not in a:
            add("注意", f"img に alt が無い（{a.get('src', '')[:60]}）", line)
            continue
        alt = a["alt"].strip()
        if alt and (alt.lower() in EMPTY_ALT_WORDS or FILENAME_RE.match(alt)):
            add("注意", f"alt の中身が無い・ファイル名のまま「{alt[:40]}」", line)

    # リンクと参照
    external = 0
    for href, line in p.links:
        if href in ("", "#") or href.lower().startswith("javascript:"):
            add("要修正", f"中身の無いリンク href=\"{href}\"", line)
        elif urlparse(href).scheme in ("http", "https") or href.startswith("//"):
            external += 1
        elif is_local(href) and not exists(root, f, href):
            add("要修正", f"リンク先のファイルが無い {href}", line)
    for kind, ref, line in p.refs:
        if is_local(ref) and not exists(root, f, ref):
            add("要修正", f"参照しているファイルが無い（{kind}）{ref}", line)
    if external:
        add("情報", f"外部へのリンクが {external} 件（開くかは通信しないので未確認）")

    # ダミー文字
    texts = p.text + [(p.title or "", None), (desc, None)]
    for s, line in texts:
        for rx, label in DUMMY:
            if rx.search(s):
                add("要修正", f"{label}「{s[:40]}」", line)


def check_css(root: Path, f: Path, out: dict):
    rel = f.relative_to(root)
    for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for u in CSS_URL_RE.findall(line):
            u = u.strip()
            if is_local(u):
                target = f.parent / unquote(urlparse(u).path)
                if not target.exists():
                    out["要修正"].append(f"`{rel}:{i}` CSS から参照しているファイルが無い {u}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--out")
    a = ap.parse_args()

    target = Path(a.target).resolve()
    if target.is_file():
        root, pages, styles = target.parent, [target], []
    elif target.is_dir():
        root = target
        pages = sorted(p for p in target.rglob("*.htm*") if "node_modules" not in p.parts)
        styles = sorted(p for p in target.rglob("*.css") if "node_modules" not in p.parts)
    else:
        print(f"見つかりません: {target}", file=sys.stderr)
        return 1
    if not pages:
        print(f"HTMLファイルがありません: {target}", file=sys.stderr)
        return 1

    out = {"要修正": [], "注意": [], "情報": []}
    for f in pages:
        check_page(root, f, out)
    for f in styles:
        check_css(root, f, out)

    lines = [f"# 公開前の点検レポート", "", f"- 対象: `{target.name}`（HTML {len(pages)} 件・CSS {len(styles)} 件）",
             f"- 要修正 {len(out['要修正'])} 件／注意 {len(out['注意'])} 件／情報 {len(out['情報'])} 件", ""]
    for level in ("要修正", "注意", "情報"):
        lines.append(f"## {level}（{len(out[level])} 件）")
        lines.append("")
        lines += [f"- {m}" for m in out[level]] or ["- なし"]
        lines.append("")
    lines.append("通信をしていないため、外部リンクが開くか・見た目・動きは確かめていません。")
    report = "\n".join(lines) + "\n"

    if a.out:
        Path(a.out).write_text(report, encoding="utf-8")
        print(f"レポート: {a.out}")
    print(report)
    return 1 if out["要修正"] else 0


if __name__ == "__main__":
    sys.exit(main())

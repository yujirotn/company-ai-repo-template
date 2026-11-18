#!/usr/bin/env python3
"""文字の色と背景の色の明るさの差（コントラスト比）を出す（design-review 用）。

使い方:
    python3 contrast.py <文字の色> <背景の色>
    例: python3 contrast.py "#333333" "#ffffff"
        python3 contrast.py "rgb(120,120,120)" "#f5f5f5"

色の書き方: #rgb / #rrggbb / rgb(r,g,b)
目安（WCAG 2 の AA）: 本文 4.5:1 以上、大きな文字・アイコン・枠線 3:1 以上
標準ライブラリだけで動く。通信もファイルの書き込みもしない。
"""
import re
import sys


def parse(color: str):
    c = color.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", c)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*[\d.]+\s*)?\)", c)
    if m:
        return tuple(min(255, int(v)) for v in m.groups())
    sys.exit(f"色の書き方が読めません: {color}（#rrggbb か rgb(r,g,b) で書いてください）")


def luminance(rgb):
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    r = ratio(parse(sys.argv[1]), parse(sys.argv[2]))
    body = "合格" if r >= 4.5 else "不合格"
    large = "合格" if r >= 3.0 else "不合格"
    print(f"コントラスト比 {r:.2f}:1")
    print(f"  本文（4.5:1 以上）: {body}")
    print(f"  大きな文字・アイコン・枠線（3:1 以上）: {large}")
    return 0 if r >= 4.5 else 1


if __name__ == "__main__":
    sys.exit(main())

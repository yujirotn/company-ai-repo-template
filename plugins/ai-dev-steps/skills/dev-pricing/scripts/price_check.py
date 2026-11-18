#!/usr/bin/env python3
"""価格の集計（dev-pricing 用）。Python の標準ライブラリだけで動き、外には何も送らない。

使い方:
  python3 price_check.py vw   <アンケート.csv>
  python3 price_check.py cost <費用.csv> <プラン.csv> --users 100

vw   : 4つの値段の問い（安すぎる・安い・高い・高すぎる）の答えから、
       受け入れられる値段の幅と目安を出す（Van Westendorp の値段の感じ方の調べ方）。
       CSV の列: 安すぎる,安い,高い,高すぎる（1行が1人。数字だけ。円・カンマは入れない）
cost : 月の費用とプランの配分から、1か月の売上・費用・利益と、元が取れる人数を出す。
       費用.csv の列: 項目,区分,金額   区分は「固定」（毎月かかる）か「1人あたり」（使う人1人に毎月かかる）
       プラン.csv の列: プラン,月額,割合   割合は 2:6:2 なら 20,60,20 のように書く（合計が100でなくてもよい）
"""
import argparse
import csv
import sys

VW_COLS = ["安すぎる", "安い", "高い", "高すぎる"]


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(s, where):
    try:
        return float(str(s).replace(",", "").replace("円", "").strip())
    except ValueError:
        sys.exit(f"数字として読めません: {where} = {s!r}")


def crossing(prices, f, g):
    """f - g の符号が変わる所を、直線でつないで求める。無ければ None。"""
    prev = None
    for p in prices:
        d = f(p) - g(p)
        if d == 0:
            return p
        if prev is not None and (prev[1] > 0) != (d > 0):
            p0, d0 = prev
            return p0 + (p - p0) * (d0 / (d0 - d))
        prev = (p, d)
    return None


def cmd_vw(args):
    rows = read_rows(args.csv)
    missing = [c for c in VW_COLS if rows and c not in rows[0]]
    if not rows or missing:
        sys.exit(f"列が足りません: {missing or VW_COLS}（1行目に {','.join(VW_COLS)} を書く）")
    data = []
    for i, r in enumerate(rows, start=2):
        v = [num(r[c], f"{i}行目の{c}") for c in VW_COLS]
        if not (v[0] <= v[1] <= v[2] <= v[3]):
            print(f"注意: {i}行目は 安すぎる≦安い≦高い≦高すぎる の順になっていません（集計には入れます）", file=sys.stderr)
        data.append(v)
    n = len(data)
    if n < 5:
        print(f"注意: 答えた人が {n} 人です。目安としても少なめです（30人以上あると安定します）", file=sys.stderr)
    prices = sorted({x for v in data for x in v})

    too_cheap = lambda p: sum(v[0] >= p for v in data) / n      # この値段だと安すぎて不安な人
    not_cheap = lambda p: 1 - sum(v[1] >= p for v in data) / n  # この値段は「安い」と感じない人
    not_exp = lambda p: 1 - sum(v[2] <= p for v in data) / n    # この値段は「高い」と感じない人
    too_exp = lambda p: sum(v[3] <= p for v in data) / n        # この値段だと高すぎて買わない人

    low = crossing(prices, too_cheap, not_cheap)
    high = crossing(prices, too_exp, not_exp)
    best = crossing(prices, too_cheap, too_exp)
    neutral = crossing(prices, not_cheap, not_exp)

    fmt = lambda x: "求められませんでした" if x is None else f"{round(x):,} 円"
    print(f"答えた人: {n} 人")
    print(f"受け入れられる値段の幅: {fmt(low)} 〜 {fmt(high)}")
    print(f"  下の端（これより安いと品質を疑われ始める）: {fmt(low)}")
    print(f"  上の端（これより高いと買わない人が増え始める）: {fmt(high)}")
    print(f"「安すぎる」と「高すぎる」が同じ割合になる値段（嫌がる人が一番少ない）: {fmt(best)}")
    print(f"「安いとも高いとも感じない」人が多い値段: {fmt(neutral)}")


def cmd_cost(args):
    costs = read_rows(args.costs)
    plans = read_rows(args.plans)
    fixed = per_user = 0.0
    for i, r in enumerate(costs, start=2):
        kind = (r.get("区分") or "").strip()
        amount = num(r.get("金額"), f"費用 {i}行目の金額")
        if kind == "固定":
            fixed += amount
        elif kind == "1人あたり":
            per_user += amount
        else:
            sys.exit(f"費用 {i}行目の区分は「固定」か「1人あたり」にしてください: {kind!r}")
    total_share = sum(num(p.get("割合"), "プランの割合") for p in plans)
    if total_share <= 0:
        sys.exit("プランの割合の合計が0です")
    avg_price = sum(num(p["月額"], "プランの月額") * num(p["割合"], "プランの割合") for p in plans) / total_share
    u = args.users
    revenue = avg_price * u
    cost = fixed + per_user * u
    margin = avg_price - per_user
    print(f"使う人: {u:,} 人 / 1人あたりの平均の月額: {avg_price:,.0f} 円")
    for p in plans:
        share = num(p["割合"], "プランの割合") / total_share
        print(f"  {p['プラン']}: 月額 {num(p['月額'], '月額'):,.0f} 円 × {share:.0%} → {round(u * share):,} 人")
    print(f"1か月の売上: {revenue:,.0f} 円")
    print(f"1か月の費用: {cost:,.0f} 円（固定 {fixed:,.0f} 円 ＋ 1人あたり {per_user:,.0f} 円 × {u:,} 人）")
    print(f"1か月の利益: {revenue - cost:,.0f} 円（利益の割合 {((revenue - cost) / revenue if revenue else 0):.0%}）")
    if margin <= 0:
        print("元が取れる人数: なし（1人あたりの費用が平均の月額以上です。値段か費用を見直してください）")
    else:
        need = -(-fixed // margin)  # 切り上げ
        print(f"元が取れる人数: {int(need):,} 人（この人数から黒字）")


def main():
    ap = argparse.ArgumentParser(description="価格の集計（外には何も送らない）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("vw", help="値段の感じ方のアンケートを集計する")
    a.add_argument("csv")
    a.set_defaults(func=cmd_vw)
    b = sub.add_parser("cost", help="費用とプランから利益を試算する")
    b.add_argument("costs")
    b.add_argument("plans")
    b.add_argument("--users", type=int, required=True, help="使う人の数")
    b.set_defaults(func=cmd_cost)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

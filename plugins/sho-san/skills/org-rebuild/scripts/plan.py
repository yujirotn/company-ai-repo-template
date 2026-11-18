#!/usr/bin/env python3
"""③ 移行表を作る（読むだけ。何も動かさない）。

使い方:
  python3 -I plan.py --rules rules.json --out <出力フォルダ>

rules.json（rules.example.json を参照）に会社ごとの設定を書く:
  source        旧環境のパス
  skip          最初から見ないもの（.git など。前方一致）
  rules         [[旧パスの接頭辞, 行き先]] 上から順に最初に一致したもの
                行き先は 新しいパス / "KEEP"（旧環境にだけ残す）/ "DROP"（持っていかない）/ "SKIP"
                どれにも一致しないものは ARCHIVE（保存先の _archive/<旧パス>）
  heavy_ext     重いものの拡張子（新しいパスに行くものでも保存先へ回す）
  text_limit    この容量を超えるテキスト系（html/json/js/csv/txt/svg/ndjson）は保存先へ（バイト）
  any_limit     種類に関係なくこの容量を超えるものは保存先へ（バイト）

出力:
  migration-plan.csv  kind,source,destination,bytes
    kind = REPO（新リポへ）/ DRIVE（保存先の同じパスへ）/ ARCHIVE（保存先の _archive/）/ KEEP / DROP
  画面にサマリー（種類別の件数・容量、新しい置き場ごとの内訳、新リポに入る大きいファイル上位）
"""
import argparse
import collections
import csv
import json
import os
import sys

TEXT_EXT = {"html", "htm", "json", "jsonl", "ndjson", "js", "mjs", "csv", "txt", "svg"}


def load_rules(path):
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    cfg.setdefault("skip", [".git", "node_modules", ".venv", ".DS_Store"])
    cfg.setdefault("heavy_ext", [])
    cfg.setdefault("text_limit", 1_000_000)
    cfg.setdefault("any_limit", 5_000_000)
    cfg["heavy_ext"] = {e.lower().lstrip(".") for e in cfg["heavy_ext"]}
    return cfg


def match(rel, prefix):
    p = prefix.rstrip("/")
    return rel == p or rel.startswith(p + "/") or (prefix.endswith("-") and rel.startswith(prefix))


def classify(rel, cfg):
    for prefix, dst in cfg["rules"]:
        if match(rel, prefix):
            if dst in ("KEEP", "DROP", "SKIP"):
                return dst, ""
            return "MAP", dst + rel[len(prefix.rstrip("/")) if not prefix.endswith("-") else len(prefix):]
    return "ARCHIVE", "_archive/" + rel


def is_heavy(rel, size, cfg):
    name = os.path.basename(rel)
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext in cfg["heavy_ext"]:
        return True
    if ext in TEXT_EXT and size > cfg["text_limit"]:
        return True
    return size > cfg["any_limit"]


def walk(cfg):
    src = cfg["source"]
    skip_names = {s for s in cfg["skip"] if "/" not in s}
    skip_prefix = [s for s in cfg["skip"] if "/" in s]
    for root, dirs, files in os.walk(src):
        relroot = os.path.relpath(root, src)
        dirs[:] = [d for d in dirs if d not in skip_names
                   and not any(match(os.path.normpath(os.path.join(relroot, d)), p) for p in skip_prefix)]
        for f in files:
            if f in skip_names:
                continue
            p = os.path.join(root, f)
            rel = os.path.normpath(os.path.join(relroot, f))
            try:
                size = os.lstat(p).st_size
            except OSError:
                continue
            yield rel, size, os.path.islink(p)


def main():
    ap = argparse.ArgumentParser(description="移行表を作る（何も動かさない）")
    ap.add_argument("--rules", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = load_rules(a.rules)
    if not os.path.isdir(cfg["source"]):
        sys.exit(f"source が見つからない: {cfg['source']}")
    os.makedirs(a.out, exist_ok=True)

    rows = []
    links = 0
    for rel, size, link in walk(cfg):
        if link:
            links += 1
            continue
        kind, dst = classify(rel, cfg)
        if kind == "SKIP":
            continue
        if kind == "MAP":
            kind = "DRIVE" if is_heavy(rel, size, cfg) else "REPO"
        rows.append((kind, rel, dst, size))

    out = os.path.join(a.out, "migration-plan.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["kind", "source", "destination", "bytes"])
        w.writerows(sorted(rows))

    tot = collections.defaultdict(lambda: [0, 0])
    for k, _, _, s in rows:
        tot[k][0] += 1
        tot[k][1] += s
    print(f"移行表: {out}")
    print("== 振り分けの合計")
    for k in ["REPO", "DRIVE", "ARCHIVE", "KEEP", "DROP"]:
        n, s = tot[k]
        print(f"{k:8s} {n:7d} 件 {s/1e9:8.2f} GB")
    if links:
        print(f"(シンボリックリンク {links} 件は対象外)")

    by = collections.defaultdict(lambda: [0, 0])
    for k, _, d, s in rows:
        if k in ("REPO", "DRIVE"):
            top = "/".join(d.split("/")[:2])
            by[(k, top)][0] += 1
            by[(k, top)][1] += s
    print("\n== 新しい置き場ごと（REPO=新リポ / DRIVE=保存先の同じパス）")
    for (k, top), (n, s) in sorted(by.items(), key=lambda x: (x[0][1], x[0][0])):
        print(f"{k:5s} {top:45s} {n:6d} 件 {s/1e6:9.1f} MB")

    big = sorted([r for r in rows if r[0] == "REPO"], key=lambda r: -r[3])[:10]
    print("\n== 新リポに入る大きいファイル上位10（大きすぎれば rules を直す）")
    for _, _, d, s in big:
        print(f"{s/1e6:7.2f} MB  {d}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""④ コピーと照合。既定は dry-run（何もコピーせず、やることの件数・容量だけ出す）。

使い方:
  python3 -I copy_verify.py --plan migration-plan.csv --source <旧環境> --repo <新リポ> --drive <保存先のルート>            # dry-run
  python3 -I copy_verify.py ... --apply      # 実際にコピー（元は消さない。同じサイズが既にあれば飛ばす）
  python3 -I copy_verify.py ... --verify     # 照合だけ（全行の存在とサイズ一致を数える）

- REPO 行 → <新リポ>/<destination>、DRIVE・ARCHIVE 行 → <保存先>/<destination>
- KEEP・DROP 行は何もしない
- 途中で止まっても再実行で続きから進む（同じサイズのものは飛ばす）
- 照合で「欠け」「サイズ違い」が 0 になるまで、移行が終わったと言わない
- 外部への通信はしない。何も消さない。移行表の行が --source/--repo/--drive の外を指していたら止まる
"""
import argparse
import csv
import os
import shutil
import sys
import time


def inside(base, rel):
    """base の中に収まるパスを返す。絶対パスや .. で外へ出る行は止める。"""
    base = os.path.abspath(base)
    path = os.path.normpath(os.path.join(base, rel))
    if os.path.isabs(rel) or os.path.commonpath([base, path]) != base:
        sys.exit(f"移行表の行が書き込み先の外を指している: {rel}")
    return path


def target(row, repo, drive):
    if row["kind"] == "REPO":
        return inside(repo, row["destination"])
    if row["kind"] in ("DRIVE", "ARCHIVE"):
        return inside(drive, row["destination"])
    return None


def main():
    ap = argparse.ArgumentParser(description="移行表どおりにコピーし、照合する（既定は dry-run）")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--drive", required=True)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true")
    ap.add_argument("--log", default=None)
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.plan, encoding="utf-8")))
    todo = [r for r in rows if r["kind"] in ("REPO", "DRIVE", "ARCHIVE")]

    if a.verify:
        ok = miss = bad = link = 0
        ok_bytes = 0
        examples = []
        for r in todo:
            if os.path.islink(os.path.join(a.source, r["source"])):
                link += 1
                continue
            t = target(r, a.repo, a.drive)
            if not os.path.exists(t):
                miss += 1
                examples.append("欠け: " + r["destination"])
            elif os.path.getsize(t) != int(r["bytes"]):
                bad += 1
                examples.append("サイズ違い: " + r["destination"])
            else:
                ok += 1
                ok_bytes += int(r["bytes"])
        print(f"一致={ok} 欠け={miss} サイズ違い={bad} リンク(対象外)={link} 一致容量={ok_bytes/1e9:.2f}GB")
        for e in examples[:10]:
            print("  " + e)
        sys.exit(0 if miss == 0 and bad == 0 else 1)

    if not a.apply:
        need = n_bytes = skip = 0
        for r in todo:
            t = target(r, a.repo, a.drive)
            if os.path.exists(t) and os.path.getsize(t) == int(r["bytes"]):
                skip += 1
            else:
                need += 1
                n_bytes += int(r["bytes"])
        print(f"[dry-run] コピーが必要={need}件 {n_bytes/1e9:.2f}GB／既に同じサイズで存在={skip}件")
        print("実行するには --apply、照合だけなら --verify")
        return

    log = open(a.log or os.path.join(os.path.dirname(os.path.abspath(a.plan)), "copy.log"), "a", encoding="utf-8")
    done = skipped = failed = 0
    nbytes = 0
    start = time.time()
    log.write(f"start {time.ctime()} rows={len(todo)}\n")
    for i, r in enumerate(todo, 1):
        src = inside(a.source, r["source"])
        dst = target(r, a.repo, a.drive)
        try:
            if os.path.islink(src):
                skipped += 1
                continue
            if os.path.exists(dst) and os.path.getsize(dst) == int(r["bytes"]):
                skipped += 1
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            done += 1
            nbytes += int(r["bytes"])
        except Exception as e:  # 失敗は記録して続ける
            failed += 1
            log.write(f"FAIL {r['source']} -> {r['destination']}: {e}\n")
        if i % 500 == 0:
            log.write(f"progress {i}/{len(todo)} copied={done} skipped={skipped} failed={failed} "
                      f"{nbytes/1e9:.2f}GB {time.time()-start:.0f}s\n")
            log.flush()
    log.write(f"end {time.ctime()} copied={done} skipped={skipped} failed={failed} {nbytes/1e9:.2f}GB\n")
    log.close()
    print(f"copied={done} skipped={skipped} failed={failed} {nbytes/1e9:.2f}GB（続けて --verify で照合）")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""候補サムネを「実際に一覧で見える大きさ」（246×138）に縮小して5列に並べる。

使い方:
  /usr/bin/python3 scripts/small_sheet.py --out small_sheet.jpg 50A.png 50B.png src.jpg r_xxx.jpg
余白8px・白地・ラベル無し（大きさを正直に見るため）。16:9 でない画像は短辺合わせ→中央切り抜き。
★ここで読めない文字・分からない表情は、YouTube の一覧でも読めない・分からない。
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgutil import cover  # noqa: E402

TW, TH, PAD, COLS = 246, 138, 8, 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("images", nargs="+")
    a = ap.parse_args()
    from PIL import Image
    paths = [os.path.expanduser(p) for p in a.images]
    miss = [p for p in paths if not os.path.exists(p)]
    if miss:
        sys.exit("✗ 画像がありません: " + ", ".join(miss))
    rows = (len(paths) + COLS - 1) // COLS
    cols = min(COLS, len(paths))
    sheet = Image.new("RGB", (cols * (TW + PAD) + PAD, rows * (TH + PAD) + PAD), "white")
    for i, p in enumerate(paths):
        sheet.paste(cover(Image.open(p), TW, TH), (PAD + (i % COLS) * (TW + PAD), PAD + (i // COLS) * (TH + PAD)))
    out = os.path.abspath(os.path.expanduser(a.out))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sheet.save(out, quality=92)
    print(f"{len(paths)}枚 → {sheet.width}×{sheet.height}: {out}")


if __name__ == "__main__":
    main()

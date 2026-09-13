#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完成サムネの色を実測し、自社の再生上位5本のレンジと比べる（参考。合否ゲートではない）。

使い方:
  /usr/bin/python3 scripts/color_check.py 50A.png 50B.png
  /usr/bin/python3 scripts/color_check.py 50A.png --range ~/サムネ作業/_channel/own_color_range.json
320×180 に縮小して 明るさ（0.299R+0.587G+0.114B の平均）／彩度（HSVのS平均×100）／
白飛び（RGBすべて>245 の画素%）／R−B（平均）を出す。
レンジ＝own_channel.py が書く work_dir/_channel/own_color_range.json。無ければ数値だけ出す。
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config  # noqa: E402
from imgutil import color_metrics  # noqa: E402

KEYS = [("brightness", "明るさ"), ("saturation", "彩度"), ("white_clip", "白飛び%"), ("r_minus_b", "R−B")]


def judge(v, rng):
    if not rng:
        return ""
    lo, hi = rng
    return "レンジ内" if lo <= v <= hi else ("上回る" if v > hi else "下回る")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--range", default="", help="own_color_range.json（省略時は work_dir/_channel/ のもの）")
    a = ap.parse_args()
    from PIL import Image
    rp = os.path.expanduser(a.range) if a.range else ""
    if not rp:
        cfg = load_config(required=False)
        rp = os.path.join(cfg["work_dir"], "_channel", "own_color_range.json") if cfg.get("work_dir") else ""
    rng = {}
    if rp and os.path.exists(rp):
        with open(rp, encoding="utf-8") as f:
            rng = json.load(f)
        print(f"比較レンジ: {rp}（自社上位 {len(rng.get('videos', []))}本・{rng.get('measured_at', '')}）")
    else:
        print("比較レンジ: なし（own_color_range.json が無い → 数値だけ。先に own_channel.py を回すと比較できる）")

    head = "| 画像 | " + " | ".join(j for _, j in KEYS) + " |"
    print("\n" + head + "\n|---|" + "---:|" * len(KEYS))
    if rng:
        print("| 自社レンジ | " + " | ".join(
            f"{rng[k][0]}〜{rng[k][1]}" if k in rng else "-" for k, _ in KEYS) + " |")
    ng = 0
    for p in a.images:
        p = os.path.expanduser(p)
        if not os.path.exists(p):
            print(f"| {os.path.basename(p)} | 見つからない |")
            ng += 1
            continue
        m = color_metrics(Image.open(p))
        cells = []
        for k, _ in KEYS:
            j = judge(m[k], rng.get(k))
            cells.append(f"{m[k]}" + (f"（{j}）" if j else ""))
        print(f"| {os.path.basename(p)} | " + " | ".join(cells) + " |")
    print("\n※参考値で合否ゲートではない。彩度は後処理で上げない（生成の段階で作る）。")
    sys.exit(1 if ng else 0)


if __name__ == "__main__":
    main()

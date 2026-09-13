#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中央画像（生成画像）に座標グリッドを引いて、記号・セリフの置き場所を数値で決めるための画像を作る。

使い方:
  /usr/bin/python3 scripts/grid.py cand_C.png                # 画像と同じフォルダに出力
  /usr/bin/python3 scripts/grid.py cand_C.png --out-dir ~/サムネ作業/50
出力:
  canvas_<name>.png  1280×720 に「短辺合わせ→中央切り抜き」した画像
  grid_<name>.jpg    上に 80px毎の縦線（黄・x座標）／40px毎の横線（シアン・y座標）／
                     y150 と y491 の赤い太線（可視帯：上は1行目の黄色文字、下は2行目・3行目の帯）
★合成器（thumb_psd_compose.py）も背景を同じく「全面被覆・中央合わせ」で置く。
  だからこのグリッドで読んだ座標＝合成後の座標。ただし bg_dy を指定すると背景がその分だけ縦にずれる
  （bg_dy=+55 なら画の中身は合成後 y+55 に来る）。記号の座標は bg_dy ぶん足して考える。
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgutil import cover, jp_font  # noqa: E402

W, H, TOP, BOTTOM = 1280, 720, 150, 491


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--out-dir", default="")
    a = ap.parse_args()
    from PIL import Image, ImageDraw
    src = os.path.abspath(os.path.expanduser(a.image))
    if not os.path.exists(src):
        sys.exit(f"✗ 画像がありません: {src}")
    out = os.path.abspath(os.path.expanduser(a.out_dir)) if a.out_dir else os.path.dirname(src)
    os.makedirs(out, exist_ok=True)
    name = os.path.splitext(os.path.basename(src))[0]
    im0 = Image.open(src)
    canvas = cover(im0, W, H)
    cp = os.path.join(out, f"canvas_{name}.png")
    canvas.save(cp)

    g = canvas.copy()
    d = ImageDraw.Draw(g)
    f = jp_font(16)
    for y in range(0, H + 1, 40):
        d.line((0, y, W, y), fill=(0, 255, 255), width=1)
        d.text((4, y + 2), str(y), fill=(0, 255, 255), font=f, stroke_width=2, stroke_fill="black")
    for x in range(0, W + 1, 80):
        d.line((x, 0, x, H), fill=(255, 230, 0), width=1)
        d.text((x + 3, H - 22), str(x), fill=(255, 230, 0), font=f, stroke_width=2, stroke_fill="black")
    for y, lab in ((TOP, "y150 可視帯の上端"), (BOTTOM, "y491 可視帯の下端")):
        d.line((0, y, W, y), fill=(255, 0, 0), width=5)
        d.text((W - 190, y + 6), lab, fill=(255, 60, 60), font=f, stroke_width=2, stroke_fill="black")
    gp = os.path.join(out, f"grid_{name}.jpg")
    g.save(gp, quality=90)
    print(f"元 {im0.width}×{im0.height} → 1280×720（短辺合わせ・中央切り抜き）")
    print(f"canvas: {cp}\ngrid:   {gp}")


if __name__ == "__main__":
    main()

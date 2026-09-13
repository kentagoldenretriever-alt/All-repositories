#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画像まわりの共通ヘルパー（サムネ取得・全面被覆の切り抜き・色の実測・一覧タイル）。

他のスクリプトから import して使う。単体では動かさない。
  from imgutil import fetch_thumb, cover, color_metrics, jp_font, tile_sheet
YouTube のサムネは i.ytimg.com の maxresdefault → 無ければ hqdefault（4:3 の黒帯は cover で落ちる）。
"""
import os, urllib.request

from common import nfc


def fetch_thumb(vid, path):
    """maxresdefault → 無ければ hqdefault を保存。成功で True。"""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return True
    for q in ("maxresdefault", "hqdefault"):
        try:
            with urllib.request.urlopen(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", timeout=30) as r:
                data = r.read()
            if len(data) > 2000:
                with open(path, "wb") as f:
                    f.write(data)
                return True
        except Exception:
            continue
    return False


def cover(img, w, h):
    """短辺合わせ→中央切り抜きで w×h（合成器の背景「全面被覆・中央合わせ」と同じ）。"""
    from PIL import Image
    img = img.convert("RGB")
    sc = max(w / img.width, h / img.height)
    img = img.resize((max(w, round(img.width * sc)), max(h, round(img.height * sc))), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def color_metrics(img):
    """320×180 で 明るさ・彩度・白飛び%・R−B。hqdefault の黒帯は cover で落ちる。"""
    from PIL import ImageChops, ImageStat
    im = cover(img, 320, 180)
    r, g, b = ImageStat.Stat(im).mean
    sat = ImageStat.Stat(im.convert("HSV").split()[1]).mean[0] / 255 * 100
    m = [ch.point(lambda v: 255 if v > 245 else 0) for ch in im.split()]
    white = ImageChops.multiply(ImageChops.multiply(m[0], m[1]), m[2]).histogram()[255]
    return {"brightness": round(0.299 * r + 0.587 * g + 0.114 * b, 1), "saturation": round(sat, 1),
            "white_clip": round(white / (320 * 180) * 100, 2), "r_minus_b": round(r - b, 1)}


def jp_font(size):
    from PIL import ImageFont
    d = "/System/Library/Fonts"
    for n in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if nfc(n) in ("ヒラギノ角ゴシック W6.ttc", "ヒラギノ角ゴシック W3.ttc"):
            return ImageFont.truetype(os.path.join(d, n), size)
    return ImageFont.load_default()


def tile_sheet(tiles, out, cols=5, tw=480, th=270, label_h=40, pad=8):
    """tiles=[(画像パス or None, ラベル)] を cols 列で並べて保存。None は空きタイル。"""
    from PIL import Image, ImageDraw
    rows = max(1, (len(tiles) + cols - 1) // cols)
    W, H = cols * (tw + pad) + pad, rows * (th + label_h + pad) + pad
    sheet = Image.new("RGB", (W, H), "white")
    dr, font = ImageDraw.Draw(sheet), jp_font(22)
    for i, (p, lab) in enumerate(tiles):
        x, y = pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + label_h + pad)
        if p and os.path.exists(p):
            sheet.paste(cover(Image.open(p), tw, th), (x, y))
        else:
            dr.rectangle((x, y, x + tw, y + th), fill=(230, 230, 230))
        lab = lab or ""
        while lab and dr.textlength(lab, font=font) > tw:
            lab = lab[:-1]
        dr.text((x, y + th + 6), lab, fill="black", font=font)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out, quality=90)
    return out

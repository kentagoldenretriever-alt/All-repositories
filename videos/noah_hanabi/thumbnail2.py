"""チャンネルの体裁に合わせたサムネイル(1280x720)を作る。

上: 黄色の太字セリフ(黒フチ)
下: 黒地に水色の1行目と赤の2行目(極太・黒フチ)、1行目の末尾に米国旗
使い方: python3 thumbnail2.py [背景画像]   (省略時は out/images/b01_0.jpg)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BLACK = os.path.join(HERE, "fonts", "NotoSansCJKjp-Black.otf")
W, H = 1280, 720


def fit_font(draw, text, max_w, size):
    while size > 20:
        f = ImageFont.truetype(BLACK, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(BLACK, size)


def outlined(draw, xy, text, font, fill, stroke, width):
    draw.text(xy, text, font=font, fill=fill, stroke_width=width, stroke_fill=stroke)


def us_flag(w):
    h = int(w * 0.53)
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([0, i * h / 13, w, (i + 1) * h / 13], fill=(178, 34, 52))
    d.rectangle([0, 0, w * 0.4, h * 7 / 13], fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            x, y = w * 0.4 * (c + 0.5) / 6, h * 7 / 13 * (r + 0.5) / 5
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255))
    return img


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "images", "b01_0.jpg")
    bg = Image.open(src).convert("L").convert("RGB")  # ヒット動画に合わせてモノクロ
    # 背景を上 62% に敷く
    top_h = int(H * 0.62)
    scale = max(W / bg.width, top_h / bg.height)
    bg = bg.resize((int(bg.width * scale), int(bg.height * scale)), Image.LANCZOS)
    x0 = (bg.width - W) // 2
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    canvas.paste(bg.crop((x0, 0, x0 + W, top_h)), (0, 0))
    d = ImageDraw.Draw(canvas)

    quote = "「僕、日本に行きたい…」"
    f = fit_font(d, quote, W - 30, 96)
    outlined(d, ((W - d.textlength(quote, font=f)) / 2, 6), quote, f, (255, 238, 0), (0, 0, 0), 9)

    flag = us_flag(170)
    canvas.paste(flag, (36, 150))

    small = "ママ、僕、日本に行きたい…"
    fs = ImageFont.truetype(BLACK, 34)
    outlined(d, (W - d.textlength(small, font=fs) - 60, top_h - 70), small, fs, (255, 255, 255), (0, 0, 0), 4)

    line1 = "余命宣告された少年の最後の願いを叶えに"
    f1 = fit_font(d, line1, W - 20, 84)
    outlined(d, ((W - d.textlength(line1, font=f1)) / 2, top_h + 8), line1, f1, (0, 230, 255), (0, 0, 0), 7)

    line2 = "訪れた日本で起きた奇跡とは？"
    f2 = fit_font(d, line2, W - 20, 104)
    outlined(d, ((W - d.textlength(line2, font=f2)) / 2, top_h + 118), line2, f2, (235, 20, 20), (0, 0, 0), 7)

    out = os.path.join(HERE, "out", "thumbnail_v2.png")
    canvas.save(out)
    print(out)


if __name__ == "__main__":
    main()

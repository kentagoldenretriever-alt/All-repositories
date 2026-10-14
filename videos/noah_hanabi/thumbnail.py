"""サムネイル画像(1280x720)を作る。"""
import os
from PIL import Image, ImageDraw, ImageFont
import scenes

HERE = os.path.dirname(os.path.abspath(__file__))
img = scenes.s_fireworks("gold").crop((96, 54, 96 + 1920, 54 + 1080))
d = ImageDraw.Draw(img)
f1 = ImageFont.truetype(scenes.FONT, 150)
f2 = ImageFont.truetype(scenes.FONT, 110)
f3 = ImageFont.truetype(scenes.FONT, 80)
d.rectangle([0, 0, 1920, 190], fill=(200, 20, 30))
d.text((60, 25), "余命1年の少年", font=f1, fill=(255, 255, 255), stroke_width=8, stroke_fill=(0, 0, 0))
d.text((1080, 55), "最後の夢は日本", font=f3, fill=(255, 240, 120), stroke_width=6, stroke_fill=(0, 0, 0))
d.text((60, 720), "日本人医師の「ある疑問」が", font=f2, fill=(255, 255, 255), stroke_width=9, stroke_fill=(0, 0, 0))
d.text((60, 860), "運命を変えた", font=f1, fill=(255, 220, 60), stroke_width=10, stroke_fill=(0, 0, 0))
img.resize((1280, 720), Image.LANCZOS).save(os.path.join(HERE, "out", "thumbnail.png"))

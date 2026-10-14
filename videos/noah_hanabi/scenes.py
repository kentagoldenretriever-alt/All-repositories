"""背景イラストを手続き的に描画する。各シーンは W x H のPNGとして書き出す。

画像生成AIが使えない環境向けに、PILだけで「フラットイラスト風」の背景を作る。
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 2112, 1188  # 1920x1080 より一回り大きく描き、動画側でゆっくりパンする
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"


# ---------------------------------------------------------------- helpers
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(top, bottom, size=(W, H), stops=None):
    top, bottom = rgb(top), rgb(bottom)
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / (size[1] - 1)
        d.line([(0, y), (size[0], y)], fill=lerp(top, bottom, t))
    return img


def gradient3(top, mid, bottom, midpos=0.5):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    a, b, c = rgb(top), rgb(mid), rgb(bottom)
    for y in range(H):
        t = y / (H - 1)
        col = lerp(a, b, t / midpos) if t < midpos else lerp(b, c, (t - midpos) / (1 - midpos))
        d.line([(0, y), (W, y)], fill=col)
    return img


def glow_layer(base, draw_fn, radius=30, strength=1.0):
    """draw_fn(draw) で描いた発光体を、ぼかしてから加算合成する。"""
    layer = Image.new("RGB", base.size, (0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    blurred = layer.filter(ImageFilter.GaussianBlur(radius))
    out = Image.blend(base, base, 0)
    from PIL import ImageChops
    out = ImageChops.add(base, blurred.point(lambda v: min(255, int(v * strength))))
    out = ImageChops.add(out, layer)
    return out


def add(base, layer):
    from PIL import ImageChops
    return ImageChops.add(base, layer)


def stars(d, n=300, ymax=0.6, seed=1):
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.randint(0, W), r.randint(0, int(H * ymax))
        s = r.choice([1, 1, 1, 2, 2, 3])
        c = r.randint(150, 255)
        d.ellipse([x, y, x + s, y + s], fill=(c, c, min(255, c + 20)))


def vignette(img, strength=0.55):
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    w, h = img.size
    d.ellipse([-w * 0.15, -h * 0.25, w * 1.15, h * 1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", img.size, (0, 0, 0))
    v = Image.composite(img, dark, mask)
    return Image.blend(img, v, strength)


def grain(img, amount=10, seed=3):
    noise = Image.effect_noise(img.size, amount).convert("RGB")
    return Image.blend(img, noise, 0.04)


def person(d, x, y, h, color, kind="adult", hair=None):
    """シルエットの人物。(x, y) は足元中央。"""
    head = h * (0.16 if kind == "adult" else 0.2)
    body_w = h * (0.28 if kind == "adult" else 0.32)
    d.ellipse([x - head / 2, y - h, x + head / 2, y - h + head], fill=color)
    top = y - h + head * 1.05
    d.rounded_rectangle([x - body_w / 2, top, x + body_w / 2, y - h * 0.38],
                        radius=int(body_w * 0.35), fill=color)
    leg = body_w * 0.36
    d.rounded_rectangle([x - body_w / 2 + 2, y - h * 0.42, x - body_w / 2 + 2 + leg, y],
                        radius=int(leg / 2), fill=color)
    d.rounded_rectangle([x + body_w / 2 - 2 - leg, y - h * 0.42, x + body_w / 2 - 2, y],
                        radius=int(leg / 2), fill=color)


def seated(d, x, y, h, color, kind="adult"):
    """座っている人物(後ろ姿)。(x, y) は腰の位置。"""
    head = h * (0.22 if kind == "adult" else 0.26)
    body_w = h * (0.36 if kind == "adult" else 0.4)
    d.ellipse([x - head / 2, y - h, x + head / 2, y - h + head], fill=color)
    d.rounded_rectangle([x - body_w / 2, y - h + head * 1.02, x + body_w / 2, y],
                        radius=int(body_w * 0.4), fill=color)


def wheelchair(d, x, y, s, color, rider=None):
    """車椅子(横向き)。(x, y) は大きい車輪の中心。"""
    d.ellipse([x - s, y - s, x + s, y + s], outline=color, width=max(3, int(s * 0.12)))
    d.ellipse([x - s * 0.15, y - s * 0.15, x + s * 0.15, y + s * 0.15], fill=color)
    d.ellipse([x + s * 1.3, y + s * 0.55, x + s * 1.75, y + s], outline=color, width=4)
    d.line([x - s * 0.2, y - s * 0.9, x + s * 1.3, y - s * 0.9], fill=color, width=int(s * 0.14))
    d.line([x - s * 0.2, y - s * 0.9, x - s * 0.5, y - s * 2.1], fill=color, width=int(s * 0.12))
    d.line([x + s * 1.3, y - s * 0.9, x + s * 1.5, y + s * 0.55], fill=color, width=int(s * 0.1))
    if rider:
        d.ellipse([x - s * 0.25, y - s * 2.7, x + s * 0.55, y - s * 1.9], fill=rider)
        d.rounded_rectangle([x - s * 0.35, y - s * 1.95, x + s * 0.55, y - s * 0.85], radius=int(s * 0.3), fill=rider)
        d.rounded_rectangle([x + s * 0.2, y - s * 1.15, x + s * 1.35, y - s * 0.75], radius=int(s * 0.2), fill=rider)
        d.rounded_rectangle([x + s * 1.0, y - s * 1.15, x + s * 1.35, y + s * 0.2], radius=int(s * 0.17), fill=rider)


def house(d, x, y, w, h, wall, roof, window=None, jp=False):
    d.rectangle([x, y - h, x + w, y], fill=wall)
    if jp:
        d.polygon([(x - w * 0.12, y - h), (x + w * 1.12, y - h), (x + w * 0.85, y - h * 1.45),
                   (x + w * 0.15, y - h * 1.45)], fill=roof)
    else:
        d.polygon([(x - w * 0.08, y - h), (x + w * 1.08, y - h), (x + w / 2, y - h * 1.6)], fill=roof)
    if window:
        ww = w * 0.22
        for i in (0.2, 0.58):
            d.rectangle([x + w * i, y - h * 0.7, x + w * i + ww, y - h * 0.38], fill=window)


def lantern(d, x, y, s, lit=True):
    body = (230, 60, 45) if lit else (170, 40, 35)
    d.rectangle([x - s * 0.35, y - s * 0.75, x + s * 0.35, y - s * 0.62], fill=(40, 30, 30))
    d.ellipse([x - s * 0.55, y - s * 0.65, x + s * 0.55, y + s * 0.65], fill=body)
    for k in (-0.35, 0, 0.35):
        d.arc([x - s * 0.55, y - s * 0.65 + s * k * 0.3, x + s * 0.55, y + s * 0.65 + s * k * 0.3],
              200, 340, fill=(150, 35, 30), width=2)
    d.rectangle([x - s * 0.35, y + s * 0.62, x + s * 0.35, y + s * 0.75], fill=(40, 30, 30))


def lantern_row(img, y0, n, s, sag=40, lit=True, x0=-50, x1=None):
    x1 = x1 or W + 50
    d = ImageDraw.Draw(img)
    pts = [(x0 + (x1 - x0) * i / 40, y0 + sag * math.sin(math.pi * i / 40)) for i in range(41)]
    d.line(pts, fill=(30, 25, 25), width=3)
    centers = []
    for i in range(n):
        t = (i + 0.5) / n
        x = x0 + (x1 - x0) * t
        y = y0 + sag * math.sin(math.pi * t) + s * 0.9
        centers.append((x, y))
    if lit:
        def fn(g):
            for x, y in centers:
                g.ellipse([x - s, y - s, x + s, y + s], fill=(255, 120, 60))
        img = glow_layer(img, fn, radius=int(s * 0.9), strength=0.6)
    d = ImageDraw.Draw(img)
    for x, y in centers:
        d.line([x, y - s * 0.9, x, y - s * 0.75], fill=(30, 25, 25), width=2)
        lantern(d, x, y, s, lit)
    return img


def firework(img, cx, cy, r, color, seed=0, rings=1, trail=True, glow=True, density=1.0):
    """まん丸に開く花火。光の粒を同心円状に並べる。"""
    rnd = random.Random(seed)
    color = rgb(color) if isinstance(color, str) else color
    layer = Image.new("RGB", img.size, (0, 0, 0))
    d = ImageDraw.Draw(layer)
    for ring in range(rings):
        rr = r * (1 - ring * 0.42)
        n = int((90 - ring * 30) * density)
        col = color if ring == 0 else lerp(color, (255, 255, 230), 0.6)
        for k in range(n):
            a = 2 * math.pi * k / n + rnd.uniform(-0.01, 0.01)
            for j in range(9 if trail else 1):
                t = 1 - j * 0.06
                px, py = cx + math.cos(a) * rr * t, cy + math.sin(a) * rr * t + j * j * 0.4
                s = max(1.2, rr * 0.012 * (1 - j * 0.09))
                c = lerp((0, 0, 0), col, max(0.15, 1 - j * 0.11))
                d.ellipse([px - s, py - s, px + s, py + s], fill=c)
    d.ellipse([cx - r * 0.05, cy - r * 0.05, cx + r * 0.05, cy + r * 0.05], fill=lerp(color, (255, 255, 255), 0.5))
    if glow:
        g = layer.filter(ImageFilter.GaussianBlur(r * 0.08))
        img = add(img, g)
        g2 = layer.filter(ImageFilter.GaussianBlur(r * 0.35)).point(lambda v: int(v * 0.8))
        img = add(img, g2)
    return add(img, layer)


def reflection(img, y_water, strength=0.45, blur=6):
    """水面への映り込み。"""
    sky = img.crop((0, 0, W, y_water)).transpose(Image.FLIP_TOP_BOTTOM)
    h = min(sky.size[1], H - y_water)
    sky = sky.crop((0, 0, W, h)).filter(ImageFilter.GaussianBlur(blur))
    water = img.crop((0, y_water, W, y_water + h))
    # 横縞のゆらぎ
    rip = Image.new("L", (W, h), 0)
    d = ImageDraw.Draw(rip)
    r = random.Random(9)
    for y in range(0, h, 6):
        d.line([(0, y), (W, y)], fill=int(255 * strength * (0.6 + 0.4 * r.random())), width=3)
    mixed = Image.composite(sky, water, rip)
    img.paste(mixed, (0, y_water))
    return img


def text_center(img, text, y, size, fill=(255, 255, 255), stroke=6, stroke_fill=(0, 0, 0)):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, size)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def finish(img, vig=0.5):
    img = vignette(img, vig)
    return grain(img)


# ---------------------------------------------------------------- reusable sets
def night_river_base(sky=("#060a1e", "#1b2350", "#2b2a55"), with_town=True):
    img = gradient3(*sky, midpos=0.6)
    d = ImageDraw.Draw(img)
    stars(d, 220, 0.5)
    y_w = int(H * 0.72)
    if with_town:
        r = random.Random(4)
        x = -20
        while x < W:
            w = r.randint(90, 180)
            h = r.randint(40, 110)
            house(d, x, y_w - 30, w, h, (18, 20, 40), (12, 14, 30), window=(255, 200, 120) if r.random() < 0.4 else None, jp=True)
            x += w + r.randint(10, 40)
        d.rectangle([0, y_w - 32, W, y_w], fill=(14, 16, 32))
    d.rectangle([0, y_w, W, H], fill=(10, 14, 36))
    return img, y_w


def embankment_crowd(img, y, color=(8, 8, 16), seed=2, n=60, scale=1.0):
    d = ImageDraw.Draw(img)
    d.polygon([(0, y), (W, y - 40), (W, H), (0, H)], fill=color)
    r = random.Random(seed)
    for i in range(n):
        x = r.randint(-40, W + 40)
        hh = r.randint(110, 170) * scale
        seated(d, x, y + r.randint(30, 140) * scale + hh * 0.5, hh, color, "adult" if r.random() < 0.7 else "child")
    return img


def room(wall, floor, window_sky=None, window_box=None):
    img = gradient(wall[0], wall[1])
    d = ImageDraw.Draw(img)
    fy = int(H * 0.78)
    d.rectangle([0, fy, W, H], fill=rgb(floor))
    d.line([0, fy, W, fy], fill=(0, 0, 0), width=4)
    if window_box:
        x0, y0, x1, y1 = window_box
        if window_sky:
            win = gradient(window_sky[0], window_sky[1], size=(x1 - x0, y1 - y0))
            img.paste(win, (x0, y0))
        d.rectangle(window_box, outline=(70, 60, 55), width=18)
        d.line([(x0 + x1) // 2, y0, (x0 + x1) // 2, y1], fill=(70, 60, 55), width=12)
    return img, fy


def bed(d, x, y, w, color=(235, 235, 240), frame=(150, 160, 175)):
    d.rectangle([x, y - 140, x + w, y - 60], fill=color)
    d.rounded_rectangle([x + 20, y - 190, x + 220, y - 130], radius=30, fill=(250, 250, 252))
    d.rectangle([x - 10, y - 260, x + 15, y], fill=frame)
    d.rectangle([x + w - 15, y - 180, x + w + 10, y], fill=frame)
    d.rectangle([x, y - 70, x + w, y - 50], fill=frame)


def iv_stand(d, x, y):
    d.line([x, y, x, y - 560], fill=(170, 175, 185), width=8)
    d.line([x - 60, y - 560, x + 60, y - 560], fill=(170, 175, 185), width=6)
    d.rounded_rectangle([x + 20, y - 540, x + 70, y - 450], radius=10, fill=(220, 235, 245), outline=(160, 170, 180), width=3)
    d.line([x + 45, y - 450, x + 140, y - 260], fill=(200, 210, 220), width=3)
    for dx in (-60, 0, 60):
        d.line([x, y, x + dx, y + 20], fill=(150, 155, 165), width=6)


def brain_scan(size, seed=0, tumor=(0.62, 0.42, 0.08)):
    """モノクロの脳MRI風画像。"""
    s = size
    img = Image.new("RGB", (s, s), (5, 5, 8))
    d = ImageDraw.Draw(img)
    d.ellipse([s * 0.15, s * 0.08, s * 0.85, s * 0.92], fill=(190, 190, 195))
    d.ellipse([s * 0.18, s * 0.11, s * 0.82, s * 0.89], fill=(70, 70, 78))
    r = random.Random(seed)
    for _ in range(140):
        a = r.uniform(0, 2 * math.pi)
        rr = r.uniform(0.05, 0.3)
        x, y = s * (0.5 + math.cos(a) * rr), s * (0.5 + math.sin(a) * rr * 1.25)
        w = r.uniform(0.02, 0.06) * s
        c = r.randint(110, 170)
        d.ellipse([x - w, y - w * 0.4, x + w, y + w * 0.4], fill=(c, c, c + 4))
    d.line([s * 0.5, s * 0.14, s * 0.5, s * 0.86], fill=(30, 30, 35), width=max(2, s // 120))
    d.ellipse([s * 0.43, s * 0.38, s * 0.48, s * 0.55], fill=(25, 25, 30))
    d.ellipse([s * 0.52, s * 0.38, s * 0.57, s * 0.55], fill=(25, 25, 30))
    tx, ty, tr = tumor
    d.ellipse([s * (tx - tr), s * (ty - tr), s * (tx + tr), s * (ty + tr)], fill=(235, 235, 240))
    d.ellipse([s * (tx - tr * 0.5), s * (ty - tr * 0.5), s * (tx + tr * 0.5), s * (ty + tr * 0.4)], fill=(140, 140, 145))
    return img.filter(ImageFilter.GaussianBlur(s / 260))


def monitor(img, box, content):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 - 22, y0 - 22, x1 + 22, y1 + 22], radius=18, fill=(30, 32, 38))
    img.paste(content.resize((x1 - x0, y1 - y0)), (x0, y0))
    d.rectangle([(x0 + x1) / 2 - 30, y1 + 22, (x0 + x1) / 2 + 30, y1 + 110], fill=(30, 32, 38))
    d.rounded_rectangle([(x0 + x1) / 2 - 150, y1 + 100, (x0 + x1) / 2 + 150, y1 + 130], radius=10, fill=(30, 32, 38))


# ---------------------------------------------------------------- scenes
def s_title():
    img = gradient3("#02030a", "#0b0f2a", "#1a1430", 0.7)
    d = ImageDraw.Draw(img)
    stars(d, 300, 0.7)
    img = firework(img, W * 0.22, H * 0.3, 260, "#ffcc66", seed=1, rings=2)
    img = firework(img, W * 0.8, H * 0.25, 200, "#ff7799", seed=2, rings=2)
    img = firework(img, W * 0.55, H * 0.15, 120, "#88ccff", seed=3)
    img = embankment_crowd(img, int(H * 0.86), n=40, scale=0.8)
    text_center(img, "余命1年と告げられた少年が", int(H * 0.40), 110, fill=(255, 255, 255), stroke=10)
    text_center(img, "日本で見た「まん丸の花火」", int(H * 0.53), 130, fill=(255, 214, 90), stroke=12)
    return finish(img, 0.4)


def s_midwest(season="autumn"):
    if season == "spring":
        img = gradient3("#8fb8e0", "#cfe3f0", "#e8efe0", 0.55)
        field = (120, 160, 80)
    elif season == "summer":
        img = gradient3("#5d9de0", "#a8d4f5", "#eaf4f0", 0.55)
        field = (110, 160, 70)
    else:
        img = gradient3("#3b4a7a", "#e59a6a", "#f4c98a", 0.6)
        field = (150, 120, 70)
    d = ImageDraw.Draw(img)
    hy = int(H * 0.62)
    d.rectangle([0, hy, W, H], fill=field)
    for i in range(14):
        y = hy + (i + 1) ** 1.6 * 4
        d.line([0, y, W, y], fill=lerp(field, (60, 50, 30), 0.25), width=2 + i // 3)
    # 工場
    fx = int(W * 0.7)
    d.rectangle([fx, hy - 160, fx + 380, hy], fill=(70, 70, 85))
    for k in range(4):
        d.polygon([(fx + k * 95, hy - 160), (fx + k * 95 + 95, hy - 160), (fx + k * 95 + 95, hy - 220)], fill=(60, 60, 75))
    d.rectangle([fx + 300, hy - 360, fx + 340, hy - 160], fill=(80, 75, 85))
    for k in range(5):
        d.ellipse([fx + 290 + k * 40, hy - 420 - k * 50, fx + 370 + k * 55, hy - 360 - k * 45], fill=(200, 200, 205))
    # 家と給水塔
    house(d, int(W * 0.18), hy + 10, 220, 150, (220, 205, 180), (120, 60, 50), window=(255, 230, 160))
    house(d, int(W * 0.36), hy + 5, 160, 110, (200, 190, 175), (90, 70, 60), window=(255, 230, 160))
    tx = int(W * 0.52)
    d.ellipse([tx - 70, hy - 330, tx + 70, hy - 230], fill=(190, 190, 200))
    for dx in (-50, 50):
        d.line([tx + dx, hy - 250, tx + dx * 1.4, hy], fill=(150, 150, 160), width=8)
    # 電柱
    for k in range(6):
        px = 80 + k * 400
        d.line([px, hy - 200, px, hy + 60], fill=(70, 55, 45), width=10)
        d.line([px - 40, hy - 180, px + 40, hy - 180], fill=(70, 55, 45), width=8)
    d.line([(80 + k * 400, hy - 175) for k in range(6)], fill=(40, 40, 40), width=2)
    return finish(img, 0.35)


def s_dawn():
    img = gradient3("#1a2140", "#5a5a8a", "#e8a070", 0.7)
    d = ImageDraw.Draw(img)
    stars(d, 60, 0.3)
    hy = int(H * 0.7)
    d.rectangle([0, hy, W, H], fill=(30, 30, 45))
    house(d, int(W * 0.3), hy, 520, 300, (60, 55, 70), (40, 35, 50), window=None)
    d.rectangle([int(W * 0.3) + 110, hy - 210, int(W * 0.3) + 220, hy - 110], fill=(255, 210, 130))
    person(d, int(W * 0.62), hy + 40, 300, (20, 20, 30))
    d.rounded_rectangle([int(W * 0.66), hy - 80, int(W * 0.69), hy - 10], radius=8, fill=(20, 20, 30))
    return finish(img, 0.5)


def s_noah_room(dark=False):
    img, fy = room(("#3a3560", "#2a2848") if not dark else ("#16142a", "#100e20"), "#4a3a35",
                   window_sky=("#0a0f30", "#25306a"), window_box=(1400, 160, 1880, 600))
    d = ImageDraw.Draw(img)
    r = random.Random(5)
    cols = [(240, 120, 140), (110, 190, 240), (250, 210, 90), (150, 220, 150), (220, 150, 240), (250, 160, 90)]
    for k, (x, y) in enumerate([(160, 170), (430, 140), (700, 200), (230, 470), (560, 450), (980, 170)]):
        w, h = 220, 300
        c = cols[k] if not dark else lerp(cols[k], (20, 20, 30), 0.7)
        d.rectangle([x, y, x + w, y + h], fill=c)
        d.ellipse([x + 50, y + 50, x + 170, y + 170], fill=lerp(c, (255, 255, 255), 0.4))
        d.polygon([(x + 30, y + h - 20), (x + 110, y + 150), (x + 190, y + h - 20)], fill=lerp(c, (0, 0, 0), 0.3))
        d.rectangle([x + 20, y + h - 60, x + w - 20, y + h - 30], fill=lerp(c, (0, 0, 0), 0.5))
    # テレビ
    tx, ty = 900, fy - 330
    d.rectangle([tx - 40, ty + 250, tx + 460, fy], fill=(60, 45, 40))
    d.rounded_rectangle([tx, ty - 60, tx + 420, ty + 250], radius=20, fill=(30, 30, 35))
    if not dark:
        scr = gradient("#9fd8ff", "#f6e7a8", size=(360, 250))
        sd = ImageDraw.Draw(scr)
        sd.ellipse([220, 30, 300, 110], fill=(255, 250, 200))
        sd.polygon([(0, 250), (120, 120), (240, 250)], fill=(110, 170, 120))
        img.paste(scr, (tx + 30, ty - 30))

        def g(gd):
            gd.rectangle([tx, ty - 60, tx + 420, ty + 250], fill=(90, 130, 170))
        img = glow_layer(img, g, 120, 0.5)
        d = ImageDraw.Draw(img)
        seated(d, tx + 210, fy + 120, 260, (15, 15, 25), "child")
    else:
        d.rectangle([tx + 30, ty - 30, tx + 390, ty + 220], fill=(12, 12, 16))
        # ベッドで丸くなる少年
        d.rounded_rectangle([1350, fy - 160, 2050, fy], radius=30, fill=(40, 40, 70))
        d.ellipse([1500, fy - 230, 1800, fy - 120], fill=(55, 55, 90))
    return finish(img, 0.55)


def s_hospital_us():
    img, fy = room(("#dfe6ea", "#c8d3d8"), "#9aa6ad", window_sky=("#a8c8e8", "#dceaf5"), window_box=(1450, 150, 1950, 560))
    d = ImageDraw.Draw(img)
    # 受付カウンターと待合の椅子
    d.rectangle([150, fy - 260, 900, fy], fill=(120, 140, 160))
    d.rectangle([150, fy - 290, 900, fy - 250], fill=(90, 110, 130))
    d.rectangle([380, 150, 680, 230], fill=(60, 120, 170))
    d.text((420, 165), "HOSPITAL", font=ImageFont.truetype(FONT, 48), fill=(255, 255, 255))
    for k in range(5):
        x = 1000 + k * 170
        d.rounded_rectangle([x, fy - 140, x + 140, fy - 90], radius=10, fill=(70, 110, 150))
        d.rounded_rectangle([x, fy - 250, x + 140, fy - 130], radius=12, fill=(80, 120, 160))
        d.line([x + 20, fy - 90, x + 20, fy], fill=(60, 60, 70), width=6)
        d.line([x + 120, fy - 90, x + 120, fy], fill=(60, 60, 70), width=6)
    seated(d, 1340, fy - 90, 260, (60, 60, 75))
    seated(d, 1510, fy - 90, 190, (60, 60, 75), "child")
    return finish(img, 0.35)


def s_scan_us():
    img = gradient("#141a24", "#0a0d14")
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(H * 0.8), W, H], fill=(25, 22, 22))
    monitor(img, (560, 160, 1560, 760), brain_scan(800, seed=4))

    def g(gd):
        gd.rectangle([560, 160, 1560, 760], fill=(80, 90, 110))
    img = glow_layer(img, g, 150, 0.6)
    d = ImageDraw.Draw(img)
    seated(d, 330, int(H * 0.98), 420, (8, 8, 12))
    seated(d, 1830, int(H * 0.98), 470, (8, 8, 12))
    return finish(img, 0.6)


def s_parking():
    img = gradient3("#24284a", "#b0607a", "#f0a868", 0.65)
    d = ImageDraw.Draw(img)
    hy = int(H * 0.62)
    d.rectangle([0, hy, W, H], fill=(45, 45, 55))
    d.rectangle([200, hy - 330, 1100, hy], fill=(70, 70, 90))
    for i in range(6):
        for j in range(4):
            d.rectangle([240 + i * 140, hy - 300 + j * 70, 320 + i * 140, hy - 260 + j * 70], fill=(240, 200, 140) if (i + j) % 3 else (90, 90, 110))
    for k in range(8):
        d.line([k * 300 - 100, H, k * 300 + 100, hy + 40], fill=(200, 200, 160), width=6)
    # 車(後ろ姿)
    cx, cy = 1400, 980
    d.rounded_rectangle([cx - 330, cy - 260, cx + 330, cy], radius=60, fill=(25, 25, 35))
    d.rounded_rectangle([cx - 250, cy - 420, cx + 250, cy - 230], radius=60, fill=(25, 25, 35))
    d.rounded_rectangle([cx - 220, cy - 400, cx + 220, cy - 260], radius=40, fill=(230, 150, 110))
    seated(d, cx, cy - 250, 150, (25, 25, 35))
    d.rectangle([cx - 320, cy - 140, cx - 220, cy - 100], fill=(200, 40, 40))
    d.rectangle([cx + 220, cy - 140, cx + 320, cy - 100], fill=(200, 40, 40))
    return finish(img, 0.55)


def s_living_room():
    img, fy = room(("#4a3d40", "#3a2f35"), "#5a463c", window_sky=("#e08a5a", "#f3c88a"), window_box=(160, 160, 640, 560))
    d = ImageDraw.Draw(img)
    # テレビの光とソファの後ろ姿
    d.rounded_rectangle([1450, 300, 1950, 620], radius=16, fill=(30, 30, 35))
    d.rectangle([1475, 325, 1925, 595], fill=(150, 200, 240))

    def g(gd):
        gd.rectangle([1450, 300, 1950, 620], fill=(90, 120, 160))
    img = glow_layer(img, g, 140, 0.5)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([700, fy - 260, 1600, fy + 80], radius=50, fill=(90, 60, 55))
    seated(d, 1120, fy - 170, 230, (20, 15, 20), "child")
    d.rounded_rectangle([700, fy - 140, 1600, fy + 80], radius=50, fill=(110, 75, 65))
    person(d, 420, H - 20, 560, (15, 12, 18))
    return finish(img, 0.55)


def s_kitchen_table():
    img, fy = room(("#5a4a42", "#463a36"), "#3a2e2a")
    d = ImageDraw.Draw(img)
    d.ellipse([W / 2 - 120, 80, W / 2 + 120, 180], fill=(255, 220, 150))

    def g(gd):
        gd.polygon([(W / 2 - 100, 160), (W / 2 + 100, 160), (W / 2 + 700, fy + 100), (W / 2 - 700, fy + 100)], fill=(90, 70, 40))
    img = glow_layer(img, g, 80, 0.6)
    d = ImageDraw.Draw(img)
    d.line([W / 2, 0, W / 2, 90], fill=(30, 25, 25), width=6)
    d.rectangle([300, fy - 120, W - 300, fy - 70], fill=(140, 95, 60))
    for k in range(18):
        d.line([320 + k * 85, fy - 115, 360 + k * 85, fy - 75], fill=(120, 80, 50), width=2)
    d.rectangle([380, fy - 70, 420, H], fill=(110, 75, 50))
    d.rectangle([W - 420, fy - 70, W - 380, H], fill=(110, 75, 50))
    seated(d, 620, fy - 100, 420, (25, 20, 25))
    seated(d, W - 650, fy - 100, 300, (25, 20, 25), "child")
    d.rounded_rectangle([760, fy - 160, W - 790, fy - 115], radius=20, fill=(25, 20, 25))
    return finish(img, 0.6)


def s_kitchen_night():
    img, fy = room(("#232840", "#1a1e32"), "#2a2a3a", window_sky=("#05081a", "#141a3a"), window_box=(700, 140, 1400, 520))
    d = ImageDraw.Draw(img)
    d.rectangle([500, fy - 260, 1650, fy], fill=(60, 65, 85))
    d.rectangle([480, fy - 290, 1670, fy - 250], fill=(150, 155, 170))
    d.rectangle([900, fy - 285, 1200, fy - 255], fill=(90, 100, 120))
    d.line([1050, fy - 290, 1050, fy - 380], fill=(180, 185, 195), width=12)
    d.line([1050, fy - 380, 1110, fy - 380], fill=(180, 185, 195), width=12)
    d.line([1105, fy - 375, 1105, fy - 300], fill=(150, 200, 255), width=3)
    person(d, 1180, fy + 60, 520, (15, 15, 25))
    person(d, 1850, fy + 120, 330, (35, 35, 55), "child")
    return finish(img, 0.6)


def s_airplane():
    img = gradient3("#3d6fb6", "#8fbbe6", "#f3e2c2", 0.7)
    d = ImageDraw.Draw(img)
    r = random.Random(7)
    for _ in range(14):
        x, y = r.randint(-100, W), r.randint(int(H * 0.5), H)
        for k in range(6):
            rr = r.randint(80, 180)
            d.ellipse([x + k * 90 - rr, y - rr * 0.6, x + k * 90 + rr, y + rr * 0.6], fill=(250, 250, 255))
    img = img.filter(ImageFilter.GaussianBlur(3))
    d = ImageDraw.Draw(img)
    # 飛行機
    px, py, s = W * 0.55, H * 0.33, 1.4
    d.polygon([(px - 420 * s, py), (px + 380 * s, py - 30 * s), (px + 470 * s, py), (px + 380 * s, py + 30 * s), (px - 420 * s, py + 30 * s)], fill=(245, 245, 250))
    d.polygon([(px - 50 * s, py), (px + 80 * s, py), (px - 140 * s, py + 260 * s), (px - 230 * s, py + 260 * s)], fill=(220, 225, 235))
    d.polygon([(px - 50 * s, py), (px + 80 * s, py), (px - 180 * s, py - 200 * s), (px - 250 * s, py - 200 * s)], fill=(210, 215, 228))
    d.polygon([(px - 380 * s, py), (px - 320 * s, py), (px - 430 * s, py - 150 * s), (px - 470 * s, py - 150 * s)], fill=(200, 60, 60))
    for k in range(14):
        d.ellipse([px - 300 * s + k * 45 * s, py - 12 * s, px - 285 * s + k * 45 * s, py + 2 * s], fill=(80, 100, 130))
    return finish(img, 0.3)


def s_airport():
    img = gradient("#e8ecef", "#cfd6db")
    d = ImageDraw.Draw(img)
    fy = int(H * 0.8)
    for k in range(9):
        x = k * 260
        d.rectangle([x, 80, x + 230, fy - 120], fill=(170, 200, 225))
        d.line([x + 115, 80, x + 115, fy - 120], fill=(200, 210, 220), width=4)
    d.rectangle([0, 0, W, 80], fill=(200, 205, 210))
    d.rectangle([0, fy - 120, W, fy], fill=(210, 215, 220))
    d.rectangle([0, fy, W, H], fill=(190, 192, 195))
    d.rectangle([700, 140, 1500, 280], fill=(30, 40, 60))
    f = ImageFont.truetype(FONT, 64)
    d.text((740, 170), "到着 Arrivals  →", font=f, fill=(255, 220, 80))
    wheelchair(d, 1100, fy + 40, 80, (40, 40, 60), rider=(50, 60, 100))
    person(d, 970, fy + 130, 440, (60, 50, 70))
    person(d, 1380, fy + 130, 360, (30, 70, 120))
    r = random.Random(11)
    for _ in range(12):
        x = r.randint(0, W)
        if 850 < x < 1500:
            continue
        person(d, x, fy + r.randint(60, 140), r.randint(300, 420), lerp((120, 125, 140), (60, 60, 80), r.random()))
    return finish(img, 0.3)


def s_tokyo():
    img = gradient3("#4d8fd8", "#a6cdf0", "#f6f0dc", 0.7)
    d = ImageDraw.Draw(img)
    d.ellipse([1700, 60, 1900, 260], fill=(255, 250, 220))

    def g(gd):
        gd.ellipse([1650, 10, 1950, 310], fill=(255, 230, 150))
    img = glow_layer(img, g, 120, 0.8)
    d = ImageDraw.Draw(img)
    r = random.Random(3)
    gy = int(H * 0.82)
    x = -30
    while x < W:
        w = r.randint(120, 260)
        h = r.randint(300, 760)
        c = lerp((150, 165, 190), (90, 100, 130), r.random())
        d.rectangle([x, gy - h, x + w, gy], fill=c)
        for yy in range(gy - h + 30, gy - 40, 50):
            for xx in range(x + 20, x + w - 30, 45):
                d.rectangle([xx, yy, xx + 22, yy + 28], fill=lerp(c, (230, 240, 255), 0.4))
        if r.random() < 0.6:
            sc = r.choice([(230, 60, 70), (250, 200, 50), (60, 160, 230), (240, 120, 40)])
            sw = min(w - 20, 120)
            d.rectangle([x + 10, gy - h + 60, x + 10 + 50, gy - h + 60 + r.randint(200, 360)], fill=sc)
            d.rectangle([x + 70, gy - h * 0.45, x + 70 + sw * 0.7, gy - h * 0.45 + 70], fill=lerp(sc, (255, 255, 255), 0.2))
        x += w + r.randint(0, 20)
    d.rectangle([0, gy, W, H], fill=(120, 120, 125))
    for k in range(14):
        d.rectangle([k * 160, gy + 60, k * 160 + 90, H], fill=(235, 235, 235))
    for _ in range(90):
        person(d, r.randint(-20, W + 20), r.randint(gy + 120, H + 60), r.randint(160, 260), lerp((40, 40, 55), (90, 90, 110), r.random()))
    # 陽炎
    return finish(img, 0.3)


def s_hotel():
    img, fy = room(("#d9cbb5", "#c4b39a"), "#8a6a50", window_sky=("#8cb6e0", "#dfe9f1"), window_box=(1350, 140, 1950, 600))
    d = ImageDraw.Draw(img)
    d.rectangle([1360, 150, 1940, 590], fill=(200, 190, 175))  # カーテンを閉めた窓
    for k in range(12):
        d.line([1360 + k * 50, 150, 1360 + k * 50, 590], fill=(180, 168, 150), width=6)
    bed(d, 200, fy + 40, 900)
    d.ellipse([290, fy - 230, 430, fy - 120], fill=(70, 60, 60))
    d.rounded_rectangle([420, fy - 170, 900, fy - 100], radius=30, fill=(200, 210, 230))
    seated(d, 1200, fy + 30, 380, (60, 50, 60))
    return finish(img, 0.5)


def s_riverside(evening=False):
    if evening:
        img = gradient3("#3a3a78", "#d8807a", "#f6c890", 0.6)
    else:
        img = gradient3("#3f8fe0", "#9fd0f5", "#eaf6ff", 0.55)
    d = ImageDraw.Draw(img)
    r = random.Random(8)
    if not evening:
        for _ in range(5):
            x, y = r.randint(0, W), r.randint(60, 360)
            for k in range(5):
                rr = r.randint(60, 120)
                d.ellipse([x + k * 70 - rr, y - rr * 0.55, x + k * 70 + rr, y + rr * 0.55], fill=(255, 255, 255))
        # 入道雲
        for k in range(8):
            rr = 160 - k * 10
            d.ellipse([200 + k * 60 - rr, 380 - k * 35 - rr, 200 + k * 60 + rr, 380 - k * 35 + rr], fill=(255, 255, 255))
    img = img.filter(ImageFilter.GaussianBlur(2))
    d = ImageDraw.Draw(img)
    hy = int(H * 0.55)
    # 遠くの山
    d.polygon([(0, hy), (300, hy - 120), (650, hy - 40), (1000, hy - 160), (1400, hy - 60), (1800, hy - 140), (W, hy - 50), (W, hy)], fill=(110, 150, 170) if not evening else (90, 80, 120))
    # 向こう岸の町
    x = 0
    while x < W:
        w = r.randint(60, 120)
        house(d, x, hy + 20, w, r.randint(30, 60), (190, 185, 175) if not evening else (110, 90, 110), (80, 90, 110) if not evening else (60, 50, 80), jp=True)
        x += w + r.randint(10, 50)
    d.rectangle([0, hy + 20, W, hy + 40], fill=(100, 140, 80))
    # 川
    wy = hy + 40
    d.rectangle([0, wy, W, int(H * 0.78)], fill=(90, 150, 200) if not evening else (140, 110, 150))
    for k in range(40):
        y = r.randint(wy + 10, int(H * 0.77))
        xx = r.randint(0, W)
        d.line([xx, y, xx + r.randint(40, 160), y], fill=(200, 230, 250) if not evening else (240, 190, 170), width=3)
    # 手前の土手
    by = int(H * 0.78)
    d.polygon([(0, by), (W, by - 30), (W, H), (0, H)], fill=(90, 150, 60) if not evening else (60, 80, 50))
    for _ in range(400):
        xx = r.randint(0, W)
        yy = r.randint(by - 20, H)
        d.line([xx, yy, xx + r.randint(-6, 6), yy - r.randint(10, 30)], fill=(60, 120, 40) if not evening else (40, 60, 35), width=3)
    # 土手の道を歩く2人
    person(d, 1500, by + 110, 300, (60, 60, 80) if not evening else (30, 25, 40))
    person(d, 1620, by + 110, 210, (50, 70, 120) if not evening else (30, 25, 40), "child")
    return finish(img, 0.3)


def s_lanterns(evening=False):
    if evening:
        img = gradient3("#2c2a60", "#c9707a", "#f2b080", 0.6)
    else:
        img = gradient3("#5fa3e6", "#bfe0f6", "#f5f1e6", 0.6)
    d = ImageDraw.Draw(img)
    gy = int(H * 0.8)
    # 両側の家並み
    for side in (0, 1):
        for k in range(5):
            w = 380 - k * 60
            h = 360 - k * 50
            x = (k * 250 - 80) if side == 0 else (W - k * 250 - w + 80)
            wall = (215, 205, 190) if not evening else (120, 100, 110)
            d.rectangle([x, gy - h - k * 20, x + w, gy - k * 20], fill=wall)
            d.polygon([(x - 30, gy - h - k * 20), (x + w + 30, gy - h - k * 20), (x + w, gy - h - 60 - k * 20), (x, gy - h - 60 - k * 20)], fill=(70, 75, 90))
            d.rectangle([x + 40, gy - h * 0.6 - k * 20, x + w - 40, gy - k * 20], fill=(120, 90, 70) if not evening else (70, 55, 60))
            for j in range(6):
                d.line([x + 40 + j * (w - 80) / 6, gy - h * 0.6 - k * 20, x + 40 + j * (w - 80) / 6, gy - k * 20], fill=(90, 65, 50), width=3)
    d.polygon([(0, gy), (W, gy), (W, H), (0, H)], fill=(160, 155, 150) if not evening else (90, 80, 90))
    d.polygon([(W * 0.42, gy - 100), (W * 0.58, gy - 100), (W * 0.8, H), (W * 0.2, H)], fill=(185, 180, 172) if not evening else (110, 95, 105))
    img = lantern_row(img, 150, 13, 48, sag=70, lit=evening)
    img = lantern_row(img, 330, 9, 38, sag=40, lit=evening, x0=200, x1=W - 200)
    d = ImageDraw.Draw(img)
    # 提灯を抱えた車椅子の少年と大人
    wheelchair(d, 900, gy + 150, 70, (40, 40, 60), rider=(50, 60, 110))
    lantern(d, 975, gy + 0, 40, evening)
    person(d, 1250, gy + 250, 470, (45, 50, 70))
    d.line([1300, gy - 120, 1500, gy - 330], fill=(140, 120, 70), width=14)
    return finish(img, 0.35)


def s_inn(night=False):
    if night:
        img = gradient3("#060a1e", "#141c40", "#242a50", 0.6)
    else:
        img = gradient3("#3d3a78", "#d88878", "#f4c08a", 0.6)
    d = ImageDraw.Draw(img)
    if night:
        stars(d, 200, 0.5)
    gy = int(H * 0.82)
    x0, x1 = 300, 1800
    wall = (200, 185, 160) if not night else (60, 55, 70)
    d.rectangle([x0, gy - 500, x1, gy], fill=wall)
    d.polygon([(x0 - 120, gy - 500), (x1 + 120, gy - 500), (x1 - 40, gy - 680), (x0 + 40, gy - 680)], fill=(60, 65, 80) if not night else (25, 25, 40))
    d.rectangle([x0 - 40, gy - 270, x1 + 40, gy - 240], fill=(70, 70, 90))
    # 格子戸と暖簾
    door = (255, 215, 150) if night else (230, 200, 150)
    d.rectangle([850, gy - 230, 1250, gy], fill=door)
    for k in range(9):
        d.line([850 + k * 50, gy - 230, 850 + k * 50, gy], fill=(110, 80, 60), width=6)
    d.rectangle([830, gy - 260, 1270, gy - 160], fill=(40, 60, 120))
    for k in range(4):
        d.line([830 + k * 110 + 110, gy - 260, 830 + k * 110 + 110, gy - 160], fill=(30, 40, 90), width=6)
    for wx in (420, 1450):
        d.rectangle([wx, gy - 440, wx + 260, gy - 300], fill=door)
        for k in range(5):
            d.line([wx + k * 65, gy - 440, wx + k * 65, gy - 300], fill=(110, 80, 60), width=4)
    if night:
        def g(gd):
            gd.rectangle([850, gy - 230, 1250, gy], fill=(140, 100, 50))
            gd.rectangle([420, gy - 440, 680, gy - 300], fill=(140, 100, 50))
            gd.rectangle([1450, gy - 440, 1710, gy - 300], fill=(140, 100, 50))
        img = glow_layer(img, g, 90, 0.7)
        d = ImageDraw.Draw(img)
    lantern(d, 780, gy - 330, 55, True)
    lantern(d, 1320, gy - 330, 55, True)
    d.rectangle([0, gy, W, H], fill=(120, 110, 100) if not night else (35, 32, 40))
    sil = (35, 30, 40) if not night else (12, 10, 18)
    person(d, 640, gy + 140, 500, sil)
    wheelchair(d, 1450, gy + 70, 75, sil, rider=sil)
    person(d, 1680, gy + 140, 420, sil)
    if not night:
        lantern(d, 600, gy - 160, 40, False)
    else:
        d.rounded_rectangle([700, gy - 110, 770, gy - 30], radius=8, fill=(200, 170, 120))
    return finish(img, 0.45)


def s_senko():
    img = gradient("#03040c", "#0c0e1c")
    d = ImageDraw.Draw(img)
    gy = int(H * 0.86)
    d.rectangle([0, gy, W, H], fill=(14, 14, 20))
    # 縁側と庭木のシルエット
    d.ellipse([-300, 100, 600, 800], fill=(8, 10, 14))
    d.ellipse([1700, 50, 2500, 700], fill=(8, 10, 14))
    cx, cy = W * 0.5, H * 0.52
    d.line([cx - 30, cy - 420, cx, cy], fill=(150, 80, 120), width=5)
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ld = ImageDraw.Draw(layer)
    r = random.Random(12)
    for _ in range(46):
        a = r.uniform(0, 2 * math.pi)
        L = r.uniform(80, 330)
        x1, y1 = cx + math.cos(a) * L, cy + 20 + math.sin(a) * L * 0.8
        ld.line([cx, cy + 20, x1, y1], fill=(255, 170, 70), width=3)
        for _ in range(3):
            b = a + r.uniform(-1.2, 1.2)
            l2 = r.uniform(20, 80)
            ld.line([x1, y1, x1 + math.cos(b) * l2, y1 + math.sin(b) * l2], fill=(255, 200, 110), width=2)
    ld.ellipse([cx - 22, cy - 2, cx + 22, cy + 42], fill=(255, 140, 50))
    img = add(img, layer.filter(ImageFilter.GaussianBlur(25)))
    img = add(img, layer.filter(ImageFilter.GaussianBlur(4)))
    img = add(img, layer)
    d = ImageDraw.Draw(img)
    seated(d, cx - 360, gy + 40, 380, (28, 18, 12), "child")
    seated(d, cx + 380, gy + 40, 470, (22, 14, 10))
    seated(d, cx - 720, gy + 40, 480, (14, 10, 10))

    def g(gd):
        gd.ellipse([cx - 600, cy - 300, cx + 600, cy + 500], fill=(40, 20, 5))
    img = glow_layer(img, g, 200, 0.4)
    return finish(img, 0.5)


def s_festival_morning():
    img, fy = room(("#e8dcc4", "#d6c6a8"), "#c2a676", window_sky=("#7ab8f0", "#d4eaff"), window_box=(160, 140, 780, 600))
    d = ImageDraw.Draw(img)
    for k in range(10):
        d.line([160, 140 + k * 46, 780, 140 + k * 46], fill=(240, 235, 220), width=6)
    # 姿見と浴衣の少年
    d.rounded_rectangle([1300, 140, 1800, fy + 20], radius=20, fill=(120, 80, 50))
    d.rounded_rectangle([1330, 170, 1770, fy - 10], radius=12, fill=(200, 220, 230))
    for mx, alpha in ((1550, 0.65), (1040, 1.0)):
        col = lerp((200, 220, 230), (40, 50, 110), alpha)
        x, y = mx, fy + 60
        d.ellipse([x - 60, y - 560, x + 60, y - 440], fill=lerp((200, 220, 230), (60, 45, 40), alpha))
        d.polygon([(x - 110, y - 440), (x + 110, y - 440), (x + 130, y), (x - 130, y)], fill=col)
        d.polygon([(x - 110, y - 440), (x - 220, y - 300), (x - 160, y - 260), (x - 100, y - 330)], fill=col)
        d.polygon([(x + 110, y - 440), (x + 220, y - 300), (x + 160, y - 260), (x + 100, y - 330)], fill=col)
        d.rectangle([x - 115, y - 290, x + 115, y - 240], fill=lerp((200, 220, 230), (230, 180, 60), alpha))
        for k in range(6):
            d.ellipse([x - 90 + k * 30, y - 200 + (k % 2) * 60, x - 70 + k * 30, y - 180 + (k % 2) * 60], fill=lerp(col, (255, 255, 255), 0.6))
    return finish(img, 0.3)


def s_festival(dark=False):
    img = gradient3("#1d1f52", "#a65a7a", "#f09a6a", 0.65) if not dark else gradient3("#0c0c24", "#3a2a48", "#6a4048", 0.65)
    d = ImageDraw.Draw(img)
    gy = int(H * 0.86)
    names = ["やきそば", "りんご飴", "金魚すくい", "たこ焼き", "かき氷"]
    cols = [(220, 60, 50), (240, 240, 240), (60, 120, 200), (240, 180, 40), (80, 170, 220)]
    for k in range(5):
        x = 60 + k * 420
        w = 380
        d.rectangle([x, gy - 420, x + w, gy - 100], fill=(70, 50, 45))
        for j in range(8):
            d.rectangle([x + j * w / 8, gy - 470, x + (j + 1) * w / 8, gy - 400], fill=cols[k] if j % 2 == 0 else (250, 250, 250))
        d.rectangle([x + 20, gy - 390, x + w - 20, gy - 320], fill=(250, 245, 230))
        f = ImageFont.truetype(FONT, 48)
        tw = d.textlength(names[k], font=f)
        d.text((x + (w - tw) / 2, gy - 382), names[k], font=f, fill=(40, 30, 30))
        d.rectangle([x, gy - 140, x + w, gy - 90], fill=(110, 80, 60))

    def g(gd):
        for k in range(5):
            x = 60 + k * 420
            gd.rectangle([x + 20, gy - 320, x + 360, gy - 140], fill=(150, 100, 40))
    img = glow_layer(img, g, 60, 0.9 if not dark else 0.4)
    img = lantern_row(img, 70, 14, 40, sag=50, lit=True)
    d = ImageDraw.Draw(img)
    d.rectangle([0, gy, W, H], fill=(40, 30, 40) if not dark else (20, 15, 25))
    r = random.Random(21)
    for _ in range(28):
        person(d, r.randint(-20, W + 20), r.randint(gy + 20, H + 120), r.randint(260, 420), (20, 15, 25) if not dark else (10, 8, 14))
    if dark:
        # 倒れた少年に駆け寄る母
        d.ellipse([900, gy + 40, 1200, gy + 110], fill=(25, 35, 80))
        person(d, 1300, gy + 160, 420, (10, 8, 14))
    return finish(img, 0.45 if not dark else 0.7)


def s_goldfish():
    img = gradient("#2a2236", "#1a1424")
    d = ImageDraw.Draw(img)
    # 水槽(上から)
    d.rounded_rectangle([200, 300, W - 200, H - 60], radius=40, fill=(90, 70, 60))
    d.rounded_rectangle([240, 340, W - 240, H - 100], radius=30, fill=(60, 140, 190))
    r = random.Random(31)
    for _ in range(60):
        x, y = r.randint(300, W - 300), r.randint(400, H - 160)
        a = r.uniform(0, 2 * math.pi)
        c = r.choice([(240, 90, 40), (250, 110, 50), (230, 60, 40), (30, 30, 30), (250, 250, 250)])
        dx, dy = math.cos(a) * 30, math.sin(a) * 30
        d.ellipse([x - 26, y - 16, x + 26, y + 16], fill=c)
        d.polygon([(x - dx, y - dy), (x - dx * 2 - dy * 0.6, y - dy * 2 + dx * 0.6), (x - dx * 2 + dy * 0.6, y - dy * 2 - dx * 0.6)], fill=c)
    for _ in range(80):
        x, y = r.randint(260, W - 260), r.randint(360, H - 120)
        d.line([x, y, x + r.randint(20, 80), y], fill=(150, 210, 240), width=2)
    # ポイ
    for (x, y) in ((900, 640), (1350, 560)):
        d.ellipse([x - 90, y - 90, x + 90, y + 90], outline=(240, 80, 120), width=14)
        d.ellipse([x - 80, y - 80, x + 80, y + 80], fill=(200, 225, 240))
        d.line([x + 60, y + 60, x + 260, y + 300], fill=(240, 80, 120), width=22)
    img = lantern_row(img, 40, 12, 36, sag=40, lit=True)
    return finish(img, 0.5)


def s_ambulance():
    img = gradient3("#0c0c24", "#2a2240", "#40304a", 0.65)
    d = ImageDraw.Draw(img)
    gy = int(H * 0.82)
    d.rectangle([0, gy, W, H], fill=(25, 22, 30))
    ax = 800
    d.rounded_rectangle([ax, gy - 420, ax + 900, gy - 60], radius=30, fill=(235, 235, 240))
    d.rectangle([ax + 600, gy - 420, ax + 900, gy - 260], fill=(150, 190, 220))
    d.rectangle([ax, gy - 230, ax + 900, gy - 180], fill=(210, 40, 40))
    d.ellipse([ax + 100, gy - 120, ax + 240, gy + 20], fill=(30, 30, 35))
    d.ellipse([ax + 640, gy - 120, ax + 780, gy + 20], fill=(30, 30, 35))
    d.rectangle([ax + 90, gy - 380, ax + 160, gy - 260], fill=(210, 40, 40))
    d.rectangle([ax + 65, gy - 345, ax + 185, gy - 295], fill=(210, 40, 40))

    def g(gd):
        gd.ellipse([ax + 380, gy - 500, ax + 520, gy - 400], fill=(255, 40, 40))
        gd.polygon([(ax + 450, gy - 450), (0, gy - 650), (0, gy - 250)], fill=(110, 10, 10))
    img = glow_layer(img, g, 70, 1.0)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([ax + 380, gy - 470, ax + 520, gy - 420], radius=12, fill=(255, 80, 80))
    r = random.Random(41)
    for _ in range(16):
        person(d, r.choice([r.randint(0, 700), r.randint(1750, W)]), r.randint(gy + 40, H + 80), r.randint(300, 440), (12, 10, 16))
    img = lantern_row(img, 60, 12, 34, sag=40, lit=True)
    return finish(img, 0.55)


def s_hospital_corridor():
    img = gradient("#cfd8dc", "#b8c4ca")
    d = ImageDraw.Draw(img)
    vx, vy = W / 2, H * 0.45
    d.polygon([(0, H), (W, H), (vx + 160, vy + 120), (vx - 160, vy + 120)], fill=(170, 180, 186))
    d.polygon([(0, 0), (W, 0), (vx + 160, vy - 120), (vx - 160, vy - 120)], fill=(225, 230, 232))
    d.rectangle([vx - 160, vy - 120, vx + 160, vy + 120], fill=(200, 210, 215))
    for k in range(6):
        t = k / 6
        x = vx - 160 - (vx - 160) * (1 - t) ** 2 * 1.0
        d.line([x, vy - 120 - (vy - 120) * (1 - t) ** 2, x, vy + 120 + (H - vy - 120) * (1 - t) ** 2], fill=(180, 190, 196), width=3)
        x2 = W - x
        d.line([x2, vy - 120 - (vy - 120) * (1 - t) ** 2, x2, vy + 120 + (H - vy - 120) * (1 - t) ** 2], fill=(180, 190, 196), width=3)
    for k in range(5):
        y = vy - 120 - (vy - 120) * (1 - k / 5) ** 2
        w = 160 + (vx - 160) * (1 - k / 5) ** 2 * 0.5
        d.rectangle([vx - w * 0.3, y - 6, vx + w * 0.3, y + 6], fill=(255, 255, 250))
    d.rectangle([1500, 420, 1700, 470], fill=(40, 120, 70))
    d.text((1520, 425), "処置室", font=ImageFont.truetype(FONT, 40), fill=(255, 255, 255))
    # 長椅子の母
    d.rounded_rectangle([200, 760, 900, 820], radius=10, fill=(80, 120, 150))
    seated(d, 520, 790, 330, (40, 50, 100))
    return finish(img, 0.45)


def s_hospital_room(mode="night"):
    if mode == "night":
        img, fy = room(("#1c2238", "#141a2c"), "#262c3c", window_sky=("#3a3a48", "#2a2a36"), window_box=(1350, 150, 1950, 620))
    elif mode == "evening":
        img, fy = room(("#c8a898", "#a88a80"), "#7a6a68", window_sky=("#e2906a", "#f6c890"), window_box=(1350, 150, 1950, 620))
    else:
        img, fy = room(("#e6ecef", "#d2dade"), "#a8b2b8", window_sky=("#86c0f0", "#dff0ff"), window_box=(1350, 150, 1950, 620))
    d = ImageDraw.Draw(img)
    if mode == "night":
        # 窓の外は向かいの建物の壁
        d.rectangle([1368, 168, 1932, 602], fill=(55, 55, 65))
        for k in range(8):
            d.line([1368, 168 + k * 55, 1932, 168 + k * 55], fill=(45, 45, 55), width=3)

        def g(gd):
            gd.rectangle([1368, 168, 1932, 602], fill=(70, 40, 60))
        img = glow_layer(img, g, 160, 0.6)
        d = ImageDraw.Draw(img)
        d.rectangle([1350, 150, 1950, 620], outline=(60, 60, 70), width=18)
        d.line([1650, 150, 1650, 620], fill=(60, 60, 70), width=12)
    bedc = (235, 235, 240) if mode != "night" else (120, 125, 150)
    bed(d, 260, fy + 60, 950, color=bedc)
    d.ellipse([350, fy - 210, 480, fy - 100], fill=(90, 70, 60) if mode != "night" else (40, 35, 40))
    d.rounded_rectangle([470, fy - 150, 1150, fy - 70], radius=30, fill=(170, 200, 230) if mode != "night" else (70, 85, 120))
    iv_stand(d, 160, fy + 40)
    # モニター
    d.rounded_rectangle([1240, fy - 420, 1500, fy - 230], radius=12, fill=(30, 35, 40))
    d.line([(1260 + k * 12, fy - 330 + (-60 if k % 7 == 3 else (25 if k % 7 == 4 else 0))) for k in range(19)], fill=(80, 255, 140), width=4)
    if mode == "day":
        seated(d, 1400, fy + 60, 420, (70, 75, 95))  # 孝志
    if mode == "evening":
        person(d, 1500, fy + 80, 560, (240, 240, 245))  # 白衣の医師
        d.ellipse([1460, fy - 480, 1540, fy - 400], fill=(60, 50, 50))
    return finish(img, 0.5 if mode != "night" else 0.65)


def s_goldfish_bag():
    img = gradient("#141a2c", "#0c101c")
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(H * 0.72), W, H], fill=(70, 80, 110))
    d.rounded_rectangle([200, int(H * 0.62), 1100, int(H * 0.8)], radius=60, fill=(220, 225, 235))
    # ビニール袋
    bx, by = 1450, 640
    d.polygon([(bx - 60, by - 360), (bx + 60, by - 360), (bx + 230, by + 60), (bx + 180, by + 200), (bx - 180, by + 200), (bx - 230, by + 60)], fill=(110, 150, 190))
    d.ellipse([bx - 240, by - 60, bx + 240, by + 230], fill=(90, 160, 210))
    d.line([bx - 60, by - 360, bx + 60, by - 360], fill=(230, 60, 60), width=14)
    d.ellipse([bx - 70, by + 40, bx + 40, by + 100], fill=(250, 100, 40))
    d.polygon([(bx + 30, by + 70), (bx + 110, by + 30), (bx + 100, by + 120)], fill=(250, 120, 60))

    def g(gd):
        gd.ellipse([bx - 300, by - 200, bx + 300, by + 300], fill=(30, 60, 90))
    img = glow_layer(img, g, 120, 0.6)
    d = ImageDraw.Draw(img)
    seated(d, 620, int(H * 1.0), 380, (20, 22, 30))
    return finish(img, 0.6)


def s_shell(half=False):
    img = gradient("#3a2e24", "#241c16")
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(H * 0.72), W, H], fill=(120, 90, 60))
    for k in range(10):
        d.line([0, int(H * 0.72) + k * 34, W, int(H * 0.72) + k * 34 + 10], fill=(105, 78, 52), width=3)
    cx, cy, R = W / 2, H * 0.48, 380 if not half else 440
    d.ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=(170, 130, 80))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(80, 60, 45))
    r = random.Random(51)
    star_r = 24
    ring = R - star_r - 6
    cols = [(240, 200, 90), (230, 120, 60), (180, 160, 120)]
    # 外周の星
    n = int(2 * math.pi * ring / (star_r * 2.1))
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + math.cos(a) * ring, cy + math.sin(a) * ring
        d.ellipse([x - star_r, y - star_r, x + star_r, y + star_r], fill=(70, 70, 70), outline=(40, 40, 40), width=2)
        d.ellipse([x - star_r * 0.5, y - star_r * 0.6, x - star_r * 0.05, y - star_r * 0.15], fill=(120, 120, 120))
    if not half:
        # 内側の割薬
        for _ in range(900):
            a = r.uniform(0, 2 * math.pi)
            rr = math.sqrt(r.random()) * (ring - star_r * 1.6)
            x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            c = r.choice(cols)
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=lerp(c, (40, 30, 20), 0.5))
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(50, 40, 30))
    else:
        d.ellipse([cx - ring + star_r * 1.2, cy - ring + star_r * 1.2, cx + ring - star_r * 1.2, cy + ring - star_r * 1.2], fill=(95, 72, 54))
        # ピンセット
        d.polygon([(cx + ring * 0.7, cy - ring * 0.7), (W - 120, 80), (W - 90, 110)], fill=(200, 200, 210))
        d.polygon([(cx + ring * 0.72, cy - ring * 0.68), (W - 80, 150), (W - 60, 180)], fill=(180, 180, 190))
    # 手のひらの1粒
    if not half:
        hx, hy = 1700, 940
        d.ellipse([hx - 200, hy - 90, hx + 200, hy + 120], fill=(220, 180, 150))
        d.ellipse([hx - 30, hy - 30, hx + 30, hy + 30], fill=(70, 70, 70))
    return finish(img, 0.45)


def s_round_vs_tube():
    img = gradient3("#05071a", "#10163a", "#1a1c40", 0.7)
    d = ImageDraw.Draw(img)
    stars(d, 200, 0.8)
    img = firework(img, W * 0.3, H * 0.45, 330, "#ffd070", seed=61, rings=2)
    # 筒型(片側からだけ綺麗に見える花火)
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ld = ImageDraw.Draw(layer)
    cx, cy = W * 0.74, H * 0.45
    rr = random.Random(62)
    for k in range(70):
        a = -math.pi / 2 + rr.uniform(-0.55, 0.55)
        L = rr.uniform(150, 360)
        for j in range(10):
            t = j / 10
            x, y = cx + math.cos(a) * L * t * 0.5 + rr.uniform(-4, 4), cy + 200 + math.sin(a) * L * t * 1.3 + j * j * 1.5
            ld.ellipse([x - 3, y - 3, x + 3, y + 3], fill=lerp((0, 0, 0), (140, 200, 255), 1 - t * 0.6))
    img = add(img, layer.filter(ImageFilter.GaussianBlur(14)))
    img = add(img, layer)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 62)
    for x, t in ((W * 0.3, "日本の花火：どこから見てもまん丸"), (W * 0.74, "海外の花火：筒のような形")):
        w = d.textlength(t, font=f)
        d.text((x - w / 2, H * 0.08), t, font=f, fill=(255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0))
    img = embankment_crowd(img, int(H * 0.9), n=30, scale=0.7)
    return finish(img, 0.4)


def s_scan_compare():
    img = gradient("#0e1420", "#070a10")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 56)
    for k, (x, lab) in enumerate(((210, "2ヶ月前(アメリカ)"), (1150, "昨日(日本)"))):
        d.rounded_rectangle([x - 20, 180, x + 772, 972], radius=16, fill=(28, 32, 40))
        img.paste(brain_scan(752, seed=4), (x, 200))
        w = d.textlength(lab, font=f)
        d.text((x + 376 - w / 2, 90), lab, font=f, fill=(230, 235, 245), stroke_width=4, stroke_fill=(0, 0, 0))
    d = ImageDraw.Draw(img)
    for x in (210, 1150):
        cx, cy = x + 752 * 0.62, 200 + 752 * 0.42
        d.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], outline=(255, 200, 60), width=8)
    d.text((W / 2 - 40, 520), "＝", font=ImageFont.truetype(FONT, 120), fill=(255, 200, 60))
    return finish(img, 0.45)


def s_ct_chart():
    img = gradient("#f4f1ea", "#e6e0d4")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 70)
    fs = ImageFont.truetype(FONT, 54)
    title = "人口100万人あたりのCT台数"
    d.text(((W - d.textlength(title, font=f)) / 2, 90), title, font=f, fill=(40, 40, 50))
    data = [("日本", 107, (210, 60, 60)), ("アメリカ", 41, (90, 110, 150)), ("ドイツ", 35, (90, 110, 150))]
    x0, y0, maxw = 520, 290, 1250
    for i, (name, v, c) in enumerate(data):
        y = y0 + i * 230
        d.text((x0 - 40 - d.textlength(name, font=f), y + 20), name, font=f, fill=(40, 40, 50))
        w = maxw * v / 110
        d.rounded_rectangle([x0, y, x0 + w, y + 130], radius=14, fill=c)
        d.text((x0 + w + 30, y + 30), f"{v}台", font=f, fill=c)
    d.text((x0, 1010), "※ナレーションで紹介した数値", font=fs, fill=(120, 120, 130))
    return finish(img, 0.15)


def s_clinic_jp():
    img, fy = room(("#eef3f4", "#dbe5e8"), "#b9c6cc", window_sky=("#9cc9f0", "#e2f0fb"), window_box=(160, 160, 640, 560))
    d = ImageDraw.Draw(img)
    # CT装置
    cx, cy = 1350, fy - 300
    d.rounded_rectangle([cx - 380, cy - 380, cx + 380, cy + 330], radius=120, fill=(245, 247, 250), outline=(200, 210, 220), width=6)
    d.ellipse([cx - 210, cy - 210, cx + 210, cy + 210], fill=(60, 70, 85))
    d.ellipse([cx - 180, cy - 180, cx + 180, cy + 180], fill=(30, 35, 45))
    d.rectangle([cx - 800, cy + 60, cx + 100, cy + 130], fill=(230, 235, 240))
    d.rectangle([cx - 650, cy + 130, cx - 450, fy], fill=(200, 208, 215))
    d.rectangle([cx - 380, cy - 30, cx + 380, cy - 10], fill=(80, 160, 210))
    return finish(img, 0.25)


def s_doctor_desk():
    img, fy = room(("#e0e6e8", "#cdd6da"), "#9aa6ac")
    d = ImageDraw.Draw(img)
    d.rectangle([200, fy - 200, W - 200, fy - 160], fill=(150, 120, 90))
    monitor(img, (300, fy - 640, 900, fy - 300), brain_scan(600, seed=4))
    d = ImageDraw.Draw(img)
    # 書類
    for k in range(4):
        d.rectangle([1100 + k * 12, fy - 230 - k * 6, 1500 + k * 12, fy - 205 - k * 6], fill=(250, 250, 250), outline=(200, 200, 200))
    d.line([1200, fy - 260, 1450, fy - 330], fill=(30, 30, 40), width=10)
    person(d, 1750, fy + 80, 600, (245, 245, 250))
    d.ellipse([1705, fy - 525, 1795, fy - 430], fill=(50, 40, 40))
    return finish(img, 0.35)


def s_notebook():
    img = gradient("#d9cdb8", "#c6b79c")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([450, 120, 1660, 1080], radius=20, fill=(252, 250, 242), outline=(180, 170, 150), width=4)
    d.line([1055, 120, 1055, 1080], fill=(200, 190, 170), width=6)
    for k in range(14):
        d.line([500, 220 + k * 60, 1610, 220 + k * 60], fill=(190, 210, 230), width=2)
    f = ImageFont.truetype(FONT, 58)
    words = [("arigatou", "ありがとう"), ("ohayou", "おはよう"), ("oishii", "おいしい"), ("konbanwa", "こんばんは"), ("genki desu ka?", "げんきですか")]
    for k, (ro, ja) in enumerate(words):
        d.text((520, 210 + k * 150), ro, font=f, fill=(40, 60, 120))
        d.text((1100, 210 + k * 150), ja, font=f, fill=(60, 50, 50))
    # 痛みの顔カード
    for k in range(4):
        x = 160 + k * 0
        y = 200 + k * 220
        d.rounded_rectangle([90, y, 360, y + 190], radius=16, fill=(255, 255, 255), outline=(170, 170, 170), width=3)
        d.ellipse([155, y + 25, 295, y + 165], fill=[(140, 210, 120), (220, 220, 100), (240, 170, 80), (240, 110, 90)][k])
        d.ellipse([190, y + 70, 205, y + 85], fill=(30, 30, 30))
        d.ellipse([245, y + 70, 260, y + 85], fill=(30, 30, 30))
        d.arc([190, y + 95 + k * 8, 260, y + 145 - k * 8], 20 if k < 2 else 200, 160 if k < 2 else 340, fill=(30, 30, 30), width=5)
    return finish(img, 0.3)


def s_hospital_exit():
    img = gradient3("#4f95e0", "#a5d2f5", "#f2f4f0", 0.6)
    d = ImageDraw.Draw(img)
    gy = int(H * 0.82)
    d.rectangle([250, 200, W - 250, gy], fill=(225, 228, 232))
    for i in range(10):
        for j in range(4):
            d.rectangle([310 + i * 160, 250 + j * 110, 400 + i * 160, 320 + j * 110], fill=(150, 190, 220))
    d.rectangle([850, gy - 260, 1260, gy], fill=(120, 170, 200))
    d.rectangle([800, gy - 300, 1310, gy - 260], fill=(90, 100, 110))
    d.rectangle([0, gy, W, H], fill=(190, 190, 185))
    person(d, 1000, gy + 170, 470, (60, 60, 80))
    person(d, 1120, gy + 170, 330, (50, 70, 120), "child")
    person(d, 1550, gy + 170, 450, (70, 75, 95))
    return finish(img, 0.3)


def s_clinic_us():
    img, fy = room(("#e4e8ec", "#d0d6dc"), "#a0a8b0", window_sky=("#e8c49a", "#f4e2c4"), window_box=(1400, 160, 1900, 560))
    d = ImageDraw.Draw(img)
    d.rectangle([300, fy - 200, 1300, fy - 160], fill=(130, 110, 90))
    monitor(img, (380, fy - 620, 900, fy - 310), brain_scan(520, seed=5, tumor=(0.62, 0.42, 0.05)))
    d = ImageDraw.Draw(img)
    person(d, 1150, fy + 60, 580, (245, 245, 250))
    d.ellipse([1105, fy - 535, 1195, fy - 440], fill=(140, 110, 80))
    seated(d, 1600, fy + 160, 420, (60, 50, 70))
    seated(d, 1830, fy + 160, 320, (50, 70, 120), "child")

    def g(gd):
        gd.ellipse([1200, 0, 2100, 900], fill=(60, 45, 20))
    img = glow_layer(img, g, 200, 0.5)
    return finish(img, 0.3)


def s_surgery():
    img = gradient("#1a3a3a", "#0e2424")
    d = ImageDraw.Draw(img)
    cx = W / 2

    def g(gd):
        gd.ellipse([cx - 500, 60, cx + 500, 400], fill=(200, 230, 230))
        gd.polygon([(cx - 300, 300), (cx + 300, 300), (cx + 700, H), (cx - 700, H)], fill=(60, 90, 90))
    img = glow_layer(img, g, 80, 0.7)
    d = ImageDraw.Draw(img)
    for k in range(3):
        x = cx - 300 + k * 300
        d.ellipse([x - 120, 90, x + 120, 260], fill=(240, 255, 255), outline=(150, 170, 170), width=8)
    d.rectangle([cx - 600, 800, cx + 600, 860], fill=(60, 120, 120))
    for x in (cx - 700, cx + 700):
        person(d, x, H + 40, 640, (30, 80, 90))
    return finish(img, 0.55)


def s_station():
    img = gradient3("#3f8fe0", "#9fd0f5", "#eaf6ff", 0.55)
    d = ImageDraw.Draw(img)
    gy = int(H * 0.82)
    d.rectangle([300, 300, 1800, gy], fill=(215, 200, 170))
    d.polygon([(220, 300), (1880, 300), (1700, 180), (400, 180)], fill=(90, 70, 60))
    d.rectangle([800, 330, 1300, 420], fill=(250, 250, 245))
    f = ImageFont.truetype(FONT, 66)
    d.text((1050 - d.textlength("かわべ駅", font=f) / 2, 340), "かわべ駅", font=f, fill=(30, 30, 30))
    d.rectangle([700, gy - 340, 1400, gy], fill=(120, 90, 70))
    d.rectangle([740, gy - 300, 1360, gy], fill=(60, 50, 45))
    d.rectangle([0, gy, W, H], fill=(170, 165, 150))
    person(d, 960, gy + 170, 470, (60, 60, 80))
    person(d, 1150, gy + 170, 350, (40, 60, 120), "child")
    for k in range(6):
        x = 100 + k * 380
        d.line([x, gy - 520, x, gy + 40], fill=(80, 70, 60), width=12)
    return finish(img, 0.3)


def s_workshop():
    img = gradient("#5a4430", "#3a2a1c")
    d = ImageDraw.Draw(img)
    fy = int(H * 0.8)
    d.rectangle([0, fy, W, H], fill=(70, 55, 40))
    # 窓からの光
    d.rectangle([1500, 120, 1950, 520], fill=(255, 230, 170))
    for k in range(4):
        d.line([1500 + k * 150, 120, 1500 + k * 150, 520], fill=(90, 70, 50), width=14)

    def g(gd):
        gd.polygon([(1500, 120), (1950, 120), (1300, H), (700, H)], fill=(80, 60, 30))
    img = glow_layer(img, g, 60, 0.6)
    d = ImageDraw.Draw(img)
    # 棚の玉
    for row in range(3):
        d.rectangle([100, 200 + row * 200, 1100, 220 + row * 200], fill=(110, 80, 55))
        for k in range(7):
            x = 160 + k * 135
            r = 50 + (k % 3) * 8
            d.ellipse([x - r, 200 + row * 200 - 2 * r, x + r, 200 + row * 200], fill=(190, 150, 100), outline=(140, 100, 60), width=4)
    d.rectangle([300, fy - 180, 1400, fy - 140], fill=(140, 105, 70))
    d.rectangle([340, fy - 140, 380, fy], fill=(110, 80, 55))
    d.rectangle([1320, fy - 140, 1360, fy], fill=(110, 80, 55))
    d.ellipse([700, fy - 330, 960, fy - 170], fill=(190, 150, 100))
    seated(d, 1600, fy + 60, 520, (40, 30, 30))
    return finish(img, 0.5)


def s_yukata():
    img = gradient3("#2c2a60", "#c9707a", "#f2b080", 0.6)
    d = ImageDraw.Draw(img)
    gy = int(H * 0.88)
    d.rectangle([0, gy, W, H], fill=(70, 50, 60))
    x, y = W / 2 - 200, gy + 30
    col = (40, 50, 110)
    d.ellipse([x - 70, y - 680, x + 70, y - 540], fill=(70, 50, 40))
    d.polygon([(x - 130, y - 540), (x + 130, y - 540), (x + 150, y), (x - 150, y)], fill=col)
    d.polygon([(x - 130, y - 540), (x - 250, y - 370), (x - 190, y - 330), (x - 120, y - 420)], fill=col)
    d.polygon([(x + 130, y - 540), (x + 250, y - 370), (x + 190, y - 330), (x + 120, y - 420)], fill=col)
    d.rectangle([x - 135, y - 360, x + 135, y - 300], fill=(230, 180, 60))
    for k in range(8):
        d.ellipse([x - 110 + k * 30, y - 250 + (k % 2) * 80, x - 86 + k * 30, y - 226 + (k % 2) * 80], fill=(200, 210, 240))
    d.rectangle([x - 150, y - 25, x + 150, y], fill=(230, 210, 190))  # 短くなった丈
    person(d, W / 2 + 250, gy + 40, 640, (40, 30, 50))
    img = lantern_row(img, 80, 12, 40, sag=50, lit=True)
    return finish(img, 0.45)


def s_fireworks(kind="main"):
    img, y_w = night_river_base()
    seeds = {"main": 0, "start": 10, "gold": 20, "crowd": 30, "finale": 40}[kind]
    if kind == "start":
        d = ImageDraw.Draw(img)
        layer = Image.new("RGB", img.size, (0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for j in range(30):
            ld.ellipse([W / 2 - 5, y_w - 60 - j * 18, W / 2 + 5, y_w - 50 - j * 18], fill=lerp((0, 0, 0), (255, 220, 160), j / 30))
        img = add(img, layer.filter(ImageFilter.GaussianBlur(8)))
        img = add(img, layer)
    elif kind == "gold":
        img = firework(img, W * 0.5, H * 0.32, 420, "#ffcf6a", seed=21, rings=2)
        img = firework(img, W * 0.18, H * 0.25, 180, "#ffe7a0", seed=22)
        img = firework(img, W * 0.83, H * 0.22, 200, "#ffb84a", seed=23)
    elif kind == "finale":
        r = random.Random(41)
        for k in range(9):
            col = r.choice(["#ffcf6a", "#ff6688", "#88d0ff", "#b6ff88", "#ffffff", "#ff9a4a"])
            img = firework(img, r.uniform(W * 0.08, W * 0.92), r.uniform(H * 0.12, H * 0.45), r.uniform(150, 330), col, seed=k + 40, rings=2, density=0.8)
    elif kind == "crowd":
        img = firework(img, W * 0.35, H * 0.3, 330, "#ff7799", seed=31, rings=2)
        img = firework(img, W * 0.72, H * 0.25, 280, "#88ccff", seed=32, rings=2)
    else:
        img = firework(img, W * 0.3, H * 0.3, 330, "#ffcf6a", seed=1, rings=2)
        img = firework(img, W * 0.72, H * 0.24, 260, "#ff7aa0", seed=2, rings=2)
        img = firework(img, W * 0.55, H * 0.12, 120, "#a0e0ff", seed=3)
    img = reflection(img, y_w, 0.5)
    if kind in ("crowd", "finale", "main"):
        img = embankment_crowd(img, int(H * 0.86), n=55 if kind != "main" else 35, scale=0.85, seed=seeds)
    if kind in ("start", "gold"):
        d = ImageDraw.Draw(img)
        d.polygon([(0, int(H * 0.88)), (W, int(H * 0.85)), (W, H), (0, H)], fill=(8, 8, 16))
        seated(d, W * 0.42, H + 30, 330, (8, 8, 16))
        seated(d, W * 0.53, H + 30, 250, (8, 8, 16), "child")
    return finish(img, 0.4)


def s_riverbank_night():
    img, y_w = night_river_base(sky=("#04061a", "#0e1534", "#1a1c40"))
    d = ImageDraw.Draw(img)
    d.ellipse([1650, 120, 1790, 260], fill=(250, 245, 220))

    def g(gd):
        gd.ellipse([1600, 70, 1840, 310], fill=(80, 80, 60))
    img = glow_layer(img, g, 80, 0.8)
    img = reflection(img, y_w, 0.45)
    d = ImageDraw.Draw(img)
    # 煙の名残
    r = random.Random(71)
    for _ in range(20):
        x, y = r.randint(200, W - 200), r.randint(150, 450)
        rr = r.randint(60, 160)
        d.ellipse([x - rr, y - rr * 0.5, x + rr, y + rr * 0.5], fill=(40, 45, 70))
    img = img.filter(ImageFilter.GaussianBlur(1))
    d = ImageDraw.Draw(img)
    d.polygon([(0, int(H * 0.84)), (W, int(H * 0.8)), (W, H), (0, H)], fill=(10, 10, 18))
    person(d, 700, H + 20, 380, (6, 6, 12))
    person(d, 900, H + 20, 270, (6, 6, 12), "child")
    person(d, 1350, H + 20, 400, (6, 6, 12))
    return finish(img, 0.5)


def s_star_gift():
    img = gradient("#0a0c1c", "#05060e")
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, H * 0.58
    # 両手と紙包み
    d.ellipse([cx - 420, cy - 120, cx + 20, cy + 230], fill=(200, 160, 130))
    d.ellipse([cx - 20, cy - 120, cx + 420, cy + 230], fill=(190, 150, 120))
    d.polygon([(cx - 230, cy - 40), (cx + 230, cy - 60), (cx + 260, cy + 120), (cx - 250, cy + 130)], fill=(240, 235, 220))
    d.ellipse([cx - 55, cy - 30, cx + 55, cy + 80], fill=(80, 75, 70))
    d.ellipse([cx - 35, cy - 15, cx - 5, cy + 15], fill=(140, 135, 125))

    def g(gd):
        gd.ellipse([cx - 400, cy - 400, cx + 400, cy + 300], fill=(60, 45, 20))
    img = glow_layer(img, g, 160, 0.7)
    img = firework(img, W * 0.2, H * 0.2, 120, "#ffcf6a", seed=81, glow=True, density=0.6)
    img = firework(img, W * 0.82, H * 0.18, 100, "#ff8aa8", seed=82, glow=True, density=0.6)
    return finish(img, 0.55)


def s_photo_wall():
    img, fy = room(("#3a3560", "#2a2848"), "#4a3a35", window_sky=("#ffd8a0", "#ffeccc"), window_box=(1500, 160, 1950, 560))
    d = ImageDraw.Draw(img)
    cols = [(240, 120, 140), (110, 190, 240), (250, 210, 90)]
    for k, (x, y) in enumerate([(120, 160), (380, 140), (120, 500)]):
        d.rectangle([x, y, x + 220, y + 300], fill=cols[k])
        d.ellipse([x + 50, y + 50, x + 170, y + 170], fill=lerp(cols[k], (255, 255, 255), 0.4))
    # 写真(花火と3人)
    px, py, pw, ph = 720, 170, 640, 460
    d.rectangle([px - 20, py - 20, px + pw + 20, py + ph + 70], fill=(250, 250, 250))
    photo = gradient("#0a0e2a", "#22285a", size=(pw, ph))
    tmp = Image.new("RGB", (W, H))
    tmp.paste(photo, (0, 0))
    tmp = firework(tmp, pw * 0.5, ph * 0.3, 160, "#ffcf6a", seed=91, glow=True, density=0.7)
    photo = tmp.crop((0, 0, pw, ph))
    pd = ImageDraw.Draw(photo)
    person(pd, pw * 0.36, ph + 10, 270, (40, 50, 110), "child")
    person(pd, pw * 0.5, ph + 10, 330, (120, 80, 90))
    person(pd, pw * 0.66, ph + 30, 380, (60, 60, 70))
    for k in range(4):
        person(pd, pw * (0.1 + k * 0.08) if k < 2 else pw * (0.82 + (k - 2) * 0.08), ph + 10, 200, (30, 30, 50), "child")
    img.paste(photo, (px, py))
    d = ImageDraw.Draw(img)
    # 机と星
    d.rectangle([600, fy - 120, 1500, fy - 80], fill=(130, 95, 65))
    d.ellipse([1020, fy - 170, 1080, fy - 115], fill=(80, 75, 70))

    def g(gd):
        gd.ellipse([960, fy - 220, 1140, fy - 60], fill=(70, 50, 20))
    img = glow_layer(img, g, 50, 0.7)
    return finish(img, 0.4)


def s_ending():
    img = gradient3("#05071a", "#10163a", "#1a1c40", 0.7)
    d = ImageDraw.Draw(img)
    stars(d, 260, 0.8)
    img = firework(img, W * 0.2, H * 0.3, 250, "#ffcf6a", seed=101, rings=2)
    img = firework(img, W * 0.8, H * 0.28, 230, "#ff7aa0", seed=102, rings=2)
    text_center(img, "最後までご視聴いただき", int(H * 0.36), 100)
    text_center(img, "ありがとうございました", int(H * 0.47), 100)
    d = ImageDraw.Draw(img)
    bx, by = W / 2 - 360, int(H * 0.64)
    d.rounded_rectangle([bx, by, bx + 720, by + 140], radius=24, fill=(220, 30, 30))
    f = ImageFont.truetype(FONT, 70)
    t = "チャンネル登録"
    d.text((W / 2 - d.textlength(t, font=f) / 2, by + 32), t, font=f, fill=(255, 255, 255))
    text_center(img, "高評価・コメントもお待ちしています", int(H * 0.8), 56, fill=(255, 230, 160), stroke=5)
    return finish(img, 0.35)


SCENES = {
    "title": s_title,
    "midwest": lambda: s_midwest("autumn"),
    "midwest_spring": lambda: s_midwest("spring"),
    "midwest_summer": lambda: s_midwest("summer"),
    "dawn": s_dawn,
    "noah_room": lambda: s_noah_room(False),
    "noah_room_dark": lambda: s_noah_room(True),
    "hospital_us": s_hospital_us,
    "scan_us": s_scan_us,
    "parking": s_parking,
    "living_room": s_living_room,
    "kitchen_table": s_kitchen_table,
    "kitchen_night": s_kitchen_night,
    "airplane": s_airplane,
    "airport": s_airport,
    "tokyo": s_tokyo,
    "hotel": s_hotel,
    "riverside": lambda: s_riverside(False),
    "lanterns": lambda: s_lanterns(False),
    "inn_evening": lambda: s_inn(False),
    "inn_night": lambda: s_inn(True),
    "senko": s_senko,
    "festival_morning": s_festival_morning,
    "festival": lambda: s_festival(False),
    "festival_dark": lambda: s_festival(True),
    "goldfish": s_goldfish,
    "ambulance": s_ambulance,
    "hospital_corridor": s_hospital_corridor,
    "hospital_wall": lambda: s_hospital_room("night"),
    "hospital_day": lambda: s_hospital_room("day"),
    "hospital_evening": lambda: s_hospital_room("evening"),
    "goldfish_bag": s_goldfish_bag,
    "shell": lambda: s_shell(False),
    "shell_half": lambda: s_shell(True),
    "round_vs_tube": s_round_vs_tube,
    "scan_compare": s_scan_compare,
    "ct_chart": s_ct_chart,
    "clinic_jp": s_clinic_jp,
    "doctor_desk": s_doctor_desk,
    "notebook": s_notebook,
    "hospital_exit": s_hospital_exit,
    "clinic_us": s_clinic_us,
    "surgery": s_surgery,
    "station": s_station,
    "workshop": s_workshop,
    "yukata": s_yukata,
    "fireworks": lambda: s_fireworks("main"),
    "fireworks_start": lambda: s_fireworks("start"),
    "fireworks_gold": lambda: s_fireworks("gold"),
    "fireworks_crowd": lambda: s_fireworks("crowd"),
    "fireworks_finale": lambda: s_fireworks("finale"),
    "riverbank_night": s_riverbank_night,
    "star_gift": s_star_gift,
    "photo_wall": s_photo_wall,
    "ending": s_ending,
}


def render(name, out_dir):
    path = os.path.join(out_dir, f"{name}.png")
    SCENES[name]().save(path)
    return path


if __name__ == "__main__":
    import sys
    from concurrent.futures import ProcessPoolExecutor
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "scenes")
    os.makedirs(out, exist_ok=True)
    names = sys.argv[1:] or list(SCENES)
    with ProcessPoolExecutor(4) as ex:
        for p in ex.map(render, names, [out] * len(names)):
            print(p)

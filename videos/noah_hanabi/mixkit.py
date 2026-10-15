"""Mixkit(無料・商用利用可・クレジット不要のストック動画)を検索・取得する。

search(term) -> [{"id": 5550, "slug": "child-in-hospital-smiles-at-doctor-holding-clipboard"}, ...]
結果は out/mixkit_cache/ にキャッシュする。
"""
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "mixkit_cache")
CLIPS = os.path.join(HERE, "out", "clips")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
CARD = re.compile(r'href="/free-stock-video/([a-z0-9-]+)-(\d+)/"')


def _get(url, binary=False):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except Exception as e:
            if getattr(e, "code", None) in (403, 404):
                return None
            time.sleep(2 * (attempt + 1))
    return None


def search(term, pages=2):
    os.makedirs(CACHE, exist_ok=True)
    key = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    found, seen = [], set()
    for page in range(1, pages + 1):
        url = f"https://mixkit.co/free-stock-video/discover/{urllib.parse.quote(key)}/"
        if page > 1:
            url += f"?page={page}"
        html = _get(url)
        if not html:
            break
        new = 0
        for slug, vid in CARD.findall(html):
            if vid not in seen:
                seen.add(vid)
                found.append({"id": int(vid), "slug": slug})
                new += 1
        if new == 0:
            break
    json.dump(found, open(path, "w"))
    return found


def thumb(vid):
    return f"https://assets.mixkit.co/videos/{vid}/{vid}-thumb-360-0.jpg"


def download(vid, slug=None):
    """720p(なければ1080p, 360p)の mp4 を out/clips/{id}.mp4 に保存する。"""
    os.makedirs(CLIPS, exist_ok=True)
    path = os.path.join(CLIPS, f"{vid}.mp4")
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path
    for q in ("720", "1080", "360"):
        data = _get(f"https://assets.mixkit.co/videos/{vid}/{vid}-{q}.mp4", binary=True)
        if data and len(data) > 10000:
            open(path, "wb").write(data)
            return path
    # 新しいクリップは URL の形式が違うので、個別ページから mp4 の URL を拾う
    slug = slug or ""
    html = _get(f"https://mixkit.co/free-stock-video/{slug}-{vid}/") if slug else None
    if html:
        urls = sorted(set(re.findall(r"https://assets\.mixkit\.co/[^\"]+\.mp4", html)))
        urls.sort(key=lambda u: ("-720" not in u, "-1080" not in u))
        for u in urls:
            data = _get(u, binary=True)
            if data and len(data) > 10000:
                open(path, "wb").write(data)
                return path
    return None

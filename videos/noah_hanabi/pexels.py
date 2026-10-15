"""Pexels(無料・商用利用可・クレジット不要のストック動画)を検索・取得する。

mixkit.py と同じ使い方ができるようにしてある:
  search(term) -> [{"id": 12345, "slug": "a-bullet-train-arriving-at-a-station"}, ...]
  download(vid) -> out/clips/{id}.mp4
API キーは環境変数 PEXELS_API_KEY から読む(https://www.pexels.com/api/ で無料発行)。
"""
import json
import os
import re
import time
import urllib.parse
import urllib.request

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
HERE = os.environ.get("PROJECT_DIR", CODE_DIR)
CACHE = os.path.join(HERE, "out", "pexels_cache")
CLIPS = os.path.join(HERE, "out", "clips")
API = "https://api.pexels.com/videos/search"


def _key():
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        raise SystemExit("PEXELS_API_KEY が設定されていません")
    return key


def _get_json(url):
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"Authorization": _key(), "User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if getattr(e, "code", None) == 429:  # 回数制限
                time.sleep(30)
            else:
                time.sleep(2 * (attempt + 1))
    return None


def _slug(video):
    # 例: https://www.pexels.com/video/a-bullet-train-arriving-1234567/
    m = re.search(r"/video/([a-z0-9-]+?)-?\d+/?$", video.get("url", ""))
    return m.group(1) if m else ""


def search(term, pages=2):
    os.makedirs(CACHE, exist_ok=True)
    key = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    found, files = [], {}
    for page in range(1, pages + 1):
        q = urllib.parse.urlencode({"query": term, "per_page": 40, "page": page,
                                    "orientation": "landscape", "size": "medium"})
        data = _get_json(f"{API}?{q}")
        if not data or not data.get("videos"):
            break
        for v in data["videos"]:
            found.append({"id": v["id"], "slug": _slug(v), "duration": v.get("duration")})
            files[str(v["id"])] = _best_file(v)
        if not data.get("next_page"):
            break
    json.dump(found, open(path, "w"))
    _remember_files(files)
    return found


def _best_file(v):
    """1280〜1920 幅の mp4 を優先して選ぶ。"""
    cands = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("width")]
    if not cands:
        return None
    cands.sort(key=lambda f: (not 1280 <= f["width"] <= 1920, abs(f["width"] - 1920)))
    return cands[0]["link"]


def _remember_files(files):
    path = os.path.join(CACHE, "_files.json")
    known = json.load(open(path)) if os.path.exists(path) else {}
    known.update({k: v for k, v in files.items() if v})
    json.dump(known, open(path, "w"))


def thumb(vid):
    return None


def download(vid, slug=None):
    os.makedirs(CLIPS, exist_ok=True)
    path = os.path.join(CLIPS, f"{vid}.mp4")
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path
    known_path = os.path.join(CACHE, "_files.json")
    known = json.load(open(known_path)) if os.path.exists(known_path) else {}
    link = known.get(str(vid))
    if not link:
        v = _get_json(f"https://api.pexels.com/videos/videos/{vid}")
        link = _best_file(v) if v else None
    if not link:
        return None
    for attempt in range(4):
        try:
            req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            if len(data) > 10000:
                open(path, "wb").write(data)
                return path
        except Exception:
            time.sleep(3 * (attempt + 1))
    return None

"""video_queries.py の検索語から、各ショットに使う Mixkit のクリップを選ぶ。

出力: out/clip_choices.json  {"b01_0": 23319, ...}
手動で差し替えたいときは overrides.json に {"b01_0": 12345} のように書く。
"""
import json
import os
import sys

import mixkit
import pexels
import sys as _sys
if os.environ.get("PROJECT_DIR"):
    _sys.path.insert(0, os.environ["PROJECT_DIR"])
from video_queries import BLOCK_QUERIES  # noqa: E402

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
# 別の動画を作るときは PROJECT_DIR に、その動画のフォルダ(script.txt などがある場所)を指定する
HERE = os.environ.get("PROJECT_DIR", CODE_DIR)
OUT = os.path.join(HERE, "out")


SOURCE = pexels if os.environ.get("CLIP_SOURCE") == "pexels" else mixkit
POOL_FILE = "pexels_pool.json" if SOURCE is pexels else "mixkit_pool.json"


def score(slug, phrase):
    words = phrase.lower().split()
    hit = sum(1 for w in words if w in slug)
    return hit / len(words) + (0.5 if hit == len(words) else 0)


def main():
    pool_path = os.path.join(OUT, POOL_FILE)
    os.makedirs(OUT, exist_ok=True)
    pool = json.load(open(pool_path)) if os.path.exists(pool_path) else {}
    pool = {int(k): v for k, v in pool.items()}
    overrides_path = os.path.join(HERE, "overrides.json")
    overrides = json.load(open(overrides_path)) if os.path.exists(overrides_path) else {}
    used, choices = {}, {}
    for bi, shots in enumerate(BLOCK_QUERIES, 1):
        for k, phrases in enumerate(shots):
            name = f"b{bi:02d}_{k}"
            if name in overrides:
                choices[name] = overrides[name]
                used[overrides[name]] = used.get(overrides[name], 0) + 1
                continue
            # 検索語で直接検索した結果もプールに足す
            for ph in phrases:
                for r in SOURCE.search(ph, pages=1):
                    pool.setdefault(r["id"], r["slug"])
            if SOURCE is pexels:
                # Pexels は検索の並び順が関連度順なので、上位から未使用のものを選ぶ
                best = None
                for ph in phrases:
                    for r in SOURCE.search(ph, pages=1):
                        if r["id"] not in used:
                            best = r["id"]
                            break
                    if best:
                        break
                choices[name] = best
                if best:
                    used[best] = used.get(best, 0) + 1
                print(f"{name} {best} {pool.get(best, '-')}", flush=True)
                continue
            best, best_s = None, 0
            for rank, ph in enumerate(phrases):
                for vid, slug in pool.items():
                    s = score(slug, ph) - rank * 0.05 - used.get(vid, 0) * 0.6
                    if s > best_s:
                        best, best_s = vid, s
            choices[name] = best
            if best:
                used[best] = used.get(best, 0) + 1
            print(f"{name} {best} {pool.get(best, '-')} ({best_s:.2f})", flush=True)
    json.dump(choices, open(os.path.join(OUT, "clip_choices.json"), "w"), indent=1)
    json.dump({str(k): v for k, v in pool.items()}, open(os.path.join(OUT, POOL_FILE), "w"))


if __name__ == "__main__":
    main()

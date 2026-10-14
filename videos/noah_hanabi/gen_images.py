"""prompts.py のショットごとに、pollinations.ai で実写風の画像を生成する。

出力: out/images/bNN_K.jpg (NN=ブロック番号 1始まり, K=ショット番号)
既にあるファイルはスキップするので、途中で止まっても再実行で続きから作れる。
"""
import os
import sys
import time
import urllib.parse
import urllib.request

from prompts import BLOCKS, prompt_text

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "images")
URL = "https://image.pollinations.ai/prompt/{p}?width=1280&height=720&nologo=true&seed={seed}"


def fetch(prompt, seed, path):
    url = URL.format(p=urllib.parse.quote(prompt_text(prompt)), seed=seed)
    for attempt in range(12):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                data = r.read()
            if len(data) > 10000 and data[:2] == b"\xff\xd8":
                open(path, "wb").write(data)
                return True
        except Exception as e:
            print(f"  retry {attempt + 1}: {e}", flush=True)
        time.sleep(min(60, 10 * (attempt + 1)))
    return False


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    for bi, shots in enumerate(BLOCKS, 1):
        for k, prompt in enumerate(shots):
            name = f"b{bi:02d}_{k}"
            if only and name not in only:
                continue
            path = os.path.join(OUT, name + ".jpg")
            if os.path.exists(path) and not only:
                continue
            ok = fetch(prompt, seed=bi * 100 + k + (int(time.time()) if only else 0), path=path)
            print(f"{name} {'ok' if ok else 'FAILED'}", flush=True)


if __name__ == "__main__":
    main()

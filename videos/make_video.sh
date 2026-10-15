#!/usr/bin/env bash
# 台本フォルダから動画(1本のMP4)を作る。
#
# 使い方:  videos/make_video.sh videos/shinkansen [pexels|mixkit]
#
# 前提:
#   - 動画フォルダに script.txt / video_queries.py / assets/(cta.mp4, ending_greenscreen.mp4, opening_boom.mp3)
#   - Pexels を使う場合は環境変数 PEXELS_API_KEY
# 出力: <動画フォルダ>/out/video_1080p.mp4
set -euo pipefail

PROJECT_DIR="$(cd "$1" && pwd)"
SOURCE="${2:-pexels}"
CODE="$(cd "$(dirname "$0")/noah_hanabi" && pwd)"
export PROJECT_DIR CLIP_SOURCE="$SOURCE"

pip install -q edge-tts >/dev/null 2>&1 || true

# 字幕・サムネ用フォント(大きいのでリポジトリには入れていない)
mkdir -p "$CODE/fonts"
for w in Bold Black; do
  f="$CODE/fonts/NotoSansCJKjp-$w.otf"
  [ -s "$f" ] && [ "$(stat -c%s "$f")" -gt 1000000 ] && continue
  curl -sSL -o "$f" "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/Japanese/NotoSansCJKjp-$w.otf"
done

echo "== ナレーション"
python3 "$CODE/build_audio.py"

echo "== 素材動画の選択"
python3 "$CODE/pick_clips.py"

echo "== 素材動画のダウンロード"
python3 - <<'EOF'
import json, os, sys
sys.path.insert(0, os.path.join(os.environ["PROJECT_DIR"], "..", "noah_hanabi"))
import mixkit, pexels
src = pexels if os.environ.get("CLIP_SOURCE") == "pexels" else mixkit
out = os.path.join(os.environ["PROJECT_DIR"], "out")
choices = json.load(open(os.path.join(out, "clip_choices.json")))
missing = [k for k, v in choices.items() if not v]
if missing:
    print("素材が見つからなかったショット:", missing)
from concurrent.futures import ThreadPoolExecutor
ids = sorted({v for v in choices.values() if v})
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(src.download, ids))
print(sum(1 for r in res if r), "/", len(ids), "本ダウンロード")
EOF

echo "== 書き出し"
python3 "$CODE/render3.py"
mv -f "$PROJECT_DIR/out/noah_hanabi_v3.mp4" "$PROJECT_DIR/out/video_1080p.mp4"
echo "完成: $PROJECT_DIR/out/video_1080p.mp4"

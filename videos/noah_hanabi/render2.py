"""参考チャンネルの体裁で動画を書き出す。

- 実写風の画像を 2.37:1 で中央に置き、上下は黒帯
- 画像下部に半透明の黒い帯を敷き、白い字幕を中央に表示(話者名や色分けはしない)
- ナレーターは1人(build_audio.py が Edge TTS で生成)
- BGM と花火の音は render.py の合成音を流用

前提: build_audio.py と gen_images.py を実行済みであること。
出力: out/noah_hanabi_v2.mp4
"""
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from prompts import BLOCKS
from render import count_frames, mix, ts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
IMAGES = os.path.join(OUT, "images")
SHOTS = os.path.join(OUT, "shots_v2")
FONTS = os.path.join(HERE, "fonts")
FPS = 30
VW, VH = 1920, 1080
IMG_H = 810                     # 1920x810 = 2.37:1
BAR = (VH - IMG_H) // 2         # 上下の黒帯 135px
BAND_H = 210                    # 字幕用の半透明帯(2行が入る高さ)
BAND_Y = BAR + IMG_H - BAND_H
MIN_SHOT = 7.0                  # 1枚の画像を最低何秒見せるか

FONT_NAME = os.environ.get("SUB_FONT", "Noto Sans CJK JP Black")


def wrap(text, width=20):
    """1行20文字を目安に、読点や助詞の後ろで2行に折り返す。"""
    if len(text) <= width:
        return text
    mid = len(text) / 2
    best, score = None, 1e9
    for i in range(5, len(text) - 3):
        prev, nxt = text[i - 1], text[i]
        hira = "\u3041" <= nxt <= "\u309f"
        # 句読点の後ろ、または助詞の後ろで次が漢字・カタカナのところだけで改行する
        if prev in "、。」？?！!" or (prev in "はがをにでとものへ" and not hira):
            sc = abs(i - mid) - (5 if prev in "、。」" else 0)
            if sc < score and max(i, len(text) - i) <= width + 4:
                best, score = i, sc
    if best is None:
        best = (len(text) + 1) // 2
    return text[:best] + "\\N" + text[best:]


def write_ass(segs, path):
    cy = BAND_Y + BAND_H // 2
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VW}
PlayResY: {VH}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,{FONT_NAME},104,&H0000EEFF,&H0000EEFF,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,9,0,5,40,40,0,1
Style: Sub,{FONT_NAME},74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,7,0,1,2,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for i, s in enumerate(segs):
        nxt = segs[i + 1]["start"] if i + 1 < len(segs) else s["end"] + 1.5
        end = min(nxt, s["end"] + 0.5)
        text = s["text"]
        if s["speaker"] != "narr" and not text.startswith("「"):
            text = "「" + text + "」"
        if i == 0:
            # 冒頭のひと言は、画面中央に大きく出し、手前に近づいてくるように拡大する
            hold = segs[1]["start"] if len(segs) > 1 else end
            dur_ms = int((hold - s["start"]) * 1000)
            lines.append(f"Dialogue: 1,{ts(s['start'])},{ts(hold)},Hook,,0,0,0,,"
                         f"{{\\pos({VW // 2},{BAR + IMG_H // 2 - 40})\\fscx50\\fscy50\\fad(150,250)"
                         f"\\t(0,{dur_ms},0.6,\\fscx135\\fscy135)}}{wrap(text, 12)}")
            continue
        lines.append(f"Dialogue: 0,{ts(s['start'])},{ts(end)},Sub,,0,0,0,,{{\\pos({VW // 2},{cy})}}{wrap(text)}")

    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")


def build_shots(segs, duration):
    """ブロック(=台本の # scene: 区切り)ごとに、用意したショット画像を均等に割り当てる。"""
    blocks = []
    for s in segs:
        if not blocks or blocks[-1]["block"] != s["block"]:
            blocks.append({"block": s["block"], "starts": []})
        blocks[-1]["starts"].append(s["start"])
    blocks[0]["starts"][0] = 0.0
    shots = []
    for bi, b in enumerate(blocks):
        start = b["starts"][0]
        end = blocks[bi + 1]["starts"][0] if bi + 1 < len(blocks) else duration
        images = [f"b{b['block']:02d}_{k}.jpg" for k in range(len(BLOCKS[b["block"] - 1]))]
        images = [im for im in images if os.path.exists(os.path.join(IMAGES, im))] or images[:1]
        n = max(1, min(len(images), int((end - start) // MIN_SHOT)))
        # 切り替えは字幕の切れ目にそろえる
        cuts = [start]
        for k in range(1, n):
            target = start + (end - start) * k / n
            cut = min(b["starts"], key=lambda t: abs(t - target))
            if cut > cuts[-1] + 2:
                cuts.append(cut)
        cuts.append(end)
        for k in range(len(cuts) - 1):
            shots.append({"image": images[k % len(images)], "start": cuts[k], "end": cuts[k + 1]})
    return shots


def render_shot(args):
    i, sh = args
    path = os.path.join(SHOTS, f"{i:04d}.mp4")
    dur = sh["end"] - sh["start"]
    frames = max(1, int(round(dur * FPS)))
    if os.path.exists(path) and count_frames(path) == frames:
        return path
    img = os.path.join(IMAGES, sh["image"])
    # 生成画像(16:9)を 2.37:1 に切り抜く。下端のロゴ部分を避けて上寄りで切る
    z0, z1 = (1.0, 1.07) if i % 2 == 0 else (1.07, 1.0)
    dx = [0.5, 0.0, 1.0][i % 3]
    vf = (f"crop=iw:iw/2.37:0:ih*0.06,scale=3840:1620,setsar=1,"
          f"zoompan=z='{z0}+({z1}-{z0})*on/{frames}':x='(iw-iw/zoom)*{dx}':y='(ih-ih/zoom)/2':"
          f"d={frames}:s={VW}x{IMG_H}:fps={FPS},"
          f"pad={VW}:{VH}:0:{BAR}:black,"
          f"drawbox=x=0:y={BAND_Y}:w={VW}:h={BAND_H}:color=black@0.62:t=fill,format=yuv420p")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", img, "-vf", vf, "-frames:v", str(frames),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", path]
    subprocess.run(cmd, check=True)
    return path


def main():
    data = json.load(open(os.path.join(OUT, "segments.json"), encoding="utf-8"))
    segs, duration = data["segments"], data["duration"]
    os.makedirs(SHOTS, exist_ok=True)
    shots = build_shots(segs, duration)
    print(f"{len(shots)} shots, {duration/60:.1f} min", flush=True)
    ass = os.path.join(OUT, "subs_v2.ass")
    write_ass(segs, ass)
    # mix() はシーン名で花火の音を入れるので、シーン情報付きのショット一覧を渡す
    scene_shots = []
    for s in segs:
        if not scene_shots or scene_shots[-1]["scene"] != s["scene"]:
            scene_shots.append({"scene": s["scene"], "start": s["start"]})
    for k, sh in enumerate(scene_shots):
        sh["end"] = scene_shots[k + 1]["start"] if k + 1 < len(scene_shots) else duration
    audio = mix(duration, segs, scene_shots)
    print("audio mixed", flush=True)
    with ThreadPoolExecutor(4) as ex:
        paths = list(ex.map(render_shot, enumerate(shots)))
    print("shots rendered", flush=True)
    lst = os.path.join(OUT, "shots_v2.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in paths))
    final = os.path.join(OUT, "noah_hanabi_v2.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats", "-f", "concat", "-safe", "0", "-i", lst,
           "-i", audio, "-vf", f"ass={ass}:fontsdir={FONTS}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000",
           "-shortest", "-movflags", "+faststart", final]
    subprocess.run(cmd, check=True)
    print(final, flush=True)


if __name__ == "__main__":
    main()

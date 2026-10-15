"""画像を使わず、すべてフリー動画(Mixkit)で映像を作る版。

レイアウト・字幕・音声は render2.py と同じ。各ショットの映像は
out/clip_choices.json で選んだクリップを、2.37:1 に切り抜いて流す。
クリップが短いときはループさせる。
出力: out/noah_hanabi_v3.mp4
"""
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

import render2
from render import count_frames, mix
from render2 import BAND_H, BAND_Y, BAR, FONTS, FPS, IMG_H, MIN_SHOT, OUT, VH, VW, write_ass
from video_queries import BLOCK_QUERIES

CLIPS = os.path.join(OUT, "clips")
SHOTS = os.path.join(OUT, "shots_v3")


def build_shots(segs, duration, choices):
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
        clips = [choices[f"b{b['block']:02d}_{k}"] for k in range(len(BLOCK_QUERIES[b["block"] - 1]))]
        n = max(1, min(len(clips), int((end - start) // MIN_SHOT)))
        cuts = [start]
        for k in range(1, n):
            target = start + (end - start) * k / n
            cut = min(b["starts"], key=lambda t: abs(t - target))
            if cut > cuts[-1] + 2:
                cuts.append(cut)
        cuts.append(end)
        for k in range(len(cuts) - 1):
            shots.append({"clip": clips[k % len(clips)], "start": cuts[k], "end": cuts[k + 1]})
    return shots


def render_shot(args):
    i, sh = args
    path = os.path.join(SHOTS, f"{i:04d}.mp4")
    dur = sh["end"] - sh["start"]
    frames = max(1, int(round(dur * FPS)))
    if os.path.exists(path) and count_frames(path) == frames:
        return path
    src = os.path.join(CLIPS, f"{sh['clip']}.mp4")
    vf = (f"fps={FPS},scale={VW}:{IMG_H}:force_original_aspect_ratio=increase,crop={VW}:{IMG_H},setsar=1,"
          f"pad={VW}:{VH}:0:{BAR}:black,"
          f"drawbox=x=0:y={BAND_Y}:w={VW}:h={BAND_H}:color=black@0.62:t=fill,format=yuv420p")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", src, "-an", "-vf", vf,
           "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", path]
    subprocess.run(cmd, check=True)
    return path


def main():
    data = json.load(open(os.path.join(OUT, "segments.json"), encoding="utf-8"))
    segs, duration = data["segments"], data["duration"]
    choices = json.load(open(os.path.join(OUT, "clip_choices.json")))
    os.makedirs(SHOTS, exist_ok=True)
    shots = build_shots(segs, duration, choices)
    print(f"{len(shots)} shots, {duration/60:.1f} min", flush=True)
    ass = os.path.join(OUT, "subs_v3.ass")
    write_ass(segs, ass)
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
    lst = os.path.join(OUT, "shots_v3.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in paths))
    final = os.path.join(OUT, "noah_hanabi_v3.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats", "-f", "concat", "-safe", "0", "-i", lst,
           "-i", audio, "-vf", f"ass={ass}:fontsdir={FONTS}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000",
           "-shortest", "-movflags", "+faststart", final]
    subprocess.run(cmd, check=True)
    print(final, flush=True)


if __name__ == "__main__":
    main()

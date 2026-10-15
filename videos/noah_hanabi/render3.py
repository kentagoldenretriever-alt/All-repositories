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
import sys as _sys
if os.environ.get("PROJECT_DIR"):
    _sys.path.insert(0, os.environ["PROJECT_DIR"])
from video_queries import BLOCK_QUERIES  # noqa: E402

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


MAX_STRETCH = 1.25  # 素材が足りないときは最大 1.25 倍までスローにして伸ばす(ループはしない)


def clip_duration(vid, cache={}):
    if vid not in cache:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            os.path.join(CLIPS, f"{vid}.mp4")], capture_output=True, text=True)
        cache[vid] = float(r.stdout.strip() or 0)
    return cache[vid]


def build_shots_seq(segs, duration, choices, extras):
    """ブロックごとに素材を順番に流す。1本の素材は1回だけ、長さの範囲内で使い、ループさせない。

    素材を切り替える位置は字幕の切れ目にそろえる。素材の合計が足りないブロックだけ、
    各素材を最大 MAX_STRETCH 倍までスローにして埋める。
    """
    blocks = []
    for s in segs:
        if not blocks or blocks[-1]["block"] != s["block"]:
            blocks.append({"block": s["block"], "starts": []})
        blocks[-1]["starts"].append(s["start"])
    blocks[0]["starts"][0] = 0.0
    shots, short = [], []
    for bi, b in enumerate(blocks):
        start = b["starts"][0]
        end = blocks[bi + 1]["starts"][0] if bi + 1 < len(blocks) else duration
        n = len(BLOCK_QUERIES[b["block"] - 1])
        clips = [choices[f"b{b['block']:02d}_{k}"] for k in range(n)] + extras.get(str(b["block"]), [])
        seen = set()
        clips = [c for c in clips if c and not (c in seen or seen.add(c))]
        lens = [clip_duration(c) for c in clips]
        total = sum(lens)
        stretch = min(MAX_STRETCH, max(1.0, (end - start) / total)) if total else 1.0
        if total * stretch < end - start - 0.5:
            short.append((b["block"], round(end - start - total * stretch, 1)))
        t = start
        for k, (c, L) in enumerate(zip(clips, lens)):
            if t >= end - 0.05:
                break
            if k == len(clips) - 1:
                cut = end  # 最後の素材でブロックの終わりまで埋める
            else:
                max_end = min(end, t + L * stretch)                     # この素材で使える一番先
                min_end = max(t + 2.5, end - sum(lens[k + 1:]) * stretch)  # 残りの素材で埋めきれる位置
                cands = [x for x in b["starts"] if min_end <= x <= max_end]
                cut = max(cands) if cands else (max_end if max_end >= min_end else min_end)
            shots.append({"clip": c, "start": t, "end": cut,
                          "speed": max(1.0, (cut - t) / L) if L else 1.0})
            t = cut
        shots[-1]["end"] = end  # 端数の隙間をなくす
        last = shots[-1]
        last["speed"] = max(1.0, (last["end"] - last["start"]) / clip_duration(last["clip"]))
    if short:
        print("素材が足りないブロック(秒):", short, flush=True)
    return shots


def splice_inserts(shots, inserts):
    """差し込み区間にかかるショットを切り分け、その区間を素材動画のショットに置き換える。"""
    for ins in inserts:
        out = []
        for sh in shots:
            if sh["end"] <= ins["start"] or sh["start"] >= ins["end"]:
                out.append(sh)
                continue
            if sh["start"] < ins["start"]:
                out.append({**sh, "end": ins["start"]})
            if not any(o.get("insert") == ins["path"] for o in out):
                out.append({"insert": ins["path"], "start": ins["start"], "end": ins["end"]})
            if sh["end"] > ins["end"]:
                out.append({**sh, "start": ins["end"]})
        shots = out
    return shots


def render_shot(args):
    i, sh = args
    path = os.path.join(SHOTS, f"{i:04d}.mp4")
    dur = sh["end"] - sh["start"]
    frames = max(1, int(round(dur * FPS)))
    fresh = os.path.exists(path) and count_frames(path) == frames
    if fresh and "insert" in sh and os.path.getmtime(sh["insert"]) > os.path.getmtime(path):
        fresh = False  # 差し込み素材が差し替えられたら作り直す
    if fresh:
        return path
    if "insert" in sh:
        # 差し込み素材は黒帯や字幕帯を付けず、そのまま全画面で流す
        vf = f"fps={FPS},scale={VW}:{VH}:force_original_aspect_ratio=decrease,pad={VW}:{VH}:-1:-1:black,setsar=1,format=yuv420p"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", sh["insert"], "-an", "-vf", vf + ",tpad=stop_mode=clone:stop=-1",
               "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", path]
        subprocess.run(cmd, check=True)
        return path
    src = os.path.join(CLIPS, f"{sh['clip']}.mp4")
    speed = sh.get("speed", 1.0)
    slow = f"setpts={speed:.4f}*PTS," if speed > 1.001 else ""
    vf = (f"{slow}fps={FPS},scale={VW}:{IMG_H}:force_original_aspect_ratio=increase,crop={VW}:{IMG_H},setsar=1,"
          f"pad={VW}:{VH}:0:{BAR}:black,"
          f"drawbox=x=0:y={BAND_Y}:w={VW}:h={BAND_H}:color=black@0.62:t=fill,format=yuv420p")
    vf += ",tpad=stop_mode=clone:stop_duration=1"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-an", "-vf", vf,
           "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", path]
    subprocess.run(cmd, check=True)
    return path


def main():
    data = json.load(open(os.path.join(OUT, "segments.json"), encoding="utf-8"))
    segs, duration = data["segments"], data["duration"]
    choices = json.load(open(os.path.join(OUT, "clip_choices.json")))
    os.makedirs(SHOTS, exist_ok=True)
    assets = os.path.join(os.path.dirname(OUT), "assets")
    inserts = [{**i, "path": os.path.join(assets, f"{i['name']}.mp4")} for i in data.get("inserts", [])]
    ending = data.get("ending")
    extras_path = os.path.join(os.path.dirname(OUT), "block_extras.json")
    extras = json.load(open(extras_path)) if os.path.exists(extras_path) else {}
    shots = splice_inserts(build_shots_seq(segs, duration, choices, extras), inserts)
    print(f"{len(shots)} shots, {duration/60:.1f} min", flush=True)
    ass = os.path.join(OUT, "subs_v3.ass")
    write_ass(segs, ass)
    scene_shots = []
    for s in segs:
        if not scene_shots or scene_shots[-1]["scene"] != s["scene"]:
            scene_shots.append({"scene": s["scene"], "start": s["start"]})
    for k, sh in enumerate(scene_shots):
        sh["end"] = scene_shots[k + 1]["start"] if k + 1 < len(scene_shots) else duration
    overlays = []
    boom = os.path.join(assets, "opening_boom.mp3")
    if os.path.exists(boom):
        overlays.append({"path": boom, "start": 0.0, "gain": 1.0})
    if ending:
        ending["path"] = os.path.join(assets, f"{ending['name']}.mp4")
        overlays.append({"path": ending["path"], "start": ending["start"], "gain": 0.8})
    audio = mix(duration, segs, scene_shots, inserts=inserts, overlays=overlays)
    print("audio mixed", flush=True)
    with ThreadPoolExecutor(4) as ex:
        paths = list(ex.map(render_shot, enumerate(shots)))
    print("shots rendered", flush=True)
    lst = os.path.join(OUT, "shots_v3.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in paths))
    final = os.path.join(OUT, "noah_hanabi_v3.mp4")
    if ending:
        # 終了画面: グリーンバックを抜いて、最後の呼びかけに合わせて重ねる
        inputs = ["-i", ending["path"]]
        graph = (f"[0:v]ass={ass}:fontsdir={FONTS}[base];"
                 f"[2:v]fps={FPS},scale={VW}:{VH},chromakey=0x01FC00:0.18:0.06,"
                 f"setpts=PTS+{ending['start']}/TB[ov];"
                 f"[base][ov]overlay=eof_action=pass:format=auto[v]")
        vargs = inputs + ["-filter_complex", graph, "-map", "[v]", "-map", "1:a"]
    else:
        vargs = ["-vf", f"ass={ass}:fontsdir={FONTS}"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats", "-f", "concat", "-safe", "0", "-i", lst,
           "-i", audio] + vargs + [
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000",
           "-shortest", "-movflags", "+faststart", final]
    subprocess.run(cmd, check=True)
    print(final, flush=True)


if __name__ == "__main__":
    main()

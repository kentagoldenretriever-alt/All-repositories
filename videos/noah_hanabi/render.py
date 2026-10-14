"""背景・字幕・ナレーション・BGMを合成して最終動画を書き出す。

前提: build_audio.py と scenes.py を実行済みであること。
出力: out/noah_hanabi.mp4, out/thumbnail.png
"""
import json
import math
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SHOTS = os.path.join(OUT, "shots")
SR = 48000
FPS = 30
VW, VH = 1920, 1080

# 話者ごとの字幕色(ASSは &HBBGGRR)
COLORS = {
    "narr": "&H00FFFFFF",
    "N": "&H00FFE09F",   # ノア: 水色
    "S": "&H00C8B0FF",   # サラ: ピンク
    "T": "&H0060D0FF",   # 孝志: 橙
    "D": "&H00B0F0B0",   # 医師: 薄緑
    "B": "&H00B0F0B0",
    "U": "&H00B0F0B0",
    "K": "&H0080FFFF",
    "E": "&H00C8B0FF",
    "P": "&H00FFFFFF",
}
NAMES = {"N": "ノア", "S": "サラ", "T": "孝志", "D": "佐藤医師", "B": "ベネット医師",
         "U": "医師", "K": "子供たち", "E": "宿の女性", "P": "救急隊員"}


def ts(t):
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def wrap(text, width=24):
    """字幕を2行以内に折り返す(読点・助詞のあたりで切る)。"""
    if len(text) <= width:
        return text
    mid = len(text) / 2
    best, score = None, 1e9
    for i in range(6, len(text) - 4):
        if text[i - 1] in "、。」？?!！" or text[i - 1] in "はがをにでとものへ":
            sc = abs(i - mid) - (6 if text[i - 1] in "、。」" else 0)
            if sc < score and i <= width + 2 and len(text) - i <= width + 2:
                best, score = i, sc
    if best is None:
        best = int(math.ceil(len(text) / 2))
    return text[:best] + "\\N" + text[best:]


def write_ass(segs, path):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VW}
PlayResY: {VH}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,IPAGothic,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,6,3,2,60,60,70,1
Style: Name,IPAGothic,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,4,2,7,70,70,40,1
Style: Title,IPAGothic,96,&H0060D8FF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,4,0,1,8,4,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for i, s in enumerate(segs):
        start = s["start"]
        nxt = segs[i + 1]["start"] if i + 1 < len(segs) else s["end"] + 1.0
        end = min(nxt, s["end"] + 0.6)
        text = wrap(s["text"])
        col = COLORS[s["speaker"]]
        if s["speaker"] != "narr" and not text.startswith("「"):
            text = "「" + text + "」"
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Sub,,0,0,0,,{{\\c{col}}}{text}")
        if s["speaker"] in NAMES:
            lines.append(f"Dialogue: 1,{ts(start)},{ts(end)},Name,,0,0,0,,{{\\c{col}\\pos(70,960)\\an1}}{NAMES[s['speaker']]}")
    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")


def build_shots(segs, duration):
    shots = []
    for s in segs:
        if not shots or shots[-1]["scene"] != s["scene"]:
            shots.append({"scene": s["scene"], "start": s["start"]})
    shots[0]["start"] = 0.0
    for i, sh in enumerate(shots):
        sh["end"] = shots[i + 1]["start"] if i + 1 < len(shots) else duration
    return shots


def render_shot(args):
    i, sh = args
    path = os.path.join(SHOTS, f"{i:04d}.mp4")
    if os.path.exists(path):
        return path
    dur = sh["end"] - sh["start"]
    img = os.path.join(OUT, "scenes", f"{sh['scene']}.png")
    # ゆっくりズーム&パン。画像を一度大きく拡大しておき、サブピクセルの揺れを抑える
    z0, z1 = (1.0, 1.08) if i % 2 == 0 else (1.08, 1.0)
    dx = [0.0, 1.0, 0.5][i % 3]
    frames = max(1, int(round(dur * FPS)))
    zexpr = f"{z0}+({z1}-{z0})*on/{frames}"
    vf = (f"scale=3840:-1,zoompan=z='{zexpr}':"
          f"x='(iw-iw/zoom)*{dx}':y='(ih-ih/zoom)/2':d={frames}:s={VW}x{VH}:fps={FPS},"
          f"fade=t=in:st=0:d=0.35,fade=t=out:st={max(0, dur - 0.35):.3f}:d=0.35,format=yuv420p")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", img,
           "-vf", vf, "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "20", "-pix_fmt", "yuv420p", path]
    subprocess.run(cmd, check=True)
    return path


# ---------------------------------------------------------------- audio
def bgm(duration):
    """穏やかなピアノ風のアルペジオ+パッドを合成する。"""
    n = int(duration * SR)
    out = np.zeros(n)
    bpm = 66
    beat = 60 / bpm
    # C - G/B - Am - F の循環(ゆったり)
    chords = [[48, 55, 60, 64, 67], [47, 55, 59, 62, 67], [45, 52, 57, 60, 64], [41, 48, 53, 57, 60]]
    pattern = [0, 2, 3, 4, 3, 2, 1, 2]

    def note(midi, length, amp):
        f = 440 * 2 ** ((midi - 69) / 12)
        t = np.arange(int(length * SR)) / SR
        env = np.exp(-t * 2.2) * (1 - np.exp(-t * 200))
        w = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
        return w * env * amp

    def pad(midis, length):
        t = np.arange(int(length * SR)) / SR
        env = np.minimum(1, t / 1.5) * np.minimum(1, (length - t) / 1.5)
        w = sum(np.sin(2 * np.pi * 440 * 2 ** ((m - 69) / 12) * t * (1 + 0.0015 * k)) for k, m in enumerate(midis))
        return w * env * 0.05

    note_cache = {}
    bar = beat * 4
    t = 0.0
    ci = 0
    while t < duration:
        ch = chords[ci % 4]
        p = pad([m + 12 for m in ch[:3]], bar * 2)
        s = int(t * SR)
        e = min(n, s + len(p))
        out[s:e] += p[:e - s]
        for k in range(16):
            midi = ch[pattern[k % 8]] + 12
            key = midi
            if key not in note_cache:
                note_cache[key] = note(midi, 3.0, 0.16)
            x = note_cache[key]
            s = int((t + k * beat / 2) * SR)
            if s >= n:
                break
            e = min(n, s + len(x))
            out[s:e] += x[:e - s]
        t += bar * 2
        ci += 1
    # 簡易リバーブ
    for d, g in ((0.11, 0.35), (0.23, 0.22), (0.37, 0.14)):
        k = int(d * SR)
        out[k:] += out[:-k] * g
    return out / (np.max(np.abs(out)) + 1e-9)


def boom(seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(2.5 * SR)) / SR
    low = np.sin(2 * np.pi * (55 - 20 * t) * t) * np.exp(-t * 3.5)
    noise = r.standard_normal(len(t))
    # ローパス(移動平均)
    k = 60
    noise = np.convolve(noise, np.ones(k) / k, mode="same") * np.exp(-t * 2.0) * 3
    crack = r.standard_normal(len(t)) * (r.random(len(t)) < 0.004) * np.exp(-(t - 0.6) ** 2 * 3) * 0.6
    x = low + noise + crack
    return x / np.max(np.abs(x))


def mix(duration, segs, shots):
    import wave
    w = wave.open(os.path.join(OUT, "narration.wav"))
    narr = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    n = len(narr)
    music = bgm(duration)[:n]
    # ナレーション中はBGMを下げる(ダッキング)
    env = np.convolve(np.abs(narr), np.ones(4800) / 4800, mode="same")
    duck = np.where(env > 0.01, 0.10, 0.22)
    duck = np.convolve(duck, np.ones(24000) / 24000, mode="same")
    fx = np.zeros(n)
    times = []
    for s in segs:
        if s["scene"] in ("hospital_wall",) and "ドン" in s["text"]:
            times += [s["start"] - 0.4, s["start"] + 1.6]
        if s["scene"].startswith("fireworks") and s["scene"] != "fireworks_start" and "ドン" in s["text"]:
            times += [s["start"] - 0.2]
    for sh in shots:
        if sh["scene"] in ("fireworks", "fireworks_gold", "fireworks_crowd", "fireworks_finale", "title"):
            t0 = sh["start"] + 0.3
            k = 0
            while t0 < sh["end"] - 1:
                times.append(t0)
                t0 += 6.0 + (k % 3) * 2.5
                k += 1
    for i, t0 in enumerate(times):
        b = boom(i)
        # 病室では壁越しのくぐもった音
        s = int(max(0, t0) * SR)
        e = min(n, s + len(b))
        fx[s:e] += b[:e - s] * 0.22
    y = narr * 0.95 + music * duck + fx
    y = y / max(1.0, np.max(np.abs(y)) / 0.97)
    out = (y * 32767).astype(np.int16)
    path = os.path.join(OUT, "mix.wav")
    wo = wave.open(path, "wb")
    wo.setnchannels(1)
    wo.setsampwidth(2)
    wo.setframerate(SR)
    wo.writeframes(out.tobytes())
    wo.close()
    return path


def main():
    data = json.load(open(os.path.join(OUT, "segments.json"), encoding="utf-8"))
    segs, duration = data["segments"], data["duration"]
    os.makedirs(SHOTS, exist_ok=True)
    shots = build_shots(segs, duration)
    print(f"{len(shots)} shots, {duration/60:.1f} min")

    write_ass(segs, os.path.join(OUT, "subs.ass"))
    audio = mix(duration, segs, shots)
    print("audio mixed")

    with ThreadPoolExecutor(4) as ex:
        paths = list(ex.map(render_shot, enumerate(shots)))
    print("shots rendered")
    lst = os.path.join(OUT, "shots.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in paths))
    final = os.path.join(OUT, "noah_hanabi.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats", "-f", "concat", "-safe", "0", "-i", lst,
           "-i", audio, "-vf", f"ass={os.path.join(OUT, 'subs.ass')}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", final]
    subprocess.run(cmd, check=True)
    print(final)


if __name__ == "__main__":
    main()

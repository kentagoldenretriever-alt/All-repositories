"""台本(script.txt)を字幕チャンクに分割し、OpenJTalkでナレーション音声を合成する。

出力:
  out/narration.wav   … 全編のナレーション
  out/segments.json   … 字幕チャンクごとの開始/終了時刻・話者・シーン
"""
import json
import os
import re
import sys

import asyncio
import hashlib
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SR = 48000

# 話者ごとの声の高さ(半音)と話速
VOICES = {
    "narr": (0.0, 1.08),
    "N": (3.5, 1.05),   # ノア
    "S": (1.0, 1.05),   # サラ
    "T": (-4.0, 1.0),   # 孝志
    "D": (-3.0, 1.0),   # 佐藤医師
    "B": (-3.0, 1.0),   # ベネット医師
    "U": (-2.5, 1.0),   # 米国の医師
    "K": (5.0, 1.1),    # 子供たち
    "E": (1.5, 1.05),   # 宿・ホテルの女性
    "P": (-2.0, 1.0),   # 救急隊員
}

# 読み間違い対策(音声のみに適用)
READINGS = {
    "孝志": "たかし",
    "山下": "やました",
    "恵子": "けいこ",
    "ノア・ミラー": "ノア、ミラー",
    "下手くそ": "へたくそ",
    "持っとれ": "もっとれ",
    "つかん": "つかん",
    "開かん": "ひらかん",
    "変わらん": "かわらん",
    "言わん": "いわん",
    "比べもん": "くらべもん",
    "見りゃ": "みりゃ",
    "抑えて": "おさえて",
    "1年がかり": "いちねんがかり",
    "藍色": "あいいろ",
    "寝巻き": "ねまき",
    "胸を衝かれ": "むねをつかれ",
    "町": "まち",  # 台本の「町」はすべて「まち」(TTSが「ちょう」と読むことがある)
}

MAX_CHUNK = 34  # 字幕1枚あたりの最大文字数(2行)

GAP_CHUNK = 0.12
GAP_SENT = 0.35
GAP_PARA = 0.8


def parse(path):
    """script.txt を段落リストに変換: [(scene, speaker, text), ...] と段落区切り。"""
    items = []
    scene = "title"
    block = 0
    para_break = False
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if line.startswith("#"):
            m = re.match(r"#\s*scene:(\w+)", line)
            if m:
                scene = m.group(1)
                block += 1
            continue
        if not line:
            para_break = True
            continue
        m = re.match(r"^@insert:(\w+)$", line)
        if m:
            items.append({"insert": m.group(1), "scene": scene, "block": block, "para": para_break})
            para_break = False
            continue
        m = re.match(r"^([A-Z])\|(.*)$", line)
        if m:
            speaker, text = m.group(1), m.group(2).strip()
        else:
            speaker, text = "narr", line
        items.append({"scene": scene, "block": block, "speaker": speaker, "text": text,
                      "para": para_break})
        para_break = False
    return items


def split_sentences(text):
    """「」の外側にある句点・疑問符で文を分ける。"""
    out, buf, depth = [], "", 0
    for i, ch in enumerate(text):
        buf += ch
        if ch == "「":
            depth += 1
        elif ch == "」":
            depth = max(0, depth - 1)
        elif depth == 0 and ch in "。?？!！":
            # 「?」の直後に続く空白は文の区切りとして扱う
            out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return [s for s in out if s]


def split_chunk(sent):
    """長い文を読点で分割して字幕1枚に収める。"""
    if len(sent) <= MAX_CHUNK:
        return [sent]
    parts = re.split(r"(?<=[、,])", sent)
    chunks, buf = [], ""
    for p in parts:
        if buf and len(buf) + len(p) > MAX_CHUNK:
            chunks.append(buf)
            buf = p
        else:
            buf += p
    if buf:
        chunks.append(buf)
    # それでも長いものは機械的に半分にする
    final = []
    for c in chunks:
        while len(c) > MAX_CHUNK:
            cut = len(c) // 2
            final.append(c[:cut])
            c = c[cut:]
        final.append(c)
    # 極端に短い末尾は前に結合
    merged = []
    for c in final:
        if merged and len(c) <= 4 and len(merged[-1]) + len(c) <= MAX_CHUNK + 6:
            merged[-1] += c
        else:
            merged.append(c)
    return merged


def tts_text(text):
    t = text
    for k, v in READINGS.items():
        t = t.replace(k, v)
    t = t.replace("「", "").replace("」", "、").replace("……", "、").replace("…", "、")
    t = t.strip("、 ")
    return t


# Edge TTS(Microsoftのニューラル音声)。参考チャンネルと同じくナレーター1人で全編を読む。
EDGE_VOICE = os.environ.get("EDGE_VOICE", "ja-JP-NanamiNeural")
EDGE_RATE = os.environ.get("EDGE_RATE", "+8%")
CACHE = os.path.join(OUT, "tts_cache")


def edge_path(text):
    key = hashlib.sha1(f"{EDGE_VOICE}|{EDGE_RATE}|{text}".encode()).hexdigest()
    return os.path.join(CACHE, key + ".mp3")


async def edge_prefetch(texts, concurrency=8):
    import edge_tts
    os.makedirs(CACHE, exist_ok=True)
    proxy = os.environ.get("HTTPS_PROXY")
    sem = asyncio.Semaphore(concurrency)

    async def one(t):
        path = edge_path(t)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return
        async with sem:
            for attempt in range(5):
                try:
                    await edge_tts.Communicate(t, EDGE_VOICE, rate=EDGE_RATE, proxy=proxy).save(path)
                    return
                except Exception:
                    await asyncio.sleep(2 ** attempt)
            raise RuntimeError(f"TTS failed: {t}")

    await asyncio.gather(*(one(t) for t in set(texts)))


def synth(text, speaker):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", edge_path(tts_text(text)), "-f", "s16le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    # 前後の無音を詰める
    th = 200
    idx = np.where(np.abs(x) > th)[0]
    if len(idx):
        x = x[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.08 * SR)]
    return x


def media_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main():
    os.makedirs(OUT, exist_ok=True)
    items = parse(os.path.join(HERE, "script.txt"))
    texts = [tts_text(c) for it in items if "text" in it
             for se in split_sentences(it["text"]) for c in split_chunk(se)]
    asyncio.run(edge_prefetch(texts))
    print(f"tts ready: {len(texts)} chunks")
    audio = [np.zeros(int(0.6 * SR))]
    t = 0.6
    segs, inserts = [], []
    for it in items:
        if it["para"] and segs:
            audio.append(np.zeros(int(GAP_PARA * SR)))
            t += GAP_PARA
        if "insert" in it:
            # 素材動画(自前の音声付き)を流す間は、ナレーションを無音にしておく
            dur = media_duration(os.path.join(HERE, "assets", f"{it['insert']}.mp4"))
            inserts.append({"name": it["insert"], "start": round(t, 3), "end": round(t + dur, 3)})
            audio.append(np.zeros(int(dur * SR)))
            t += dur + GAP_SENT
            audio.append(np.zeros(int(GAP_SENT * SR)))
            continue
        sents = split_sentences(it["text"])
        for si, sent in enumerate(sents):
            chunks = split_chunk(sent)
            for ci, ch in enumerate(chunks):
                x = synth(ch, it["speaker"])
                dur = len(x) / SR
                segs.append({"start": round(t, 3), "end": round(t + dur, 3),
                             "text": ch, "speaker": it["speaker"],
                             "scene": it["scene"], "block": it["block"]})
                audio.append(x)
                t += dur
                gap = GAP_CHUNK if ci < len(chunks) - 1 else GAP_SENT
                audio.append(np.zeros(int(gap * SR)))
                t += gap
        sys.stdout.write(f"\r{len(segs)} chunks, {t/60:.1f} min")
        sys.stdout.flush()
    # 終了画面(グリーンバックの登録ボタン)を最後の「チャンネル登録」の呼びかけから重ねる。
    # アニメーションが最後まで流れるよう、末尾の無音を延ばす
    ending = None
    end_asset = os.path.join(HERE, "assets", "ending_greenscreen.mp4")
    cta_segs = [sg for sg in segs if "チャンネル登録" in sg["text"]]
    if os.path.exists(end_asset) and cta_segs:
        start = cta_segs[-1]["start"]
        ending = {"name": "ending_greenscreen", "start": start,
                  "end": round(start + media_duration(end_asset), 3)}
    tail = max(2.0, (ending["end"] + 0.5 - t) if ending else 0)
    audio.append(np.zeros(int(tail * SR)))
    t += tail
    y = np.concatenate(audio)
    peak = np.max(np.abs(y)) or 1
    y = (y / peak * 0.9 * 32767).astype(np.int16)
    import wave
    w = wave.open(os.path.join(OUT, "narration.wav"), "wb")
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(y.tobytes())
    w.close()
    json.dump({"duration": round(len(y) / SR, 3), "segments": segs, "inserts": inserts, "ending": ending},
              open(os.path.join(OUT, "segments.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\nduration {len(y)/SR/60:.1f} min, {len(segs)} segments")


if __name__ == "__main__":
    main()

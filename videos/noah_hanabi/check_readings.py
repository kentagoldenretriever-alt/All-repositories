"""ナレーションの読み間違いを、音声認識(Whisper)で聞き直して探す。

各字幕チャンクの音声を文字起こしし、台本と「読み(カナ)」同士で比べて、
ずれが大きいものを out/reading_check.tsv に書き出す。
"""
import difflib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import subprocess

import numpy as np
import pyopenjtalk

import build_audio

OUT = build_audio.OUT


def kana(text):
    t = "".join(ch for ch in text if ch not in "「」『』（）()、。，．,.!?！？…・ 　\"'“”")
    try:
        return pyopenjtalk.g2p(t, kana=True).replace("、", "").replace("ー", "")
    except Exception:
        return t


def main():
    from faster_whisper import WhisperModel
    model = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="cpu", compute_type="int8", cpu_threads=4)
    segs = json.load(open(os.path.join(OUT, "segments.json"), encoding="utf-8"))["segments"]
    rows = []
    for i, s in enumerate(segs):
        spoken = build_audio.tts_text(s["text"])
        path = build_audio.edge_path(spoken)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                             capture_output=True, check=True).stdout
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
        res, _ = model.transcribe(audio, language="ja", beam_size=1, vad_filter=False,
                                  initial_prompt="新幹線 TGV アラン クレマン 田中 美咲 修一 レア")
        heard = "".join(r.text for r in res)
        a, b = kana(spoken), kana(heard)
        ratio = difflib.SequenceMatcher(None, a, b).ratio()
        rows.append((i, round(ratio, 3), s["text"], heard, a, b))
        if i % 50 == 0:
            print(i, len(segs), flush=True)
    rows.sort(key=lambda r: r[1])
    with open(os.path.join(OUT, "reading_check.tsv"), "w", encoding="utf-8") as f:
        f.write("idx\tscore\tscript\theard\tscript_kana\theard_kana\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    print("done", sum(1 for r in rows if r[1] < 0.85), "chunks below 0.85")


if __name__ == "__main__":
    main()

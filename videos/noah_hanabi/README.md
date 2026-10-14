# 余命1年の少年と日本の花火 — 動画生成

台本 `script.txt` から、ナレーション・字幕・背景イラスト・BGM 付きの動画を生成する。

```bash
pip install pyopenjtalk-plus numpy pillow   # ffmpeg も必要
python3 build_audio.py   # 音声合成 → out/narration.wav, out/segments.json
python3 scenes.py        # 背景イラスト → out/scenes/*.png
python3 render.py        # 合成 → out/noah_hanabi.mp4
python3 thumbnail.py     # サムネイル → out/thumbnail.png
```

- `script.txt` の `# scene:名前` で背景を、`N|` などの接頭辞で話者(声の高さ・字幕色)を指定する。
- 読み間違いは `build_audio.py` の `READINGS` に追加して直す。

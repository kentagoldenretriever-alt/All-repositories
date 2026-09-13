#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完成サムネを案件フォルダの「中」へ納品する（PNG・PSD・アップ用JPG＋記録）。

使い方:
  /usr/bin/python3 scripts/deliver.py 50 ~/サムネ作業/50/50C.png ~/サムネ作業/50/50C.psd \
      --hint 視察団 --records ~/サムネ作業/50/_eval.md ~/サムネ作業/50/_元ネタ言語化.md
やること:
  <案件フォルダ>/<NO> A.png・<NO> A.psd をコピー
  <案件フォルダ>/<NO> A_アップ用.jpg を JPEG品質 95→92→90→85 で 2MB 未満になるまで保存（YouTube の上限）
  --records は <案件フォルダ>/サムネ/ へコピー
  最後に md5 一致・3点の存在とサイズ・work_root 直下に「<NO> A」の取り残しが無いかを表示
★中間ファイル（中央画像・_run.jsx 等）はコピーしない。渡したファイルだけを運ぶ。
"""
import argparse, hashlib, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, find_case_folder, nfc, norm_no  # noqa: E402

LIMIT = 2 * 1024 * 1024


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("no")
    ap.add_argument("png")
    ap.add_argument("psd")
    ap.add_argument("--hint", default="", help="案件フォルダが複数ある時の指定タイトルの一部")
    ap.add_argument("--records", nargs="*", default=[], help="_eval.md と _元ネタ言語化.md")
    a = ap.parse_args()
    from PIL import Image
    cfg = load_config()
    no = norm_no(a.no)
    png, psd = os.path.expanduser(a.png), os.path.expanduser(a.psd)
    recs = [os.path.expanduser(r) for r in a.records]
    for p, ext in [(png, ".png"), (psd, ".psd")] + [(r, "") for r in recs]:
        if not os.path.isfile(p):
            sys.exit(f"✗ ファイルがありません: {p}")
        if ext and not p.lower().endswith(ext):
            sys.exit(f"✗ {ext} ではありません: {p}")
    im = Image.open(png)
    if im.size != (1280, 720):
        print(f"! PNG が 1280×720 ではありません: {im.size}")
    try:
        F = find_case_folder(no, a.hint, cfg)
    except Exception as e:
        sys.exit(f"✗ {e}")
    print(f"案件フォルダ: {os.path.basename(F)!r}")

    dst_png, dst_psd = os.path.join(F, f"{no} A.png"), os.path.join(F, f"{no} A.psd")
    dst_jpg = os.path.join(F, f"{no} A_アップ用.jpg")
    shutil.copy2(png, dst_png)
    shutil.copy2(psd, dst_psd)
    rgb, q = im.convert("RGB"), None
    for q in (95, 92, 90, 85):
        rgb.save(dst_jpg, quality=q)
        if os.path.getsize(dst_jpg) < LIMIT:
            break
    copied = [(png, dst_png), (psd, dst_psd)]
    if recs:
        os.makedirs(os.path.join(F, "サムネ"), exist_ok=True)
        for r in recs:
            d = os.path.join(F, "サムネ", os.path.basename(r))
            shutil.copy2(r, d)
            copied.append((r, d))

    ng = 0
    print("\n[md5]")
    for s, d in copied:
        ok = md5(s) == md5(d)
        ng += not ok
        print(f"  {'✓' if ok else '✗'} {os.path.relpath(d, F)}")
    print("[3点]")
    for p in (dst_png, dst_psd, dst_jpg):
        ok = os.path.isfile(p) and os.path.getsize(p) > 0
        extra = ""
        if p == dst_jpg and ok:
            under = os.path.getsize(p) < LIMIT
            ok = ok and under
            extra = f" q={q}" + ("" if under else " ★2MB以上（YouTube に上がらない）")
        ng += not ok
        print(f"  {'✓' if ok else '✗'} {os.path.basename(p)} {os.path.getsize(p) if os.path.exists(p) else 0:,}B{extra}")
    left = [n for n in os.listdir(cfg["work_root"]) if nfc(n).startswith(f"{no} A")]
    print("[work_root 直下の取り残し] " + ("なし ✓" if not left else "✗ " + ", ".join(repr(n) for n in left)))
    ng += bool(left)
    print("\n納品OK" if not ng else f"\n✗ {ng} 件の問題あり")
    sys.exit(1 if ng else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""codex で中央画像を1枚生成し、候補画像として回収する（Mac / Windows 共通）。

使い方:
  <python> scripts/gen_image.py <NO> <候補キー> --prompt-file <work_dir>/<NO>/prompt_A.txt [--timeout 900]
  → <work_dir>/<NO>/cand_<候補キー>.png を作る。ログは <work_dir>/<NO>/run_<候補キー>.log

★必ず1件ずつ直列で回す。codex の出力先（~/.codex/generated_images/）は全案件で共通なので、
  2本同時に走らせると他の候補の画像を掴む。
★出力はサブフォルダに入るので、生成開始より新しい PNG を再帰的に探して一番新しい1枚を拾う。
★画像が出ない・時間切れのときは、語を言い換えて再実行する（入浴・子ども等の語、人種などの否定形の指示で止まることがある）。
終了コード：0=成功／1=画像が出なかった／2=時間切れ／3=codex が見つからない
"""
import argparse, glob, os, shutil, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, find_exe  # noqa: E402

SANDBOX = 'sandbox_permissions=["disk-read-cwd","disk-write-cwd","enable-optional-network"]'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("no")
    ap.add_argument("key", help="候補の記号（A/B/C…）")
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()

    cfg = load_config()
    wd = os.path.join(cfg["work_dir"], str(a.no))
    os.makedirs(wd, exist_ok=True)
    prompt = open(os.path.expanduser(a.prompt_file), encoding="utf-8").read().strip()
    codex = cfg["codex_path"]
    if not (codex and os.path.exists(codex)):
        codex = find_exe("codex")
    if not codex:
        print("✗ codex が見つからない（config.json の codex_path を確認）")
        sys.exit(3)

    gen_root = os.path.expanduser("~/.codex/generated_images")
    t0 = time.time()
    log_path = os.path.join(wd, f"run_{a.key}.log")
    print(f"生成開始: NO{a.no} 候補{a.key}（最大{a.timeout}秒）")
    try:
        with open(log_path, "w", encoding="utf-8") as log:
            # ★stdin を閉じて渡す。開いたままだと codex が「Reading additional input from stdin...」で
            #   入力の終わりを待ち続け、画像を作らずに時間切れになる（実際に起きた）
            subprocess.run([codex, "exec", "--skip-git-repo-check", "-c", SANDBOX, prompt],
                           cwd=wd, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                           timeout=a.timeout)
    except subprocess.TimeoutExpired:
        print(f"✗ {a.timeout}秒で終わらなかった → 語を言い換えて再実行（ログ: {log_path}）")
        sys.exit(2)
    time.sleep(8)  # codex はプロセス終了の後に PNG を書き終えることがある
    pngs = [p for p in glob.glob(os.path.join(gen_root, "**", "*.png"), recursive=True)
            if os.path.getmtime(p) >= t0 - 1]
    if not pngs:
        print(f"✗ 画像が出ていない → ログを見て語を言い換えて再実行（ログ: {log_path}）")
        sys.exit(1)
    newest = max(pngs, key=os.path.getmtime)
    dst = os.path.join(wd, f"cand_{a.key}.png")
    shutil.copy2(newest, dst)
    try:
        from PIL import Image
        size = Image.open(dst).size
    except Exception:
        size = "?"
    print(f"✓ {dst}  {size}  （元: {newest}）")
    if len(pngs) > 1:
        print(f"△ 生成開始より新しい画像が{len(pngs)}枚あった＝他の生成と重なった可能性。中身を目で確認する")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""環境チェック：このパソコン（Mac / Windows）でサムネ制作パッケージが動くかを ✓/✗ で表示する。

使い方:
  <python> scripts/check_env.py        （<python>＝config.json の python。Mac=/usr/bin/python3・Windows=python）
終了コード＝✗ の数（0なら全部OK）。✗ には直し方を1行添える。
★work_root に一時ファイルを作って消す＝読み書きできない状態（Mac のフルディスクアクセス切れ等）を検出する。
"""
import glob, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (load_config, resolve_cols, header_pairs, open_sheets, nfc, a1,  # noqa: E402
                    find_exe, IS_WIN)

NG = 0


def show(ok, label, fix=""):
    global NG
    print(("✓ " if ok else "✗ ") + label)
    if not ok:
        NG += 1
        if fix:
            print("    → " + fix)
    return ok


def sh(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        return r.returncode == 0, (r.stdout or r.stderr).strip().splitlines()[0:1]
    except Exception as e:
        return False, [str(e)]


def check_photoshop(cfg):
    app = cfg["photoshop_app"]
    if IS_WIN:
        pats = [os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "Adobe", "Adobe Photoshop*", "Photoshop.exe")]
        hit = sorted(p for pat in pats for p in glob.glob(pat))
        show(bool(hit), f"Photoshop: {hit[-1] if hit else '見つからない'}",
             "Creative Cloud で Photoshop（2025/2026）を入れる")
        ok, out = sh([sys.executable, "-c", "import win32com.client; print('ok')"])
        show(ok, "pywin32（Photoshop を COM で動かす）", "python -m pip install --user pywin32")
    else:
        cands = [f"/Applications/{app}.app", f"/Applications/{app}/{app}.app"]
        hit = [p for p in cands if os.path.exists(p)]
        show(bool(hit), f"Photoshop: {hit[0] if hit else app}",
             "Creative Cloud で Photoshop を入れ、config.json の photoshop_app をアプリ名に合わせる（ls /Applications | grep -i photoshop）")


def main():
    cfg = load_config()
    py = cfg.get("python") or ("python" if IS_WIN else "/usr/bin/python3")
    ok, out = sh([py, "--version"])
    show(ok, f"python（{py}）: {out[0] if out else '無し'}",
         "python.org から Python 3.10 以上を入れ、config.json の python を直す" if IS_WIN
         else "Xcode Command Line Tools を入れる: xcode-select --install")
    for mod, pipname in (("PIL", "Pillow"), ("gspread", "gspread")):
        ok, out = sh([py, "-c", f"import {mod}; print({mod}.__version__)"])
        show(ok, f"{pipname} import: {out[0] if ok and out else '失敗'}", f"{py} -m pip install --user {pipname}")
    y = find_exe("yt-dlp")
    ok, out = sh([y, "--version"]) if y else (False, [])
    show(ok, f"yt-dlp: {out[0] if ok and out else '無し'}",
         f"{py} -m pip install --user yt-dlp（または winget install yt-dlp）" if IS_WIN else "brew install yt-dlp")
    cx = cfg["codex_path"]
    ok = bool(cx) and (os.path.exists(cx) or bool(find_exe(os.path.basename(cx))))
    if ok:
        ok, out = sh([cx, "--version"])
    show(ok, f"codex: {cx or '無し'}",
         "Node.js を入れて npm install -g @openai/codex → codex login（ChatGPTでログイン）。config.json の codex_path を codex に" if IS_WIN
         else "ChatGPT.app を入れてログインし、config.json の codex_path を実在パスに")
    check_photoshop(cfg)
    t = cfg["template_psd"]
    show(os.path.exists(t), f"テンプレPSD: {t}", "assets/ にテンプレPSDを置くか template_psd を直す")

    wr = cfg["work_root"]
    if show(bool(wr) and os.path.isdir(wr), f"work_root: {wr}",
            "Google Drive for desktop を起動して同期し、config.json の work_root を実在パスに"):
        try:
            os.listdir(wr)
            fd, p = tempfile.mkstemp(prefix=".check_env_", dir=wr)
            os.close(fd)
            os.remove(p)
            show(True, "work_root 読み書き")
        except Exception as e:
            show(False, f"work_root 読み書き: {e}",
                 "共有の権限（編集者）を確認" if IS_WIN else
                 "システム設定 > プライバシーとセキュリティ > フルディスクアクセス で Claude／ターミナルをON")
    try:
        os.makedirs(cfg["work_dir"], exist_ok=True)
        show(True, f"work_dir: {cfg['work_dir']}")
    except Exception as e:
        show(False, f"work_dir 作成: {e}", "config.json の work_dir を書き込める場所に")

    s = cfg["sheet"]
    if not s.get("enabled"):
        print("- シート連携は無効（sheet.enabled=false）")
    elif show(os.path.exists(s["service_account_json"]), f"サービスアカウント鍵: {s['service_account_json']}",
              "鍵JSONを置き、sheet.service_account_json を直す（作り方は SETUP.md 手順3）"):
        try:
            main_ws, res_ws = open_sheets(cfg)
            vals = main_ws.get_all_values()
            show(True, f"管理シート: 「{main_ws.title}」{len(vals)}行")
            found, missing = resolve_cols(main_ws, cfg, values=vals, strict=False)
            for k, c in found.items():
                show(True, f"列 {k} {s[k]} → {a1(c)}列")
            for k, sec, name in missing:
                show(False, f"列 {k} ({sec or '節問わず'}, {name}) が見つからない",
                     "config.json の sheet." + k + " を下の実在見出しに合わせる")
            if missing:
                print("    実在の見出し: " + " | ".join(
                    f"{a1(c)}:{sc}/{n}" for c, sc, n in header_pairs(main_ws, cfg, vals) if n))
            rh = res_ws.row_values(int(s["research_header_row"]))
            names = [nfc(x) for x in rh]
            for k in ("research_col_no", "research_col_source_url", "research_col_title"):
                show(nfc(s[k]) in names, f"リサーチ列 {k}「{s[k]}」",
                     "実在の見出し: " + " | ".join(n for n in names if n))
        except Exception as e:
            show(False, f"シートを開けない: {type(e).__name__}: {e}",
                 "鍵のメール(...iam.gserviceaccount.com)を管理シートに編集者で共有／ID・gidを確認")
    print(f"\n✗ {NG} 件")
    sys.exit(NG)


if __name__ == "__main__":
    main()

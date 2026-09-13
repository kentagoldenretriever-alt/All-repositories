#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""外注パック共通ヘルパー（設定・パス・案件フォルダ・シート・yt-dlp 実行）。画像系は imgutil.py。

他のスクリプトから import して使う。単体では動かさない。
  from common import load_config, pkg_path, nfc, find_case_folder, open_sheets, resolve_cols

★個人のパス・ID・シートIDは一切書かない。全部 PKG/config.json から読む。
★Google Drive のファイル名は NFD のことがある → 名前の照合は必ず nfc() を通す。
★フォルダ名に改行が入ることがある → os.listdir で扱い、表示は repr()。
"""
import copy, glob, json, os, shutil, subprocess, sys, unicodedata

IS_WIN = sys.platform.startswith("win")

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULTS = {
    "channel_name": "", "channel_id": "", "work_root": "", "work_dir": "~/サムネ作業",
    "template_psd": "assets/サムネ テンプレ.psd", "photoshop_app": "Adobe Photoshop 2026",
    # ★テンプレの役割（どのレイヤーが何か）と実測値。既定は同梱テンプレの値。
    #   チャンネルのテンプレに替えたら、セットアップで inspect_template.py を回して書き換える。
    "template": {
        "lines": [{"layer": "1行目", "width": 1306, "left": -14},
                  {"layer": "2行目", "width": 1306, "left": -14},
                  {"layer": "3行目", "width": 1306, "left": -14}],
        "bg_layer": {"layer": "3839385_s"}, "flag_layer": {"layer": "2239915"},
        "mark_layer": {"layer": "挿入", "pick": "narrow"}, "speech_layer": {"layer": "挿入", "pick": "wide"},
        "arrow_layer": {"layer": "矢印"}, "ellipse_layer": {"layer": "楕円"},
        "tracking_min": -200, "band": [145, 491], "arrow_rot0": "↖",
        "chars": {"l1_max": 18, "l2": [20, 22], "l3": [13, 14], "l3_max": 14},
    },
    "codex_path": "codex" if IS_WIN else "/Applications/ChatGPT.app/Contents/Resources/codex",
    "python": "python" if IS_WIN else "/usr/bin/python3",
    "own_threshold_views": 10000,
    "sheet": {
        "enabled": True, "service_account_json": "", "spreadsheet_id": "", "main_gid": 0,
        "section_header_row": 1, "name_header_row": 2,
        "col_no": ["", "No."], "col_title": ["作業フォルダ", "タイトル"],
        "col_done": ["サムネイル", "完了日"], "col_check": ["サムネイル", "チェック"],
        "top_rows": 10, "research_gid": 0, "research_header_row": 2,
        "research_col_no": "No", "research_col_source_url": "参考URL",
        "research_col_title": "指定タイトル",
    },
    "schedule": {"cron": "0 0 * * *", "max_cases_per_run": 10},
    "scoring": {"max_rounds": None},
}
COL_KEYS = ("col_no", "col_title", "col_done", "col_check")


def nfc(s):
    return unicodedata.normalize("NFC", str(s or "")).strip()


def pkg_path(rel):
    """~ を展開し、相対パスは PKG 起点で絶対パスにする。空文字はそのまま返す。"""
    if not rel:
        return ""
    p = os.path.expanduser(str(rel))
    return p if os.path.isabs(p) else os.path.join(PKG, p)


def _merge(base, over):
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge(base[k], v)
        else:
            base[k] = v
    return base


def load_config(required=True):
    """PKG/config.json を読み、既定値で穴埋めしてパスを解決して返す。
    required=False なら config.json が無くても既定値だけで返す（画像だけ扱うスクリプト用）。"""
    path = os.path.join(PKG, "config.json")
    cfg = copy.deepcopy(DEFAULTS)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            _merge(cfg, json.load(f))
        cfg["_loaded"] = True
    elif required:
        sys.exit(f"✗ 設定ファイルがありません: {path}\n"
                 f"  {os.path.join(PKG, 'config.example.json')} をコピーして config.json を作り、"
                 "channel_id・work_root・sheet の各値を自分の環境に書き換えてください。")
    else:
        cfg["_loaded"] = False
    for k in ("work_root", "work_dir", "template_psd"):
        cfg[k] = pkg_path(cfg.get(k))
    cx = str(cfg.get("codex_path") or "")
    cfg["codex_path"] = pkg_path(cx) if ("/" in cx or "\\" in cx) else (find_exe(cx) or cx)
    cfg["sheet"]["service_account_json"] = pkg_path(cfg["sheet"].get("service_account_json"))
    return cfg


def norm_no(no):
    s = nfc(no)
    return str(int(s)) if s.isdigit() else s


def _lcs(a, b):
    """最長共通部分文字列の長さ（hint が部分的にしか一致しない時の予備）。"""
    best, prev = 0, [0] * (len(b) + 1)
    for ca in a:
        cur = [0] * (len(b) + 1)
        for j, cb in enumerate(b):
            if ca == cb:
                cur[j + 1] = prev[j] + 1
                best = max(best, cur[j + 1])
        prev = cur
    return best


def find_case_folder(no, hint="", cfg=None):
    """work_root 直下で NFC 名が f"{no}_" で始まるディレクトリの絶対パス。決まらなければ例外。"""
    cfg = cfg or load_config()
    root = cfg["work_root"]
    if not os.path.isdir(root):
        raise FileNotFoundError(f"work_root がありません: {root}")
    pre = norm_no(no) + "_"
    cands = [n for n in os.listdir(root)
             if nfc(n).startswith(pre) and os.path.isdir(os.path.join(root, n))]
    if len(cands) == 1:
        return os.path.join(root, cands[0])
    if not cands:
        raise LookupError(f"「{pre}」で始まる案件フォルダが work_root 直下にありません")
    h = nfc(hint)
    if h:
        hit = [n for n in cands if h in nfc(n)]
        if len(hit) == 1:
            return os.path.join(root, hit[0])
        if not hit:
            sc = sorted(((_lcs(h, nfc(n)), n) for n in cands), reverse=True)
            if sc[0][0] >= 3 and sc[0][0] > sc[1][0]:
                return os.path.join(root, sc[0][1])
    raise LookupError("案件フォルダが1つに決まりません（--hint に指定タイトルの一部を）: "
                      + " / ".join(repr(n) for n in cands))


def open_sheets(cfg=None):
    """service account で開いて (main_ws, research_ws) を返す。"""
    import gspread
    cfg = cfg or load_config()
    s = cfg["sheet"]
    gc = gspread.service_account(filename=s["service_account_json"])
    sh = gc.open_by_key(s["spreadsheet_id"])
    return sh.get_worksheet_by_id(int(s["main_gid"])), sh.get_worksheet_by_id(int(s["research_gid"]))


def header_pairs(ws, cfg, values=None):
    """[(列番号, 節, 列名)]。節は結合セルなので左端の値を右へ引き継ぐ。"""
    s = cfg["sheet"]
    vals = values if values is not None else ws.get_all_values()
    r1 = vals[s["section_header_row"] - 1] if len(vals) >= s["section_header_row"] else []
    r2 = vals[s["name_header_row"] - 1] if len(vals) >= s["name_header_row"] else []
    out, sec = [], ""
    for c in range(max(len(r1), len(r2))):
        if c < len(r1) and nfc(r1[c]):
            sec = nfc(r1[c])
        out.append((c + 1, sec, nfc(r2[c]) if c < len(r2) else ""))
    return out


def resolve_cols(ws, cfg, values=None, strict=True):
    """設定の (節, 列名) を列番号(1始まり)に解決して {"col_no": 1, ...} で返す。
    節が "" なら節を問わず列名だけで一致。strict=False なら (found, missing) を返す。"""
    pairs = header_pairs(ws, cfg, values)
    found, missing = {}, []
    for key in COL_KEYS:
        sec, name = (nfc(x) for x in cfg["sheet"][key])
        hit = [c for c, s_, n in pairs if n == name and (not sec or s_ == sec)]
        if hit:
            found[key] = hit[0]
        else:
            missing.append((key, sec, name))
    if not strict:
        return found, missing
    if missing:
        heads = " | ".join(f"{a1(c)}:{s_}/{n}" for c, s_, n in pairs if n)
        raise KeyError(f"見出しが見つかりません: {missing}\n  実在の見出し: {heads}")
    return found


def a1(n):
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def cell(row, col):
    return nfc(row[col - 1]) if 0 < col <= len(row) else ""


# ---------- 実行ファイルの探索と yt-dlp 実行（画像系は imgutil.py） ----------
def find_exe(name):
    """PATH から探し、無ければ OS ごとのよくある場所を探す（定期実行では PATH が細いことがある）。"""
    p = shutil.which(name)
    if p:
        return p
    if IS_WIN:
        appdata, local = os.environ.get("APPDATA", ""), os.environ.get("LOCALAPPDATA", "")
        pats = [os.path.join(appdata, "npm", name + ".cmd"),
                os.path.join(appdata, "Python", "Python3*", "Scripts", name + ".exe"),
                os.path.join(local, "Programs", "Python", "Python3*", "Scripts", name + ".exe"),
                os.path.join(local, "Microsoft", "WinGet", "Links", name + ".exe")]
    else:
        pats = [f"/opt/homebrew/bin/{name}", f"/usr/local/bin/{name}",
                os.path.expanduser(f"~/Library/Python/3.*/bin/{name}")]
    for pat in pats:
        hit = sorted(glob.glob(pat))
        if hit:
            return hit[-1]
    return ""


def run(cmd, timeout=300):
    """yt-dlp は実体を探して呼び、出力は UTF-8 で受ける（Windows の既定は cp932 で文字化けする）。"""
    cmd = list(cmd)
    if cmd and cmd[0] == "yt-dlp":
        cmd[0] = find_exe("yt-dlp") or "yt-dlp"
        cmd[1:1] = ["--encoding", "utf-8"]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout, env=env)
    return r.returncode, r.stdout, r.stderr


def to_int(s):
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None

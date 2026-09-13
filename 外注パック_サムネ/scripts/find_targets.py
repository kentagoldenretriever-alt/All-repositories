#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""今日のサムネ対象案件を管理シートから拾って JSON で出す。

使い方:
  /usr/bin/python3 scripts/find_targets.py            # 対象を全部
  /usr/bin/python3 scripts/find_targets.py --limit 3  # 上から3件
対象＝見出しより下の先頭 top_rows 行のうち、No が入っていて「サムネイル/完了日」が空の行（上から順）。
出力: [{row, no, title, source_url, designated_title, case_folder, case_folder_error}]
★行番号は人の行挿入でずれる。毎回シートを読み直す（キャッシュしない）。書き込み前に write_done.py が再照合する。
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, open_sheets, resolve_cols, find_case_folder, nfc, cell, norm_no  # noqa: E402


def research_map(ws, cfg):
    """リサーチシート：No(int) → (参考URL, 指定タイトル)。No は "0046" のような0埋めがある。"""
    s = cfg["sheet"]
    vals = ws.get_all_values()
    hr = int(s["research_header_row"])
    if len(vals) < hr:
        return {}
    heads = [nfc(x) for x in vals[hr - 1]]

    def col(name):
        name = nfc(name)
        if name not in heads:
            raise KeyError(f"リサーチシートに列「{name}」がありません。実在: {[h for h in heads if h]}")
        return heads.index(name) + 1

    cn, cu, ct = col(s["research_col_no"]), col(s["research_col_source_url"]), col(s["research_col_title"])
    out = {}
    for row in vals[hr:]:
        no = norm_no(cell(row, cn))
        if no.isdigit() and int(no) not in out:
            out[int(no)] = (cell(row, cu), cell(row, ct))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    cfg = load_config()
    s = cfg["sheet"]
    if not s.get("enabled"):
        sys.exit("✗ sheet.enabled が false です（シート連携なしでは対象を拾えません）")
    main_ws, res_ws = open_sheets(cfg)
    vals = main_ws.get_all_values()
    cols = resolve_cols(main_ws, cfg, values=vals)
    rmap = research_map(res_ws, cfg)
    start = max(int(s["section_header_row"]), int(s["name_header_row"]))
    out = []
    for i in range(start, min(len(vals), start + int(s["top_rows"]))):
        row = vals[i]
        no = norm_no(cell(row, cols["col_no"]))
        if not no or cell(row, cols["col_done"]):
            continue
        title = cell(row, cols["col_title"])
        url, dtitle = rmap.get(int(no), ("", "")) if no.isdigit() else ("", "")
        folder, err = "", ""
        for hint in (title, dtitle, ""):
            try:
                folder = find_case_folder(no, hint, cfg)
                err = ""
                break
            except Exception as e:
                err = str(e)
        out.append({"row": i + 1, "no": no, "title": title, "source_url": url,
                    "designated_title": dtitle, "case_folder": folder, "case_folder_error": err})
        if a.limit and len(out) >= a.limit:
            break
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管理シートの「サムネイル/完了日」に日付を書く（採点ループが終わってから）。

使い方:
  /usr/bin/python3 scripts/write_done.py 50              # 今日を M/D で
  /usr/bin/python3 scripts/write_done.py 50 --date 9/12
  /usr/bin/python3 scripts/write_done.py 50 --check      # 人に指示された時だけ：チェック欄にも ✓(True)
やること:
  見出しより下の先頭 top_rows 行から No の行を探す（1行に絞れなければ中止）
  完了日が空なら書く。★既に値があれば書かずに中止（上書きしない）
  --check を付けた時だけ「サムネイル/チェック」に True（boolean）を書く。付けなければ絶対に触らない
  書いた後に行を読み返して「行・セル番地・値」を表示
★行番号は人の行挿入でずれる。find_targets.py の行番号は使わず、ここで毎回 No で引き直す。
"""
import argparse, datetime, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, open_sheets, resolve_cols, cell, norm_no, a1  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("no")
    ap.add_argument("--date", default="", help="M/D（省略時は今日）")
    ap.add_argument("--check", action="store_true", help="チェック欄に True を書く（人の指示がある時だけ）")
    a = ap.parse_args()
    cfg = load_config()
    s = cfg["sheet"]
    if not s.get("enabled"):
        sys.exit("✗ sheet.enabled が false です")
    no = norm_no(a.no)
    t = datetime.date.today()
    date = a.date.strip() or f"{t.month}/{t.day}"

    ws, _ = open_sheets(cfg)
    vals = ws.get_all_values()
    cols = resolve_cols(ws, cfg, values=vals)
    start = max(int(s["section_header_row"]), int(s["name_header_row"]))
    hits = [i + 1 for i in range(start, min(len(vals), start + int(s["top_rows"])))
            if norm_no(cell(vals[i], cols["col_no"])) == no]
    if len(hits) != 1:
        sys.exit(f"✗ 先頭{s['top_rows']}行で No={no} の行が {len(hits)} 件（{hits}）→ 中止。シートを目で確認して")
    row = hits[0]
    cd, cc = cols["col_done"], cols["col_check"]
    cur = cell(vals[row - 1], cd)
    if cur:
        sys.exit(f"✗ {a1(cd)}{row} に既に「{cur}」がある → 書かずに中止（上書きしない）")

    ws.update_cell(row, cd, date)
    if a.check:
        ws.update_cell(row, cc, True)

    back = ws.row_values(row)
    title = cell(back, cols["col_title"])
    print(f"行 {row}（No={cell(back, cols['col_no'])} {title[:30]}）")
    print(f"  完了日 {a1(cd)}{row} = {cell(back, cd)!r}" + ("" if cell(back, cd) else "  ✗ 読み返しで空"))
    if a.check:
        print(f"  チェック {a1(cc)}{row} = {cell(back, cc)!r}")
    else:
        print(f"  チェック {a1(cc)}{row} は触っていない（現在 {cell(back, cc)!r}）")
    if not cell(back, cd):
        sys.exit(1)


if __name__ == "__main__":
    main()

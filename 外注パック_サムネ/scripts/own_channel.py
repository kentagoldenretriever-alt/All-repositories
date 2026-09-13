#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自社チャンネルの実績を集める（公開本数・中央値・最大・閾値以上の一覧とサムネ・色レンジ）。

使い方:
  /usr/bin/python3 scripts/own_channel.py
出力（work_dir/_channel/）:
  channel_stats.md       公開本数・中央値・最大・own_threshold_views 以上の本数と一覧
  own_videos.json        全動画 [{id, views, title}]（再生順）＋登録者数（fetch_refs.py が読む）
  own/<id>.jpg           閾値以上の動画のサムネ
  own_sheet.jpg          480×270・5列の一覧（各タイルの下に再生数）
  own_color_range.json   再生上位5本のサムネの 明るさ/彩度/白飛び/R−B の最小〜最大（color_check.py が読む）
YouTube Data API は使わない（yt-dlp とサムネ画像URLだけ）。
"""
import datetime, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, run, to_int  # noqa: E402
from imgutil import fetch_thumb, tile_sheet, color_metrics  # noqa: E402


def main():
    cfg = load_config()
    cid = cfg["channel_id"]
    if not cid:
        sys.exit("✗ config.json の channel_id が空です")
    th = int(cfg["own_threshold_views"])
    base = os.path.join(cfg["work_dir"], "_channel")
    own = os.path.join(base, "own")
    os.makedirs(own, exist_ok=True)
    url = f"https://www.youtube.com/channel/{cid}/videos"
    rc, out, err = run(["yt-dlp", "--flat-playlist", "--print", "%(id)s|%(view_count)s|%(title)s", url], 900)
    vids = []
    for ln in out.splitlines():
        p = ln.split("|", 2)
        if len(p) == 3 and p[0]:
            vids.append({"id": p[0], "views": to_int(p[1]), "title": p[2]})
    if not vids:
        sys.exit(f"✗ アップロード一覧を取れませんでした（yt-dlp rc={rc}）: {err.strip()[-300:]}")
    vids.sort(key=lambda v: v["views"] or 0, reverse=True)
    vs = [v["views"] for v in vids if v["views"] is not None]
    hits = [v for v in vids if (v["views"] or 0) >= th]

    rc, o2, _ = run(["yt-dlp", "--skip-download", "--print", "%(channel_follower_count)s",
                     f"https://www.youtube.com/watch?v={vids[0]['id']}"], 120)
    subs = to_int(o2.strip().splitlines()[-1]) if o2.strip() else None

    with open(os.path.join(base, "own_videos.json"), "w", encoding="utf-8") as f:
        json.dump({"channel_id": cid, "subscribers": subs, "videos": vids}, f, ensure_ascii=False, indent=1)

    med = statistics.median(vs) if vs else 0
    lines = [f"# {cfg['channel_name'] or cid} 実績（{datetime.date.today()}）", "",
             f"- 公開本数: {len(vids)}", f"- 登録者数: {subs if subs is not None else '不明'}",
             f"- 再生の中央値: {med:,.0f}", f"- 最大: {max(vs) if vs else 0:,}",
             f"- {th:,}回以上: {len(hits)}本", "", "| # | 再生 | 題名 | ID |", "|---|---:|---|---|"]
    lines += [f"| {i} | {v['views']:,} | {v['title']} | {v['id']} |" for i, v in enumerate(hits, 1)]
    with open(os.path.join(base, "channel_stats.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    tiles, miss = [], []
    for v in hits:
        p = os.path.join(own, f"{v['id']}.jpg")
        if fetch_thumb(v["id"], p):
            tiles.append((p, f"{v['views']:,}回"))
        else:
            miss.append(v["id"])
    if tiles:
        tile_sheet(tiles, os.path.join(base, "own_sheet.jpg"))

    from PIL import Image
    ms, used = [], []
    for v in vids[:5]:
        p = os.path.join(own, f"{v['id']}.jpg")
        if fetch_thumb(v["id"], p):
            ms.append(color_metrics(Image.open(p)))
            used.append(v["id"])
    rng = {k: [min(m[k] for m in ms), max(m[k] for m in ms)] for k in ms[0]} if ms else {}
    rng.update({"videos": used, "measured_at": str(datetime.date.today())})
    with open(os.path.join(base, "own_color_range.json"), "w", encoding="utf-8") as f:
        json.dump(rng, f, ensure_ascii=False, indent=1)

    print(f"公開 {len(vids)}本／中央値 {med:,.0f}／最大 {max(vs) if vs else 0:,}／{th:,}以上 {len(hits)}本")
    print(f"サムネ保存 {len(tiles)}枚" + (f"（取れず {len(miss)}: {', '.join(miss)}）" if miss else ""))
    print(f"色レンジ（上位{len(used)}本）: " + ", ".join(f"{k}={v}" for k, v in rng.items() if k not in ("videos", "measured_at")))
    print(f"出力: {base}")


if __name__ == "__main__":
    main()

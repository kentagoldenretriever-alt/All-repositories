#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""元ネタと他社の参考サムネを集め、拡散率（再生÷登録）付きの一覧を作る。

使い方:
  /usr/bin/python3 scripts/fetch_refs.py 50 --url "https://www.youtube.com/watch?v=XXXX" \
      --q "海外の反応 日本 視察団" --q "外国人 驚愕 日本" --must 反応
出力（work_dir/<NO>/）:
  src.jpg / source.json   元ネタのサムネ・oembed(author_name,title)・再生/登録/公開日/channel_id
  rivals.json             検索結果（--must を含む題名だけ・重複除去）。再生上位8本は登録者数と拡散率（≥3 に mark）
                          元ネタと同じチャンネルは self=true
  r_<id>.jpg              上位8本のサムネ
  ref_sheet.jpg           480×270・5列×2段。上段＝元ネタ＋拡散率≥3の他社（拡散率順）
                          下段＝自社一覧（own_channel.py の出力）の上位＋残りの参考
YouTube Data API は使わない（yt-dlp・oembed・サムネ画像URLだけ）。
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, run, to_int, nfc, norm_no  # noqa: E402
from imgutil import fetch_thumb, tile_sheet  # noqa: E402


def vid_of(url):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/live/|/embed/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None


def meta(vid):
    """yt-dlp で 再生・登録・公開日・channel_id。"""
    rc, out, err = run(["yt-dlp", "--skip-download", "--print",
                        "%(view_count)s|%(channel_follower_count)s|%(upload_date)s|%(channel_id)s",
                        f"https://www.youtube.com/watch?v={vid}"], 120)
    p = (out.strip().splitlines() or [""])[-1].split("|")
    if len(p) < 4:
        print(f"  ! {vid} のメタ取得失敗: {err.strip()[-200:]}")
        return {}
    return {"view_count": to_int(p[0]), "channel_follower_count": to_int(p[1]),
            "upload_date": p[2] if p[2] != "NA" else "", "channel_id": p[3] if p[3] != "NA" else ""}


def ratio(v, s):
    return round(v / s, 2) if v and s else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("no")
    ap.add_argument("--url", required=True, help="元ネタの動画URL")
    ap.add_argument("--q", action="append", required=True, help="検索語（複数可）")
    ap.add_argument("--must", default="", help="題名にこの語を含むものだけ残す")
    a = ap.parse_args()
    cfg = load_config()
    out = os.path.join(cfg["work_dir"], norm_no(a.no))
    os.makedirs(out, exist_ok=True)

    sid = vid_of(a.url)
    if not sid:
        sys.exit(f"✗ URL から動画IDを読めません: {a.url}")
    src = {"url": a.url, "id": sid}
    try:
        q = urllib.parse.urlencode({"url": f"https://www.youtube.com/watch?v={sid}", "format": "json"})
        with urllib.request.urlopen("https://www.youtube.com/oembed?" + q, timeout=30) as r:
            o = json.load(r)
        src.update(author_name=o.get("author_name", ""), title=o.get("title", ""))
    except Exception as e:
        print(f"  ! oembed 失敗: {e}")
    src.update(meta(sid))
    src["ratio"] = ratio(src.get("view_count"), src.get("channel_follower_count"))
    src_jpg = os.path.join(out, "src.jpg")
    if not fetch_thumb(sid, src_jpg):
        print("  ! 元ネタのサムネを取れませんでした")
    with open(os.path.join(out, "source.json"), "w", encoding="utf-8") as f:
        json.dump(src, f, ensure_ascii=False, indent=1)
    print(f"元ネタ: {src.get('author_name', '?')}「{src.get('title', '?')}」 再生{src.get('view_count')} "
          f"登録{src.get('channel_follower_count')} 拡散率{src['ratio']}")

    seen, rivals, must = {sid}, [], nfc(a.must)
    for kw in a.q:
        rc, o, err = run(["yt-dlp", "--flat-playlist", "--print",
                          "%(view_count)s|%(channel_id)s|%(channel)s|%(id)s|%(title)s", f"ytsearch12:{kw}"], 300)
        if rc != 0 and not o:
            print(f"  ! 検索失敗「{kw}」: {err.strip()[-200:]}")
        for ln in o.splitlines():
            p = ln.split("|", 4)
            if len(p) < 5 or p[3] in seen or (must and must not in nfc(p[4])):
                continue
            seen.add(p[3])
            rivals.append({"id": p[3], "url": f"https://www.youtube.com/watch?v={p[3]}", "title": p[4],
                           "channel": p[2], "channel_id": p[1], "view_count": to_int(p[0]),
                           "subscribers": None, "ratio": None, "mark": False,
                           "self": bool(src.get("channel_id")) and p[1] == src.get("channel_id"), "query": kw})
    rivals.sort(key=lambda r: r["view_count"] or 0, reverse=True)
    subs_cache = {}
    for r in rivals[:8]:
        if r["channel_id"] not in subs_cache:
            subs_cache[r["channel_id"]] = meta(r["id"]).get("channel_follower_count")
        r["subscribers"] = subs_cache[r["channel_id"]]
        r["ratio"] = ratio(r["view_count"], r["subscribers"])
        r["mark"] = (r["ratio"] or 0) >= 3
        r["thumb"] = os.path.join(out, f"r_{r['id']}.jpg")
        if not fetch_thumb(r["id"], r["thumb"]):
            r["thumb"] = ""
    with open(os.path.join(out, "rivals.json"), "w", encoding="utf-8") as f:
        json.dump(rivals, f, ensure_ascii=False, indent=1)

    top = [r for r in rivals[:8] if r["mark"] and not r["self"] and r.get("thumb")]
    top.sort(key=lambda r: r["ratio"], reverse=True)
    top = top[:4]
    rest = [r for r in rivals[:8] if r not in top and r.get("thumb")]
    lab = lambda n, x: f"{n} {x:.1f}倍" if x else f"{n} -"  # noqa: E731
    row1 = [(src_jpg, lab("元ネタ " + src.get("author_name", ""), src["ratio"]))]
    row1 += [(r["thumb"], lab(r["channel"], r["ratio"])) for r in top]
    row1 += [(None, "")] * (5 - len(row1))
    row2 = []
    ownj = os.path.join(cfg["work_dir"], "_channel", "own_videos.json")
    if os.path.exists(ownj):
        with open(ownj, encoding="utf-8") as f:
            od = json.load(f)
        for v in od.get("videos", []):
            p = os.path.join(cfg["work_dir"], "_channel", "own", f"{v['id']}.jpg")
            if os.path.exists(p) and len(row2) < 3:
                row2.append((p, lab("自社", ratio(v["views"], od.get("subscribers")))))
    else:
        print("  ! 自社一覧が無い（先に own_channel.py を回す）→ 下段は参考だけ")
    for r in rest:
        if len(row2) >= 5:
            break
        row2.append((r["thumb"], lab(("自社 " if r["self"] else "") + r["channel"], r["ratio"])))
    tile_sheet(row1 + row2, os.path.join(out, "ref_sheet.jpg"))
    print(f"他社候補 {len(rivals)}本（登録者を引いた上位 {min(8, len(rivals))}本・拡散率≥3: "
          f"{sum(r['mark'] for r in rivals)}本）")
    for r in rivals[:8]:
        print(f"  {'★' if r['mark'] else ' '}{'[自]' if r['self'] else ''} {r['ratio']}倍 "
              f"{r['view_count']}回 {r['channel']}「{r['title'][:40]}」")
    print(f"出力: {out}")


if __name__ == "__main__":
    main()

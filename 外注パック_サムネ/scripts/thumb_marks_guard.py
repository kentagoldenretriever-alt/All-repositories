#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""サムネの記号・小セリフ・矢印を「合成する前に」機械的に止めるゲート。

★なぜコードなのか
  同じ3つの欠陥を何度も出した（過去に6本まとめて再発した）：
    ① !? が毎回まったく同じ場所（実測：6本とも x62-95 / y185-250）＝一覧で量産に見える
    ② 小セリフが話者の顔・手に重なる
    ③ 矢印の向きが人物の視線と食い違う（逆向き・目線の高さから外れている）
  どれも「ルールとしては知っていた」。文書に書き足しても使われないので
  、**render() を呼ぶ前に必ず通る関数**にした。

★使い方（thumb_psd_compose.render の直前で必ず呼ぶ）
    import thumb_marks_guard as G
    G.guard(no="131", ch="main",
            face=(400,150,620,420),      # 話者の顔bbox（最終1280x720キャンバス上）※必須
            gaze="right",                # left|right|up|down|camera ※必須
            mq=(72,190,85,85,-18),
            ar=(1000,455,165,165,90),
            small="あの人、何を…！？", ms=(620,315,105,105,0))
    → 違反があれば MarksError を投げて止まる。通れば !? の座標を履歴に記録する。

  ★face と gaze は**必須の引数**。ここに数字を書くには実物を開いて見るしかない。
    「見たつもり」で通り抜けられないようにするのが目的。

★合成の“あと”は verify() を呼ぶ。記号まわりを4倍に切り出した検品画像を書き出すので、
  納品前にこれを必ず開く（数値が範囲内でも絵が悪ければ絵が正しい）。
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config  # noqa: E402

# ★テンプレごとの値は config.json の template から読む（セットアップで実測して書く）
_TP = load_config(required=False)["template"]
CANVAS = (1280, 720)
BAND_TOP, BAND_BOTTOM = _TP["band"]   # 写真が見える帯（上＝1行目の黒フチの下端／下＝2行目の帯の上端）
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "_marks_log.json")

# 矢印素材の rot=0 のときの向き（同梱テンプレは ↖）。rot は時計回り
# （同梱テンプレの実測＝0:↖ 90:↗ 135:→ 180:↘ 270:↙ 315:←）
_DIRS = {"↖": (-1, -1), "↑": (0, -1), "↗": (1, -1), "→": (1, 0),
         "↘": (1, 1), "↓": (0, 1), "↙": (-1, 1), "←": (-1, 0)}
_BASE = tuple(float(v) for v in _DIRS.get(_TP.get("arrow_rot0", "↖"), (-1, -1)))
GAZE_VEC = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}


class MarksError(Exception):
    pass


def _rot(v, deg):
    t = math.radians(deg)
    return (v[0] * math.cos(t) - v[1] * math.sin(t),
            v[0] * math.sin(t) + v[1] * math.cos(t))


def arrow_dir(rot):
    v = _rot(_BASE, rot)
    n = math.hypot(*v) or 1
    return (v[0] / n, v[1] / n)


def arrow_tip(ar):
    """矢印の先端のだいたいの座標。ar=(x,y,sx,sy,rot)。素材は約130pxなので半分を先端までとみなす。"""
    x, y, sx = ar[0], ar[1], ar[2]
    d = arrow_dir(ar[4] if len(ar) >= 5 else 0)
    r = 65.0 * (sx / 165.0)
    return (x + d[0] * r, y + d[1] * r)


def speech_box(text, ms):
    """小セリフの外接矩形。実測から 1文字 ≒ 0.34*scale、高さ ≒ 0.38*scale。"""
    x, y, sc = ms[0], ms[1], ms[2]
    w = max(1, len(text)) * 0.34 * sc
    h = 0.38 * sc
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def _inter(a, b, pad=0):
    return not (a[2] + pad < b[0] or b[2] < a[0] - pad or
                a[3] + pad < b[1] or b[3] < a[1] - pad)


def cell(x, y):
    """画面を3x3に割ったマス。(列,行) で 0..2。"""
    return (min(2, int(x / (CANVAS[0] / 3))), min(2, int(y / (CANVAS[1] / 3))))


def _off(t):
    return t is None or (len(t) >= 2 and t[0] < 0 and t[1] < 0)


def _load():
    try:
        return json.load(open(LOG, encoding="utf-8"))
    except Exception:
        return {}


def guard(no, ch, face, gaze, mouth=None, target=None, mq=None, ar=None, el=None, ms=None, small="",
          ms2=None, small2="", flag=None, allow_camera_gaze=False, record=True):
    """× があれば MarksError。△ は戻り値のリストで返す。"""
    errs, warns = [], []
    if face is None or len(face) != 4:
        raise MarksError("face（話者の顔bbox）は必須。実物を開いて座標を測ってから渡す。")
    if gaze not in list(GAZE_VEC) + ["camera"]:
        raise MarksError("gaze は left/right/up/down/camera のどれか。実物を見て決める。")
    if (small and not _off(ms)) and (mouth is None or len(mouth) != 2):
        raise MarksError("小セリフを置くなら mouth=(x,y)（話者の口の座標）が必須。実物を開いて測る。")
    if not _off(ar) and (target is None or len(target) != 4):
        raise MarksError("矢印を置くなら target=(x1,y1,x2,y2)（矢印が指す対象のbbox）が必須。実物を開いて測る。")

    # ① 小セリフが顔（と手）に掛かっていないか
    for txt, m, name in ((small, ms, "小セリフ1"), (small2, ms2, "小セリフ2")):
        if not txt or _off(m):
            continue
        b = speech_box(txt, m)
        if _inter(b, face, pad=15):
            errs.append(f"{name}『{txt}』が話者の顔に重なる（文字={tuple(round(v) for v in b)} / 顔={tuple(face)}）"
                        "→ 顔から外す。置ける空きが無いなら小さくして押し込まず**外す**。")
        elif name == "小セリフ1" and mouth is not None:
            cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            d = math.hypot(cx - mouth[0], cy - mouth[1])
            if d > 220:
                errs.append(f"{name}が口元から {round(d)}px 離れている（口={tuple(mouth)}）。"
                            "**小セリフは話者の口元に置く**（顔から逃がした結果、誰が喋っているのか分からない位置になっている）。"
                            "顔に掛からず口に近い場所＝**顎の下や頬のすぐ横**を探す。無ければ外す。")
            elif d > 170:
                warns.append(f"{name}が口元から {round(d)}px。もう少し口に寄せる。")
        if b[1] < BAND_TOP or b[3] > BAND_BOTTOM:
            warns.append(f"{name}が帯に掛かる（y={round(b[1])}-{round(b[3])}／可視帯は{BAND_TOP}-{BAND_BOTTOM}）")

    # ② 矢印の向きが視線と噛み合っているか
    if not _off(ar):
        if gaze == "camera" and not allow_camera_gaze:
            errs.append("人物がカメラを見ているのに矢印がある＝**矢印の先を誰も見ていない**。"
                        "矢印を外すか、視線の先に置き直す（どうしても必要なら allow_camera_gaze=True と理由を書く）。")
        elif gaze != "camera":
            g = GAZE_VEC[gaze]
            d = arrow_dir(ar[4] if len(ar) >= 5 else 0)
            if d[0] * g[0] + d[1] * g[1] < 0.2:
                errs.append(f"矢印の向き(rot={ar[4] if len(ar)>=5 else 0})が視線『{gaze}』と食い違う"
                            "→ 視線と同じ向きに伸ばす。")
            fc = ((face[0] + face[2]) / 2, (face[1] + face[3]) / 2)
            tip = arrow_tip(ar)
            v = (tip[0] - fc[0], tip[1] - fc[1])
            if v[0] * g[0] + v[1] * g[1] <= 0:
                errs.append(f"矢印の先{tuple(round(t) for t in tip)}が視線『{gaze}』の反対側にある"
                            f"（顔の中心={tuple(round(c) for c in fc)}）→ 視線の先へ移す。")
            if target is not None:
                aw = 130.0 * (ar[2] / 165.0)
                abox = (ar[0]-aw/2, ar[1]-aw/2, ar[0]+aw/2, ar[1]+aw/2)
                ox = min(abox[2], target[2]) - max(abox[0], target[0])
                oy = min(abox[3], target[3]) - max(abox[1], target[1])
                if ox > 0 and oy > 0 and (ox * oy) > 0.25 * aw * aw:
                    errs.append(f"矢印が対象そのものに被っている（矢印={tuple(round(v) for v in abox)} / 対象={tuple(target)}）。"
                                "**矢印は対象を隠さず、外から指す**。対象の枠の外に置いて先端だけを縁に届かせる。")
                tip2 = arrow_tip(ar)
                dd = math.hypot(max(target[0]-tip2[0], 0, tip2[0]-target[2]),
                                max(target[1]-tip2[1], 0, tip2[1]-target[3]))
                if dd > 90:
                    warns.append(f"矢印の先が対象から {round(dd)}px 離れている。先端を対象の縁まで届かせる。")
            if gaze in ("left", "right") and abs(ar[1] - fc[1]) > 140:
                warns.append(f"矢印が目線の高さから{round(abs(ar[1]-fc[1]))}px 外れている"
                             "（横向きの視線なら目線の高さに置くと繋がって見える）")

    # ③ !? は「驚いている人物」の記号。顔のすぐ横に置く。空きスペース置きは減点
    #    ★2026-09-02 ユーザー指摘で条件を入れ替えた。
    #      旧：「直近と違うマスに置く」＝変化そのものを目的にしていた＝**適当な配置**。
    #      正：「その回の驚いている人物の頭の横に置く」。位置が毎回変わるのは結果であって目的ではない。
    log = _load().get(ch, [])
    if not _off(mq):
        r = 0.72 * (mq[2] if len(mq) >= 3 else 100) / 2
        mb = (mq[0]-r, mq[1]-r, mq[0]+r, mq[1]+r)
        dx = max(face[0] - mq[0], 0, mq[0] - face[2])
        dy = max(face[1] - mq[1], 0, mq[1] - face[3])
        dist = math.hypot(dx, dy)
        if _inter(mb, face, pad=10):
            errs.append(f"!? が話者の顔に重なる（!?={tuple(round(v) for v in mb)} / 顔={tuple(face)}）→ 頭の外へ")
        elif dist > 200:
            errs.append(f"!? が話者の顔から {round(dist)}px 離れている＝**空きスペース置き**（減点対象）。"
                        "!? は『驚いている人物』の記号。**その人の頭のすぐ横**に置く。"
                        "画面の隅に固定するのも、前回と違うマスへ動かすのも、どちらも理由になっていない。")
        elif dist > 140:
            warns.append(f"!? が顔から {round(dist)}px。もう少し頭に寄せると誰が驚いているか一目で分かる。")
        if len(mq) >= 3 and len(log) >= 3 and all(abs(e["mq"][2] - mq[2]) < 8 for e in log[-3:]):
            warns.append("!? の大きさが直近3本と同じ。左右で大きさと角度を変える（実測の中央値は約61px）")
        if flag and len(flag) >= 3 and flag[2]:
            fw = flag[2]; fh = fw * 0.53
            fb = (flag[0]-fw/2, flag[1]-fh/2, flag[0]+fw/2, flag[1]+fh/2)
            if _inter(mb, fb):
                errs.append("!? が国旗に重なる → どちらかをずらす")

    # ④ 国旗が下帯に掛かっていないか／枠外に出ていないか
    if flag and len(flag) >= 3 and flag[2]:
        w = flag[2]; h = w * 0.53
        x1, y1, x2, y2 = flag[0] - w / 2, flag[1] - h / 2, flag[0] + w / 2, flag[1] + h / 2
        if x1 < 0 or x2 > CANVAS[0] or y1 < 0 or y2 > CANVAS[1]:
            errs.append(f"国旗が枠外にはみ出す（{round(x1)},{round(y1)})-({round(x2)},{round(y2)}）")
        if y2 > BAND_BOTTOM:
            errs.append(f"国旗の下端 y={round(y2)} が2行目(y{BAND_BOTTOM})に掛かる")
        if _inter((x1, y1, x2, y2), face, pad=0):
            errs.append("国旗が話者の顔に掛かる → 外す（実績で多用＝毎回入れる理由にはならない）")

    # ⑤ 記号が中央に固まっていないか（合成前の見込み）
    xs = [t[0] for t in (mq, ar, el) if not _off(t)]
    if len(xs) >= 2 and (max(xs) - min(xs)) < 0.60 * CANVAS[0]:
        warns.append(f"記号の広がりが見込み {round(max(xs)-min(xs))}px＝画面の{round((max(xs)-min(xs))/CANVAS[0]*100)}%。"
                     "上位12本の実測は中央値79%。**ただし広がりのために記号を意味の無い場所へ動かさない**"
                     "（!?=驚いている人物／矢印=対象／丸=接触点。上位12本が79%なのは引きの絵が多いから）。"
                     "寄りの絵で届かないならそれでよい。")

    if errs:
        raise MarksError("\n  × " + "\n  × ".join(errs) +
                         ("\n  △ " + "\n  △ ".join(warns) if warns else ""))
    if record and not _off(mq):
        d = _load(); d.setdefault(ch, []).append({"no": str(no), "mq": list(mq), "gaze": gaze})
        d[ch] = d[ch][-30:]
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        json.dump(d, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return warns


def verify(png_path, out_path=None, mq=None, ar=None, el=None, ms=None, ms2=None,
           eyes=None, mouth=None):
    """合成後：記号・小セリフの周りを4倍に切り出した検品画像を書き出す。納品前に必ず開く。
    ★eyes=(x,y) / mouth=(x,y) を渡すと目と口も拡大して並べる。
      視線と口元は**拡大しないと必ず読み違える**（過去に、瞳が左を向いているのに拡大せず
      gaze="right" と決めつけてゲートに渡し、素通りさせた）。"""
    from PIL import Image
    im = Image.open(png_path).convert("RGB")
    spots = [(n, t) for n, t in (("目★視線を決める", eyes), ("口★セリフの基準", mouth),
                                 ("!?", mq), ("矢印", ar), ("丸", el), ("セリフ1", ms), ("セリフ2", ms2))
             if not _off(t)]
    if not spots:
        return None
    W, H = 640, 300
    sheet = Image.new("RGB", (W, H * len(spots)), "white")
    for i, (n, t) in enumerate(spots):
        x, y = int(t[0]), int(t[1])
        box = (max(0, x - 160), max(0, y - 75), min(1280, x + 160), min(720, y + 75))
        sheet.paste(im.crop(box).resize((W, H)), (0, i * H))
    out_path = out_path or png_path.replace(".png", "_check_marks.jpg")
    sheet.save(out_path, quality=92)
    return out_path

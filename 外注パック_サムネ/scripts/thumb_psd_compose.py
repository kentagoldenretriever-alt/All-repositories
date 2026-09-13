#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""サムネ完成版の合成器（テンプレPSDを Photoshop の ExtendScript で駆動）。

★GUIクリックは一切しない。座標のブレが出ずテンプレの仕様（フォント/グラデ/不透明度）がそのまま乗る。
★テンプレ原本は開いて書き出して SaveOptions.DONOTSAVECHANGES で閉じる＝絶対に上書きしない。
★どのレイヤーが1〜3行目・背景・国旗・記号かは config.json の template で決める（チャンネルごとにテンプレが違う）。
  レイヤーはグループの中も探す。名前は部分一致。同名が複数あれば pick（narrow/wide＝幅の狭い/広い方）か nth で選ぶ。

使い方（Python から）:
    import thumb_psd_compose as T
    T.render(out="/path/120 A.png", l1="「…」", l2="…", l3="…",
             img="/path/中央画像.png",
             el=(x,y,横%,縦%), ar=(x,y,%), mq=(x,y,%,%,角度), mq2=..., ms=(x,y,%), small="…",
             ms2=..., small2="…", flag_img="/path/flag.png", flag=(x,y,幅px),
             bg_dy=55, psd_out="/path/120 A.psd")

引数の約束:
  - 記号系タプルは (x, y, 倍率) / (x, y, 横倍率, 縦倍率) / (x, y, 横倍率, 縦倍率, 角度)
    → 4要素で楕円化、5要素で回転。使わない記号は画面外 (-600,-600,100) に逃がす。
  - bg_dy: 背景を縦にずらす。全身立ちの画は頭が上帯（1行目の黒フチ）に食われるので下げる。
           上に空く分は帯の裏なので見えない。
  - flag_img を空にすると国旗レイヤーは非表示。
  - ★mark / mark2 で赤い記号の中身を差し替える（"!?" / "!!" / "?!"）。空なら既定の中身のまま。
  - ch 引数は互換のために残しているだけ（テンプレは config.json の template_psd）。
  - ★国旗はテンプレ側に縁取り/影が付いていることが多いので、**白フチを自作せず生の国旗画像を渡す**。

★Mac は AppleScript（osascript）、Windows は Photoshop の COM（pywin32）で同じ JSX を実行する。
★Mac の AppleEvent は既定タイムアウト(-1712)に必ず当たるので 900 秒に延長してある。1枚2〜4分。
"""
import json, os, subprocess, sys

# ★テンプレの場所・Photoshopのアプリ名・レイヤーの役割は config.json から読む（個人のパスを埋め込まない）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, pkg_path, IS_WIN
_CFG = load_config(required=False)
TEMPLATE = pkg_path(_CFG.get("template_psd", "assets/サムネ テンプレ.psd"))
APP = _CFG.get("photoshop_app", "Adobe Photoshop 2026")
TP = _CFG["template"]


def esc(s):
    """ExtendScript 用に \\uXXXX へ退避（日本語の文字化け回避）"""
    return "".join(c if 32 <= ord(c) < 127 and c not in '"\\' else "\\u%04x" % ord(c) for c in s)


def js_specs(obj):
    """Python の値を ExtendScript のリテラルにする（日本語は \\uXXXX）。"""
    return json.dumps(obj, ensure_ascii=True)


# レイヤーの探し方（合成とテンプレ解析で共通）
JS_FIND = r'''
function __w(L){ var b=L.bounds; return b[2].as("px")-b[0].as("px"); }
function __all(cont, out){
  for(var i=0;i<cont.layers.length;i++){
    var L=cont.layers[i];
    if(L.typename=="LayerSet") __all(L,out); else out.push(L);
  }
  return out;
}
var __ALL=null;
function findRole(doc, spec){
  if(!spec || !spec.layer) return null;
  if(!__ALL) __ALL=__all(doc,[]);
  var hit=[];
  for(var i=0;i<__ALL.length;i++){
    var L=__ALL[i];
    if(L.name.indexOf(spec.layer)>=0 && (!spec.text || L.kind==LayerKind.TEXT)) hit.push(L);
  }
  if(hit.length==0) return null;
  if(spec.nth!=null && spec.nth<hit.length) return hit[spec.nth];
  if(spec.pick && hit.length>1){
    var best=hit[0];
    for(var j=1;j<hit.length;j++){
      var w=__w(hit[j]), bw=__w(best);
      if(spec.pick=="narrow" ? (w<bw) : (w>bw)) best=hit[j];
    }
    return best;
  }
  return hit[0];
}
'''

JSX = JS_FIND + r'''
function replaceSO(doc, layer, path){
  doc.activeLayer = layer;
  var d = new ActionDescriptor();
  d.putPath(charIDToTypeID("null"), new File(path));
  d.putInteger(stringIDToTypeID("pageNumber"), 1);
  executeAction(stringIDToTypeID("placedLayerReplaceContents"), d, DialogModes.NO);
}

var TP = __TP__;
var doc = app.open(new File("__TMPL__"));
var ru = app.preferences.rulerUnits; app.preferences.rulerUnits = Units.PIXELS;
var CW = doc.width.as("px"), CH = doc.height.as("px");

// 役割のレイヤーを先に全部つかむ（複製で増える前に）
var bg   = findRole(doc, TP.bg_layer);
var flag = findRole(doc, TP.flag_layer);
var LN = TP.lines, tl = [];
for (var i=0;i<3;i++){
  var s = LN[i];
  tl.push(s ? findRole(doc, {layer:s.layer, nth:s.nth, pick:s.pick, text:true}) : null);
}
var mQ  = findRole(doc, TP.mark_layer);     // !?（文字レイヤーなので中身を差し替えられる）
var mS  = findRole(doc, TP.speech_layer);   // 小セリフ
var mAr = findRole(doc, TP.arrow_layer);    // 矢印
var mEl = findRole(doc, TP.ellipse_layer);  // 丸

// --- 背景（スマートオブジェクト）差し替え → 全面被覆にリセット → bg_dy で縦シフト ---
if (bg && "__IMG__".length>0){
  try{
    replaceSO(doc, bg, "__IMG__");
    var b=bg.bounds;
    var bw=b[2].as("px")-b[0].as("px"), bh=b[3].as("px")-b[1].as("px");
    var sc=Math.max(CW/bw, CH/bh)*100;
    bg.resize(sc, sc, AnchorPosition.MIDDLECENTER);
    var c=bg.bounds;
    bg.translate(CW/2-(c[0].as("px")+c[2].as("px"))/2,
                 CH/2-(c[1].as("px")+c[3].as("px"))/2 + __BGDY__);
  }catch(e){}
}

// --- 国旗チップ：画像指定があれば差し替えて配置、無ければ非表示 ---
if (flag){
  if ("__FLAG__".length>0){
    try{
      flag.visible = true;
      replaceSO(doc, flag, "__FLAG__");
      var fb=flag.bounds;
      var fw=fb[2].as("px")-fb[0].as("px");
      var fs2=__FLAGW__/fw*100;
      flag.resize(fs2, fs2, AnchorPosition.MIDDLECENTER);
      var fc=flag.bounds;
      flag.translate(__FLAGX__-(fc[0].as("px")+fc[2].as("px"))/2,
                     __FLAGY__-(fc[1].as("px")+fc[3].as("px"))/2);
    }catch(e){ try{ flag.visible=false; }catch(e2){} }
  } else { try{ flag.visible=false; }catch(e){} }
}

// --- 3行のテキスト ---
function cyOf(L){ var b=L.bounds; return (b[1].as("px")+b[3].as("px"))/2; }
function setLine(L, txt, spec){
  if(!L || !spec) return;
  var cy0=cyOf(L);
  // ボックス幅でのクリップ/折返しを防ぐ＝ポイントテキスト化
  try{ L.textItem.kind=TextType.POINTTEXT; }catch(e){}
  try{ L.textItem.contents=txt; }catch(e){}
  // 字送りを二分探索して行の幅（spec.width）に合わせる。下限＝TP.tracking_min。
  // 収まらなければ「詰めすぎ」でなく「文言が長い」＝字数を減らして直す。
  var lo=(TP.tracking_min!=null)?TP.tracking_min:-200, hi=420;
  for(var i=0;i<10;i++){
    var mid=(lo+hi)/2;
    try{ L.textItem.tracking=mid; }catch(e){ break; }
    if(__w(L)<spec.width) lo=mid; else hi=mid;
  }
  try{ L.textItem.tracking=lo; }catch(e){}
  var b=L.bounds;
  // 左端を spec.left に（同梱テンプレは -14＝黒フチを画面外へ逃がす）。align:"center" なら中心を spec.cx に
  var dx = (spec.align=="center") ? (spec.cx-(b[0].as("px")+b[2].as("px"))/2) : (spec.left-b[0].as("px"));
  L.translate(dx, cy0-cyOf(L));
}
setLine(tl[0],"__L1__",LN[0]);
setLine(tl[1],"__L2__",LN[1]);
setLine(tl[2],"__L3__",LN[2]);

// --- 記号・小文字 ---
function place(L, cx, cy, scale, scaleY, rot){
  if(!L) return;
  var sy=(scaleY&&scaleY>0)?scaleY:scale;
  try{
    if(rot) L.rotate(rot, AnchorPosition.MIDDLECENTER);
    if((scale&&scale!=100)||(sy&&sy!=100)) L.resize(scale, sy, AnchorPosition.MIDDLECENTER);
    var b=L.bounds;
    L.translate(cx-(b[0].as("px")+b[2].as("px"))/2, cy-(b[1].as("px")+b[3].as("px"))/2);
  }catch(e){}
}
if(mS){
  try{ mS.textItem.kind=TextType.POINTTEXT; }catch(e){}
  try{ mS.textItem.contents="__SMALL__"; }catch(e){}
}
// ★記号の中身を状況に応じて差し替える（!? / !! / ?! など）
if(mQ && "__MARK__".length>0){
  try{ mQ.textItem.kind=TextType.POINTTEXT; }catch(e){}
  try{ mQ.textItem.contents="__MARK__"; }catch(e){}
}
// ★★複製は「縮小する前」に取る（縮小後に複製すると2つ目に倍率が二重に掛かる）
var mQ2=null; try{ if(mQ) mQ2=mQ.duplicate(); }catch(e){}
if(mQ2 && "__MARK2__".length>0){
  try{ mQ2.textItem.kind=TextType.POINTTEXT; }catch(e){}
  try{ mQ2.textItem.contents="__MARK2__"; }catch(e){}
}
var mS2=null;
if("__SMALL2__".length>0){
  try{ mS2=mS.duplicate();
       try{ mS2.textItem.kind=TextType.POINTTEXT; }catch(e){}
       mS2.textItem.contents="__SMALL2__"; }catch(e){}
}
// 複製を取り終えてから、それぞれを一度だけ配置・縮小する
place(mEl,__EL__);
place(mAr,__AR__);
place(mQ, __MQ__);
place(mS, __MS__);
place(mQ2,__MQ2__);
place(mS2,__MS2__);

// --- 書き出し：PSD（レイヤー保持）→ PNG。テンプレ原本には保存しない ---
if("__PSD__".length>0){
  var po=new PhotoshopSaveOptions(); po.layers=true; po.embedColorProfile=true; po.annotations=false;
  doc.saveAs(new File("__PSD__"), po, true, Extension.LOWERCASE);
}
var opt=new PNGSaveOptions();
doc.saveAs(new File("__OUT__"), opt, true, Extension.LOWERCASE);
app.preferences.rulerUnits=ru;
doc.close(SaveOptions.DONOTSAVECHANGES);
"__OK__";
'''


def render(out, l1, l2, l3, img="", ch=None, bgkey=None,
           small="", small2="", psd_out="", bg_dy=0,
           mark="", mark2="",
           el=(-600, -600, 100), ar=(-600, -600, 100),
           mq=(-600, -600, 100), mq2=(-600, -600, 100),
           ms=(-600, -600, 100), ms2=(-600, -600, 100),
           flag_img="", flag=(0, 0, 0)):
    def fmt(t):
        return ",".join(str(int(v)) for v in t)

    tp = dict(TP)
    if bgkey:
        tp["bg_layer"] = {"layer": bgkey}
    # Windows では ExtendScript に渡すパスを「/」区切りにする（\ はエスケープ事故の元）
    _s = (lambda s: (s or "").replace("\\", "/")) if IS_WIN else (lambda s: s or "")
    tmpl, out_js, img, psd_out, flag_img = _s(TEMPLATE), _s(out), _s(img), _s(psd_out), _s(flag_img)
    jsx = (JSX.replace("__TP__", js_specs(tp))
              .replace("__TMPL__", esc(tmpl)).replace("__OUT__", esc(out_js))
              .replace("__L1__", esc(l1)).replace("__L2__", esc(l2)).replace("__L3__", esc(l3))
              .replace("__IMG__", esc(img))
              .replace("__SMALL__", esc(small)).replace("__SMALL2__", esc(small2))
              .replace("__MARK__", esc(mark)).replace("__MARK2__", esc(mark2))
              .replace("__EL__", fmt(el)).replace("__AR__", fmt(ar))
              .replace("__MQ__", fmt(mq)).replace("__MQ2__", fmt(mq2))
              .replace("__MS__", fmt(ms)).replace("__MS2__", fmt(ms2))
              .replace("__PSD__", esc(psd_out)).replace("__BGDY__", str(int(bg_dy)))
              .replace("__FLAG__", esc(flag_img))
              .replace("__FLAGX__", str(int(flag[0]))).replace("__FLAGY__", str(int(flag[1])))
              .replace("__FLAGW__", str(int(flag[2]) if flag[2] else 1)))
    p = os.path.join(os.path.dirname(os.path.abspath(out)), "_run.jsx")
    run_jsx(jsx, p)
    return os.path.exists(out)


def run_jsx(jsx, p):
    """JSX を p に書いて Photoshop で実行し、(成功したか, 戻り値の文字列) を返す。
    Mac＝osascript／Windows＝COM（pywin32）。"""
    open(p, "w", encoding="utf-8").write(jsx)
    if IS_WIN:
        # Windows：Photoshop の COM（pywin32）で同じ JSX を実行する
        try:
            import win32com.client
        except ImportError:
            print("✗ pywin32 がありません → python -m pip install --user pywin32")
            return False, ""
        try:
            ps = win32com.client.Dispatch("Photoshop.Application")
            res = str(ps.DoJavaScriptFile(p))
            print("rc= 0 out=", res[:120])
            return True, res
        except Exception as e:
            print("rc= 1 err=", str(e)[:300])
            return False, ""
    r = subprocess.run(
        ["osascript", "-e",
         f'with timeout of 900 seconds\ntell application "{APP}" to do javascript file "{p}"\nend timeout'],
        capture_output=True, text=True, timeout=900)
    print("rc=", r.returncode, "out=", r.stdout.strip()[:120], "err=", r.stderr.strip()[:200])
    return r.returncode == 0, r.stdout.strip()


if __name__ == "__main__":
    print(__doc__)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""テンプレPSDの解析（セットアップ時にチャンネルごとのテンプレへ合わせるための道具）。

使い方:
  <python> scripts/inspect_template.py [--psd <テンプレのパス>] [--write]
      → レイヤーを全部（グループの中も）一覧にし、<work_dir>/_template/layers.json と
        テンプレをそのまま書き出した preview.png を作る。役割（1〜3行目・背景・国旗・記号）と可視帯の案も出す。
        --write で案を config.json の template（と template_psd）に書き込む。
  <python> scripts/inspect_template.py --measure [--write]
      → config.json の template の割り当てで、各行に何文字まで入るかを実測する
        （字送りを下限まで詰めても幅に収まる最大字数＝物理的な上限）。--write で template.chars に書き込む。

★テンプレ原本は開いて読むだけ。保存せずに閉じる。
★Photoshop を起動しておく（Mac は自動で起動する）。1回30秒〜2分。
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_config, pkg_path, IS_WIN, PKG  # noqa: E402
import thumb_psd_compose as T  # noqa: E402

JSX_LIST = r'''
function q(s){ s=String(s); var o='"';
  for(var i=0;i<s.length;i++){ var c=s.charCodeAt(i);
    if(c==34) o+='\\"'; else if(c==92) o+='\\\\'; else if(c<32) o+=' '; else o+=s.charAt(i); }
  return o+'"'; }
function px(v){ try{ return Math.round(v.as("px")); }catch(e){ return 0; } }
var KINDS={}; try{
  KINDS[LayerKind.TEXT]="text"; KINDS[LayerKind.SMARTOBJECT]="smart"; KINDS[LayerKind.NORMAL]="pixel";
  KINDS[LayerKind.SOLIDFILL]="fill"; KINDS[LayerKind.GRADIENTFILL]="gradient"; }catch(e){}
var rows=[], idx=0;
function walk(cont, path){
  for(var i=0;i<cont.layers.length;i++){
    var L=cont.layers[i], p=path+"/"+L.name;
    if(L.typename=="LayerSet"){ rows.push('{"i":'+(idx++)+',"path":'+q(p)+',"name":'+q(L.name)+',"kind":"group","visible":'+L.visible+'}'); walk(L,p); continue; }
    var b=L.bounds, k=KINDS[L.kind]||String(L.kind);
    var r='{"i":'+(idx++)+',"path":'+q(p)+',"name":'+q(L.name)+',"kind":'+q(k)+',"visible":'+L.visible
         +',"bounds":['+px(b[0])+','+px(b[1])+','+px(b[2])+','+px(b[3])+']';
    if(L.kind==LayerKind.TEXT){ var t=L.textItem, tk="point", w=0;
      try{ if(t.kind==TextType.PARAGRAPHTEXT){ tk="box"; w=Math.round(t.width.as("px")); } }catch(e){}
      var font="",size=0,tr=0,just="",have=true;
      try{ font=t.font; }catch(e){} try{ size=Math.round(t.size.as("px")*10)/10; }catch(e){}
      try{ tr=t.tracking; }catch(e){} try{ just=String(t.justification); }catch(e){}
      try{ have=false; for(var f=0;f<app.fonts.length;f++){ if(app.fonts[f].postScriptName==font){ have=true; break; } } }catch(e){ have=true; }
      r+=',"text":'+q(t.contents)+',"font":'+q(font)+',"font_installed":'+have+',"size":'+size
        +',"tracking":'+tr+',"justification":'+q(just)+',"text_kind":'+q(tk)+',"box_width":'+w;
    }
    rows.push(r+'}');
  }
}
var doc=app.open(new File("__TMPL__"));
var ru=app.preferences.rulerUnits; app.preferences.rulerUnits=Units.PIXELS;
walk(doc,"");
var W=Math.round(doc.width.as("px")), H=Math.round(doc.height.as("px"));
var f=new File("__JSON__"); f.encoding="UTF-8"; f.open("w");
f.write('{"canvas":['+W+','+H+'],"layers":[\n'+rows.join(",\n")+'\n]}'); f.close();
doc.saveAs(new File("__PNG__"), new PNGSaveOptions(), true, Extension.LOWERCASE);
app.preferences.rulerUnits=ru;
doc.close(SaveOptions.DONOTSAVECHANGES);
"__OK__";
'''

JSX_MEASURE = r'''
__FIND__
var doc=app.open(new File("__TMPL__"));
var ru=app.preferences.rulerUnits; app.preferences.rulerUnits=Units.PIXELS;
var specs=__LINES__, out=[];
function wOf(L){ var b=L.bounds; return b[2].as("px")-b[0].as("px"); }
for(var i=0;i<specs.length;i++){
  var L=findRole(doc, specs[i]);
  if(!L || L.kind!=LayerKind.TEXT){ out.push('{"line":'+(i+1)+',"error":"not found"}'); continue; }
  try{ L.textItem.kind=TextType.POINTTEXT; }catch(e){}
  var target=specs[i].width, res=[];
  var trs=[__TRMIN__, 0];
  for(var k=0;k<trs.length;k++){
    var n=1;
    for(n=1;n<60;n++){
      var s=""; for(var j=0;j<n;j++) s+="あ";
      try{ L.textItem.contents=s; L.textItem.tracking=trs[k]; }catch(e){}
      if(wOf(L)>target) break;
    }
    res.push(n-1);
  }
  // 1文字あたりの幅（字送り0）
  try{ L.textItem.contents="ああああああああああ"; L.textItem.tracking=0; }catch(e){}
  out.push('{"line":'+(i+1)+',"max_chars_tight":'+res[0]+',"max_chars_natural":'+res[1]+',"char_w":'+Math.round(wOf(L)/10*10)/10+'}');
}
var f=new File("__JSON__"); f.encoding="UTF-8"; f.open("w"); f.write('['+out.join(",")+']'); f.close();
app.preferences.rulerUnits=ru;
doc.close(SaveOptions.DONOTSAVECHANGES);
"__OK__";
'''


def _w(l):
    return l["bounds"][2] - l["bounds"][0]


def _spec(l, same):
    """同じ名前のレイヤーが複数あるときは pick（幅の narrow/wide）で区別する。"""
    s = {"layer": l["name"]}
    if len(same) > 1:
        s["pick"] = "narrow" if _w(l) == min(_w(x) for x in same) else "wide"
    return s


def guess_roles(info):
    """役割の割り当て案（config.json の template の形）。最終判断は preview.png とテスト合成で確かめる。
    3行＝横幅の45%以上ある文字レイヤーを上から3つ。width/left は今の文字の実幅と左端。"""
    W, H = info["canvas"]
    lay = [l for l in info["layers"] if l["kind"] != "group"]
    same = lambda l: [x for x in lay if x["name"] == l["name"]]
    texts = [l for l in lay if l["kind"] == "text" and l["visible"]]
    wide = sorted([l for l in texts if _w(l) >= 0.45 * W], key=lambda l: l["bounds"][1])[:3]
    g = {"lines": [dict(_spec(l, same(l)), width=_w(l), left=l["bounds"][0]) for l in wide]}
    if len(wide) >= 2:
        g["band"] = [wide[0]["bounds"][3], wide[1]["bounds"][1]]
    area = lambda l: _w(l) * (l["bounds"][3] - l["bounds"][1])
    smart = [l for l in lay if l["kind"] == "smart" and l["visible"]]
    big = sorted([l for l in smart if area(l) >= 0.5 * W * H], key=lambda l: -area(l))
    small = sorted([l for l in smart if area(l) < 0.25 * W * H], key=lambda l: -area(l))
    if big:
        g["bg_layer"] = _spec(big[0], same(big[0]))
    if small:
        g["flag_layer"] = _spec(small[0], same(small[0]))
    rest = [l for l in texts if l not in wide]
    marks = [l for l in rest if l["text"].strip() and all(c in "!?！？ 　" for c in l["text"].strip())]
    speech = [l for l in rest if l not in marks]
    if marks:
        g["mark_layer"] = _spec(marks[0], same(marks[0]))
    if speech:
        g["speech_layer"] = _spec(speech[0], same(speech[0]))
    for key, words in (("arrow_layer", ("矢印", "arrow", "Arrow")),
                       ("ellipse_layer", ("楕円", "丸", "円", "ellipse", "Ellipse"))):
        hit = [l for l in lay if any(w in l["name"] for w in words)]
        if hit:
            g[key] = _spec(hit[0], same(hit[0]))
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--psd", default="")
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--write", action="store_true", help="結果を config.json の template に書き込む")
    a = ap.parse_args()
    cfg = load_config(required=False)
    tmpl = pkg_path(a.psd) if a.psd else cfg["template_psd"]
    if not os.path.exists(tmpl):
        sys.exit(f"✗ テンプレが見つからない: {tmpl}")
    od = os.path.join(cfg["work_dir"], "_template")
    os.makedirs(od, exist_ok=True)
    sl = (lambda s: s.replace("\\", "/")) if IS_WIN else (lambda s: s)
    js_path = os.path.join(od, "_inspect.jsx")

    if a.measure:
        tp = cfg["template"]
        out_json = os.path.join(od, "measure.json")
        jsx = (JSX_MEASURE.replace("__FIND__", T.JS_FIND)
               .replace("__TMPL__", T.esc(sl(tmpl))).replace("__JSON__", T.esc(sl(out_json)))
               .replace("__LINES__", T.js_specs(tp["lines"]))
               .replace("__TRMIN__", str(int(tp.get("tracking_min", -200)))))
        ok, _ = T.run_jsx(jsx, js_path)
        if not os.path.exists(out_json):
            sys.exit("✗ 実測できなかった（Photoshop が起動しているか・割り当てたレイヤー名が合っているか）")
        res = json.load(open(out_json, encoding="utf-8"))
        print("行 | 詰めて入る最大字数（物理的な上限）| 字送り0で入る字数 | 1字の幅px")
        for r in res:
            if "error" in r:
                print(f"{r['line']}行目 | ✗ レイヤーが見つからない")
            else:
                print(f"{r['line']}行目 | {r['max_chars_tight']} | {r['max_chars_natural']} | {r['char_w']}")
        os.remove(js_path)
        if any("error" in r for r in res) or len(res) < 3:
            sys.exit("✗ 3行そろっていないので字数を決められない（template.lines を直す）")
        t1, t2, t3 = (r["max_chars_tight"] for r in res[:3])
        # 同梱テンプレの実測（18/23/15）と、運用で確かめた字数（1行目18まで・2行目20〜22・3行目13〜14＝15は潰れる）
        # の関係をそのまま当てはめる
        chars = {"l1_max": t1, "l2": [t2 - 3, t2 - 1], "l3": [t3 - 2, t3 - 1], "l3_max": t3 - 1}
        print("字数（template.chars）:", json.dumps(chars, ensure_ascii=False))
        if a.write:
            write_template({"chars": chars})
        return

    out_json = os.path.join(od, "layers.json")
    out_png = os.path.join(od, "preview.png")
    jsx = (JSX_LIST.replace("__TMPL__", T.esc(sl(tmpl))).replace("__JSON__", T.esc(sl(out_json)))
           .replace("__PNG__", T.esc(sl(out_png))))
    T.run_jsx(jsx, js_path)
    if not os.path.exists(out_json):
        sys.exit("✗ 解析できなかった（Photoshop が起動しているか確認）")
    info = json.load(open(out_json, encoding="utf-8"))
    W, H = info["canvas"]
    print(f"キャンバス {W}x{H}" + ("" if (W, H) == (1280, 720) else "  ✗ 1280x720 ではない（このパックは1280x720前提）"))
    print("番号 | 種類 | 表示 | 位置(x1,y1,x2,y2) | 名前（グループ/名前） | 文字・フォント")
    for l in info["layers"]:
        b = l.get("bounds", "")
        extra = ""
        if l["kind"] == "text":
            extra = (f"「{l['text'][:20]}」 {l['font']} {l['size']}px 字送り{l['tracking']} {l['text_kind']}"
                     + (f" 箱幅{l['box_width']}" if l['text_kind'] == "box" else "")
                     + ("" if l["font_installed"] else "  ✗フォント未導入"))
        print(f"{l['i']} | {l['kind']} | {'○' if l['visible'] else '−'} | {b} | {l['path']} | {extra}")
    g = guess_roles(info)
    print("\n役割の割り当て案（preview.png を見て確かめる）:")
    print(json.dumps(g, ensure_ascii=False, indent=1))
    print(f"\nlayers.json: {out_json}\npreview.png: {out_png}")
    os.remove(js_path)
    if a.write:
        write_template(g, psd=tmpl if a.psd else "")


def write_template(part, psd=""):
    """config.json の template に上書きで書き込む（書いていない項目＝既定値はそのまま）。"""
    path = os.path.join(PKG, "config.json")
    raw = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    if psd:
        raw["template_psd"] = psd
    raw.setdefault("template", {}).update(part)
    json.dump(raw, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✓ config.json の template に書いた: {', '.join(part)}" + ("・template_psd" if psd else ""))


if __name__ == "__main__":
    main()

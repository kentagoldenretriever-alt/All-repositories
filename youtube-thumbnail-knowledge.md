# YouTubeサムネイル ナレッジベース（海外の反応×日本称賛系）

目標: CTR20%超え、1000万再生を狙うサムネイルの型を蓄積するナレッジ。
新しいサムネイル参考画像が送られるたびに、パターンとして追記していく。

## 共通ルール（ジャンル全体の型）

**レイアウト構造（上下3分割）**
- 上部帯（黒背景＋黄色文字）: フック性の高い「セリフ」見出し。1行、13〜20文字程度、「」付き
- 中央: 人物クローズアップ、感情が誇張された表情
- 下部帯（黒フチ2行）: 1行目＝状況説明（白 or 水色）、2行目＝結論・煽り（赤で強調）

**文字の型**
- カギ括弧「」のセリフ調、「!」「…」「?」多用
- 極太ゴシック＋黒フチ縁取り
- 色は黄色/白/赤/水色の4色ルール
- 「⁉」「!?」の赤い記号を人物の近くに添える

**PhotoScape X 設定の基準値**
- フチ(アウトライン): 4px（6pxだと重すぎる）
- 影(シャドウ): 不透明度40〜50%、ぼかし2〜3px（濃すぎ注意、クライアント指摘あり）
- 黒帯は完全な黒（半透明にしない）で視認性を確保

**画像生成プロンプトの鉄則（何度も修正して分かった注意点）**
- 生成AIは複数人物を「証明写真的な正面シンメトリー」に寄せがち → "NOT a symmetrical frontal lineup"等で明示的に禁止する
- 視線がバラバラになりがち → "all looking in the exact same direction"と強く指定
- AI感（無表情・肌が均一すぎ）が出やすい → "candid documentary-style, NOT posed", "visible pores, subtle asymmetry, avoid uncanny valley"を必ず入れる
- 背景が暗く沈みがち → "+1〜1.5 stops overexposed", "no gray/metallic tones"など数値的に明るさを縛る
- 制服など濃色の服が黒つぶれしやすい → "well-lit, visible highlights and fabric folds, not crushed to flat black"
- 年齢・美形度の指定は具体的に（例: "early-to-mid 20s, youthful glowing skin", "magazine-cover level beauty"）

---

## パターン1: CA（客室乗務員）5人・横並び型

**元ネタ画像の特徴**
- 5人の女性CA、紺の制服＋赤ストライプスカーフ
- 斜め対角線に並び、奥行きで遠近感（先頭が最大、奥ほど小さく・ソフトフォーカス）
- 先頭のみブロンド、残り4人は黒髪
- 全員が同じ方向（画面左）を見て視線が揃っている
- 表情は統一感のある感情（心配・困惑、または祈るような真剣さ）
- 先頭の女性は両手を胸元・スカーフ付近で組むポーズ
- 背景は機内窓からの明るいぼやけた光

**最終確定プロンプト（クライアントFB反映済み・要検証）**
```
Photorealistic candid documentary-style photo of five breathtakingly
beautiful young female flight attendants, all in their early-to-mid 20s,
youthful glowing skin, each with a distinct but equally stunning face,
magazine-cover level beauty. Shot on a real DSLR camera, natural skin
texture with visible pores and fine detail, subtle asymmetry in each face,
avoid airbrushed or synthetic CGI look, avoid uncanny valley, avoid
perfectly smooth AI-generated skin — this must look like a real photograph
of real young women, not a rendered image.

The frontmost woman has honey-blonde hair in a neat updo, pearl earrings,
red lipstick. The four women behind her have dark brown-to-black hair in
matching updos. Arranged in a receding diagonal row inside an airplane
cabin aisle, medium shot from the waist up, bodies at a 3/4 front angle.

All five share a deeply emotional expression of heartfelt prayer and hope —
eyes glistening, slightly moist, brows drawn together with genuine worry,
lips pressed together as if silently praying or holding back tears, a raw
and vulnerable moment, not a blank or posed stare. Each woman's intensity
varies slightly — one with eyes almost closed as if praying, one with lips
slightly parted and trembling, one staring intently — but all clearly
yearning and hoping for the same thing off-frame to the left.

The frontmost woman has both hands clasped tightly together near her chest,
knuckles slightly whitened, as if in prayer. Closest woman largest and
sharpest in frame, others progressively smaller and softer focus. Uniforms:
navy blue blazers with red-striped scarves, well-lit with a soft key light
showing visible highlights and fabric folds, not crushed to flat black.

BACKGROUND AND LIGHTING (critical): The entire cabin interior — walls,
ceiling, windows — must appear near-white and sun-drenched, as if flooded
with bright daylight, exposure pushed brighter than a normal photo (+1 to
+1.5 stops overexposed), highlights blown out near the windows. No gray,
no metallic tones, no visible shadows anywhere in the background. The
background should read as almost pure white and luminous, so the navy
uniforms and warm skin tones are the only strong colors in the frame.
Shot on 85mm lens, shallow depth of field, warm and emotionally intimate
editorial photography. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「一度乗ったらおしまいよ」（カナダ人CAエマ・キャラハンの羽田便エピソード）

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| 上部見出し | 「日本便は、一度乗ったらおしまいよ」 | 黄色＋黒フチ4px | 画面上部、中央揃え |
| リアクション記号 | ⁉ | 赤 | 人物の顔の右上 |
| 下段1行目 | 「五年目のカナダ人CAが初めて任された羽田便」 | 白＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「その"洗礼"に涙が止まらなかった理由」 | 赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン2: 新幹線・車椅子対応型（今回追加分）

**元ネタ画像の特徴**
- 主要人物3人: 日本人の男性駅員（濃紺制服、白手袋、帽子、しゃがんで案内するポーズ、笑顔）、車椅子に座る金髪外国人女性（驚いた表情でこちらを見上げる）、その後ろに立つ茶髪の女性（連れ、微笑みながら肩に手を添える）
- 背景: 新幹線車両（白地に青のライン）、車椅子マーク・禁煙マークのステッカー、ホームに並ぶ日本人通勤客の列
- 上部見出し「え…本当にこれ乗れるの？」黄色＋黒フチ
- 「⁉」赤記号、女性の顔の横
- 下段1行目「外国人が車椅子で知った日本の現実」水色＋黒フチ
- 下段2行目「新幹線に乗った瞬間、思わず涙」赤＋黒フチ

**画像生成プロンプト（初期案・未検証、次回の生成結果を見て調整）**
```
Photorealistic candid documentary-style photo at a Japanese shinkansen
station platform. A young Japanese train conductor in a navy uniform,
white gloves, and a cap crouches down with a warm, welcoming smile,
gesturing toward a wheelchair ramp leading into the train car. In front
of him, a beautiful young Western woman in her mid-20s sits in a
wheelchair, looking up at him with a surprised, emotional expression —
eyes wide, slightly parted lips, as if she cannot believe the kindness
and accessibility being offered. Behind her, another young Western woman
stands close, one hand resting gently on her shoulder, smiling warmly.
Both women have naturally beautiful, youthful features, candid real-photo
skin texture, avoid airbrushed CGI look, avoid uncanny valley.

Background: the white-and-blue shinkansen train car with visible
wheelchair and no-smoking decals, and a blurred line of Japanese
commuters in suits waiting on the platform. Bright, natural daylight
station lighting, no dark shadows, warm and inviting overall tone.
Shot on 85mm lens, shallow depth of field with sharp focus on the three
main subjects, background softly blurred. 16:9 aspect ratio, no text,
no logos.
```

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| 上部見出し | 「え…本当にこれ乗れるの？」 | 黄色＋黒フチ4px | 画面上部、中央揃え |
| リアクション記号 | ⁉ | 赤 | 女性の顔の右上 |
| 下段1行目 | 「外国人が車椅子で知った日本の現実」 | 水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「新幹線に乗った瞬間、思わず涙」 | 赤＋黒フチ（強調） | 下部帯2行目 |

---

## 追記フォーマット（次回以降このまま使う）

```
## パターンN: ○○型

**元ネタ画像の特徴**
（人数・構図・表情・背景・文字の色と配置）

**画像生成プロンプト**
（英語プロンプト）

**紐づく台本**（あれば）

**PhotoScape X 文字入れ指示**
（表）
```

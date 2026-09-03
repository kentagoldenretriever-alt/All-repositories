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

**制作方針（クライアント指示・最重要）**
- 元ネタサムネイルと同等ではなく、常に元ネタの上位互換（より綺麗・より美味しそう・よりクオリティが高い）を狙うこと
- 特に料理写真は「艶・光の反射・湯気の迫力・彩度」を抽象的な言葉（"appetizing"等）で済ませず、食材ごとに具体的な質感描写を書き込むこと

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

## パターン3: 料理×家族リアクション 左右分割型

**元ネタ画像の特徴**
- これまでの2パターンと違い、左右で別々の画像を合成する構図
- 左半分: 赤い機関車型のお子様ランチプレートのクローズアップ（湯気の演出、ハンバーグ・エビフライ・ブロッコリー・プチトマト・ケチャップライス、「夢」の小旗、緑のクリームソーダを添える）
- 右半分: 家族3人の反応ショット。母親（ブロンド、驚いて口を開ける）、娘（ツインテール・ピンクリボン、両手で頬を押さえる最も強い驚き）、父親（口髭、デニムジャケット、画面端に半分見切れる）
- 中央に赤い矢印で「料理→人物」の視線誘導
- 「⁉」記号は娘の顔の横

**画像生成プロンプト①（料理部分・上位互換狙い強化版。クライアントFB「元ネタより綺麗で美味しそうにすること」反映済み）**
```
Professional commercial food photography, magazine-advertisement quality,
of a Japanese "okosama lunch" (kids' plate) shaped like a red steam
locomotive, served on a warm wooden table. Medium-wide shot showing the
entire plate with generous empty table space around it for cropping (NOT
an extreme close-up — leave negative space on all sides for compositing).

Every element has a glossy, glistening sheen: the hamburger steak is
coated in a rich glossy demi-glace sauce with visible light reflections,
the breaded fried shrimp has a crispy golden-brown crust with visible
crunchy texture, the broccoli florets are vivid emerald green with tiny
fresh water droplets catching the light, the cherry tomatoes are glossy
and deep red, and the ketchup-fried rice is molded into a perfectly
shaped small mountain with a light glistening sheen.

Dramatic, voluminous white steam billows dynamically from the
locomotive's smokestack, backlit so it glows and catches the light
beautifully against a softly blurred warm background. A crisp small
paper flag reading "夢" (dream) stands upright in the rice.

Beside the plate, a vibrant green cream soda float with vanilla ice
cream, a glossy maraschino cherry, and a paper cocktail umbrella,
condensation glistening on the glass.

Professional food styling, soft directional studio-style lighting
creating highlights and sheen on every surface, vivid highly saturated
colors, mouthwatering sizzle-photography quality as if shot for a
high-end restaurant advertisement. Shot on a 100mm macro lens with fine
detail on food textures, shallow depth of field with the background
softly blurred. 16:9 aspect ratio, no text, no logos.
```

**画像生成プロンプト②（家族の反応部分・引き目バージョン。2画面接合の余白確保のため寄りすぎ厳禁）**
```
Photorealistic candid documentary-style photo of an American family of
three, medium-wide shot from the waist up with generous space around and
above the subjects (NOT a tight close-up on just faces — leave enough
negative space on all sides for cropping and compositing). They are
reacting with shock and amazement, as if just seeing something astonishing
off-frame to the left. The mother, attractive woman in her late 30s with
wavy blonde hair, mouth open in genuine surprise, eyes wide. Her daughter,
about 6 years old, with twin-tail hairstyle and a pink ribbon, has the most
exaggerated reaction — both hands pressed to her cheeks, mouth wide open,
eyes huge with delighted disbelief. The father, with a mustache, wearing a
denim jacket, stands beside them, also reacting with raised eyebrows and
an open mouth, his full upper body visible rather than cropped at the edge.
All three genuinely emotional, candid real-photo skin texture, avoid
airbrushed CGI look, avoid uncanny valley. Soft indoor restaurant lighting,
warm and bright, blurred cozy background. Shot on 50mm lens for a wider
natural field of view, moderate depth of field. 16:9 aspect ratio, no
text, no logos.
```

**紐づく台本**: 「だから子連れで日本へ行くなって言ったのに…」（報道記者レイチェル・モリソンと娘エラの日本橋お子様ランチエピソード）

**PhotoScape X 合成・文字入れ指示**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| レイアウト | 左に料理画像、右に家族画像を配置し中央で接合 | — | 縦分割2枚合成 |
| 赤い矢印 | 料理→家族の方向 | 赤 | 画面中央 |
| 上部見出し | 「だから子連れで日本はダメだって!!」 | 黄色＋黒フチ4px | 画面上部、中央揃え |
| リアクション記号 | ⁉ | 赤 | 娘の顔の右上 |
| 下段1行目 | 「アメリカ人家族が友人の忠告を無視して来日」 | 白＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「お子様ランチで帰国後が大変!?」 | 赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン4: 4人異なる美女・怒り顔横並び型

**元ネタ画像の特徴**
- 若い女性の激怒した顔を4体、横一列に配置
- 全員が眉間にしわを寄せ、口を大きく開けて叫んでいる表情
- 手前2人は人差し指でカメラを指差すポーズ
- 頭上に赤い漫画的な怒りマーク（角ばった爆発記号）を1体ずつ配置
- 背景は日本の繁華街（新宿風の交差点）、ぼかした通行人
- 上部見出し「絶対に許さないから!!」黄色＋黒フチ
- 下段1行目「中国でブチギレたフランス人」水色＋黒フチ
- 下段2行目「その後…日本に来た結果」赤＋黒フチ

**制作方式**: 当初は「1人を生成してPhotoScape Xで複製」方式を検討したが、クライアント要望により「4人とも別の顔・別の髪色の美人」を1枚で一括生成する方式に変更。CA5人型で得たノウハウ（全員同じ方向を向かせる、AI感を消す指示）を流用。

**画像生成プロンプト（4人一括生成版）**
```
Photorealistic candid documentary-style photo of four stunningly beautiful,
sexy young European women in their early-to-mid 20s, standing side by side
in a busy Japanese city street (Shibuya-style crossing), blurred crowds of
pedestrians and shop signs in the background, bright daytime natural light.

Each woman has a distinctly different face and hairstyle — one with long
wavy brunette hair, one with blonde hair, one with auburn/red hair, one
with straight black hair — all with magazine-cover level beauty, natural
real-photo skin texture, avoid airbrushed CGI look, avoid uncanny valley,
avoid identical or mirrored faces between them.

All four are shouting with intense rage directly at the camera — mouths
wide open showing teeth, eyebrows sharply furrowed, deep frown lines,
eyes fierce and confrontational — as if collectively yelling at the
viewer. Each has at least one arm raised, index finger pointing
accusingly toward the camera, poses varying slightly between them so
they don't look like copies of each other.

They wear casual stylish outfits in a light color palette (denim
jackets, fitted tops). Medium-wide framing showing all four from
roughly waist up, with generous space around them for cropping and
compositing. Shot on 50mm lens, shallow depth of field with the four
women in sharp focus and the crowd behind them blurred. 16:9 aspect
ratio, no text, no logos.
```

**紐づく台本**: 「正直、日本には期待してなかった…」（マノン・デュボワ、上海の駅で母を助ける人が誰もいなかった経験から、日本での財布紛失・善意の連鎖エピソードへ）

**PhotoScape X 複製・配置・文字入れ指示**
| 要素 | 内容 |
|---|---|
| 複製方法 | 生成した1〜2種の顔画像を4回配置。完全同一だと不自然なので明るさ・拡大率・トリミング位置を1体ごとに微妙に変える |
| 配置 | 横一列、肩が触れるくらいの間隔で密集 |
| 怒りマーク | 赤い角ばった爆発記号を各人の頭上に1個ずつ、位置を少しずらして配置 |
| 上部見出し | 「絶対に許さないから!!」黄色＋黒フチ4px、画面上部中央 |
| 下段1行目 | 「中国でブチギレたフランス人」水色＋黒フチ |
| 下段2行目 | 「その後…日本に来た結果」赤＋黒フチ（強調） |

---

## パターン5: 対峙構図（審査官vs女性）×背景案内板型

**元ネタ画像の特徴**
- 左: 白人男性の入国審査官（50代、頭髪後退、丸メガネ、濃紺制服、金属バッジ、腕組み、鋭く真剣な表情）
- 右: 派手な身なりの女性（巻き髪、毛皮/アニマル柄コート、大きなフープピアス、サングラスを頭上に、眉をひそめて不機嫌な顔、赤い日本国旅券を突き出すように見せている）
- 中央下に「●●●」（沈黙・間の演出）
- 背景にぼやけた日本語フレーズの案内表示（「いただきます」「よろしくお願いします」「お手数をおかけします」）
- 上部見出し「日本人なら答えられる…よね？」黄色＋黒フチ
- 下段1行目「アメリカの空港で暴れる自称日本人」水色＋黒フチ
- 下段2行目「審査官の質問で正体が暴かれた理由」赤＋黒フチ

**画像生成プロンプト（第3版・顔の見え方/パスポート再現性/表情を強化。クライアントFB「顔が見えない」「パスポートが日本のものに見えない」「表情をもっと大げさに」を反映）**
```
Professional photorealistic editorial photo, candid documentary style, of
a tense face-to-face confrontation in a US airport secondary inspection
room. On the left, a serious American male immigration officer in his
mid-50s, receding gray hair, round wire-frame glasses, navy blue uniform
with a metal badge, arms crossed, sharp and skeptical expression, sitting
behind a desk.

On the right, a breathtakingly beautiful woman in her late 20s, supermodel
-level facial features, flawless glowing skin, striking and glamorous,
voluminous wavy brown hair pushed back so her full face is clearly
visible to the camera (NOT in profile, NOT obscured by hair — face fully
visible at a three-quarter angle toward the viewer). Sunglasses pushed up
on her head, large gold hoop earrings, wearing a flashy leopard-print fur
coat. Her expression is exaggerated and dramatic — deeply furrowed brows,
mouth open mid-argument, an indignant scowl clearly readable even at
thumbnail size, more theatrical than a subtle expression.

She holds up an authentic Japanese passport toward the officer: a deep
maroon/wine-red cover, a gold 16-petal imperial chrysanthemum emblem
centered on the front, gold Japanese kanji text "日本国旅券" arranged
above the emblem, and gold English text "JAPAN" and "PASSPORT" below the
emblem — rendered accurately and legibly, matching the real Japanese
passport design.

Background: a blurred wall-mounted display showing faint Japanese text
phrases in a clean sans-serif font on a blue background, out of focus,
suggesting an official signage board. Bright, neutral fluorescent airport
lighting, clean institutional atmosphere. Medium-wide framing showing
both subjects from the chest up, generous negative space around them for
cropping and compositing. Shot on 50mm lens, moderate depth of field with
both subjects in sharp focus. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「本当に日本人なら分かるはずです…」（LA空港の審査官デイビッドが、なりすまし女性を「いただきます」「よろしくお願いします」「お手数をおかけします」の3つの言葉で見抜くエピソード）

**PhotoScape X 文字入れ指示（上位互換版）**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| 上部見出し | 「日本人なら、答えられますよね?」 | 黄色＋黒フチ4px | 画面上部中央 |
| 沈黙記号 | 「●●●」 | 黒 | 画面中央下、2人の間 |
| 下段1行目 | 「28年のベテラン審査官が見抜いた"自称日本人"」 | 水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「たった3つの言葉で、嘘は全て崩れた」 | 赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン6: 雑踏の引きショット×赤丸強調型

**元ネタ画像の特徴**
- これまでのクローズアップ肖像型と異なり、広角の環境ショット＋赤丸で視線誘導する新しい型
- 空港ターミナルの広角ショット（成田風、木目調の床、オレンジ色の椅子、多くの旅行者が行き交う）
- 中央やや左に、スーツ姿の日本人男性が外国人の男の子を抱きかかえて歩いている場面を赤い点線の丸で強調
- 「⁉」記号を画面左右に2つ配置
- 上部見出し「オイオイ、嘘だろ！？日本人！」黄色＋黒フチ
- 下段1行目（白/水色）「成田空港で偶然撮影されたわずか10秒の映像が」
- 下段2行目（赤）「拡散され世界が絶賛した理由」

**画像生成プロンプト（第3版・引き・向き・親子の対比を修正済み）**

初版は被写体が主役化しすぎ、第2版は群衆に埋もれさせるところまでは改善したが、①まだ画角が元ネタほど引いていない、②被写体が後ろ向き/横向きで顔が見えない、③父子の国籍対比（父=日本人、子=白人）が判別できない、という3点のズレが残った。以下は修正版。

```
Photorealistic ultra-wide-angle candid photo of a very busy Japanese
airport terminal concourse (Narita-style), warm honey-toned wood
flooring, rows of orange cushioned chairs, tall floor-to-ceiling windows,
bright natural daylight. The shot is framed wider and further back than
a typical photo — dozens of travelers of various nationalities fill the
frame at a natural, ordinary pace, business people with briefcases,
students with backpacks, people rolling suitcases, some seated checking
phones. The whole space should feel expansive, not tightly cropped.

Somewhere in the crowd, roughly centered but not isolated, a Japanese
businessman in his 50s, black hair, ordinary dark suit, is walking while
gently carrying a young Western boy in his arms — the boy has visibly
light/blond hair and fair skin, a clear visual contrast to the man's
Japanese features, so the pairing reads at a glance as father-and-child
from different backgrounds. They are angled roughly three-quarters toward
the camera (not walking away with backs turned) so their faces are
visible at a normal viewing distance, same as the surrounding pedestrians.

This pair should NOT be more sharply focused, more brightly lit, or
otherwise visually emphasized compared to the surrounding pedestrians —
same size, distance, and focus level as everyone else, easy to miss on
first glance. Overall even, snapshot-like focus across the whole scene,
natural candid photojournalism style, realistic skin tones and textures,
avoid airbrushed CGI look. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「オイオイ、嘘だろ？日本人!?」（脳性麻痺の息子イーサンを連れたマイケル・ハリスが、成田空港で見知らぬ会社員に息子を抱えて助けられるエピソード）

**PhotoScape X 合成・文字入れ指示**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| 赤丸強調 | 点線の楕円で男性+男の子のペアを囲む | 赤 | 画面中央やや左 |
| 「⁉」記号 | 2箇所配置 | 赤 | 画面左上・右上 |
| 上部見出し | 「オイオイ、嘘だろ！？日本人！」 | 黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「成田空港で偶然撮影されたわずか10秒の映像が」 | 白/水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「拡散され世界が絶賛した理由」 | 赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン7: 1人クローズアップ驚愕×相手後ろ姿型

**元ネタ画像の特徴**
- メインはブロンドの女性、驚愕・ショックの表情（目を見開き、片手で口を覆う）
- 背景はファストフード店内（赤い看板・照明要素、ぼやけた他の客）
- 右端に男性の後ろ姿（会話相手、顔は見えない、添え物的な配置）
- 「⁉」記号を女性の右側に配置
- 上部見出し「何食べてもマズイ...!?」黄色＋黒フチ
- 下段1行目「帰国後パニックに陥る外国人」水色＋黒フチ
- 下段2行目「日本で味覚崩壊した理由」赤＋黒フチ

**画像生成プロンプト（第3版・カメラ目線・中央配置・背景具体化・美人セクシー強化。クライアントが構図に満足したため以後はこの版をベースにする）**
```
Professional photorealistic editorial photo, candid documentary style, of
a breathtakingly beautiful American woman in her 40s, supermodel-level
facial features, flawless glowing skin, glamorous and sexy, wavy honey-
blonde hair, a fitted stylish top with a flattering neckline, sitting in
a fast-food restaurant, positioned close to the center of the frame. She
is looking directly at the camera, direct eye contact with the viewer,
with a genuinely shocked, horrified expression — eyes wide open,
eyebrows raised high, one hand pressed over her open mouth as if she
just realized something disturbing about the food in front of her.
Natural real-photo skin texture, avoid airbrushed CGI look, avoid uncanny
valley, striking magazine-editorial level beauty.

To the right edge of the frame, partially visible and out of focus, the
back of a man's head and shoulder, seated across from her, blurred and
clearly secondary to the composition.

Background: a generic American fast-food restaurant interior evoking a
casual burger chain — bold red and yellow color accents, a blurred
illuminated menu board, plastic booth seating, warm bright indoor
lighting — but with no real brand logos, trademarks, or readable text.
Medium-close framing on the woman from the chest up, roughly centered in
the frame, generous negative space around her for cropping and
compositing. Shot on 85mm lens, shallow depth of field with only the
woman in sharp focus. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「帰国したら何を食べても不味い!」（外食チェーン商品開発責任者レイチェル・モーガンが、日本の天ぷら職人・うどん店の仕事ぶりに触れ、効率至上主義の価値観が揺らぐエピソード）

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| 上部見出し | 「何食べてもマズイ...!?」 | 黄色＋黒フチ4px | 画面上部中央 |
| リアクション記号 | ⁉ | 赤 | 女性の顔の右側 |
| 下段1行目 | 「帰国後パニックに陥る外国人」 | 水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「日本で味覚崩壊した理由」 | 赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン8: 同一人物3コマ連続リアクション型

**元ネタ画像の特徴**
- 同一人物と思われる若い女性の3コマ連続リアクション（左→中→右で表情が変化）
- 共通の外見: ウェーブがかった茶色〜ブロンドの髪、ゴールドフープピアス、ネックレス、頬にほんのり赤み（艶っぽいメイク）
- 左: 目を見開いて横目で驚く／中: 戸惑いながら口を開け横を見る／右: 手で口を覆って驚愕、背景にトイレの洗面台
- 「⁉」記号をコマとコマの間に2箇所
- 上部見出し「え、ここでするの…!?」黄色＋黒フチ
- 下段1行目「日本の無料トイレに入って3秒後…」水色＋黒フチ
- 下段2行目「外国人の態度が一変した理由」赤＋黒フチ

**制作方式（第3版・最終）**: 当初は「同一人物の連続リアクション」と誤認しキャラクター統一方式で設計→クライアント指摘で3人の別人と判明し3枚個別生成方式に変更→さらにクライアントより「3枚合成ではなく1枚のサムネイル画像として3人が自然に横並びになるよう一括生成してほしい」と指摘。CA5人型・4人型と同じ「1枚に複数人を一括生成」方式に統一。

**画像生成プロンプト（1枚に3人一括生成）**
```
Professional photorealistic editorial photo, candid documentary style, of
three beautiful young Western women in their mid-20s standing naturally
side by side in a bright, clean Japanese public restroom, blurred sinks
and mirrors visible in the background. Each woman has a distinctly
different face and hair color — one with wavy chestnut-brown hair, one
with wavy honey-blonde hair with bangs, one with straight golden-blonde
hair — all with magazine-editorial level beauty, warm sun-kissed skin
with naturally flushed rosy cheeks, dewy glowing makeup look, gold hoop
earrings. Natural real-photo skin texture, avoid airbrushed CGI look,
avoid uncanny valley, avoid identical or mirrored faces between them.

All three share a moment of surprise upon entering the restroom, but with
varying intensity: the woman on the left has a wide-eyed startled look,
glancing sideways with raised eyebrows; the woman in the center looks
confused and uncertain, mouth slightly open as if mid-sentence, glancing
to the side; the woman on the right is the most shocked, eyes wide, one
hand pressed over her open mouth in disbelief. They are positioned close
together at roughly the same height and distance from camera, a natural
group composition rather than a rigid lineup.

Bright, clean, warm indoor lighting. Medium-close framing from the chest
up, generous negative space around the group for cropping and
compositing. Shot on 50mm lens, shallow depth of field with the group in
sharp focus. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「え…本当にここでするの!?」（オーストラリア人公共施設管理者ポール・ベネットが、富士山麓の道の駅の無料トイレの清掃員の姿勢に触れ、25年間の不信感が変わるエピソード）

**PhotoScape X 文字入れ指示**
| 要素 | 内容 |
|---|---|
| 「⁉」記号 | 左の女性と中央の女性の間、中央と右の女性の間に1つずつ |
| 上部見出し | 「え、ここでするの…!?」黄色＋黒フチ4px |
| 下段1行目 | 「日本の無料トイレに入って3秒後…」水色＋黒フチ |
| 下段2行目 | 「外国人の態度が一変した理由」赤＋黒フチ（強調） |

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

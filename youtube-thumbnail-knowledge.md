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

**画像生成プロンプト（第4版・群衆が全員後ろ向きになる問題を修正）**

第3版でもまだ、群衆のほぼ全員が奥に向かって歩く後ろ姿になってしまう問題が残っていた。歩く向きのバリエーションを明示的に指定して修正。

```
Photorealistic ultra-wide-angle candid photo of a very busy Japanese
airport terminal concourse (Narita-style), warm honey-toned wood
flooring, rows of orange cushioned chairs, tall floor-to-ceiling windows,
bright natural daylight. The shot is framed wider and further back than
a typical photo — dozens of travelers of various nationalities fill the
frame. The whole space should feel expansive, not tightly cropped.

CRITICAL: Travelers walk in many different directions, not all in the
same direction. A substantial number of pedestrians walk toward the
camera or diagonally across the frame, so their faces are clearly visible
(NOT everyone shown from behind walking away into the distance). Mix of
people walking toward camera, away from camera, and crossing left-to-
right or right-to-left, business people with briefcases, students with
backpacks, people rolling suitcases, some seated checking phones.

Somewhere in the crowd, roughly centered but not isolated, a Japanese
businessman in his 50s, black hair, ordinary dark suit, is walking while
gently carrying a young Western child in his arms — the child has visibly
light/blond hair and fair skin, a clear visual contrast to the man's
Japanese features. They are angled roughly three-quarters toward the
camera (NOT walking away with backs turned) so their faces are clearly
visible at a normal viewing distance, same as the surrounding pedestrians.

This pair should NOT be more sharply focused, more brightly lit, or
otherwise visually emphasized compared to the surrounding pedestrians —
same size, distance, and focus level as everyone else, easy to miss on
first glance. Overall even, snapshot-like focus across the whole scene,
natural candid photojournalism style, realistic skin tones and textures,
avoid airbrushed CGI look. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**:
- 「オイオイ、嘘だろ？日本人!?」（脳性麻痺の息子イーサンを連れたマイケル・ハリスが、成田空港で見知らぬ会社員に息子を抱えて助けられるエピソード）
- 「オイオイ、嘘だろ？日本人⁉」（同型の別台本。脳性麻痺の娘エマを連れたデイヴィッド・コリンズが、成田空港で見知らぬ会社員に娘を抱えて助けられるエピソード。プロンプト中の "young Western boy" を "young Western girl" に置き換えて使用）

**運用メモ**: この型は複数の類似台本（父親×障害のある子×空港での親切エピソード）で使い回されている。台本が変わっても画像・文字入れは基本的に共通のプロンプトを流用し、性別など細部だけ差し替えればよい。

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

## パターン9: 電車内家族×国旗アイコン×吹き出し型

**元ネタ画像の特徴**
- 電車内（新幹線風、青いシート、白い枕カバー）に母親と娘2人が並んで座っている
- 母親（40代、グレーのカーディガン、黒タートルネック）は窓の外を見つめる悲しげな表情、「ごめんね…」の吹き出しテキストが添えられている
- 長女（17歳、黒髪ロングストレート、俯いた悲しい表情、紺パーカー）
- 次女（14歳、眼鏡、黒髪ボブ、俯いた表情、紺パーカー）
- 画面左上に中国国旗、右上に日本国旗のアイコンを配置（対比構造）
- 背景に他の乗客がぼやけて見える
- 上部見出し「もう日本に帰れないの？」黄色＋黒フチ
- 下段1行目「在留資格切れで中国人一家が帰国」水色＋黒フチ
- 下段2行目「母国到着5分で全員が絶望」赤＋黒フチ
- これまでの「驚き・怒り」系と違い、「悲しみ・後悔」の感情を扱う初のパターン

**画像生成プロンプト（第2版・中国人らしさと母親の表情を強化）**
```
Photorealistic candid documentary-style photo inside a Japanese shinkansen
or express train car, blue upholstered seats with white headrest covers,
other blurred passengers visible in the background rows. A Chinese mother
in her early 40s, clearly of Chinese ethnicity with features typical of
southern China (Guangzhou region), wearing a gray cardigan over a black
turtleneck, sits by the window. Her expression is exhausted and remorseful
— shoulders slightly slumped, head tilted down, eyes downcast with deep
guilt and quiet shame, as if silently apologizing to herself, far more
weary and regretful than a simple sad look.

Beside her, her two daughters, also clearly of Chinese ethnicity, sit in
a row: the elder daughter, about 17, long straight black hair, wearing a
navy hoodie, looking down with a melancholic, downcast expression. The
younger daughter, about 14, wearing glasses, black bob haircut, navy
hoodie, also looking down, subdued and tired.

All three have genuine, understated sad expressions, natural real-photo
skin texture, avoid airbrushed CGI look, avoid uncanny valley. Soft
natural daylight through the train window, warm but muted color tone
reflecting the somber mood. Medium-wide framing showing all three from
the waist up, generous negative space around them for cropping and
compositing. Shot on 50mm lens, moderate depth of field. 16:9 aspect
ratio, no text, no logos.
```

**紐づく台本**: 「中国の方が日本より快適に決まってる…」（中国人女性ワン・メイリンが在留資格切れで娘2人と一時帰国し、広州の実家で食の安全性の違いに直面するエピソード）

**PhotoScape X 合成・文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 中国国旗アイコン | 実際の国旗素材画像を配置（生成不要） | 画面左上 |
| 日本国旗アイコン | 実際の国旗素材画像を配置（生成不要） | 画面右上 |
| 吹き出し「ごめんね…」 | 白背景の吹き出し、黒文字 | 母親の口元付近 |
| 上部見出し | 「もう日本に帰れないの？」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「在留資格切れで中国人一家が帰国」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「母国到着5分で全員が絶望」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン10: モノクロ親子抱擁×国旗1つ×吹き出し型

**元ネタ画像の特徴**
- モノクロ（白黒）写真、これまでの全パターンと違う初めての演出
- 父親が娘を優しく抱きしめ、頬を寄せている構図
- 父親: 短髪、ヨーロッパ系、目を伏せて憂いのある切ない表情
- 娘: 金髪、悲しげな瞳でカメラ目線
- 画面左上にドイツ国旗（1つのみ、パターン9は2つだった）
- セリフ吹き出し「パパ、日本に行きたい…」を人物の横に配置
- 上部見出し「パパ、日本に行きたい…」黄色＋黒フチ（吹き出しと同じ文言を大きく強調）
- 下段1行目「余命宣告された娘の最期の願いを叶えに」水色＋黒フチ
- 下段2行目「訪れた日本で起きた奇跡とは？」赤＋黒フチ

**画像生成プロンプト（第2版・娘の年齢が成人女性化する問題を修正、父も若く）**

初版では娘が成人女性のように生成されてしまった（AIは「young girl」の指定だけでは大人化しやすい）。子供の身体的特徴を明示的に記述して修正。

```
Black-and-white photorealistic editorial portrait, emotionally intimate
documentary style. A German father in his mid-to-late 30s, short neatly
-cut hair, European features, youthful appearance, tenderly embraces his
young daughter, cheek gently pressed against the top of her head, eyes
closed or downcast with a quiet, sorrowful, weary expression — a man
holding back deep emotion.

His daughter is a young girl, exactly 9 years old — child-sized body
proportions, a small, round, youthful face with soft baby-fat cheeks,
short stature clearly consistent with a child, NOT an adult woman, NOT a
teenager. Blonde hair, held close in her father's arms, looking directly
at the camera with sad, wistful eyes, a fragile and melancholic
expression, as if silently pleading — the innocent, delicate features of
an actual 9-year-old child.

Simple neutral gray studio-style background, soft directional lighting
creating gentle shadows and highlights across their faces, classic black-
and-white portrait photography with rich tonal contrast. Natural real-
photo skin texture, avoid airbrushed CGI look, avoid uncanny valley.
Medium-close framing from the chest up, generous negative space around
them for cropping and compositing. Shot on 85mm lens, shallow depth of
field. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「パパ、最後に日本に行きたい…」（ドイツ人エンジニアのトーマス・ベルクマンが、余命宣告を受けた娘レアの願いで来日、大阪の病院で誤診が判明し娘が救われるエピソード）

**PhotoScape X 合成・文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| ドイツ国旗アイコン | 実際の国旗素材画像を配置（生成不要） | 画面左上 |
| セリフ吹き出し | 「パパ、日本に行きたい…」白背景吹き出し、黒文字 | 人物の横 |
| 上部見出し | 「パパ、日本に行きたい…」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「余命宣告された娘の最期の願いを叶えに」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「訪れた日本で起きた奇跡とは？」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン11: 涙のクローズアップ×空港窓外の街並み型

**元ネタ画像の特徴**
- メインは1人の女性、涙を流しながら頬を拭う、疲れた自然な表情（化粧っ気は控えめ、長旅の疲労感がある）
- 「⁉」記号を顔の右上に配置
- 背景は空港到着ロビー、大きな窓越しに曇り空と都市の建物群、ぼやけた他の乗客やスーツケース
- 上部見出し「これは一体、何ですか…!?」黄色＋黒フチ
- 下段1行目「日本に来るため10年貯金したポーランド人女性」水色＋黒フチ
- 下段2行目「日本上陸直後に泣き崩れた理由」赤＋黒フチ

**画像生成プロンプト（第2版・服装/背景の高層ビル/表情を修正）**

初版は黒いカーディガンになり、背景が高層ビル群（マンハッタン風）になってしまい、元ネタの「明るめグレーの服・低層の日本的な街並み」と乖離した。以下は修正版。

```
Photorealistic candid documentary-style close-up portrait of a Polish
woman in her late 30s, wavy brown hair slightly disheveled from a long
flight, natural minimal makeup, wearing a light gray casual sweater/hoodie
(NOT a dark cardigan). Tired but genuine expression, overwhelmed with
emotion. She is crying — eyes red and glistening with tears, tears
visibly streaking down her cheeks, one hand raised to wipe her cheek,
mouth open wider in a mix of shock, disbelief, and overwhelmed emotion —
more startled and open-mouthed than a subtle quiet cry. Natural real-
photo skin texture with visible pores and realistic imperfections, avoid
airbrushed CGI look, avoid uncanny valley — she should look like an
ordinary, real woman worn out from travel, not glamorous or posed.

Background: an airport arrival lounge with large floor-to-ceiling windows
showing an overcast gray sky and a LOW-RISE Japanese cityscape in the
distance — modest low buildings spread out toward the horizon, NOT a
skyline of tall skyscrapers, NOT a Manhattan-style skyline. Blurred
fellow travelers and luggage further back. Soft, slightly cool natural
window light matching the cloudy sky. Medium-close framing from the chest
up, generous negative space around her for cropping and compositing.
Shot on 85mm lens, shallow depth of field with only the woman in sharp
focus. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「10年かけて貯めた貯金が、数日で消えた…」（ポーランド人女性カタジナ・ノヴァクが10年間貯金して来日、羽田空港で整備士が飛行機に敬礼する光景に涙し、落とし物の封筒が無事戻ってくるエピソード）

**制作メモ**: このパターンは「美人でセクシー」路線ではなく、長旅で疲れた自然体のリアルな表情が求められる構図（元ネタも化粧控えめ・涙で顔が濡れた飾らない印象）。美人化要望が来た場合は「疲労感・素朴さは保ったまま整った顔立ちにする」バランス調整が必要になる想定。

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| 上部見出し | 「これは一体、何ですか…!?」 | 黄色＋黒フチ4px | 画面上部中央 |
| リアクション記号 | ⁉ | 赤 | 女性の顔の右上 |
| 下段1行目 | 「日本に来るため10年貯金したポーランド人女性」 | 水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「日本上陸直後に泣き崩れた理由」 | 赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン12: 夜の空港×手前驚き男女×背景群衆矢印強調型

**元ネタ画像の特徴**
- 夜間の空港ロビー、青みがかった照明、窓の外は暗い夜景
- 手前に外国人の男女2人、驚いた表情でカメラ目線
- 「⁉」記号と小さい吹き出し「あれは何…!?」
- 背景に多数の乗客が床に座り込んで待機している光景（欠航による足止め）
- 赤い矢印で背景の座り込む乗客群の一部を指し示す（パターン6の「引きショット＋矢印強調」に近い要素）
- 上部見出し「こんな国、ありえるのか…?」黄色＋黒フチ
- 下段1行目「全便欠航で羽田に足止めされたイギリス人旅行者」水色＋黒フチ
- 下段2行目「朝5時のロビーで見た光景とは」赤＋黒フチ

**画像生成プロンプト**
```
Photorealistic candid documentary-style photo at night inside a Japanese
airport terminal (Haneda-style), cool blue-toned ambient lighting, dark
night sky visible through large windows. In the foreground, medium-close,
a British man in his early 40s and a Western woman in her late 20s to
30s, both with genuinely startled, wide-eyed expressions, looking toward
something off-frame with surprise and disbelief, mouths slightly open.

In the background, softly blurred but visible, hundreds of stranded
travelers sit quietly on the floor on thin mats in neat, orderly rows,
some with blankets, a calm and orderly atmosphere despite the crowding —
no chaos, no mess, everyone seated calmly. The scene should feel eerily
peaceful for a flight-cancellation crowd.

Natural real-photo skin texture, avoid airbrushed CGI look, avoid uncanny
valley. Medium-wide framing with generous negative space around the two
foreground subjects for cropping and compositing. Shot on 50mm lens,
shallow depth of field with the two foreground people in sharp focus and
the background crowd softly blurred. 16:9 aspect ratio, no text, no
logos.
```

**紐づく台本**: 「こんな国があり得るのか…？」（ヒースロー空港運行管理歴15年のイギリス人トーマス・ハワードが、台風で羽田に足止めされ、深夜に見知らぬ老人乗客・佐藤さんが誰に頼まれるでもなく秩序を保つ姿に価値観を揺さぶられるエピソード）

**制作メモ**: サムネの女性は台本本文には明示的に登場しないキャラクター（旅の連れ、または感情移入を誘う演出上の追加人物）。台本には登場しないが、サムネの構図としてそのまま採用。

**PhotoScape X 合成・文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 赤い矢印 | 背景の座り込む乗客群の一部を指し示す | 画面中央〜左寄り |
| 「⁉」記号＋吹き出し「あれは何…!?」 | 白背景吹き出し＋赤記号 | 男性の頭上付近 |
| 上部見出し | 「こんな国、ありえるのか…?」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「全便欠航で羽田に足止めされたイギリス人旅行者」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「朝5時のロビーで見た光景とは」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン13: 和室対面母娘×朝食膳×矢印強調型

**元ネタ画像の特徴**
- 旅館の和室（畳、障子、座布団、床の間の飾り棚）
- 左に母親（30代後半、茶色いウェーブヘア、グレーのセーター）、優しい笑顔でこちらを見る、吹き出し「最高でしょ？」
- 右に娘（9歳、茶髪、薄紫のセーター）、目を見開いて驚いた表情、口が半開き、吹き出し「なにこれ…！」＋「‼」マーク
- 座卓に和朝食の膳：ご飯茶碗、味噌汁椀、漬物・煮物の小鉢、焼き魚の切り身
- 赤い矢印で焼き魚の皿を指し示す
- 上部見出し「朝ごはん、こんなに豪華なの？」黄色＋黒フチ
- 下段1行目「偏食のイギリス人少女が日本旅館で見た朝食」水色＋黒フチ
- 下段2行目「一口食べて人生が激変した理由」赤＋黒フチ

**画像生成プロンプト**
```
Photorealistic candid documentary-style photo inside a traditional
Japanese ryokan tatami room, low wooden table, shoji sliding doors in
the background, a tokonoma alcove shelf with a small plant, floor
cushions (zabuton) visible. On the left, a British mother in her late
30s, brown wavy shoulder-length hair, wearing a gray sweater, sitting at
the low table with a warm, gentle smile, looking toward her daughter.

On the right, her daughter, about 9 years old, long brown hair, wearing
a light purple sweater, sitting at the table with a genuinely astonished
expression — eyes wide open, mouth slightly parted in surprise, staring
down at the elaborate breakfast spread in front of her.

On the table between them, an elaborate traditional Japanese breakfast
set: a bowl of white rice, a lacquered miso soup bowl, small side dishes
of pickles and simmered vegetables, and a plate with a grilled fish
fillet, all arranged neatly. Soft natural morning light filtering through
the shoji screens. Natural real-photo skin texture, avoid airbrushed CGI
look, avoid uncanny valley. Medium-wide framing showing both figures from
the waist up and the full table spread, generous negative space around
them for cropping and compositing. Shot on 35mm lens, moderate depth of
field. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「朝ごはん、なんでこんなに豪華なの?」（極度の偏食児エラ・ハーパーが、日本海沿いの旅館の仲居さゆきさんの3日間変わらぬ朝食への向き合い方に触れ、初めて自分から食事を口にするエピソード）

**PhotoScape X 合成・文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 赤い矢印 | 焼き魚の皿を指し示す | 皿の右上 |
| 母親の吹き出し | 「最高でしょ？」白背景吹き出し、黒文字 | 母親の口元付近 |
| 娘の吹き出し＋記号 | 「なにこれ…！」＋「‼」 | 娘の頭上付近 |
| 上部見出し | 「朝ごはん、こんなに豪華なの？」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「偏食のイギリス人少女が日本旅館で見た朝食」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「一口食べて人生が激変した理由」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン14: 4人グループ×路地裏暖簾×矢印強調型

**元ネタ画像の特徴**
- 東京下町の古い路地（木造建築、赤提灯、紺色の暖簾）
- 手前に4人のフランス人（年配の男性、若い男性、女性2人）、全員が驚いた表情でこちらを見る
- 「⁉」「?!」の記号2つ
- 吹き出し「聞いてないよ…」
- 赤い矢印で暖簾を指し示す
- 上部見出し「嘘だろ…この店で食べるのか？」黄色＋黒フチ
- 下段1行目「フランス人ソムリエが東京下町の大衆居酒屋へ」水色＋黒フチ
- 下段2行目「暖簾の先で見た衝撃の光景とは」赤＋黒フチ

**画像生成プロンプト（第4版・元ネタとの寄り/配置/光のズレを修正）**

第3版でAI感は改善したが、クライアントが元ネタ画像を再提示し「もっと寄せてほしい」と指摘。元ネタは①顔のドアップ（肩の一部のみ）、②手前が最大で奥へ行くほど重なって小さくなる遠近配置（CA5人型と同じロジック）、③暖簾・提灯が近く大きめに見える、④日中の柔らかい拡散光（夕暮れの暖色ではない）という特徴があり、第3版はこれらとズレていた。以下は修正版。

```
Photorealistic candid documentary-style extreme close-up photo of four
French travelers' faces, shot from very close range — framing shows
mostly faces and just a hint of shoulders, NOT a waist-up shot. The
group is arranged in a receding diagonal cluster: the older man in the
front-left is closest to the camera and largest in frame, with the other
three overlapping behind him at progressively smaller sizes and slightly
greater distance, creating a natural depth stack (similar to a tight
huddled group looking at the same thing).

The group: an older French man in his early 50s in front, dark suit,
graying hair, mouth open in shock; behind him, a French man in his late
30s with short beard, startled; two French women in their 30s-40s
further back, one with a scarf, each with a genuinely different
intensity and shape of surprised expression — not identical.

Background, closer and larger than a distant backdrop: an old wooden
Tokyo backstreet alley softly blurred, a red paper lantern glowing
nearby, a well-worn indigo noren curtain hanging over a doorway,
relatively close and clearly visible though softly out of focus behind
the sharp foreground faces.

Lighting: soft, diffused daytime natural light, slightly backlit, NOT
warm golden-hour tones — overcast-daylight quality. Natural real-photo
skin texture with visible pores and asymmetry, avoid airbrushed CGI look,
avoid uncanny valley, avoid a flat AI-rendered look. Shot on 85mm lens,
shallow depth of field with only the front one or two faces in sharpest
focus. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「え、ここは天国なの…⁉」（パリの三つ星レストランでシェフソムリエを26年務めたリュック・モローが、蔵人の藤田に連れられ東京下町の12席の酒場を訪れ、格付けや数字では測れない人へのまなざしに触れるエピソード）

**PhotoScape X 合成・文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 赤い矢印 | 暖簾を指し示す | 暖簾の左上 |
| 「⁉」「?!」記号 | 2箇所 | 人物の頭上付近2箇所 |
| 吹き出し「聞いてないよ…」 | 白背景吹き出し、黒文字 | 女性の口元付近 |
| 上部見出し | 「嘘だろ…この店で食べるのか？」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「フランス人ソムリエが東京下町の大衆居酒屋へ」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「暖簾の先で見た衝撃の光景とは」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン15: 空港ロビー4人家族×困惑表情×セリフ吹き出し型

**元ネタ画像の特徴**
- 空港ロビー、明るい室内、背景にぼやけた他の乗客と椅子
- 4人家族が横並び：父（40代後半、黒髪短髪、黒いジャケット）、息子（13歳、茶髪、グレーのパーカー）、娘（10歳、茶色い長髪）、母（ブロンド、ベージュのコート）
- 全員が困惑・心配そうな深刻な表情でこちらを見ている
- 「⁉」「?!」記号が父と母の頭上に
- 娘の吹き出し「どこ行くの…？」
- 上部見出し「日本だと言えなかった…」黄色＋黒フチ
- 下段1行目「旅行先を伏せたまま子どもたちを空港へ連れ出し」水色＋黒フチ
- 下段2行目「兄妹が泣き崩れ世界が騒然」赤＋黒フチ

**画像生成プロンプト**
```
Photorealistic candid documentary-style photo of a British family of
four sitting together in an airport departure lounge, bright indoor
lighting, blurred fellow travelers and seating rows in the background.

The father, late 40s, short dark hair, wearing a black jacket, has a
worried, conflicted expression, brows furrowed. Beside him, his son,
about 13, light brown hair, wearing a gray hoodie, looks uneasy and
guarded. Next to him, his younger sister, about 10, long light brown
hair, looking directly at the camera with an anxious, questioning
expression. On the far side, the mother, blonde shoulder-length hair,
wearing a beige coat, has a similarly worried expression, brows raised
slightly with concern.

All four share a subdued, tense, uncertain mood — not shock or excitement,
but quiet worry and unspoken tension within the family. Natural real-
photo skin texture, avoid airbrushed CGI look, avoid uncanny valley.
Medium-wide framing showing all four from the chest up, generous
negative space around them for cropping and compositing. Shot on 50mm
lens, moderate depth of field. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「え、本当に日本に行くの?…」（活版印刷職人ダニエル・ハーパーが、3年前の旅行中止のトラウマから空港到着まで行き先を伏せ、日本滞在中に息子ノアの心が少しずつ開いていくエピソード）

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 「⁉」記号 | 父の頭上 | 父の右上 |
| 「?!」記号 | 母の頭上 | 母の右上 |
| 娘の吹き出し | 「どこ行くの…？」白背景吹き出し、黒文字 | 娘の口元付近 |
| 上部見出し | 「日本だと言えなかった…」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「旅行先を伏せたまま子どもたちを空港へ連れ出し」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「兄妹が泣き崩れ世界が騒然」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン16: 涙の娘×寄り添う母×空港窓外の飛行機型

**元ネタ画像の特徴**
- 空港ロビー、窓の外に駐機中の飛行機、ぼやけた他の乗客
- 左: 父（50代後半、白髪交じりの短髪、黒Tシャツ＋グレーのジップパーカー）、やや離れた位置で心配そうな表情
- 中央: 娘（18歳、ブロンドの巻き髪、涙を流している、悲しげな表情）
- 右: 母（ブロンドのまとめ髪、ベージュのカーディガン）、娘の顔を覗き込むように心配そうに向き合う
- 「?!」記号が父と母の頭上に2つ
- 上部見出し「ママ、もう日本に住もうよ」黄色＋黒フチ
- 下段1行目「10日間の日本旅行を終え帰国するイギリス人一家」水色＋黒フチ
- 下段2行目「羽田空港で娘が崩れ落ちた理由」赤＋黒フチ

**画像生成プロンプト**
```
Photorealistic candid documentary-style photo in a Japanese airport
departure lounge, large windows showing a parked airplane and tarmac
outside, blurred fellow travelers seated in the background.

On the left, a father in his late 50s, graying short hair, wearing a
black t-shirt under a gray zip-up hoodie, standing slightly apart with
arms crossed, a worried, concerned expression on his face.

In the center, his 18-year-old daughter, long wavy blonde hair, visibly
crying — eyes red, tears streaking down her cheeks, a raw, emotional,
vulnerable expression, looking toward her mother.

On the right, the mother, blonde hair pulled back in a bun, wearing a
beige cardigan, leaning in close to her daughter, studying her face with
tender concern, one hand near her daughter's shoulder.

Natural real-photo skin texture, avoid airbrushed CGI look, avoid uncanny
valley. Soft natural daylight through the terminal windows. Medium-close
framing showing all three from the chest up, generous negative space
around them for cropping and compositing. Shot on 50mm lens, moderate
depth of field. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「ママ、もう帰りたくない」（人前で声を出すのが怖くなった18歳のソフィー・ベネットが、家族旅行の日本で空港職員への態度を後悔し、帰国前日の早朝に誰も見ていない時間に働くその職員の姿を見て涙するエピソード）

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 「?!」記号 | 父の頭上 | 父の右上 |
| 「?!」記号 | 母の頭上 | 母の右上 |
| 上部見出し | 「ママ、もう日本に住もうよ」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「10日間の日本旅行を終え帰国するイギリス人一家」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「羽田空港で娘が崩れ落ちた理由」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン17: 夜の飲み屋横丁×男女の驚き（横顔＋正面）×提灯と暖簾型

**元ネタ画像の特徴**
- 夜の飲み屋横丁、ネオンと提灯の灯り
- 左: 男性（50代、白髪交じりの短髪、青いシャツ）、横顔で見上げるように驚いた表情
- 右: 女性（50代、茶色い巻き髪）、正面向きで大きく口を開け目を見開く強い驚愕表情
- 「‼」記号1つ（男性の耳の近く）
- 背景: 赤提灯、黒地に白文字の「居酒屋」の暖簾、「やきとり」「もつ煮」「生ビール」の品書き札
- 上部見出し「えっ、ここで食べるの？」黄色＋黒フチ
- 下段1行目「初来日の外国人が日本好きになった」水色＋黒フチ
- 下段2行目「忘れられない衝撃の夜とは」赤＋黒フチ

**画像生成プロンプト**
```
Photorealistic candid documentary-style photo at night in a narrow
Japanese izakaya alley (yokocho-style), warm glowing red paper lanterns,
a black noren curtain with white Japanese text reading "居酒屋"
(izakaya), small illuminated menu signs on the wall reading "やきとり"
"もつ煮" "生ビール", neon signage glowing softly in the blurred
background, warm nighttime lighting typical of a Japanese drinking
alley.

In the foreground, an American man in his early 50s, graying short hair,
wearing a blue button-up shirt, shown in profile, looking upward and
sideways with a genuinely startled expression, mouth slightly open.

Beside him, his wife, also in her 50s, wavy brown hair, facing the
camera directly with an intensely shocked expression — eyes wide open,
eyebrows raised high, mouth wide open in astonishment, a floral scarf
around her neck.

Natural real-photo skin texture, avoid airbrushed CGI look, avoid uncanny
valley. Medium-close framing from the chest up, generous negative space
around them for cropping and compositing. Shot on 50mm lens, shallow
depth of field with the couple in sharp focus and the alley softly
blurred behind them. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「ここは天国なの…?」（何事も細かく予定を立てるニューヨークの商社マンダニエル・ターナーが、予約日を間違えたことがきっかけで路地裏の小さな居酒屋に入り、予定にない出会いの楽しさを知るエピソード）

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 「‼」記号 | 男性の耳の近く | 男性の右上 |
| 上部見出し | 「えっ、ここで食べるの？」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「初来日の外国人が日本好きになった」水色＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「忘れられない衝撃の夜とは」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン18: 状況再現型（人物不在・日本の日常光景が主役）

**元ネタ画像の特徴**
- これまでの外国人クローズアップ型と異なり、外国人は画面に登場しない「状況再現ショット」
- 日中の住宅街の交差点、複数の車（白い車、黒いセダンなど）が横断歩道付近を走行・停止
- 手前右に小学生2人（黄色い通学帽、紺の制服、赤いランドセル）が横断歩道の脇に立っている
- 「!!!?」の記号、吹き出し「この後……」
- 上部見出し「あれは一体、なに！？」黄色＋黒フチ
- 下段1行目「日本旅行中のイギリス人夫婦」緑＋黒フチ
- 下段2行目「わずか7秒の衝撃的な光景に絶句!!」赤＋黒フチ

**画像生成プロンプト**
```
Photorealistic candid documentary-style photo of an ordinary Japanese
suburban intersection in daytime, multiple cars (a white sedan, a black
sedan, several other vehicles) traveling or stopped near a crosswalk with
clear white stripes, typical Japanese residential street with houses,
utility poles, and small shop signage in the background, natural bright
daylight.

In the foreground on the right side, two elementary school children stand
at the edge of the crosswalk, seen from behind or in three-quarter view:
both wearing yellow school safety hats, navy school uniforms, and
matching red randoseru backpacks (traditional Japanese school satchels),
waiting to cross.

Natural real-photo quality, documentary snapshot style, avoid airbrushed
CGI look, avoid uncanny valley. Wide-angle framing capturing the full
intersection and the children in the foreground, generous negative space
around the scene for cropping and compositing. Shot on 35mm lens,
moderate depth of field with everything reasonably in focus like a real
street photo. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「あれは一体なんだ…？」（元ロンドン警視庁警部補トーマス・ウィットフィールドが、日本の治安を疑いながら視察旅行に訪れ、信号のない横断歩道で小学生が見せた深いお辞儀に30年の信念を揺さぶられるエピソード）

**制作メモ**: これまでのパターンと異なり、外国人夫婦（トーマスとマーガレット）自体は画面に写らず、彼らが目撃した「状況」だけを再現する構図。この型は今後「衝撃的な光景そのものを見せる」系の台本で使い回せる。

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 「!!!?」記号 | 画面中央上部 | 交差点上空あたり |
| 吹き出し「この後……」 | 白背景吹き出し、黒文字 | 画面右上、子供たちの近く |
| 上部見出し | 「あれは一体、なに！？」黄色＋黒フチ4px | 画面上部中央 |
| 下段1行目 | 「日本旅行中のイギリス人夫婦」緑＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「わずか7秒の衝撃的な光景に絶句!!」赤＋黒フチ（強調） | 下部帯2行目 |

---

## パターン19: 俯瞰×カルガモの群れ×警察官交通規制型（人物不在）

**元ネタ画像の特徴**
- パターン18と同系統の「状況再現型」だが、俯瞰（ドローン/高所）アングルが新要素
- 日中の日本の住宅街の交差点を真上に近い斜め上から見下ろすアングル。横断歩道の白線が複数方向に伸びる十字路
- 交差点中央に、クリーム色〜薄茶色の綿毛のカルガモの子ガモの大群（100羽以上）が団子状に固まって道路を横断している
- 警察官5〜6名が交差点の各所（横断歩道脇・角）に立ち、紺の制服＋白い制帽姿で車両を止めてカルガモの群れを見守っている。走ったり慌てたりせず、静かに見守る立ち位置
- 警察官のうち1人の頭上に「!!?」記号（白地＋黒フチ）を配置し、驚き・注目を強調
- 車両は画面内にほぼ見えない（停止線の外またはフレーム外に処理されている）
- 背景は低層の住宅・電柱・街路樹など、日本的な生活道路の雰囲気
- 上部見出し「「日本の道路には神がいるのか…?」」黄色文字＋黒フチ、鍵カッコで囲む
- 下段1行目「日本の異様な光景を写した1分の映像」黄緑（ライムグリーン寄り）文字＋黒フチ
- 下段2行目「世界が驚愕し脅威の500万再生!!」赤文字＋黒フチ

**画像生成プロンプト**
```
Photorealistic aerial/high-angle documentary photo of an ordinary Japanese
residential street intersection in daytime, shot from a high oblique angle
(as if from a drone or a tall building) looking down at a crosswalk-marked
crossroads with clear white pedestrian-crossing stripes running in
multiple directions. Typical Japanese suburban townscape in the
background: low-rise houses, utility poles, small shop signage, street
trees, natural bright daylight, no harsh shadows.

In the center of the intersection, a large flock of fluffy cream-to-light-
brown baby ducklings (well over a hundred, mallard/domestic duckling
appearance) is clustered tightly together, waddling across the crosswalk
as a dense huddled mass, photographed from above so the flock reads as an
organic cluster shape on the asphalt.

Around the intersection, five to six Japanese traffic police officers in
navy-blue uniforms and white peaked caps stand calmly at the corners and
edges of the crosswalk, having stopped traffic so the ducklings can cross;
their postures are calm and attentive, not rushed or alarmed, some facing
toward the duckling cluster, positioned at slightly different distances
and angles for a natural, non-symmetrical arrangement. No vehicles visible
in frame, or only far in the background beyond the stop line.

Natural real-photo aerial documentary quality, avoid airbrushed CGI look,
avoid uncanny valley, avoid perfectly symmetrical or evenly-spaced
placement of the officers. Wide-angle high-angle framing capturing the
full intersection with generous negative space around the edges for
cropping and text compositing. 16:9 aspect ratio, no text, no logos, no
watermarks.
```

**紐づく台本**: パリの新聞記者クレール・デュボワ（44歳）。取材中のひったくり被害と警察の冷淡な対応をきっかけに人間不信に陥り、「秩序正しい日本社会は監視社会の産物に過ぎない」と疑って視察取材に訪れる。新宿の交差点で、警察官たちが車両を止めてカルガモの親子（子ガモの群れ）のために道を空け、誰一人苛立たず静かに見守る光景を目撃し、凍りついていた心が涙とともにほどける、という物語。

**制作メモ**: パターン18（状況再現型・人物不在）の派生バリエーション。今回新たに「俯瞰アングル」と「動物（カルガモ）×警察官」という要素が加わった。今後、動物がらみの心温まる日本の日常光景を扱う台本で、この俯瞰×人物不在の型を使い回せる。カルガモの群れは密集した塊として描写し、警察官の配置は均等になりすぎないよう非対称に散らすことでAI感を回避する。

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 位置 |
|---|---|---|
| 「!!?」記号 | 白地＋黒フチ、警察官の頭上に小さく配置 | 画面右上寄り、警察官の近く |
| 上部見出し | 「「日本の道路には神がいるのか…?」」黄色＋黒フチ4px、鍵カッコごと表示 | 画面最上部、横一杯 |
| 下段1行目 | 「日本の異様な光景を写した1分の映像」黄緑＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「世界が驚愕し脅威の500万再生!!」赤＋黒フチ（強調） | 下部帯2行目 |
| 上下レターボックス帯（任意） | 上下に薄い黒帯を敷いて見出し文字の視認性を上げる | 画面上端・下端 |

---

## パターン20: 姉妹2人ドアップ見下ろし×料理拒絶反応型

**元ネタ画像の特徴**
- パターン3（料理×家族リアクション左右分割型）と異なり、画面分割なしの1枚構図。少女2人と料理が同一フレーム内に収まっている
- 手前に金髪の少女2人（姉：長めのウェーブヘア、妹：やや幼い顔立ち）が身を乗り出し、テーブルに肘やお腹を預けて皿を見下ろしている
- 2人とも眉をひそめ、口を「への字」に結んだ強い警戒・拒絶の表情（美味しそうという反応では全くない）
- 皿の中身：黒々と艶のあるハンバーグ、ケチャップ味のナポリタン風スパゲティ、紫キャベツと千切りキャベツのコールスロー
- 背景は奥がぼかされた木目調のレストラン内装、うっすら他の客のシルエット
- 赤い矢印がハンバーグを指して強調
- 「⁉」記号が2つ、姉妹それぞれの頭上（左は黒文字、右は黒文字、どちらも白フチ）
- 白背景の吹き出し「ナニこれ？」（黒文字）が右の少女の右上に配置
- 上部見出し「「ハンバーグ？絶対食べない！」」黄色文字＋黒フチ、鍵カッコごと表示
- 下段1行目「超偏食のアメリカ人姉妹が初めての日本旅行で」緑文字＋黒フチ
- 下段2行目「一口食べて価値観激変した理由」赤文字＋黒フチ（最も大きく強調）

**画像生成プロンプト（クライアント方針「元ネタの上位互換」を反映し、食べ物は艶・湯気・質感を具体的に描写）**
```
Photorealistic candid documentary-style photo, close-up shot from a
slightly high angle looking down at a restaurant table. Two young
American sisters, one about 8 years old with long wavy blonde hair and
one about 6 years old with shorter blonde hair, lean forward over the
table with their forearms resting near the plate, faces close together
and close to the camera, looking down at the food with clearly negative,
skeptical, wary expressions: furrowed eyebrows, mouths pulled into a
disgusted or apprehensive frown. This is a genuine reluctance/refusal
reaction, not curiosity or delight. The two sisters have distinct,
different facial features and slightly different hair tones so they read
as clearly different individuals, not clones. Natural real skin texture
with subtle imperfections, avoid airbrushed CGI look, avoid uncanny
valley, avoid a perfectly symmetrical mirrored pose between the two girls
— vary their head tilt and arm position naturally.

On the plate in the foreground, a glossy Japanese-style hamburger steak
(hambagu) with a deep brown, glistening demi-glace sauce pooling around
it and visible steam softly rising, showing a tender, juicy cut with
moist interior texture just barely visible; beside it a portion of
ketchup-based Napolitan-style spaghetti with glossy red sauce catching
the light, and a small mound of shredded cabbage coleslaw mixing pale
green and purple cabbage for color contrast. Every food element has a
polished, mouthwatering restaurant-photography sheen, shot as if for a
food magazine, contrasted against the children's wary expressions.

Background is a warm, softly blurred traditional Japanese diner/yoshoku
restaurant interior, wooden tables and dim warm lighting, indistinct
silhouettes of other patrons further back. Shot on a 35mm lens, shallow
depth of field with the girls and plate in sharp focus and the background
softly blurred, generous negative space around the top and sides of the
frame for text compositing. 16:9 aspect ratio, no text, no logos.
```

**紐づく台本**: 「この子たちは絶対に食べない」（ニューヨークに暮らすアメリカ人母レイチェル・カーターと、回避制限性食物摂取症の8歳エミリー・6歳ソフィア姉妹が、日本旅行中に下町の洋食店で宮本さん夫妻の作ったハンバーグを一口食べたことをきっかけに、8年間の偏食が少しずつ変わっていくエピソード）

**制作メモ**: これまでの「料理×家族リアクション」型（パターン3）は左右2枚合成だったが、本パターンは子供2人と料理を1枚のフレームに収める密着構図。表情は「美味しそう」ではなく「拒絶・警戒」を明確に描くのがポイント（台本の偏食エピソードに対応）。クライアント方針により、料理自体はどんな回でも艶・湯気・質感を具体的に描写して「元ネタの上位互換」を狙う。

**PhotoScape X 文字入れ指示**
| 要素 | 内容 | 色 | 位置 |
|---|---|---|---|
| 赤い矢印 | ハンバーグを指す | 赤 | 皿の中央〜ハンバーグ |
| 「⁉」記号（左） | 姉の頭上 | 黒文字＋白フチ | 画面左上 |
| 「⁉」記号（右） | 妹の頭上 | 黒文字＋白フチ | 画面右上 |
| 吹き出し「ナニこれ？」 | 白背景の吹き出し | 黒文字 | 画面右側、妹の右上 |
| 上部見出し | 「「ハンバーグ？絶対食べない！」」 | 黄色＋黒フチ4px | 画面最上部、横一杯 |
| 下段1行目 | 「超偏食のアメリカ人姉妹が初めての日本旅行で」 | 緑＋黒フチ | 下部帯1行目 |
| 下段2行目 | 「一口食べて価値観激変した理由」 | 赤＋黒フチ（最も大きく強調） | 下部帯2行目 |

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

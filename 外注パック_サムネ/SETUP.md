# セットアップ手順（Claude が読んで、この順に進める）

> 「セットアップして」と言われたら、この手順を**上から順に**進める。飛ばさない。
> ★**必要な情報は手順0でまとめて聞く。** 以後の手順では手順0の答えを使い、同じことを聞き直さない（答えが無い・違っていた時だけ聞く）。
> ★パスワード・APIキー・鍵ファイルの**中身**は聞かない・表示しない。聞くのは「置き場所のパス」だけ。
> 各手順が終わったら「手順○ 完了」と1行で伝えてから次へ進む。
> **Mac と Windows で手順が分かれるところは【Mac】【Windows】と書いてある。** OS は最初に自動で判定する（聞かない）。

## 手順0 はじめに・必要な情報をまとめて聞く
1. OS を判定する：`python3 -c "import platform;print(platform.system())"`（Windows なら `python -c …`）。Darwin＝Mac／Windows。
2. 次の3行を伝える。
   - これから、このチャンネル用のサムネ制作の仕組みを設定する（所要30〜60分）
   - 最初に必要な情報をまとめて聞く。あとは確認だけで進む
   - 最後に使い方の説明を表示し、定期実行を登録して終わる
3. **先に用意しておくもの**を表示する（無いものは、あとの手順で入れ方を案内する）：
   - Photoshop（2025以降・Creative Cloud にログイン済み）
   - テンプレPSDで使っているフォント（Adobe Fonts で有効化）
   - 【Mac】ChatGPT のデスクトップアプリ（ログイン済み）／【Windows】Node.js（LTS）と Python 3.12
   - Google Drive for desktop（案件フォルダが同期されている）
4. 次の記入欄を**そのまま表示し、1回でまとめて答えてもらう**（分からない項目は「不明」でよい＝その手順で案内する）：
   ```
   ① チャンネル名：
   ② チャンネルのURL（https://www.youtube.com/@… でよい）：
   ③ 管理シートのURL（案件一覧のタブを開いた状態でアドレスバーからコピー）：
   ④ リサーチシートのURL（元ネタURLと指定タイトルが入っているタブを開いた状態で）：
   ⑤ 自動で着手してよい範囲（空欄なら「管理シートの上から10行目まで」）：
   ⑥ このチャンネルのサムネのテンプレPSDの場所：
   ⑦ Google Drive の作業フォルダ（案件フォルダが並んでいる所）の場所：
   ⑧ シートの鍵（サービスアカウントの json）の場所（持っていなければ「無し」）：
   ⑨ 定期実行の時刻（例：毎日0時／平日9時／自動実行しない）：
   ⑩ 1回に処理する最大件数（空欄なら10件。1件＝トークン約30万・30〜60分）：
   ```
   - 場所（パス）の取り方も一緒に伝える：【Mac】Finder でファイルを選び option を押しながら右クリック →「"…"のパス名をコピー」／【Windows】Shift を押しながら右クリック →「パスのコピー」
   - ★YouTube の API キーは要らない（元ネタ・同じ題材の他社・自社の実績は、公開データを yt-dlp で取る）。Google の鍵はシートの読み書きだけに使う。
5. 答えを受け取ったら①〜⑩を一覧で復唱し、空欄・読めない項目だけを聞き直す。

## 手順1 道具がそろっているか
以下 `<python>` は、【Mac】`/usr/bin/python3`／【Windows】`python`。
1. `<python> --version`（3.9以上）。
   - 【Windows】無ければ python.org から Python 3.12 を入れてもらう（インストーラーで「Add python.exe to PATH」にチェック）。
2. Python ライブラリを入れる（入れる前に何を入れるか伝える）：
   - 共通：`<python> -m pip install --user pillow gspread`
   - 【Windows】追加で `<python> -m pip install --user pywin32`（Photoshop を動かすのに使う）
3. yt-dlp：`yt-dlp --version`。無ければ、了承を得てから入れる。
   - 【Mac】`brew install yt-dlp`（Homebrew が無ければ `<python> -m pip install --user yt-dlp`）
   - 【Windows】`<python> -m pip install --user yt-dlp`（または `winget install yt-dlp`）
4. 画像生成の codex：
   - 【Mac】ChatGPT のデスクトップアプリに同梱。`ls /Applications/ChatGPT.app/Contents/Resources/codex` で確認し、`codex --version`
   - 【Windows】`npm install -g @openai/codex` → `codex login`（ChatGPT アカウントでログイン）→ `codex --version`
5. Photoshop のアプリ名を調べる（聞かない）：【Mac】`ls /Applications | grep -i photoshop`／【Windows】`dir "C:\Program Files\Adobe"`

## 手順2 チャンネルと管理シート（手順0の②〜⑤を使う）
1. ②のURLからチャンネルIDを取る：`yt-dlp --print channel_id --playlist-items 1 "<URL>/videos"`
2. ③のURLの `/d/<ここ>/` がスプレッドシートID、`#gid=<ここ>` がタブのgid。④も同じ（別のブックなら、そのIDも控える）。
3. ⑤が空欄なら上から10行目まで。

## 手順3 シートに書き込むための鍵（手順0の⑧を使う）
⑧が「無し」なら、作り方を案内する：
1. Google Cloud Console（https://console.cloud.google.com/）でプロジェクトを作る
2. 「APIとサービス」→「ライブラリ」で **Google Sheets API** を有効にする
3. 「IAMと管理」→「サービスアカウント」→ 作成 → 「鍵」→「鍵を追加」→ JSON をダウンロード
4. ダウンロードした json を、**このフォルダの外**の安全な場所に置く（例：【Mac】`~/.config/サムネ/sa.json`／【Windows】`%USERPROFILE%\.config\サムネ\sa.json`）→ 置いた場所を聞く（中身は開かない）
5. json の中の `client_email`（xxx@xxx.iam.gserviceaccount.com）を、管理シート（とリサーチシート）の「共有」に**編集者**で追加してもらう
★鍵を使わない運用も選べる（その場合は完了日を人が手で書く）。その時は `sheet.enabled=false` にし、対象は「NO○○のサムネ作って」で名指ししてもらう。

## 手順4 Drive の作業フォルダ（手順0の⑦を使う）
1. ⑦のフォルダが開けるか確かめる。
   - 【Mac】例：`~/Library/CloudStorage/GoogleDrive-<アカウント>/マイドライブ/…/01_作業フォルダ`（共有されたフォルダは「共有アイテム」やショートカットの場所になることがある）
   - 【Windows】例：`G:\マイドライブ\…\01_作業フォルダ`（ドライブ文字は環境による）
2. 中の案件フォルダの名前が `<NO>_<タイトル>` の形か見る（違う場合は形を聞き、`scripts/common.py` の `find_case_folder` の照合を合わせる）。
3. 中間ファイルの置き場は `~/サムネ作業`（既定）。
4. 【Mac】Claude が Drive のフォルダを読み書きできないと失敗する。手順5で ✗ が出たら「システム設定 → プライバシーとセキュリティ → フルディスクアクセス」で Claude を許可してもらう。

## 手順5 設定ファイルを作ってチェックする
1. `config.example.json` を写して `config.json` を作り、ここまでの答えを書き込む（`template` はまだ触らない＝手順6で書く）。
   - `python`：【Mac】`/usr/bin/python3`／【Windows】`python`
   - `codex_path`：【Mac】`/Applications/ChatGPT.app/Contents/Resources/codex`／【Windows】`codex`
   - `photoshop_app`：【Mac】手順1-5で調べたアプリ名（例：Adobe Photoshop 2026）／【Windows】使わない（そのままでよい）
   - `schedule`：⑨を cron 式に、⑩を `max_cases_per_run` に
   - 【Windows】パスは `\` を `\\` にするか `/` で書く（JSON の決まり）
2. 管理シートの見出しを読み、**列の対応を確定する**：`<python> scripts/check_env.py` を実行。見出しが見つからない列があれば、実在の見出し一覧を見せて「No／タイトル／サムネイルの完了日／サムネイルのチェック」はどれかを聞き、`config.json` の `col_*` を直す。リサーチシートの「No／参考URL／指定タイトル」も同じ。
3. **`check_env.py` が全部 ✓ になるまで**直す（テンプレPSDの ✗ は手順6で直るので、ここでは無視してよい）。

## 手順6 テンプレを合わせる（チャンネルごとにテンプレが違うため）
合成器は「どのレイヤーが1〜3行目・背景・国旗・記号か」「各行に何文字入るか」「写真が見える帯」を `config.json` の `template` で知る。ここで⑥のテンプレから実測して書く。
1. Photoshop を起動してもらい、`<python> scripts/inspect_template.py --psd "<⑥のパス>" --write` を実行する。
   → レイヤー一覧（グループの中も）と、役割の割り当て案が出て、`config.json` の `template` と `template_psd` に書き込まれる。
   - ★Photoshop が「フォントが見つからない」ダイアログを出したら**「置換」を押さない**（押すと別のフォントで書き出される）。キャンセルしてフォントを有効化してから再実行。一覧に「✗フォント未導入」があるときも同じ。
   - ★1回目は Photoshop が「スクリプトの実行を許可するか」を聞くことがある。許可してもらう。
   - ★キャンバスが1280×720でなければ止めて伝える（このパックは1280×720前提）。
2. `preview.png`（テンプレをそのまま書き出したもの）を開いて見せ、割り当て案を表にして確認してもらう：
   | 役割 | 割り当てたレイヤー |
   |---|---|
   | 1行目／2行目／3行目 | … |
   | 背景（中央画像を差し替えるスマートオブジェクト） | … |
   | 国旗／!?／小セリフ／矢印／丸 | … |
   - 違っていたら、レイヤー一覧から正しい名前を聞いて `config.json` の `template` を直す。同じ名前が2つあるときは `"pick": "narrow"`（幅の狭い方）／`"wide"`、または `"nth": 0,1…`（上から何番目か）で区別する。
   - テンプレに無い要素（国旗・丸など）は `{"layer": ""}` にする（その記号は使わない）。
3. `<python> scripts/inspect_template.py --measure --write` → 各行に入る字数を実測して `template.chars` に書く。結果の字数を伝える。
4. **テスト合成**をして、書き出された画像を開いて見せる：
   ```python
   import sys; sys.path.insert(0, "scripts")
   import thumb_psd_compose as T
   c = T.TP["chars"]
   T.render(out="<work_dir>/_template/test.png", psd_out="",
            l1="「" + "あ" * (c["l1_max"] - 2) + "」", l2="い" * c["l2"][1], l3="う" * c["l3_max"],
            img="", mark="!?", mq=(300, 300, 100, 100, 0),
            ar=(640, 320, 165, 165, 0), small="テスト", ms=(950, 320, 100, 100))
   ```
   確かめること（ずれていたら `config.json` の `template` を直して、もう一度合成する）：
   - 3行が元のテンプレと同じ位置・幅に入り、右端が切れていないか（左右の位置＝`lines[].left`、幅＝`lines[].width`。中央揃えのテンプレなら `"align": "center", "cx": 640`）
   - **矢印の向き**：rot=0 で矢印の先がどちらを向いたか（↖↑↗→↘↓↙←）を見て `arrow_rot0` に書く
   - **写真が見える帯**：`band` の [上, 下] が、1行目の帯の下端と2行目の帯の上端に合っているか（案は文字の範囲からの推定。実物を拡大して直す）
   - !? と小セリフが出ているか・中身が差し替わっているか
   - 【Windows】ここで失敗したら、エラー文をそのまま控えて報告してもらう（Windows 対応の確認ポイント）。よくある原因＝pywin32 が入っていない／Photoshop が起動していない／パスに `\` が残っている。

## 手順7 自社チャンネルの実績を取り、試運転する
1. `<python> scripts/own_channel.py`（自社の再生一覧・1万再生以上のサムネ・色のレンジを作る）。結果の `own_sheet.jpg` を開いて見せる。
2. `<python> scripts/find_targets.py --limit 3` を実行し、対象の案件を表にして見せる（No・タイトル・元ネタURL・案件フォルダが見つかったか）。
3. **codex の試運転**：短いプロンプト（例：「A photo of a red apple on a white table. No text.」）を `<work_dir>/_test/prompt.txt` に書き、
   `<python> scripts/gen_image.py _test T --prompt-file <work_dir>/_test/prompt.txt` を実行。`cand_T.png` ができて開けることを確認する。

## 手順8 定期タスク（自動実行・手順0の⑨⑩を使う）
1. 定期タスクを登録する（Claude デスクトップアプリの定期タスク機能＝`create_scheduled_task` ツール）：
   - taskId：`thumbnail-<チャンネル名の英字略>`
   - cronExpression：⑨を cron 式にしたもの（ローカル時刻）
   - prompt：`<このフォルダの絶対パス> の CLAUDE.md と skill/SKILL.md を読み、SKILL.md の手順どおりに今日の対象を全件処理する。終わったら報告を書く。`
   - ⑨が「自動実行しない」なら登録しない（「サムネ作って」で手動実行）。
   ★`create_scheduled_task` が使えない環境なら、その旨を伝え、Claude デスクトップアプリの「定期タスク」から同じ内容で登録してもらう手順を案内する。それも無い場合は、手動運用（「サムネ作って」）にする。
   ★定期実行はパソコンが起動していて、Claude アプリが開いている間だけ動く（スリープ中は動かない）ことを伝える。
2. 登録できたら、次回の実行予定時刻を伝える。

## 手順9 使い方を表示して終わる
1. **`使い方.md` の全文をそのまま表示する**（要約しない）。
2. 最後に「セットアップ完了」と、次にやること（例：「NO○○のサムネ作って」で試しに1本作る）を1行で伝える。

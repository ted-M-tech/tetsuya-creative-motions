# 制作の経緯

Notion Content Calendar ID 077（Drive「077. How Do You Say It 3 - Itadakimasu」、Prefix `Say3_Itadakimasu`）。シリーズ「How Do You Say It?」の第3話。コマンダー（オーナーと話すセッション）の指示で、origin/main の第2話 `films/mimi-say-otsukare` の source/ から作った。

## オーナーの言葉（原文）

- 2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- 2026-10-23（セーフエリア）：「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」
- 2026-10-23（シリーズの見た目、別の続編について）：「フォントの色とか変わってる？統一感出して過去と」

コマンダーの企画（要約）：フック「いただきます、英語で？」、夕ごはんの食卓で友だちと Mimi。友だちが直訳を言い（オーナーの声）、Mimi は困惑（吹き出し）。実アプリで「食べる前のいただきます」→ フレーズを作成 → 本物の結果 → 保存。場面カードはアプリの本物の答えと、自然なら一般的な別の言い方を1つ（"Let's eat!" / "This looks great!" など）をはっきり区別して。CTA「次は何を英語にしたい？」。

## アプリで確かめたこと（Lanclo origin/main 1088ae0b、native-ios が正）

第2話（5f5571ad）のあと、フレーズの追加画面は変わっていた。いまの流れ（`Views/VocabularyScreen.swift`、`Views/PhraseComposerThinking.swift`、ja は `Resources/Localizable.xcstrings`）：

- 入力画面：Mimi の「言いたいことや、気になる表現を教えて。」と、選択肢「意味・表現を知りたい」（初期値）/「自然か確かめたい」。入力欄は `notes.manual.text`、下に「フレーズを作成」（`notes.manual.create`）と「手入力する」。
- 作成中：「表現を考えています…」と「中止」（`PhraseComposerThinking`）。第2話の「生成を中止」はなくなった。
- 候補が1つなら、そのまま「フレーズを確認」（`selectCandidate`）。「こんな表現が使えるよ。」、英語、意味、例文（`generateExample` が自動で呼ばれる）、タグ（任意）、「保存」（`notes.manual.save`）。保存はユーザーが押したときだけ。
- 保存後：「マイノートに保存したよ。」「復習のタイミングで、また出すね。」と保存したフレーズ、「完了」（`notes.manual.done`）/「続けて追加」。一覧に戻らないので、フィクスチャの枚数カードや「Please」の行は映らない（隠すものなし）。

## 本物の答え（正直さのルール）

製品のサーバー処理 `vocabularyApi`（`voice-web/cloudflare/vocabulary.ts`）を、新しい detached ワークツリー（`~/orca/workspaces/native-voice-clone/compose-probe-itadakimasu`、origin/main 1088ae0b、`npm ci --ignore-scripts` をルートと voice-web で）から、`source/scripts/compose_probe.mjs` でそのまま呼んだ（専用 Gemini キー、表示しない）。

作成（フレーズを作成が送るもの）：入力 `{"purpose":"compose","input":"食べる前のいただきます","language":"en","meaningLocale":"ja","consent":true}` を3回（`process/compose-probe-itadakimasu.jsonl`）：

1. **"Let's eat!" / いただきます（食事を始めるときのあいさつ）** ← 採用
2. "Let's eat." / いただきます（食事を始める時の合図）
3. "Let's eat." / いただきます（食事を始めるときの表現）

3回とも候補は1つで "Let's eat"。1 を使った理由：意味の文が「あいさつ」で一番わかりやすく、"!" が食卓の明るさに合う。

例文（下書きで自動で作られるもの）：QA フィクスチャはふつう英語そのものを例文に返すので、本物の例文も同じ処理で取った。入力 `{"purpose":"example","term":"Let's eat!","meaning":"いただきます（食事を始めるときのあいさつ）","language":"en","translationLocale":"ja","consent":true}` を2回（`process/example-probe-lets-eat.jsonl`）：

1. **"Everything looks so delicious, let's eat!" / どれもすごく美味しそうだね、いただきます！** ← 採用
2. "Dinner is ready, so let's eat!" / ご飯ができたから、いただきます！

返ったとおりの文字を、撮影専用パッチ `source/app-capture/compose-result.patch` で QA フィクスチャの答えにした（この入力のときだけ、2秒待って「表現を考えています…」も見せる）。アプリには入れていない。画面の大きなラベルも同じ文字。

場面カード：食べはじめる "Let's eat!" はアプリの答え（「アプリの答え」と表示）。作ってくれた人に "This looks great!" はアプリの答えではなく、食卓でよく言う自然なひと言として「よく言うひと言」と分けて表示（アプリの例文 "Everything looks so delicious" と同じ気持ち）。

## 判断

- キャストは Mimi と友だちだけ。新しいポーズは作っていない：ライブラリの食卓（`dining`）、Mimi（`yum` を左右反転、`stunned`、`point`、`confident`、`bowl`）、友だち（お茶わんの `friend-offer`、`friend-yay`）。暗い背景で透けがないことを確かめた。食卓の板の手前（y 1278 から下）を背景の複製で上に重ね、2人がテーブルについて見えるようにした。
- 声（オーナーの声、3行・作り直し0回）：友だち "I will receive!"（learner、ふつうに明るく）、カード "Let's eat!" / "This looks great!"（us）。最後の友だちの "Let's eat!" は同じ "Let's eat!" の声を使った（追加の生成なし）。「Receive… what?」は吹き出しだけ。置き方はすべて発声の 63–70 ms 前から、頭と終わりの 10 ms はクリップのピークより -54 dB 以下（基準 -38 dB）。
- 実画面：入力の打鍵は1.3倍速、生成待ち（作成中の後半）と下書きから保存までの待ちは切った。
- シリーズの見た目：第2話の CSS とそろえた（シリーズ札、フック、色 #273b4b / #2a8dff / #344f69 / #5b7f9f、結果ラベル 64px、カードの行 58px・余白 22px・間 26px）。増やしたのは、カードの出どころの小さな文字（結果ラベルの small と同じ 30px・#5b7f9f）と結果ラベルの例文の行（意味の行と同じ 30px）だけ。
- セーフエリア：英語字幕は下から 430px（箱の下端 y 1490）・x 60–880、右のアクション列に文字・吹き出し・小さい Mimi を置かない（スマホは x 390–870、カードは右端 x 880、カードの Mimi は x 520–850）、友だちの顔は x 900 より左、上の文字は y 200 から。確認は線を引いたコンタクトシート（`process/00-draft-frames.jpg`）。
- 音：声が主、BGM はキットのテーマ、SFX は小さく。Mix.write の後に第2話と同じ「足りない分のゲイン＋リミッター」。ただし render-cuts.sh の AAC で mix.wav より 0.4 LU 下がった（-14.2 → -14.6）ので、wav の目標を -13.6 にした。両カットで -14.2 LUFS・トゥルーピーク -1.7 dBTP。
- 時間は `source/scripts/cues.py` 1か所。

## 学んだこと

- フレーズの追加画面は版ごとに変わる（今回：意味・表現／自然か確かめる の選択、作成中の Mimi、保存後の確認画面）。前の話のウォークスルーをそのまま使わず、origin/main のコードを読み直す。
- `notes.group.add` は「すべて」を開いてから出る（最初のテイクはこれを抜かして空振り）。
- 下書きは例文を自動で作るので、フィクスチャのままだと例文が英語そのものになる。本物の例文も API で取ってパッチに入れる。

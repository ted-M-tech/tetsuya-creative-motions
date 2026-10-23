# 制作の経緯

Notion Content Calendar ID 64（Drive「064. How Do You Say It 2 - Otsukaresama」、Prefix `Say2_Otsukaresama`）。シリーズ「How Do You Say It?」の第2話。バッチ 055–066 の1本として、コマンダー（オーナーと話すセッション）の指示で、第1話のブランチ `feat/mimi-say-yoroshiku` から作った。

## オーナーの言葉（原文）

- 2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- 2026-10-23（セーフエリア）：「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」

承認された企画（コマンダーの要約）：フック「お疲れ様、英語にない？」、仕事終わりに友だちが Mimi（第1話の同僚の役衣装）に手を振り "You are tired!"、Mimi は困惑（「Am I…?」は吹き出しだけ）。実アプリで「仕事終わりにお疲れ様」→ フレーズを作成 → 本物の結果 → 保存。Mimi の気持ちカード：帰るとき "See you tomorrow!" / 感謝 "Thanks for today!" / ねぎらい（アプリの本物の答え）。CTA「次は何を英語にしたい？」。学びどころ：英語はお疲れ様を気持ちで分ける（別れ・感謝・労い）。"You are tired" は相手の状態を言う文で、あいさつではない。

## アプリで確かめたこと（Lanclo origin/main 5f5571ad、native-ios が正）

- 作成の結果が2つ以上のとき、アプリはそのまま下書きにせず「意味を選択」（`Choose a meaning` の ja）の一覧を出し、各行に英語（term）と意味（meaning）を表示する。行をタップすると、その候補が編集できる下書きになる（`Views/VocabularyScreen.swift` `createPhrase` / `selectCandidate`、行の id `notes.manual.choice.<meaning>`）。1つのときは直接下書きになる。保存はユーザーが「保存」を押したときだけ。
- そのほかの文言（フレーズを作成・生成を中止・手入力する・保存・保存済み）と作成の流れは第1話の PROCESS.md のとおり。

## 本物の答え（正直さのルール）

- 「仕事終わりにお疲れ様」の答えは第1話の制作時に、製品のサーバー処理 `vocabularyApi`（purpose `compose`）を新しい detached ワークツリーからそのまま3回呼んで記録した（`process/compose-probe-otsukare.jsonl`、方法は `source/scripts/compose_probe.mjs` と第1話の source/README.md）：
  1. "Good work today." / 仕事終わりの「お疲れ様」
  2. **2候補："Have a good evening!" / お疲れ様でした（退社・別れ際の挨拶）と "Good work today!" / 今日はお疲れ様でした（一日の労いの言葉）** ← 採用
  3. "Great work today!" / 仕事終わりの「お疲れ様」
- 2 を使った理由：アプリは2候補を本当に「意味を選択」として並べるので、意味ごとに分かれることがそのまま画面で見え、学びどころと合う。返ったとおりの文字（"!" も意味の文も）を、撮影専用パッチ `source/app-capture/compose-result.patch` で QA フィクスチャの答えにした（この入力のときだけ、2秒待って「生成を中止」も見せる）。アプリには入れていない。
- カードのねぎらいの行と最後の吹き出しはアプリの答えどおり "Good work today!"。帰るときの行は企画どおり "See you tomorrow!"（アプリのもう1つの候補 "Have a good evening!" も画面の候補ラベルに出ている）。

## 判断

- キャストは Mimi と友だちだけ。新しいポーズは作っていない：第1話の友だち（シャツとネクタイ、手を振る笑顔 `friend-bow-smile`）と同僚 Mimi（`mimi-colleague-hello-r`・`mimi-colleague-puzzled`）、ライブラリの point・confident と会議室の背景。仕事終わりは背景に夕方の色をかけて出した。
- 声（オーナーの声、4行・作り直し0回）：友だち "You are tired!"（learner、ふつうに明るく。わざと間違える発音ではない）、カード "See you tomorrow!" / "Thanks for today!" / "Good work today!"（us）。「Am I…?」と最後の友だちのせりふは吹き出しだけ。
- 実画面：入力の打鍵は1.3倍速、生成待ちと候補の前の待ちは切った。テストの「保存」が下書き表示の 0.05 秒後に押されてしまったので、下書きの1コマ（60.65 秒）を 0.8 秒止めて見せた（本物の画面のコマ。中身は変えていない）。保存後の一覧に出るフィクスチャの枚数カード（「2枚」）とフィクスチャのフレーズ「Please」の行は隠した。候補一覧と結果は、スマホの画面が小さいので大きなラベルでも同じ文字を出した。
- セーフエリア（オーナーの指摘を第1話と同時に反映）：英語字幕は下から 430px（箱の下端 y 1490）・x 60–880、右のアクション列に文字・吹き出し・小さい Mimi を置かない（スマホは x 390–870、ラベル・カードは右端 x 880、カードの Mimi は x 520–850）、友だちの顔は x 900 より左、上の文字は y 200 から（シリーズ名の札とフックを下げた）、エンドカードは中身を上げて字幕とストアバッジが重ならないようにした。確認は線を引いたコンタクトシート（`process/00-draft-frames.jpg`）。
- 音：声が主、BGM はキットのテーマ、SFX は小さく、明るいベルなし。Mix.write の後に、`films/mimi-katakana-mcdonalds` と同じ「足りない分のゲイン＋リミッター」で -14.2 LUFS・トゥルーピーク -1.6 dBTP（両カットで測定）。リミッターの上限は -1.5 dBTP を確実に下回るよう 0.76 にした（0.84 ではトゥルーピーク -0.9 dBTP だった）。
- 時間は `source/scripts/cues.py` 1か所にまとめ、`cues.json`（mix.py が読む）と `hf/index.html`（`scripts/index.tpl.html` から）を書き出す。

## 学んだこと

- 作成の答えが複数のときの画面（意味を選択）は、1つのときとは別の流れ。複数候補の本物の答えを見せるときは、ウォークスルーで候補の行をタップする手順が要る。
- UI テストの待ち（`Thread.sleep`）は、画面録画のうえでは思った長さにならないことがある（候補は8秒出ていたのに、下書きは0.05秒で保存された）。録画のコマで確かめてから切る。
- `alimiter` の上限はサンプルのピーク。トゥルーピーク -1.5 dBTP を守るには、上限を下げて測り直す。

## Owner approval

- 2026-10-23: 「全部OK」 (all twelve shorts of the 055–066 batch approved as delivered; the card keeps "See you tomorrow!" for leaving, as delivered; the Drive cuts were renamed without `_draft_`: `Say2_Otsukaresama_2026-10-23.mp4`, `Say2_Otsukaresama_EN-subs_2026-10-23.mp4`).
- Earlier owner notes in the same review round (2026-10-23): 「56の英語音声少し切れている？」 (clipped English in 056; led to the voice-cut audit of every episode); 「62透過されている？」 (the see-through angry pose in 062; fixed there with a filled pose).

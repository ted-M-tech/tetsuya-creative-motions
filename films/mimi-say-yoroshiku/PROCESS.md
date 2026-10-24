# 制作の経緯

Notion Content Calendar ID 63（Drive「063. How Do You Say It 1 - Yoroshiku Onegaishimasu」、Prefix `Say1_Yoroshiku`）。新シリーズ「How Do You Say It?」の第1話（シリーズの型）。バッチ 055–066 の1本として、コマンダー（オーナーと話すセッション）の指示で制作。

## オーナーの言葉（原文）

- 2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

承認された企画（コマンダーの要約）：1対1の英語がない日本語を、iOS の実アプリのフレーズ作成に入れるシリーズ。フック「よろしくお願いします、英語で？」、初出勤でお辞儀のまま固まる友だち、同僚役は役衣装の Mimi（ブルーノは出さない）。友だち "Please... yoroshiku?"、Mimi 困惑、実アプリで「新しい職場でよろしくお願いします」→ フレーズを作成 → 結果 → 保存、字幕「日本語のまま打てばOK」、Mimi の場面カード（初対面 / 一緒に働く）、CTA「次は何を英語にしたい？」。正直さのルール：画面の結果は Lanclo の作成機能がその入力に本当に返すもの。

## アプリで確かめたこと（Lanclo origin/main 5f5571ad、native-ios が正）

- 入力欄のプレースホルダ「覚えたい表現、または言いたいこと」、ボタン「フレーズを作成」、生成中は「生成を中止」、ほかに「手入力する」（`Localizable.xcstrings`、`Views/VocabularyScreen.swift` の `notes.manual.*`）。
- 作成は `AppStore.composePhrase` → `POST /api/daily/vocabulary`（purpose `compose`、study language、meaningLocale、consent）。結果（英語・意味）は編集できる入力欄で、保存はユーザーが「保存」を押したときだけ（自動では保存されない）。UI テスト `PracticeRefinementUITests/testMultilingualPhraseCreatesEditablePreviewAndSavesTarget` が同じ流れをフィクスチャの文で確かめている。
- サーバー（`voice-web/cloudflare/vocabulary.ts` `vocabularyComposeApi`、指示文 `packages/core/src/phraseCompose.ts`）：Gemini（`gemini-3.8-flash`、temperature 0.2）で候補を最大3つ。本番は stateless の呼び出しを dedicated プロジェクトに送る設定（`docs/operations/gemini-project-isolation.md`）。

## 本物の答えの取り方（正直さのルール）

- シミュレーターのアプリは QA フィクスチャでバックエンドなしで動く（本番のログインは使えない）ので、製品の本物のサーバー処理 `vocabularyApi` を、新しい detached ワークツリー（origin/main 5f5571ad）からそのまま呼んだ（`source/scripts/compose_probe.mjs`）。キーは製品の dev ツールが使う `~/.config/lanclo/gemini-dedicated.env`（dedicated プロジェクト）。キーは表示していない。入力 `{"purpose":"compose","input":…,"language":"en","meaningLocale":"ja","consent":true}`。
- 「新しい職場でよろしくお願いします」を3回（`process/compose-probe-yoroshiku.jsonl`）：
  1. "I look forward to working with you at my new workplace." / 新しい職場でよろしくお願いします
  2. **"I look forward to working with you."** / 新しい職場などで「よろしくお願いします」と伝える表現 ← 採用
  3. "I look forward to working with you at my new workplace." / 新しい職場でよろしくお願いします。
  AI なので毎回少し変わる。3つとも本物の答えで、画面で読める短い 2 を使った。企画の "Looking forward to working with you." ではなく、アプリの答えどおり "I look forward to working with you." を場面カードと声にも使った。
- エピソード2用に「仕事終わりにお疲れ様」も3回（`process/compose-probe-otsukare.jsonl`、エピソード2は作っていない）：
  1. "Good work today." / 仕事終わりの「お疲れ様」
  2. 2候補："Have a good evening!" / お疲れ様でした（退社・別れ際の挨拶）と "Good work today!" / 今日はお疲れ様でした（一日の労いの言葉）
  3. "Great work today!" / 仕事終わりの「お疲れ様」
- 画面への出し方：撮影専用パッチ `source/app-capture/compose-result.patch` で、QA フィクスチャの作成結果を、この入力のときだけ上の 2 にした（2秒待たせて「生成を中止」も見せる）。アプリには入れていない。

## 判断

- キャストは Mimi と友だちだけ。同僚役は Mimi（水色カーディガン＋白紙の社員証）。新しいポーズ5枚（`prompts/01`、`02`）：友だちのお辞儀（固まる・笑顔）、同僚 Mimi（握手の手・困惑）。最初の握手 Mimi は左向きで、友だち（右側で左向きにお辞儀）と向き合わないので、右向きで描き直した（1回）。ほかはライブラリの point・confident と会議室の背景。
- 声（オーナーの声、3行・作り直し0回）：友だち "Please... yoroshiku?"（learner の style、ためらいの間は mix で詰めた。前の「うん」と途中の小さな息は使っていない）、場面カード "Nice to meet you." / "I look forward to working with you."（us）。最後の友だちのせりふは吹き出しだけ（声を増やさない）。
- 実画面：入力の打鍵は1.3倍速、生成待ちと保存待ちは切った（待ちを切るのは過去作と同じ）。保存後の一覧に出るフィクスチャの枚数カード（「2枚」）と、フィクスチャのフレーズ「Please」の行は隠した（数字なし・フィクスチャ文字なし）。保存したフレーズの行は見せている。
- 字幕「保存は自分で」は「自動では保存されない」から。「直してもOK」は結果が編集できる入力欄であることから。
- 音：声が主、BGM はキットのテーマ、SFX は小さく、明るいベルなし。

## コマンダーの確認（2026-10-23、v2）

- 内容は承認。答えは短い方 "I look forward to working with you." のまま。
- 音量：−15.7 → −14.1 LUFS、トゥルーピーク −1.9 dBTP（mimi-katakana-mcdonalds と同じ後段ゲイン＋リミッター。リミッターは −2.5 dBFS にしてトゥルーピークを −1.5 dBTP 未満に。バランスは同じ）。
- プラットフォームのセーフエリア（オーナー「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」）：右のアクション列（x>900、y 820–1520）から吹き出し・友だち・電話・結果ラベル・カード・小さいMimi・エンドカードの文字を左へ。英語字幕は x 60–880、下端 y 1500 以内（エンドカードだけ上に）。フックの1行目は y 200 以降（シリーズ名のラベルも 200 以降）。区域を重ねたシートで確認。App Store バッジはキットのエンドカードのまま下の区域に一部かかる。
- 旧版は Drive の old/ に `_v1` で移した。

## 学んだこと

- ffmpeg で倍速の区間を切るとき、`-t` を `-i` の後ろに置くと出力の長さになり、倍速分だけ後ろがずれる。入力の長さは `-ss … -t … -i` で指定する。
- 作成の AI は temperature 0.2 でも毎回言い回しが変わる。複数回取って全部記録し、どれを使ったかを書く。

## Owner approval

- 2026-10-23: 「全部OK」 (all twelve shorts of the 055–066 batch approved as delivered; the Drive cuts were renamed without `_draft_`: `Say1_Yoroshiku_2026-10-23.mp4`, `Say1_Yoroshiku_EN-subs_2026-10-23.mp4`).
- Earlier owner notes in the same review round (2026-10-23): 「56の英語音声少し切れている？」 (clipped English in 056; led to the voice-cut audit of every episode); 「62透過されている？」 (the see-through angry pose in 062; fixed there with a filled pose).

## 履歴

- 2026-10-24: `compose_probe.mjs`（この話と mimi-say-itadakimasu・mimi-say-otsukare）を本番の `gemini-dedicated.env` から内部ツールプロジェクト `lanclo-internal-tools` のキー（`~/.config/lanclo/gemini-internal.env`、共通の `kits/mimi-short/scripts/internal-gemini-key.mjs`）に移した。上の3回の答えは移す前に本番キーで取ったもの。

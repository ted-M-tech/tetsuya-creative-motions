# 制作の経緯

オーナーの言葉（2026-10-21、新しいネタ案から）：

> 2,3,6,7,8,9,11,12 作成で

この回の案（コーディネーター経由の指示）：フック「カフェで固まった人、手を挙げて」→ 空港・ホテル・病院の短い場面、ただしアプリに実在する場面だけ。17本目（[mimi-roleplay](../mimi-roleplay/PROCESS.md)）の続編。学習者のセリフはオーナーの声、スタッフはKokoroの英語でよい。共通ルール：最初の1.5秒で止める（フックの文字は1フレーム目から）、15〜25秒、実機能はコードで確認、英語の発音シーンはオーナーの声（`ownvoice.py`）、日本語は吹き出し・字幕のみ。

## アプリで確かめたこと（native-voice-clone `origin/main` 5998d20d）

- 会話練習のカテゴリ：`native-ios/Lanclo/Resources/roleplay-catalog.json` の `categories` はレストラン・カフェ・空港・交通・ホテル・買い物・人との交流・仕事の8つ。**病院はない**ので、3つ目は「交通」の `roleplay-en-transport`（駅までの行き方を聞く、相手はバスの運転手）にした。
- 使った場面と、作者が書いたセリフ（同じファイルの `utterances`）：
  - `roleplay-en-airport-checkin`「飛行機の搭乗手続きをする」：相手 "May I see your passport?" / 返答 "Here you are."
  - `roleplay-en-accommodation`「チェックインして確認する」（ホテル）：相手 "Welcome. Do you have a reservation?"（動画では "Do you have a reservation?" の部分だけ）。返答の原文は "Yes, I have a booking under Lee." なので、動画では名前を出さない "Yes, I have a reservation." にした。
  - `roleplay-en-transport`：相手 "Hello. Where are you going?" / 返答 "Does this bus go to the station?"
- 場面を選ぶと `RoleplayCatalogScreen.swift` の `RoleplayOverview` が `SituationPracticeScreen`（AIの会話相手・ヒント・録音）を開く（英語の16場面すべて `situations-catalog.json` に `SituationTask` がある）。
- 実画面は `--qa-situations` のQAフィクスチャ。フィクスチャ（`Core/SituationQA.swift`）はどの場面でもカフェのセリフを返すので、撮影時だけ `app-capture/airport-lines.patch` で空港の場面に作者のセリフ（"May I see your passport?"、ヒント "Here you are." ほか）を返させた。締めの "Thank you. Have a nice flight!" とヒントの2つ目 "Yes, here's my passport." はフィクスチャ用に足した文。アプリへのコミットはしていない。
- 左上の「デモデータ」はマスク。

## 決めたこと

- フック：1フレーム目から白いカードの問いかけ＋氷漬けのMimi。0.45秒で氷の中のMimiが手を挙げ「はい…」。
- 3場面は各1.6〜2.2秒。質問の最後の語で凍る（`freeze` 効果音と「カチッ!」）。背景とスタッフ衣装（空港・ホテル・バス）、手を挙げるMimiは codex-p で新規（`prompts/01-codex-scenes-staff.txt`）。カウンター前面は背景から切り出してスタッフの手前に重ねた（17本目と同じ方式）。
- 解決後の3場面では返答をオーナーの声（`us`）。スタッフ（女性の友だち）はKokoro（空港 `bf_emma`、ホテル `af_bella`、バス `am_michael`）。Mimiの声は成人男性のオーナーの声になる（キャラクターとの不一致は承知の上、指示どおり）。
- BGMは17本目と同じくコピーカードから（冒頭は効果音と声だけ）。

## 学び

- GSAP の時刻0の `set` で初期表示を決めると、描画側のシーク順によって0秒付近が空白になった。初期の表示・非表示はCSSで決め、GSAPは切り替えだけにする。
- 共有シミュレーターの撮影スクリプトで `PATCH=... 関数` と書くと sh では変数が残り、次の撮影にもパッチが適用されようとして失敗した。撮影ごとに `env -u PATCH` で消す。

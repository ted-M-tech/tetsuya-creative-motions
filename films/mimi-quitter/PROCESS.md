# 制作の経緯

Notion Content Calendar ID 29（Drive「029. How a Quitter Kept Going for a Month」）。オーナーの言葉（原文、コーディネーター経由）：

> 2,3,6,7,8,9,11,12 作成で

承認された企画（コーディネーターの要約）：フック「3日坊主の私が、1ヶ月続いた理由」。友だちはいつも3日でやめる。Lancloのホーム画面・ロック画面のウィジェットとMimiの毎日のまとめ（Mimiのアドバイス）が引き戻し、最後は連続日数で終わる。あるものだけを見せる。フック重視（最初の1.5秒で止める、1フレーム目からフックの文、15–25秒、速いテンポ）。

## アプリで確かめたこと（Lanclo origin/main 5998d20d、native-ios が正）

- ウィジェット（`native-ios/LancloWidgets/LancloWidgets.swift`、`ja.lproj/Localizable.strings`）：
  - デイリーレッスン（`DailyLessonWidget`、ホーム画面の小・中）：中サイズは MimiListening の絵、「デイリーレッスン」、連続日数バッジ（炎、「連続」、「N日」）、「今日も、自分の声で練習。」「はじめる」、リンク `lanclo://practice/daily`。
  - 英語日記（`JournalTodayWidget`）：ホームの小（MimiArtist＋連続バッジ）とロック画面（円形・長方形・インライン、MimiJournal）。フレーズを追加（`AddPhraseWidget`）と復習（`QuickReviewWidget`、新規・学習中・復習の数）もホームの小とロック画面。デイリーレッスンはロック画面には出せないので、ロック画面は英語日記とフレーズを追加にした。
  - 連続日数は `WidgetHabit.streak`（アプリの学習日から）。
- 通知（`Services/PracticeReminder.swift`）：Mimi専用の通知はなく、練習リマインダー（初期20:00）の文言が、まとめに気づきがある日だけ「Mimiが今日のまとめで気づいたことがあるよ。見てみよう！」になる。タイトル「Mimi · Lanclo」、添付はMimiListening。
- Mimiのまとめ（`Views/MimiReportView.swift`、`docs/features/mimi-ai.md`）：毎日リマインダーの時刻に、直近7日の日記と練習から癖をまとめる。
- ホームの連続日数（`Views/RootView.swift` の `home.streak`、炎と数）。

## 判断

- ウィジェットとロック画面・通知は実機の録画ではなく、上のコードと文言どおりにHTMLで描いた（ウィジェットの絵はアプリのアセットをそのまま使う）。シミュレーターのホーム画面にウィジェットを置くUIテストは不安定で、兄弟ワーカーと共有の端末も変えてしまうため。コピーカードに「ウィジェットはアプリの表示をもとに再現」と注記した。ウィジェットの数字（連続4日、新規8・学習中4・復習12）は例。
- 実画面は1回の録画（`source/app-capture/QuitterWalkthrough.swift`）：デイリーレッスンの概要、`--qa-mimi` のまとめ、`--qa-widgets` のホーム。`--qa-widgets` の学習日は7日なので、撮影用パッチ `month-streak.patch` で30日にした（アプリは変えていない）。
- 学習記録（Progress）画面の「これまで30日、練習できたね」は良い一言だったが、同じ画面の累計練習日数（3日）・グラフがパッチの30日と合わないので使わず、ホームの🔥30にした。
- フィクスチャのレッスン名「QA：Lの音をはっきりと」はマスク。まとめの日付は録画の「10月20日(火)」なので、ロック画面の日付もそれに合わせた。
- キット：`apply-patch.py` を複数ファイル・複数か所のパッチに対応させた（036で使う。1か所のパッチは従来どおり）。
- 新しいポーズは1つ（`prompts/01-codex-poses.txt`）：お坊さん姿の友だち（ライブラリのMimiの bozu の衣）。ほかは mimi-loop・mimi-voice の友だちとライブラリの jump。
- 英語の発音シーンがないので、オーナーの声（ownvoice.py）は使っていない。日本語のTTSも使わず、せりふは吹き出し。
- 音：声のない作品なので、mimi-watching と同じく作品全体に1つのゲイン（−14 LUFS）＋ピークリミッター（キットの動的 loudnorm は静かな部分を持ち上げるため）。

## 学んだこと

- `data-start` を持つ包み（クリップ）の中に `<video data-start>` を入れると、書き出しで映像の時間がずれる（hyperframes check の StaticGuard）。包みはクリップにせず、GSAPで表示を切り替える。
- セッションが途中で切れると scratchpad が消える。撮影スクリプトやログは作品の外に置くので、再開時に作り直す前提で短く保つ。

# 制作過程：治ったはずのRが…（066 The R Came Back）

## オーナーの言葉（原文）

2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」

2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

（バッチ制作。指揮セッションの企画：フック「治ったはずのRが…」、ホラーパロディだが軽くかわいく、回想→しばらくして→言い間違い→実アプリの再確認の行→Lおばけがバイバイ。）

## 機能の確認（Lanclo origin/main）

- デイリーレッスンの概要（`native-ios/Lanclo/Views/LessonHomeDetails.swift`）：見出し「デイリーレッスン」、「Mimiが気づいた: …。」、各文の理由チップ `LessonReasonChip`（`Views/LessonLevel.swift`）。再確認は `slot.recheck == true` で `"\(label) · check again"`、日本語 `"%@ · 再確認"`（Localizable.xcstrings）。音のラベルは例の単語つき：`/ɹ/ (right)`（docs/features/personalized-lessons.md）。
- 再確認の作られ方：`packages/core/src/weaknessRanking.ts` の `lessonSlots()` が、以前メインだったキーで再確認の時期が来たものを Open 枠に `fill('open', due, true)` で入れる（key・label・category・words・recheck）。時期（3日・7日）は画面では言わない。
- 「解決した」まとめ（"/θ/ hasn't come up…"）はドキュメントで Planned（未実装）なので出さない。
- 注意：依頼文の「今日の練習のポイント」はレッスン概要の見出しではなく、Mimiのまとめ（`MimiReportView.swift`、初回レッスン）の見出し。概要の実際の表示（デイリーレッスン／Mimiが気づいた）をそのまま撮り、字幕にはこの語を使っていない。
- フィクスチャに再確認の行はない（`Core/VisualQAData.swift` の `qaSlot`：/l/ ×2、stress、rhythm、Open）。撮影専用パッチ `source/app-capture/recheck-row.patch` で Open 枠だけを `lessonSlots()` と同じ形の /ɹ/ 再確認（words: right, room、targetWord: room）にした。アプリには入れない。
- 撮影：`--uitesting --visual-fixtures --qa-route /practice/daily --qa-lesson-overview`、日本語（LessonLevelUITests / FeedbackFiveUITests と同じ起動引数）。

## 判断

- キャストはMimiと友だちだけ。Lおばけは文字の小道具（SVG）で、キャラクターとしては扱わない。新しいポーズなし（Pronunciation Disasters 11 の living・friend-ask・mimi-flashlight とライブラリ）。
- 声：友だちの英語はオーナーの声2本だけ（us “That's right!”、learner スタイル “That's light!”）。最後の正しい “That's right!” は us のテイクを再利用。
- 発音の確認（音響）：Praat（parselmouth）でフォルマントを確認。us-right の語頭（0.60–0.68 s）は F3 が約1600–1780 Hz まで下がり、はっきりした /ɹ/。learner-light の語頭（0.71–0.80 s）は F1 約250–300 Hz、F3 約2500–3700 Hz で F3 の落ち込みなし＝ /l/。Whisperは使っていない。
- 怖くしない：暗さは乗算 0.62、音は低くやわらかいドゥンと短調パッドだけ。おばけには目とほっぺ、最後は笑顔で手を振る。
- 音量：Mix.write（−14 LUFS 目標の loudnorm）。書き出しの実測は約 −17 LUFS、ピーク −1.4 dBFS。声が一番上、フックのドゥンは声より約5 dB下に下げた。

# 制作の経緯

Notion Content Calendar ID 54（Drive「054. Why Lanclo - Speak Think Improve」）。オーナーの言葉（原文、コーディネーター経由）：

> なぜこのアプリがいいかとか、今までの学習方法へのアンチテーゼ、あえてLancloが声で出す練習に機能特化させているか（それは日本の今までの教育から根本的に変えたい。）海外に住んでいる自分の体験と、5言語話せる大学講師の根拠を掛け算して作り上がっていること

> 実際に海外いったら、全然喋れなかったってのがいいかな

> 他の国の人は逆にリーディングとかが苦手だけど自信持って話している。日本人と逆。現実世界では話して議論する力も必要。大学の先生は、自分で考えて話して、改善することが大事という。

> 研究はついでに一般的なやつの裏付け。あとIELTSの固有名詞は不要

> Lancloにはあえて「声が必要な機能、考えないと出来ない機能」を揃えている

> ひとこともってのは変だな。議論する場で、自分だけぽつんとなっていたとかかな。他の人はめちゃ喋ってるのに。知ってるシチュエーションは喋れる。でもそれの繰り返しをするだけ。

> あえてのところ、英語日記もね

> 少し長くなってもいい

> 1本にまとめて

コーディネーターの指示：約50秒、キャストはMimi（創業者）・友だち（講師の衣装）・ブルーノ・ピッパ・ココのみ。主張は「僕は」「出会った人たちは」の個人の体験として書き、一般化しない。TOEIC/IELTSの名前は出さない。

## アプリと出典で確かめたこと（Lanclo origin/main c5eb7438、native-ios が正）

- 写真を見て話す：`Views/DescribePracticeScreen.swift` の録音上限が `FreeSpeechContract.recordingSeconds = 180`（`Core/FreeSpeechContract.swift`）、画面の「最大 3:00」。「3分話し続ける」と「写真を説明する」はアプリでは同じ機能なので、1枚「写真を見て、最大3分 話す」にまとめた。
- ディベート：`Views/DebatePracticeScreen.swift`（同じく180秒上限）、Localizable「ディベート」。
- 会話練習（ロールプレイ）：`Views/RoleplayCatalogScreen.swift` / `RoleplayDialogueView.swift`、ラベルは films/mimi-roleplay と同じ「会話練習」。
- 英語日記：Localizable「英語日記」、`Views/JournalGuidanceScreen.swift`（話して録音、「3分話しました。仕上げて日記を見てみましょう。」）。
- デイリーレッスン：Localizable「デイリーレッスン」。お手本を聴いて1文ずつ声に出すので、モンタージュでは「考えないとできない」タグを薄くして「声が必要」だけを残した。
- 研究：一般的な裏付けとして Swain (1985) のアウトプット仮説（話そうとすると言えないところに気づける）。films/mimi-freespeech と同じ扱い。LPの自声研究（Li, Lian & Yodkamlue, GEMA 2020「抑揚テストの伸び、約1.3倍」、`voice-web/src/landing/ResearchEvidence.tsx`）は話題が発音でこの作品の主張とずれるので使っていない。数字は出していない。

## 判断

- 実アプリは新しく撮らず、過去作のシミュレーター録画を再利用（Drive：021 FreeSpeech、019 Debate、017 Roleplay、018 Loop の英語日記、009 Daily）。各1.6秒。録画は数日前のアプリだが、見せている画面とラベルは origin/main と一致。フィクスチャの「デモデータ」とデイリーレッスンの「QA用データ」の文はマスク。
- 新しいポーズ7つを codex-p で（`prompts/01-codex-poses.txt`）：mimi-silent、mimi-try、mimi-study、pippa-chat、pippa-squint、coco-chat（ビーチの水着ではなくワンピース、麦わら帽は残す）、teacher-explain（025の講師の衣装、バゲットなし）。ほかはライブラリ（bruno-talk、bruno-boss-nod、bruno-tourist-laugh、pippa-clerk-smile、confident、notes）と背景（meeting、cafe、cafe-counter、desk）。
- 議論の英語はKokoro（ブルーノ am_michael、ピッパ af_nicole、ココ af_bella）。かぶせ合うように重ね、Mimiにはせりふなし（「…」の吹き出しのみ）。講師の言葉は日本語の吹き出し。オーナーの声は使っていない（発音の場面がない）。
- 「自信を持って話す」は文法ミスを含む英語（"Yesterday I go … and I say …"、赤い波線）で見せ、「読むのは苦手」はピッパが紙に目を細める絵、「逆」は 読む／話す の◎△の比較カードで。
- BGMはテーマ曲をキットの音量で、22.4–38.4秒（現実〜講師〜研究）はさらに下げて落ち着かせた（同じ曲、新しい音楽なし）。声が前半19秒だけなので、mimi-quitter と同じく静的ゲイン＋リミッター（出来上がり約−16 LUFS、イヤホンでは控えめ側）。
- 長さ：約50秒の依頼に対して52.6秒（エンドカード込み）。

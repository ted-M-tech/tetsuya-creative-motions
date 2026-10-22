# 制作の経緯

オーナーの言葉（2026-10-21、企画の採用）：「2,3,6,7,8,9,11,12 作成で」。親セッションからの指示（この作品）：

- 030「US vs UK English in My Own Voice」。フック「アメリカ英語とイギリス英語、同じ私の声で言ってみた」＋聞き分けクイズ「Which one is British?」（A/B、少し間をおいて正解）。
- 声の調整（話し方＋自由入力のアクセント）を使う。両方ともオーナーの声（ownvoice.py の `us` と `uk`）、イギリス英語の目印（r を発音しない、t をはじかない、broad a：water, can't, party, car）が詰まった文。初めて聞いて違いがはっきりわかること。UK がアメリカ英語っぽければ作り直し（最大3回）。
- #23（mimi-tuning、同じ題材を別のエージェントが作り直し中）のコピーではなく、短いクイズ形式のスピンオフに。アプリの録画は合えば再利用してよい。
- オーナーのルール（2026-10-21）：Mimiの一人称は日本語の文字ではすべて「僕」（私・わたし・あたしは使わない）。→ フックは「同じ僕の声で言ってみた」、オチは「AもBも、僕の声だよ」。

判断：

- 機能の確認（Lanclo `origin/main` 5998d20d）：`native-ios/Lanclo/Views/VoiceTuningEditor.swift` に「話し方」（`voice.style.*`：自然に・落ち着いて・いきいきと・やさしく・はっきり）、「話す速さ」「表現」、自由入力「発音・話し方のリクエスト」（`voice.direction`、プレースホルダ「Describe a regional accent, dialect, or delivery you would like.」、最大400文字）、「試聴音声を作る」（`store.generateVoice(… direction: …)`）。アクセントは「リクエスト」で、結果の保証はしない表現にした（キャプション「声は同じ。アクセントはリクエスト」）。
- アプリの録画は mimi-tuning の撮影（Lanclo 57b4fc93、`TuningWalkthrough.swift` + `british-preview.patch`）を再利用。57b4fc93 → 5998d20d で VoiceTuningEditor.swift / VoiceScreen.swift に差分なし。使ったのは調整シートの「落ち着いて」タップと「イギリス英語っぽく」の入力（キーボードが無いコマを1文字ずつ）、「試聴音声を作る」に赤枠（押していない）。生成後の一覧（パッチで作った表示）は使っていない。QA用データ等の表示は映っていない。
- 文は「I can't park the car by the water.」：can't（broad a）、park / car（r を発音しない、a は「アー」）、water（t をはじかない、語末の r なし）。#23 の文とは別にした。短い（約2.4秒）のでクイズで2回＋答え合わせでもう1回聞ける。
- 違いの確認（UK は1回目の生成で採用、作り直しなし）：Praat（parselmouth）の F3 中央値 park 3015 Hz / car 2867 Hz（UK、r の響きなし）に対し US は park 1972 Hz / car 2469 Hz（r の響きで下がる）。can't の F2 は UK 1223 Hz（後ろ寄りの「アー」）、US 1410 Hz。長さ UK 0.21–2.61秒、US 0.26–2.15秒。whisper（large-v3-turbo）で両方とも全文一致。
- 出題順：フックは「アメリカ英語とイギリス英語」の順なので、A をイギリス英語にして「Bでしょ！」と外す友だちのボケに。
- 声は「試聴音声を作る」で作ったものではない（ownvoice.py で同じ登録声・同じモデルから生成）ので、注記「※英語の声は制作者本人がLancloに登録した声のAIボイスです（イメージ）。」を付けた。
- ポーズは既存のみ（Mimi：speak-open/closed、mimi-tease。友だち：friend-tease、friend-oops、friend-amazed）。国旗・紋章は使っていない。Mimiは左右反転していない（ヘッドホンの「L」は見て左）。

学び：アクセント比較では「r の後の母音」が多い短文が一番わかりやすく、F3（r の響き）で客観的に確認できる。

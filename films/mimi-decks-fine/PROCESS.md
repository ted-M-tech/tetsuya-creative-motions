# 制作の経緯

Notion Content Calendar ID 065（Drive「065. Beyond Im Fine Thank You」、Prefix `Decks_ImFine`）。バッチ 055–066 の1本。オーナーの言葉（原文）：

> 2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」

> 2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

> 2026-10-23（セーフエリア）：「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」

承認された企画（コーディネーターの要約）：フック「I'm fine, thank you. しか言えない」。Mimiが "How's it going?"、友だちがロボットのように "I'm fine, thank you, and you?"。Mimiがあくび、「間違いじゃないけど教科書っぽい」。実アプリ：マイノート → 単語帳 → スラング・カジュアル → カード → 保存。友だちが単語帳に本当にある言い方でやり直し、ハイタッチ。エンドカード。キャストはMimiと友だちだけ（Notionの当初案のBrunoは使わない）。デッキの語数・件数は出さない、監修・正確さの主張もしない。

## アプリで確かめたこと（Lanclo origin/main 5f5571ad、native-ios が正）

- 単語帳はiOSのマイノートの「単語帳」（`native-ios/Lanclo/Views/OfficialDecksScreen.swift`）：デッキ一覧 → ユニット一覧 → ユニットのカード（用語、IPA、意味、使い方、例文）。カードごとの保存ボタン（`decks.save.<id>`、`SavedNoteButton`、押すとすぐ保存されタグのメニューが出る）、下に「すべて保存」「学習」。
- デッキ名：初級／中級／上級／ビジネス／句動詞・イディオム／スラング・カジュアル。一覧とユニットに「N語・保存済みN」が出る（`OfficialDeckCopy.counts`）ので、編集で全部マスクした。
- 撮影は `LancloUITests/OfficialDecksUITests.swift` の `testBundledJapaneseCatalogBrowseAndSave` と同じ起動（`--qa-notes`、`--qa-route /vocabulary`、同梱の本物のデッキ、ネットワークと音声なし）。撮影専用パッチなし。
- 返しの言い方は `packages/core/decks/source/slang-casual/04.json`（ユニット4「あいさつ・お礼・謝罪」）から：`how's it going`（調子はどう）、`all good`（全部大丈夫・問題ない）、`what's new`（何か変わったことある）。"How's it going?" への自然な返しで、デッキにあるものとして「All good! What's new?」にした（ブリーフの "and you?" に当たる聞き返しも、同じユニットの what's new）。「Not bad」などはデッキにないので使わない。

## 判断

- Mimiの "How's it going?" は吹き出しだけ（声なし）。オーナーの声を両方のうさぎに当てると一人で話しているように聞こえるため。声は友だちの2行だけ。
- 声（ownvoice.py、有料）：2行、各1回の生成、再生成なし。`fine` は教科書を読み上げるロボット口調（style指定）、`casual` は自然なアメリカ英語。Whisperはタイムスタンプと言葉の確認だけ（"I'm fine. Thank you. And you?" / "All good. What's new?"、余計な語なし）。
- 新しいポーズ2つ（codex-p、キャスト参照画像つき）：`mimi-yawn`（あくび）と `highfive`（Mimiと友だちのハイタッチ）。1回目のハイタッチは手が合っているのが分かりにくく（頬を寄せているように見えた）、`prompts/02-codex-highfive-retry.txt` で1回やり直して採用。参考にした mimi-origin の highfive は友だちがベレー帽なので使わなかった。ほかはライブラリの friend-speech（紙を持つ＝教科書っぽい）、friend-shrink、friend-hello、speak-open、point。
- 録画は2回。1回目はユニット内のスクロールが足りず all good に届かなかった（Drive には上げない）。2回目は届いたがカードを上に寄せる動作が効かず、カードは画面下のまま保存した。編集で端末を1.4倍に寄せて見せた（35秒ほどのスクロールの停滞は使っていない）。スクロール部分は45倍速で1秒。
- xcodebuild の test-without-building がテスト終了後も終わらず、1回目は手で止めた（シミュレーターのロックは毎回解放）。
- 音（v1）：キットの Mix.write のあと、mimi-katakana-mcdonalds と同じ後処理（不足分のゲイン＋リミッター）で −14.1 LUFS、トゥルーピーク −1.6 dBTP。
- セーフエリア（コーディネーター指示）：英語字幕は y≤1500・x 60–880 に収め、エンドカードの英語字幕は上（y 230）へ。右の操作列（x>900, y 820–1520）にラベル・吹き出し・小さいMimiを置かない（説明ラベルは x 60–880、保存時の小さいMimiは左下）。キャラの顔は x 900 より左。フックの1行目は y≥200。

## v2（コマンダーのレビュー、2026-10-23）

指示（要約）：アプリ部分（5.5–12.2秒、BGMとSFXだけ）が約 −14.5 LUFS で大きすぎる。イヤホンで聞くオーナーはBGM・SFXを声の下で静かにしたい。声のない区間はほかの作品のBGMだけの部分と同じ（約 −25〜−27 dB RMS、キットの THEME_GAIN のまま、追加ゲインなし）。−14 LUFS は声がはっきり上にある場合だけ。ベッドが上がるなら静かな方を選んで数値を報告。フックの「I'm fine, thank you.」がカードの右端に触れているので余白を。

- 原因：Mix.write の loudnorm（1パス、動的）が声のない区間を持ち上げていた。`mix.py` は Mix.write と同じバス配分とダッキングのまま、loudnorm を使わず作品全体に1つのゲイン（−14 LUFS に必要な量と、アプリ部分を −26 dBFS RMS にする量の小さい方）＋リミッター 0.8 にした。
- 結果：アプリ部分 −26 dBFS RMS（約 −24.4 LUFS）、声の区間 −13.4 / −9.9 LUFS、全体 −17.4 LUFS integrated、トゥルーピーク −1.7 dBTP。声のクレストが大きく、ベッドを上限に置くと −14 には届かないので、指示どおり静かな方を採った。
- フック：文字 84→74px、左右の余白 36→52px、折り返しなし。
- Drive：v1 は `old/` に `_v1` を付けて移動。

## v3（コマンダーのフォローアップ、2026-10-23）

指示（要約）：v2 はリミッターが声のピークを最大 ~7 dB 削っていて潰れて聞こえるおそれ、2つの声も −13.4 / −9.9 LUFS で不揃い。リミッターではなくクリップごとのゲインで、2つの声をそろえる（casual を下げる）。アプリ部分は ~−26 dBFS RMS のまま、全体ゲインはリミッターの削りが 2 dB 以下になるように。integrated は結果を受け入れる（−15〜−17 程度で可）。

- 各声クリップに軽いダイアログ用コンプレッサー（ratio 3、attack 0.5 ms、soft knee、threshold −30 dB）をかけてから、クリップごとのゲインで同じラウドネスにそろえた（casual を下げる側）。コンプなしだと声のクレストが ~15 dB あり、ピーク 2 dB 以内の条件ではベッドが −30 dBFS まで下がった。
- 全体ゲインは「−14 LUFS」「アプリ部分 −26 dBFS RMS」「リミッター 2 dB 以内」の最小。今回はリミッター条件で決まった。
- 結果：リミッター最大 2.0 dB、声 −12.1 / −11.5 LUFS（クリップ区間）、アプリ部分 −27.1 dBFS RMS（約 −25.5 LUFS）、全体 −17.3 LUFS、トゥルーピーク −1.6 dBTP。
- Drive：v2 は `old/` に `_v2` を付けて移動。

## 学んだこと

- 単語帳のユニットはカードが長く（例文・使い方つき）、遅いスワイプでは後半のカードに届くまで1分以上かかる。録画は速いスワイプで進め、編集で早送りにする。
- `ps -o etimes` は macOS にない（ウォッチドッグは `etime` を使う）。

## Owner approval

- 2026-10-23: 「全部OK」 (all twelve shorts of the 055–066 batch approved as delivered; the Drive cuts were renamed without `_draft_`: `Decks_ImFine_2026-10-23.mp4`, `Decks_ImFine_EN-subs_2026-10-23.mp4`).
- Earlier owner notes in the same review round (2026-10-23): 「56の英語音声少し切れている？」 (clipped English in 056; led to the voice-cut audit of every episode); 「62透過されている？」 (the see-through angry pose in 062; fixed there with a filled pose).

# 制作の経緯

Notion Content Calendar ID 068（Drive「068. Real Slang 1 - No Cap」、Prefix `Slang1_NoCap`）。新シリーズ「Real Slang」第1話（公式単語帳「スラング・カジュアル」から1話1枚）。第2〜4話（hangry、ghosted、mid）はこの `source/` を写して作る（README の Series template）。オーナーの言葉（原文）：

> 2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」

> 2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

> 2026-10-23（セーフエリア）：「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」

> 2026-10-23（シリーズの見た目）：「フォントの色とか変わってる？統一感出して過去と」

承認された企画（コーディネーターの要約）：フック「"No cap" = 帽子なし？」と帽子のギャグ。Mimiが大げさな自慢＋「No cap!」、友だちは帽子を探す。意味カード（単語帳の文言）と単語帳の例文1つ（オーナーの声）。実アプリ：単語帳 → スラング・カジュアル → ユニット → カード → 保存。CTA「次のスラングは？コメントで」。キャストはMimiと友だちだけ。単語帳の意味・例文だけを使う（Notion当初案の「cap = 嘘だろ」は単語帳の「うそ・大げさな話」に直した）。

## アプリと単語帳で確かめたこと（Lanclo origin/main 1088ae0b、native-ios が正）

- 単語帳の中身：`packages/core/decks/source/slang-casual/03.json`（ユニット3「賛成・反対・返事」）。`no-cap`（14枚目）：意味「うそなしで・まじで」／"used to emphasize that you are being honest"、例文 "No cap, I practiced that move fifty times."／「うそなしで、その動きを50回練習した。」、使い方の例 "This is my favorite soup, no cap."。`cap-slang`（15枚目）：意味「うそ・大げさな話」／"a statement considered false or exaggerated"、ヒント「帽子ではなくうその意味。相手に直接言うと不信感を示す。」（映像ではヒントの1文目だけ）。同梱カタログ `native-ios/Lanclo/Resources/official-decks.json` にも入っている。
- 画面：`native-ios/Lanclo/Views/OfficialDecksScreen.swift`。デッキ一覧 → ユニット一覧 → カード（用語、IPA、品詞・スラングのバッジ、意味、使い方、その他の例文、ヒント）。保存はカードのブックマーク（`decks.save.<id>`、押すとタグのメニュー）。一覧とユニットに「N語・保存済みN」（`OfficialDeckCopy.counts`）が出るので編集で全部マスク。カード画面には件数なし。
- 撮影は `LancloUITests/OfficialDecksUITests.swift` の `testBundledJapaneseCatalogBrowseAndSave` と同じ起動（`--qa-notes`、`--qa-route /vocabulary`、`--qa-official-decks` なし＝同梱の本物のデッキ、ネットワークと音声なし）。撮影専用パッチなし。origin/main では他のテストが `--qa-official-decks`（小さいテスト用データ）を使うので、それは付けない。

## 判断

- 大げさな自慢は単語帳の例文そのもの（"No cap, I practiced that move fifty times."）にした。単語帳の文言以外を使わないため。意味カードの例文も同じ文で、声をもう一度流す（追加の生成なし）。
- 声（ownvoice.py、有料）：3本、各1回、再生成なし。`claim`（Mimi、自慢げな米語）、`huh`（友だち「Cap...?」、帽子を探す疑問）、`nocap`（カードの用語だけの単独テイク。文から切り出さない）。どのクリップも丸ごと置き、頭と尾10msはピーク比 −62〜−88 dB（圧縮後 −44〜−70 dB）で −38 dB 以下。
- Whisper（small.en と medium.en）は claim を "I've practiced" と書いたが、スペクトログラムでは「I」（1.12–1.25秒）のあとに無声の閉鎖（1.25–1.32秒、/p/）があり、/v/ の有声の摩擦は見えない。"I practiced" と判断（耳での確認はオーナーに依頼）。
- 新しいポーズと小物（codex-p、キャスト参照画像つき、`prompts/01-codex-search-and-cap.txt`）：`friend-search`（友だちが頭をさわって帽子を探す）と `cap`（ロゴなしの野球帽）。暗い背景で透けがないことを確認。ほかはライブラリの confident、tease、point、friend-nod、friend-amazed、friend-yay、jump。
- 録画は1回。速いスワイプでユニット3の先頭から no cap のカードまで一瞬で進み、スクロールのフレームが録画に残らなかったので、編集でカードのクリップを下からスライドさせた。保存後のタグのメニュー（63.8–67.0秒）は飛ばした。xcodebuild は今回は止まらず終了（念のためウォッチドッグつきで実行）。シミュレーターのロックは毎回解放。
- 音：Mix.write の loudnorm はアプリ部分（声なし）を声と同じ −16 dBFS まで持ち上げたので、mimi-decks-fine v3 と同じく、各声に軽いコンプ＋クリップごとのゲイン（−20 LUFS）、Mix.write と同じバス配分とダッキングで静的に混ぜ、全体に1つのゲイン（声のない区間を −26 dBFS RMS に抑える上限つき）＋リミッター。共有ブリーフの −14 LUFS に合わせて、リミッターで減った分を同じ上限内で足した。結果：両カット −14.4 LUFS、トゥルーピーク −2.2 dBTP、アプリ部分 −26.0 dBFS RMS、声 −12〜−13 dBFS RMS、リミッターの最大 3.8 dB（圧縮済みの声のピークだけ）。
- セーフエリア：英語字幕は y≤1500・x 60–880、エンドカードの英語字幕は上（y 230）。意味カードは右端 x 880 まで（右の操作列に文字を入れない）。小さいMimiと友だちは顔が字幕にかからない位置（y 1185）。説明ラベルは端末の上（y 345）に置き、アプリのカード見出しとブックマークを隠さない。キャラの顔は x 900 より左。フックの1行目は y≥200。
- シリーズの見た目：テンプレート（mimi-decks-fine）とCSSを比べ、色はキットと同じ（文字 #273b4b、青 #2a8dff、赤 #e5484d、グレーの面 #eef2f5、ラベル #344f69）、フック 74px、英語の吹き出し 56px、字幕 `.caption.small` にそろえた（初版のヒントのオレンジ色、フック 76px、吹き出し 52px をやめた）。

## 学んだこと

- `timeout` コマンドは macOS にない。ウォッチドッグは `sleep N; pkill -f ...` をバックグラウンドで。
- 速いスワイプはシミュレーター録画にスクロールのフレームを残さないことがある。スクロールを見せたいならゆっくり、見せないなら編集でつなぐ。

## オーナー承認

> 2026-10-23：「あと全部確認した。YouTubeあげてOK」

下書きのまま完成版にした（変更なし）。Driveの2本は `_draft_` を外して `Slang1_NoCap_2026-10-23.mp4`、`Slang1_NoCap_EN-subs_2026-10-23.mp4` に改名。

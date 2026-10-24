# 制作の経緯

Notion Content Calendar ID 069（Drive「069. Real Slang 2 - Hangry」、Prefix `Slang2_Hangry`）。シリーズ「Real Slang」第2話。第1話 `films/mimi-slang-no-cap`（ブランチ `feat/mimi-slang-no-cap`）の Series template をそのまま使った（同じビートid、レイアウト、色、フォント、静的ミックス）。オーナーの言葉（原文）：

> 2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」

> 2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

> 2026-10-23（セーフエリア）：「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」

> 2026-10-23（シリーズの見た目）：「フォントの色とか変わってる？統一感出して過去と」

承認された企画（コーディネーターの要約）：フック「お腹すいてイライラ＝？」、昼前に空のお弁当箱を持って不機嫌な友だち、Mimi「You're hangry!」。意味カード hungry + angry = hangry（単語帳の文言）。実アプリ：単語帳のカード → 保存。CTA「次のスラングは？コメントで」、エンドカード。キャストはMimiと友だちだけ。第1話からの改善：意味カードの行を速く出し、半分空のカードを0.5秒以上見せない。

## アプリと単語帳で確かめたこと（Lanclo origin/main ff11569c、native-ios が正）

- 単語帳の中身：`packages/core/decks/source/slang-casual/06.json`（ユニット6「気分・テンション」）。`hangry`（13枚目、形容詞、スラング）：意味「空腹でいらいらした」／"irritable because you are hungry"、例文 "I'm getting hangry; let's find lunch."／「空腹でいらいらしてきた。昼食の店を探そう。」と "A snack helped my hangry mood."／「軽食で空腹によるいらいらが和らいだ。」。`usage` と `tip` はない。同梱カタログ `native-ios/Lanclo/Resources/official-decks.json` にも入っている。
- 「hungry ＋ angry」は単語帳の文言ではない（企画の指定）。カードの見出しとして語の成り立ちだけを小さく出し、意味・例文は単語帳の文言そのまま。気になるなら外せる（`#r0`）。
- 画面：`native-ios/Lanclo/Views/OfficialDecksScreen.swift`（`decks.deck.<id>`、`decks.unit.<N>`、`decks.card.<id>`、`decks.save.<id>`）。カードには IPA がない（単語帳に `ipa` がないため）。一覧とユニットに「N語・保存済みN」が出るので全部マスク。
- 撮影は第1話と同じ起動（`--qa-notes`、`--qa-route /vocabulary`、`--qa-official-decks` なし＝同梱の本物のデッキ）。撮影専用パッチなし。`SlangWalkthrough.swift` は `DECK_UNIT=6`、`CARD_ID=hangry`、`NEXT_ID=i-m-dead`、`UNIT_FIRST_TERM=chill` に変え、ユニットが画面外なら少しスクロールする行を足した（今回は不要だった）。

## 判断

- 話の流れ：フックの答えをMimiが1.0秒で言う（「You're hangry!」）、友だちは単語帳の例文で認める。例文は意味カードでもう一度流す（追加の生成なし）。
- 声（ownvoice.py、有料）：3本のうち2本を生成、各1回、再生成なし。`youre`（Mimi「You're hangry!」）、`example`（友だち、単語帳の例文）。3本目の `term`（カード用の単独テイク「Hangry.」）は共有TTSの1日の上限（HTTP 429）で未生成。コーディネーターの指示どおり再試行をやめた。上限が戻ったら `python3 kits/mimi-short/scripts/ownvoice.py films/mimi-slang-hangry/source/own-voice.json` で `term` だけが生成され、`mix.py` がそのまま 6.0 秒に置く（今はスキップして警告を出す）。429 は生成されていないので回数に数えていない。
- どのクリップも丸ごと置き、頭と尾10msはピーク比 −78〜−80 dB（圧縮後 −61〜−62 dB）で −38 dB 以下。Whisper（medium、タイムスタンプのみ）でも文言どおり。
- 新しいポーズ（codex-p、キャスト参照画像つき、`prompts/01-codex-hangry.txt`）：`friend-hangry`（空のお弁当箱、怒りマーク、湯気、お腹の音の線）と `friend-lunch`（おにぎりで元気）。暗い背景で透けがないことを確認。ほかはライブラリの tilt、point、tease、friend-amazed、jump。
- 意味カード：4行（hungry ＋ angry、hangry ＝ 意味、例文1、例文2）を 5.95〜6.45 秒で全部出す（第1話は 5.35〜8.9 秒に分けて出していた）。話している例文1は 7.4〜9.9 秒に青い枠で光らせる。
- 録画は1回（ロックは毎回解放）。今回はスワイプのフレームが残ったので、カードを上に寄せる実際のドラッグ（90.95–91.55秒）をそのまま使い、第1話の作りもののスライドはやめた。ユニット一覧ではユニット6が一番下で、その「25語・保存済み0」がガラスのタブバー越しに透けていたので、デッキ一覧（タブバーの後ろに何もない）から切り出したタブバーを重ねて隠した。保存後のタグのメニュー（96.2–100.1秒）は飛ばした。xcodebuild が録画のあと終わらなかったので、自分の xcodebuild だけを止めた。
- 音：第1話の mix.py と同じ静的ミックス（各声に軽いコンプ＋−20 LUFS、全体1ゲイン＋リミッター）。お腹の音はコードで作った低い音（約85 Hz、ローパス、小さめ）。結果：両カット −14.0 LUFS、トゥルーピーク −2.2 dBTP、アプリ部分 −26.9 dBFS RMS、声 −13〜−14 dBFS RMS。
- セーフエリア：`process/01-zones-en.jpg`（英語字幕版、0.75秒ごと、下420px・右の操作列・上200pxを描いたもの）で確認。英語字幕は y≤1500・x 60–880、エンドカードの英語字幕は上。右のMimiを60px左に寄せ、tilt の「?」と顔が x 900 より左に来るようにした。端末の下部（タブバー）は下の帯にかかるが、第1話と同じく雰囲気で、意味はラベルと字幕にある。
- シリーズの見た目：CSS は第1話からコピーし、色（#273b4b、#2a8dff、#e5484d、#eef2f5、#344f69）、フック 74px、吹き出し 56px、字幕 `.caption.small` はそのまま。足したのは「hungry ＋ angry」の行（44px、青と赤はキットの色）と例文の青い枠だけ。

## 学んだこと

- ウォッチドッグの `pkill -f 'testSlangWalkthrough'` は、ロック待ちのほかのエージェントのシェル（同じ文字列を含む）まで止めてしまう。止めるのは自分の xcodebuild の PID だけにする。

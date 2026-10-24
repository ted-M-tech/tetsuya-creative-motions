# 制作の経緯

Notion Content Calendar ID 070（Drive「070. Real Slang 3 - Ghosted」、Prefix `Slang3_Ghosted`）。シリーズ「Real Slang」第3話。`films/mimi-slang-no-cap` の `source/` を写し、README の Series template どおりに作った。オーナーの言葉（原文）：

> 2026-10-23 依頼：「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」

> 2026-10-23 承認：「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

> 2026-10-23（セーフエリア）：「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」

> 2026-10-23（シリーズの見た目）：「フォントの色とか変わってる？統一感出して過去と」

承認された企画（コーディネーターの要約）：フック「既読スルー、英語で？」、返事の来ないスマホを見つめる友だち、Mimi「You got ghosted.」。おばけの小物はよい（小物で、顔のあるキャラにしない）。実アプリ：単語帳のカード → 保存。カードは単語帳 08.json の「ghost」と「leave sb on read」（アプリで見せるのは ghost、2枚目は意味カードで触れる）。キャストはMimiと友だちだけ。改善点：意味カードの行を速く出す（半分空のカードを約0.5秒以上見せない）。

## アプリと単語帳で確かめたこと（Lanclo origin/main ff11569c、native-ios が正）

- 単語帳の中身：`packages/core/decks/source/slang-casual/08.json`（ユニット8「SNS・ネット文化」）。`ghost`（3枚目）：意味「突然連絡を絶つ」／"to stop responding to someone without explanation"、例文 "I didn't mean to ghost you; my phone broke."／「無視するつもりじゃなかった。電話が壊れたんだ。」。`leave-sb-on-read`（4枚目）：意味「既読のまま返事をしない」／"to read someone's message without replying"。どちらも同梱カタログ `native-ios/Lanclo/Resources/official-decks.json` に同じ文言で入っている。leave sb on read のヒント（「既読は返信できる状態や無視する意図の証拠ではない。」）は長いので映像には入れない。
- 画面：`native-ios/Lanclo/Views/OfficialDecksScreen.swift`（`decks.unit.<N>`、`decks.card.<id>`、`decks.save.<id>`）。ユニット一覧に「N語・保存済みN」が出るので編集でマスク。ユニットとカードの画面には件数なし。
- 撮影は no-cap と同じ起動（`--qa-notes`、`--qa-route /vocabulary`、`--qa-official-decks` なし、撮影専用パッチなし）。ユニット8は一覧の画面外なので、タップの前にゆっくり1回スワイプする処理を足した。

## 判断

- 今回の録画はアプリが最初からスラング・カジュアルのユニット一覧で開いた（直前の別の撮影の画面状態が残ったとみられる）。単語帳のデッキ一覧のフレームがないので、アプリ部分はユニット一覧（ユニット8が見えている静止部分、件数はマスク）から始めた。字幕「マイノートの単語帳にスラング・カジュアル」はそのまま（画面の見出しもスラング・カジュアル）。カードまでのスクロールは録画に本物が残ったので、no-cap のような編集のスライドは使わない。
- 意味カード：3行（ghost、例文、leave sb on read）を 5.05／5.45／5.85 秒に出し、0.9秒で全部そろう（no-cap は3.6秒かけていた）。leave sb on read の行は長いので用語だけ 72px（他は 84px）、意味は2行に分けた。
- フックのチャットはHTMLで作った汎用の小物（実在のアプリではない）。「今夜ひま？」「既読 21:03」、入力中の「•••」が0.8秒で消える。
- おばけの小物（codex-p、キャスト参照画像はスタイル参照）：1回目のシーツ型のおばけはSNSアプリのロゴに似ていたので不採用（`prompts/01`）、2回目の尾の長い形は読みにくいので不採用（`prompts/02`）、3回目の三角の布つきの日本のおばけ（顔なし）を採用（`prompts/03`）。暗い背景で透けがないことを確認。ポーズはライブラリの friend-sigh、friend-shock、tease、grin、point、friend-amazed、friend-yay、jump（新しいポーズなし）。
- 声（ownvoice.py、有料）：4本（`ghosted` Mimi、`huh` 友だち「Ghosted...?」、`ghost` 用語の単独テイク、`example` 単語帳の例文）。2026-10-23 の生成は共有の Gemini TTS の1日の上限（HTTP 429、100回/日）で止まり、まだ1本も生成していない（課金なし）。上限が戻ってから生成して、無音を測ってタイミングを合わせる。それまでの `mix.py` は声なしで BGM と効果音だけを混ぜる（暫定、警告を出す）。
- セーフエリア：英語字幕は y≤1500・x 60–880、エンドカードの英語字幕は上。意味カードは x 880 まで。Mimi の顔は x 900 より左（フックとギャグの Mimi を 30–40px 左へ）。フックの1行目は y≥200。
- シリーズの見た目：no-cap と CSS を比べ、色はすべて同じ役割（文字 #273b4b、青 #2a8dff、赤 #e5484d、面 #eef2f5、ラベル #344f69）。フック 74px、吹き出し 56px、字幕 `.caption.small`。新しいサイズはチャットの小物の 52px と長い用語の 72px だけ。

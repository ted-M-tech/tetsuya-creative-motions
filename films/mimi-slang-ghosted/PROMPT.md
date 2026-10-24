# 統合プロンプト（完成形を作り直すための指示。最初の入力の原文ではない）

Lanclo SNSショート「Real Slang」第3話（Mimiと友だち、公式2D、1080×1920・60fps、17.1秒、HyperFrames）を作る。`lanclo-sns-short` スキルの固定ルールと `films/mimi-slang-no-cap/README.md` の Series template に従う。内容は単語帳 `packages/core/decks/source/slang-casual/08.json` の「ghost」「leave sb on read」の文言だけを使う。

- hook 0–3.0秒：1フレーム目からフック「既読スルー（赤）、英語で？」。左に友だち（friend-sigh、スマホを見てため息）、その上にチャットの小物（青い吹き出し「今夜ひま？」、「既読 21:03」、入力中の「•••」が0.8秒で消える）。0.9秒から右にMimi（tease）、吹き出しと声で「You got ghosted.」（オーナーの声）。
- gag 3.0–5.0秒：チャットからおばけ（顔なしの小物、三角の布つき）が「?」とともに浮かぶ。友だち（friend-shock）「Ghosted…?」（オーナーの声）、Mimi（grin）。字幕「おばけ…？」。
- meaning 5.0–9.4秒：カード。行は0.9秒以内に全部出す（半分空のカードを見せない）：「ghost ＝ 突然連絡を絶つ」（「Ghost.」の単独テイク）、例文「I didn't mean to ghost you; my phone broke.／無視するつもりじゃなかった。電話が壊れたんだ。」（例文の声）、「leave sb on read ＝ 既読のまま返事をしない」。小さいMimi（point）と友だち（friend-amazed）。英語字幕は単語帳の英語の意味。
- app 9.4–13.8秒：実アプリ。マイノートの単語帳 → スラング・カジュアル → ユニット8 SNS・ネット文化 → 「ghost」のカードで保存。語数・保存数の行はマスク。ラベル「ghost ＝ 突然連絡を絶つ」、字幕「カードを保存！」。
- cta 13.8–15.6秒：二人で喜ぶ（friend-yay、jump）。字幕「次のスラングは？／コメントで」。
- end 15.6–17.1秒：エンドカード、16.2秒にCTAタップ（pochi）。
- 英語字幕版は `.sub`（y≤1500、x 60–880）。音は声が主、テーマBGMはキットの音量、全体に1つのゲイン＋リミッターで −14 LUFS。

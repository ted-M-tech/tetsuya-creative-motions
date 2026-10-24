# 統合プロンプト（完成形を作り直すための指示。最初の入力の原文ではない）

Lanclo SNSショート「Real Slang」第4話（Mimiと友だち、公式2D、1080×1920・60fps、15.9秒、HyperFrames）を作る。`lanclo-sns-short` スキルの固定ルールと `films/mimi-slang-no-cap` の Series template に従う。内容は単語帳 `packages/core/decks/source/slang-casual/02.json` の「mid」の文言だけを使う。

- hook 0–3.2秒：1フレーム目からフック「"It's mid"（赤）って／褒められてる？」。左の友だち（friend-proud）がごはんを掲げ、右のMimiが食べて（chew、0–0.8秒）から淡々と（flat）「It's… mid.」（オーナーの声、"It's…" と "mid." の間の長い無音だけを無音の中で詰める）。
- gag 3.2–5.0秒：友だち（friend-yay）「Mid? Thanks!」（オーナーの声）。字幕「やった！褒められた！」。
- meaning 5.0–8.4秒：カード「mid ＝ たいしたことない」（「Mid.」の単独テイク）、0.45秒後に例文「The trailer was great, but the movie was mid.／予告編はよかったけど、映画は微妙だった。」。友だち（friend-shrink）がしょんぼり、吹き出し「褒めてなかった…」。Mimi（point）。英語字幕は単語帳の英語の意味。
- app 8.4–12.8秒：実アプリ。単語帳 → スラング・カジュアル → ユニット2 → 実際のスクロール（早送り）→「mid」のカードで保存。語数・保存数の行はマスク。ラベル「mid ＝ たいしたことない」、字幕「カードを保存！」。
- cta 12.8–14.4秒：二人で喜ぶ（friend-yay、jump）。「次のスラングは？／コメントで」。
- end 14.4–15.9秒：エンドカード、15.0秒にCTAタップ（pochi）。
- 英語字幕は y≤1500・x 60–880。音は声が主、テーマBGMはキットの音量、全体に1つのゲイン＋リミッターで −14 LUFS。

# 統合プロンプト（完成形を作り直すための指示。最初の入力の原文ではない）

Lanclo SNSショート「Real Slang」第1話（Mimiと友だち、公式2D、1080×1920・60fps、17.4秒、HyperFrames）を作る。`lanclo-sns-short` スキルの固定ルールに従う。内容は単語帳 `packages/core/decks/source/slang-casual/03.json` の「no cap」「cap」の文言だけを使う。

- hook 0–3.4秒：1フレーム目からフック「"No cap"（赤）＝ 帽子なし？」と×のついた野球帽。右のMimi（confident）が吹き出しと声で「No cap, I practiced that move fifty times.」（単語帳の例文、オーナーの声、自慢げな米語）。左の友だち（friend-nod）。
- gag 3.4–5.3秒：友だち（friend-search、頭をさわる）「Cap…?」（オーナーの声）、帽子が「?」とともに浮かぶ。Mimi（tease）。字幕「帽子…どこ？」。
- meaning 5.3–9.7秒：カード。「no cap ＝ うそなしで・まじで」（「No cap.」の単独テイク）、例文「No cap, I practiced that move fifty times.／うそなしで、その動きを50回練習した。」（例文の声をもう一度）、「cap ＝ うそ・大げさな話」、ヒント「帽子ではなくうその意味。」。小さいMimi（point）と友だち（friend-amazed）は字幕の上。英語字幕は単語帳の英語の意味。
- app 9.7–14.1秒：実アプリ。マイノートの単語帳 → スラング・カジュアル → ユニット3 → 「no cap」のカードで保存（ブックマークが塗られる）。語数・保存数の行はマスク。ラベル「no cap ＝ うそなしで・まじで」、字幕「カードを保存！」。
- cta 14.1–15.9秒：二人で喜ぶ（friend-yay、jump）。字幕「次のスラングは？／コメントで」。
- end 15.9–17.4秒：エンドカード、16.5秒にCTAタップ（pochi）。
- 英語字幕版は `.sub`（y≤1500、x 60–880）。音は声が主、テーマBGMはキットの音量。動的 loudnorm を使わず全体に1つのゲイン（声のない区間は −26 dBFS RMS）＋リミッターで −14 LUFS。

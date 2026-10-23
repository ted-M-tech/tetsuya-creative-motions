# Can You Hear It? 3 - Ship or Sheep

[English](README.md)

Lanclo SNS ショート #078。シリーズ「Can You Hear It?（聞き分けクイズ）」第3話。視聴者はコメントで A / B を答える。16.2秒、1080×1920、60fps、2カット（日本語のみ／英語字幕つき）。ドラフト（2026-10-23、オーナー確認待ち）。

1フレーム目から A・B の2枚のカードとフック「ship？sheep？聞き分けて」。カウントダウン 3-2-1 の間に、オーナー本人の声（US）で “I saw a sheep.”（A）と “I saw a ship.”（B）が流れ、問いは「sheep はどっち？」。友だちは「Bでしょ！」。正解は A、カードの下に羊と船のアイコン、友だち「えっ！？ 同じに聞こえた…」、Mimi が「ふふっ、ハズレ〜」とにやり。Mimi のルールカード「「イ」の長さと口の形を聞く！」：ship＝短く、ゆるむ（軽い「イ」）、sheep＝長く、口を横に引く（ニッと「イー」）、母音の長さバーが伸びる、2文をもう一度、「口を横に「イー」→sheep」。最後に「A？B？コメントで！」とエンドカード。

学習ポイント（アメリカ英語）：ship は短くゆるい /ɪ/、sheep は長く張った /iː/（口を横に引き、舌は高く前）。母音の長さと明るさを聞く。

| 秒 | ビート（id） |
|---|---|
| 0.00–1.80 | `hook`：A / B カード＋「ship？sheep？聞き分けて」 |
| 1.80–5.50 | `play`：「sheep はどっち？」、カウントダウン 3（A 2.0秒）→2（B 3.55秒）→1、友だち「Bでしょ！」4.75秒 |
| 5.50–7.90 | `reveal`：正解は… A（6.0秒）、カードの下に a sheep / a ship、友だち「えっ！？ 同じに聞こえた…」、Mimi「ふふっ、ハズレ〜」 |
| 7.90–13.10 | `rule`：Mimi のカード、“I saw a ship.” 8.5秒、“I saw a sheep.” 9.75秒、「口を横に「イー」→sheep」11.25秒 |
| 13.10–14.80 | `ask`：「A？B？コメントで！」／最初、どっちが sheep に聞こえた？ |
| 14.80–16.20 | `end`：エンドカード、CTA タップ 15.4秒 |

- 声：2文ともオーナー本人の登録済み Lanclo ボイス（accent `us`、`kits/mimi-short/scripts/ownvoice.py`）。WAV は生体データのため Git に入れない（Drive `078. Can You Hear It 3 - Ship or Sheep/Hear3_Ship_assets/own-voice/`）。母音の長さと F1 / F2 の音響チェックは [PROCESS.md](PROCESS.md)。
- キャスト：Mimi と友だちのみ（ライブラリのポーズ）。Mimi の一人称の台詞はなし（使うなら「僕」）。
- ドラフト：Lanclo の Google Drive `002.SNS/078. Can You Hear It 3 - Ship or Sheep/`（`Hear3_Ship_draft_2026-10-23.mp4`、`Hear3_Ship_draft_EN-subs_2026-10-23.mp4`）。
- 再現手順：[source/README.md](source/README.md)。

![フレーム](process/00-draft-frames.jpg)

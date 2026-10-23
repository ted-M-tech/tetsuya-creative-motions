# Can You Hear It? 1 - Can or Can't

[English](README.md)

Lanclo SNS ショート #061。新シリーズ「Can You Hear It?（聞き分けクイズ）」第1話。視聴者はコメントで A / B を答える。16.1秒、1080×1920、60fps、2カット（日本語のみ／英語字幕つき）。**ドラフト**（2026-10-23）、オーナー確認待ち。

1フレーム目から A・B の2枚のカードとフック「can？can't？聞き分けて」。カウントダウン 3-2-1 の間に、オーナー本人の声（US）で “I can't swim.”（A）と “I can swim.”（B）が流れ、問いは「can はどっち？」。友だちは「Aでしょ！」（t が聞こえなかったから）。正解は B、Mimi が「ふふっ、ハズレ〜」とにやり。Mimi のルールカード「t じゃなく、母音を聞く！」：can＝弱く短い（クン）、can't＝はっきり強い（t はほぼ聞こえない）、2文をもう一度。最後に「A？B？コメントで！」とエンドカード。

学習ポイント（アメリカ英語）：文の中の can は弱く短く（k'n）、強勢は動詞に来る。can't は /æ/ の母音と強勢を保ち、t はほとんど聞こえないことが多い。t ではなく母音を聞く。

| 秒 | ビート（id） |
|---|---|
| 0.00–1.80 | `hook`：A / B カード＋「can？can't？聞き分けて」 |
| 1.80–5.40 | `play`：「can はどっち？」、カウントダウン 3（A 2.0秒）→2（B 3.35秒）→1、友だち「Aでしょ！」4.6秒 |
| 5.40–7.80 | `reveal`：正解は… B（5.9秒）、カードの下に答え、友だち「えっ！？ t が聞こえなかったのに…」、Mimi「ふふっ、ハズレ〜」 |
| 7.80–13.00 | `rule`：Mimi のカード、“I can swim.” 8.4秒、“I can't swim.” 9.7秒、「「キャン」と強い→can't」11.1秒 |
| 13.00–14.70 | `ask`：「A？B？コメントで！」／最初、どっちが can に聞こえた？ |
| 14.70–16.10 | `end`：エンドカード、CTA タップ 15.3秒 |

- 声：2文ともオーナー本人の登録済み Lanclo ボイス（accent `us`、`kits/mimi-short/scripts/ownvoice.py`）。WAV は生体データのため Git に入れない（Drive `061. Can You Hear It 1 - Can or Cant/Hear1_Can_assets/own-voice/`）。音響チェックは [PROCESS.md](PROCESS.md)。
- キャスト：Mimi と友だちのみ（ライブラリのポーズ）。Mimi の一人称の台詞はなし（使うなら「僕」）。
- ドラフト：Lanclo の Google Drive `002.SNS/061. Can You Hear It 1 - Can or Cant/`（`Hear1_Can_draft_2026-10-23.mp4`、`Hear1_Can_draft_EN-subs_2026-10-23.mp4`）。
- 再現手順：[source/README.md](source/README.md)。シリーズのテンプレート（第2話以降）：[README.md の Series template](README.md#series-template-episodes-2)。

![ドラフトのフレーム](process/00-draft-frames.jpg)

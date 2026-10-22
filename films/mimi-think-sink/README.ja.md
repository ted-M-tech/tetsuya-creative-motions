# think が sink に — Mimi 2Dショート

[English](README.md) · **日本語**

Mimiが得意げに "I sink so!" と言うと、空からシンク（流し台）が落ちてくる。もう一度言うと2台目。Lancloで自分の声の正しい "I think so." を聴き、レーダーで th の直し方を1つ知り、お手本に合わせて練習すると、シンクが消えて言えるようになる。Mimiショート2本目で、共通キットで作った最初の作品。

0:15 / 1080×1920、60 fps / 日本語字幕・英語の声 / 2D：公式の絵柄をCodexで描画＋Riveの骨＋HyperFrames

![完成フレーム](process/00-final-frames.jpg)

## ファイル

- [PROCESS.md](PROCESS.md)：制作過程。依頼者の指示、共通キット、レビュー、判断、学んだこと。
- [PROMPT.md](PROMPT.md)：作り直す・別の話を作るための統合プロンプト。
- [prompts/](prompts/)：Codexに渡したプロンプトの原文（絵とレビュー）。
- [reviews/](reviews/)：Codexの完成版レビュー。
- [source/](source/README.md)：この回のショット、音、HyperFramesの編集、書き出し手順。
- [kits/mimi-short](../../kits/mimi-short/README.md)：共通キット（ライブラリの写し、リグ、音、見た目）。
- [CREDITS.md](CREDITS.md)：素材と権利。
- 汎用ガイド：[2Dキャラクターアニメ制作ガイド](../../docs/2D-CHARACTER-ANIMATION.ja.md)。

## 再現

[source/README.md](source/README.md) の手順どおり。声2本（依頼者本人の声。公開リポジトリには入れず、Driveの `Mimi_02_Think_Becomes_Sink_assets/own-voice/` に保管、または `kits/mimi-short/scripts/ownvoice.py` で作り直す）、書き出し途中のファイル、完成MP4以外はすべてGitにある。

2026-10-21から、Mimiの英語の声は依頼者本人のLanclo登録音声（Gemini `gemini-3.8-flash-tts`）。"I sink so!" は学習者の発音、"I think so." はアメリカ英語のお手本。

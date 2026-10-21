# 日記、3日で終わる — Mimi 2Dショート

[English](README.md) · **日本語**

英語日記3日目、Mimiは本当にお坊さんに（三日坊主）。Lancloの英語日記なら話すだけで自然な英語に直り（go → went）、自分の声で聴けて、その日がMimiの絵になる。絵日記みたいに見返すのが楽しくて、三日坊主を卒業。Mimiショート4本目、機能（英語日記）を紹介する最初の回。

0:16.6 / 1080×1920、60 fps / 日本語字幕・英語の声 / 2D：公式の絵柄をCodexで描画＋Riveの骨＋HyperFrames

![完成フレーム](process/00-final-frames.jpg)

## ファイル

- [PROCESS.md](PROCESS.md)：制作過程。依頼者の指示（イラスト中心への作り直しを含む）、レビュー、判断、学んだこと。
- [PROMPT.md](PROMPT.md)：作り直す・別の機能の回を作るための統合プロンプト。
- [prompts/](prompts/)・[reviews/](reviews/)：Codexへのプロンプトと2回のレビュー。
- [source/](source/README.md)：ショット、音、編集、書き出し手順。
- [kits/mimi-short](../../kits/mimi-short/README.md)：共通キット。
- [CREDITS.md](CREDITS.md)：素材と権利。

## 再現

[source/README.md](source/README.md) の手順どおり。声も含め必要なものはすべてGitにあり、書き出し途中のファイルと完成MP4だけが入っていない。

2026-10-21から、Mimiの英語の声は依頼者本人のLanclo登録音声（Gemini `gemini-3.8-flash-tts`）。"Yesterday... I go to cafe." は学習者の発音、"Yesterday, I went to a cafe." はアメリカ英語のお手本。声の素材はGitに入れず、Driveの `Mimi_04_Journal_Ends_in_3_Days_assets/own-voice/` に保管。

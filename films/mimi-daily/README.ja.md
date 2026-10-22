# 積読 — Mimiがデイリーレッスンを使う

[English](README.md) · **日本語**

英語の本が増えるだけで読まれない（積読）Mimiが、実際のLancloでデイリーレッスンを開く（シミュレーターでQA用のデモデータを表示して録画）。今日の一文 "Please leave the light on." を自分の声のネイティブ発音で聴き、録音すると "right" と言ってしまい、5つの視点の採点と、直す音（right → light）がわかる。Mimiショート6本目、実画面の2本目。

0:15.2 / 1080×1920、60 fps / 日本語字幕・英語はLancloに登録したオーナー本人の声 / 2DのMimi（Rive）とアプリの録画

![完成フレーム](process/00-final-frames.jpg)

## ファイル

- [PROCESS.md](PROCESS.md)：制作過程。
- [PROMPT.md](PROMPT.md)：この回の統合プロンプト。
- [prompts/](prompts/)・[reviews/](reviews/)：本の山の作画プロンプトとCodexのレビュー。
- [source/](source/README.md)：操作手順、切り出し、ショット、音、編集。
- [kits/mimi-short/app-capture](../../kits/mimi-short/app-capture/capture.sh)：共通の録画スクリプト。
- [CREDITS.md](CREDITS.md)。

## 再現

[source/README.md](source/README.md) の手順どおり。アプリの録画にはLancloのリポジトリとXcodeが要る。この版で使った録画はLancloのGoogle Driveに保管。

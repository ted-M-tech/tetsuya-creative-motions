# 写真で英語 — Mimiが実際のアプリを使う

[English](README.md) · **日本語**

カフェの写真を英語で説明しようとして "People is sitting..." しか言えないMimiが、Lancloの写真描写を使う。実際のアプリ（シミュレーターでQA用のデモデータを表示して録画）が答えを採点し、間違いに印を付け、is → are を直し、もっと自然な一文を自分の声で聴かせる。Mimiショート5本目、実画面を使う最初の回。

0:15 / 1080×1920、60 fps / 日本語字幕・英語の声 / 2DのMimi（Rive）とアプリの録画

![完成フレーム](process/00-final-frames.jpg)

## ファイル

- [PROCESS.md](PROCESS.md)：制作過程。アプリの録画方法を含む。
- [PROMPT.md](PROMPT.md)：実画面の回の統合プロンプト。
- [prompts/](prompts/)・[reviews/](reviews/)：Codexのレビュー。
- [source/](source/README.md)：操作手順、切り出し、ショット、音、編集。
- [kits/mimi-short/app-capture](../../kits/mimi-short/app-capture/capture.sh)：共通の録画スクリプト。
- [CREDITS.md](CREDITS.md)。

## 再現

[source/README.md](source/README.md) の手順どおり。アプリの録画にはLancloのリポジトリとXcodeが要る。この版で使った録画はLancloのGoogle Driveに保管。

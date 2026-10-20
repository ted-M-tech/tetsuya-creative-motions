# Mimi 3D — マスコットを、ソフビのように

[English](README.md) · **日本語**

LancloのマスコットMimi（2D）を、Blender 5.2のPythonスクリプトだけで3Dに。Claude CodeとCodexで9往復レビューし合って仕上げ、ショートアニメ用の3D正本として承認されたもの。

![モデルシート](process/12-final-sheet.jpg)

## ファイル

- [PROCESS.md](PROCESS.md)：制作過程。依頼者の指示、すべてのプロンプト、各レビューの採否、途中経過の画像を順に。
- [PROMPT.md](PROMPT.md)：別のキャラクターで同じことをするための統合プロンプト。
- [prompts/](prompts/)：Codexに渡したプロンプトの原文（英語）。
- [reviews/](reviews/)：Codexのレビュー（往復3〜9と最終判定は原文、1〜2は要約）。
- [source/](source/README.md)：v1時点のスクリプトと参照画像。
- 汎用の手順：[3Dキャラクター制作ガイド](../../docs/3D-CHARACTER-WORKFLOW.ja.md)

## 正本

承認済みの `.blend`・スクリプト・シートは、Lanclo本体リポジトリの `design/mimi-3d/`（非公開）にあります。ここの `source/` は公開記録用のv1（2026-10-20）の写しです。変更は正本から行ってください。

Mimi、Lanclo のロゴ、目標画像はLanclo のもので、再利用はできません。コードはこのリポジトリの他と同じくMITです。

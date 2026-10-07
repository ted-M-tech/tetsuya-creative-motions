# Reproduction prompts / 再現用プロンプト

2026-10-07に実装・資料を確認して再構成。原文の会話ログではありません。1回の入力で完成したという意味ではありません。

## 事前に渡すもの

製品の現行仕様、利用できる機能と予定機能、承認済みブランド、権利確認済みの画像・画面、主な訪問者とCTA。秘密情報や実ユーザーのデータは含めない。

## 1. 構成

```text
日本語学習アプリのLPを作る。対象は単語を知っていても会話になると言葉が出ない学習者。冒頭でその悩みに触れ、最初の5分を「話す→すぐ振り返る→漢字スタンプを残す」で見せる。承認済みキャラクターと実機画面を使い、説明は1場面1メッセージ。英語を主に日本語切替を用意。近日予定の機能と利用できる機能を明確に分け、320・390・768・1440pxで画面、改行、CTA、言語切替を確認する。
まず各セクションの目的・見せる素材・一番伝えることを整理し、重複を削った構成を提示する。
```

## 2. 実装・調整

```text
承認した構成を実装する。既存のブランド・コピーの事実・導線を維持。画像が主役になる場所では説明を重ねない。レスポンシブな改行、画像比率、フォーカス表示、言語切替を確認。動きは意味を説明する箇所に限定し、reduced-motionで内容が消えないようにする。
```

## 3. レビューと記録

```text
320/390/768/1440pxで表示する。横はみ出し、画像読み込み、リンク、CTA、動画のポスターと再生、キーボード操作を確認する。主題と重複する補足を削る。変更した理由、残った制約、素材出典、公開版のファイルSHA、検証結果を制作ノートに追記する。
```

## English brief

```text
Create a Japanese-learning app landing page for people who know words but freeze in conversation. Show the first five minutes as talk → review immediately → keep a kanji stamp. Use approved characters and real app screens, with one message per scene. Support English and Japanese. Separate upcoming from available features. Verify screens, text wrapping, CTAs and language switching at 320, 390, 768 and 1440px.
```

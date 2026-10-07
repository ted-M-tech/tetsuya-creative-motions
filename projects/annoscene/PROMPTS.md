# Reproduction prompts / 再現用プロンプト

2026-10-07に実装・資料を確認して再構成。原文の会話ログではありません。1回の入力で完成したという意味ではありません。

## 事前に渡すもの

製品の現行仕様、利用できる機能と予定機能、承認済みブランド、権利確認済みの画像・画面、主な訪問者とCTA。秘密情報や実ユーザーのデータは含めない。

## 1. 構成

```text
旅の記録を自分のAtlasとして残すiPhoneアプリのLPを作る。現行の仕様と承認済み画面だけを使う。霧の山並みを大きく置き、「Your world, drawn over time.」を軸に静かな余白で構成する。世界→国→地域へ進む短い操作デモ、その国の記録、年別表示へつなぐ。写真の取り込みや位置情報記録など旧仕様を混ぜない。説明は短く、App Store導線を明確にする。画像サイズ、動画ポスター、読み込み失敗時、390pxと1440pxでの表示を検証する。
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
Create a landing page for an iPhone app that records places in a personal Atlas. Use only current product facts and approved screens. Lead with misty mountains and “Your world, drawn over time.” Use quiet space, a short world → country → region demo, country context and year view. Do not introduce retired photo-import or location-tracking features. Keep copy brief and the App Store path clear. Check image sizes, video posters, loading fallbacks and layouts at 390 and 1440px.
```

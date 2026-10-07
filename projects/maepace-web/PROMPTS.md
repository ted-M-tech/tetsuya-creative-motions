# Reproduction prompts / 再現用プロンプト

2026-10-07に実装・資料を確認して再構成。原文の会話ログではありません。1回の入力で完成したという意味ではありません。

## 事前に渡すもの

製品の現行仕様、利用できる機能と予定機能、承認済みブランド、権利確認済みの画像・画面、主な訪問者とCTA。秘密情報や実ユーザーのデータは含めない。

## 1. 構成

```text
個人開発者の実績と創作物を伝えるMaePaceのWebサイトをAstroで作る。承認済みロゴと単色のブランドを維持。ツール群が動くヒーロー、人物紹介、開発プロジェクト、完成作品、相談導線へつなぐ。作品はLPひとつ・動画ひとつの単位にし、クリック後に完成物、制作ノート、再現プロンプトを置く。日英コピーはデータで管理。ヘッダー・フッターは共通化。Canvasの描画ループ重複を防ぎ、スマホの改行、キーボード操作、動きを減らす設定でも確認する。
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
Build an Astro website for a developer’s projects and creative work. Preserve the approved MaePace mark and monochrome identity. Connect a moving tool-universe hero to the person, projects, completed works and contact. Count one LP or film as one artifact; its detail page shows the result, making-of and reproduction prompts. Manage bilingual copy as data and share the header and footer. Prevent duplicate Canvas animation loops and check mobile wrapping, keyboard navigation and reduced motion.
```

# MaePace — 好奇心を、前へ進む力に。

[完成したサイト](https://maepace.com/) · [作品ページ](https://maepace.com/works/maepace-web)

## この作品の狙い

ツール群が動くヒーローから、人物・開発実績・完成作品へ。仕事のプロジェクトと見て試せる成果物を分けつつ、共通のヘッダーと言語設定で行き来できる構成にしました。

A moving tool universe leads into the person, development projects and completed creative work. Projects and finished artifacts remain distinct, joined by a shared header and language preference.

## 設計判断

- プロジェクト集の下に作品集を置き、完成物の一覧から制作方法へ進める。 / Place creative works below projects, with finished previews leading into making-of notes.
- コピーを日英のデータとして分離し、同じ部品で両言語を表示する。 / Separate bilingual copy from layout and use the same components for both languages.
- 動きはCanvas・CSS・IntersectionObserverで実装し、表示外では不要な描画を止める。 / Use Canvas, CSS and IntersectionObserver; avoid unnecessary rendering off screen.

## 再現するには

1. [PROMPTS.md](PROMPTS.md) の段階別指示を使い、独自の製品情報・ブランド・承認済み画像を渡す。
2. 対応する現行仕様と公開予定を分け、画面構成を先に確認する。
3. 小さい画面で表示し、コピー・操作・動きの確認を経て公開する。

## 記録の範囲

ブランド資料・実装・Git履歴を根拠に整理。公開ノートは再現用の設計資料で、サイト全体のソース一式ではありません。

完全な会話ログ・原制作時のモデル版・全依存バージョンは揃っていません。この公開は同一画面を自動生成する完全なビルドキットではなく、同じ設計判断を辿れる制作ノートです。実装の観察・履歴と、後からの再構成を区別しています。

- 1172743: rebuild on Astro with real content and the MaePace brand.
- 9344f47: promote the tool universe to the hero.
- 3c77425: completed works gallery under the shared MaePace site.

確認したファイルのSHAは [EVIDENCE.json](EVIDENCE.json)。使用技術は [SKILLS.md](SKILLS.md)、権利と素材の扱いは [CREDITS.md](CREDITS.md)。

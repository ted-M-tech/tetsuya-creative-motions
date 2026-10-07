# Tako Talk — 会話を、明日の習慣へ。

[完成したサイト](https://helpkansai.maepace.com/) · [作品ページ](https://maepace.com/works/tako-talk)

## この作品の狙い

「日本語は知っている。でも話せない」から始まり、最初の5分でできることを見せる。会話の直後に振り返り、漢字スタンプを残す流れを、端末画面と短い動きでつなぎました。

Start with knowing Japanese but struggling to speak, then show the first five minutes. Actual phone screens and short motion connect conversation, immediate review and a daily kanji stamp.

## 設計判断

- 機能の列挙より、会話→振り返り→スタンプの体験順で見せる。 / Show conversation → review → stamp in experience order, rather than listing features.
- 実際のアプリ画面を主役にし、Takoのキャラクターで親しみを添える。 / Lead with actual app screens; use Tako’s character to add warmth.
- 標準語での練習と、近日予定の関西弁を区別する。 / Distinguish available standard-Japanese practice from the upcoming Kansai mode.

## 再現するには

1. [PROMPTS.md](PROMPTS.md) の段階別指示を使い、独自の製品情報・ブランド・承認済み画像を渡す。
2. 対応する現行仕様と公開予定を分け、画面構成を先に確認する。
3. 小さい画面で表示し、コピー・操作・動きの確認を経て公開する。

## 記録の範囲

LPの復元記録と更新履歴から整理。制作時の会話ログ全体や使用スキルは確認できていないため、以下は再構成した指示です。

完全な会話ログ・原制作時のモデル版・全依存バージョンは揃っていません。この公開は同一画面を自動生成する完全なビルドキットではなく、同じ設計判断を辿れる制作ノートです。実装の観察・履歴と、後からの再構成を区別しています。

- site/README.md records recovery of the deployed static site; it explicitly says the original commit was not identified.
- cf9c4454: conversation review and daily kanji habit integration.
- 8a3e6adc: legal page layout and simpler section curves.

確認したファイルのSHAは [EVIDENCE.json](EVIDENCE.json)。使用技術は [SKILLS.md](SKILLS.md)、権利と素材の扱いは [CREDITS.md](CREDITS.md)。

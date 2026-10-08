# AnnoScene — 旅の記憶を、静かな地図に。

[完成したサイト](https://annoscene.maepace.com/) · [作品ページ](https://maepace.com/works/annoscene)

## この作品の狙い

霧の山並みから、自分のAtlasを開く体験へ。世界→国→地域と進む操作デモと、年を選ぶ画面に絞り、説明を増やさず製品の静けさを伝えました。

Move from misty mountains into a personal Atlas. A world → country → region demo and a year-view screen convey the quiet product without adding long explanations.

## 設計判断

- 最初に旅の気配を見せ、続いて実際のAtlas操作で機能を説明する。 / Lead with the feeling of travel, then explain function through actual Atlas interactions.
- 世界・国・地域・年という地図の文脈を崩さず、画面を見せる。 / Keep the map’s world, country, region and year context intact in the demo.
- プライバシーとApp Storeへの導線を短くまとめ、機能を詰め込みすぎない。 / Keep privacy and the App Store path concise rather than overloading the page.

## 再現するには

1. [PROMPTS.md](PROMPTS.md) の段階別指示を使い、独自の製品情報・ブランド・承認済み画像を渡す。
2. 対応する現行仕様と公開予定を分け、画面構成を先に確認する。
3. 小さい画面で表示し、コピー・操作・動きの確認を経て公開する。

## 記録の範囲

現行のAtlas版LPを対象に記録。過去の位置情報・写真・旅程リプレイ中心の製品説明は、この作品の再現指示に含めていません。

完全な会話ログ・原制作時のモデル版・全依存バージョンは揃っていません。この公開は同一画面を自動生成する完全なビルドキットではなく、同じ設計判断を辿れる制作ノートです。実装の観察・履歴と、後からの再構成を区別しています。

- At the recorded design revision, `lp/index.html` held the Atlas page. The 2026-10-07 Astro migration moved the authoritative page to `lp/src/pages/index.astro` (upstream PR #97, source `5f5296cebeedf0cbc74a3c67cf2adbf11f138758`). Existing screenshots and the demo were preserved.
- scripts/lp-check.mjs: rejects obsolete Journey Replay copy and checks required media size budgets.
- c9dc484: regional Atlas navigation; 20328fc: every Regional Atlas made free.

確認したファイルのSHAは [EVIDENCE.json](EVIDENCE.json)。使用技術は [SKILLS.md](SKILLS.md)、権利と素材の扱いは [CREDITS.md](CREDITS.md)。

# 制作と確認に使ったもの

スキル（AIへの作業指示）、実行ツール、素材、技術スタックを分けて記録します。以下は保存済み記録から確認できた範囲で、全会話・全呼出しの完全な一覧ではありません。

| 工程 | 使ったもの | 確認できる範囲 |
|---|---|---|
| 製品・体験の設計 | Product Design | Lanclo発音練習UI。初期プロトタイプでの指定、後続UI改善でのガイダンス参照。最終LP全面への使用は未確認 |
| LPのデザイン比較 | Taste Skill / Impeccable | 初期案・批評と、採用した最終方向。[スキル記録](../projects/lanclo-lp/SKILLS.md) |
| 根拠・出典の調査 | agent-reach、GitHub CLI、Web検索・一次資料 | 研究・参照元の確認。調査結果は作品の出典へ。全検索履歴は未保存 |
| 旧版のイラスト案 | imagegen、Sharp | Lanclo旧版に生成イラストと画像最適化の記録あり。現在の主な人物画はunDrawで、生成案を最終採用素材と混同しない |
| 最終LP素材 | unDraw、Pexels、製品UI | 素材ライブラリ・写真・実装画面。[権利と出典](../projects/lanclo-lp/CREDITS.md)。スキルではない |
| LP実装 | React / JSX、Vite、Motion、CSS、Phosphor | Lanclo公開ソースの依存と実装。新規標準のAstroへ移行済みという意味ではない |
| Web作品集 | Astro、TypeScript、CSS | MaePaceの実装。作品ごとの記録に従う |
| 動画 | HyperFrames系スキル、HTML/SVG、GSAP、Gemini TTS、FFmpeg | [動画制作フロー](VIDEO-WORKFLOW.ja.md)と[Lanclo素材記録](../films/lanclo/CREDITS.md)。すべての版で同じ工程を使ったとは限らない |
| レスポンシブ・挙動確認 | Playwright、Chromium、WebKit、スクリーンショット目視 | Lancloの多言語・幅別検証、比較表のセル確認。エンジン検証は実機Safari確認とは異なる |
| 作業・公開 | Git、GitHub CLI、ビルド、Cloudflareの静的配信 | ソースを固定して公開。プロジェクト別の公開手順と権限に従う |
| 再現記録の整備 | skill-creator、web-production、open-creative-handoff | 完成物・指示・判断・素材・実行手順の保存。Web標準は今回抽出した工程 |

Lanclo側の根拠文書：`docs/self-voice-practice/lp-taste-direction.md`、`lp-impeccable-direction.md`、`lp-visual-assets.md`、`lp-video-integration.md`、`lp-publication.json`、`feedback-practice-refinement.md`。履歴には途中で廃止した動画モーダルや停止ボタンの検証もあるため、そのすべてを現在のUI仕様として扱わないでください。

## 他の人が再現する入口

1. [Lancloの固定ソースと実行手順](../projects/lanclo-lp/README.md)で完成形を動かす。
2. [指示と修正の記録](../projects/lanclo-lp/PROMPTS.md)、[判断理由](../projects/lanclo-lp/DECISIONS.md)、[使用スキル](../projects/lanclo-lp/SKILLS.md)を読む。
3. [レスポンシブ検証](WEB-QA.ja.md)を実行し、画像を目視する。
4. [共通制作フロー](WEB-WORKFLOW.ja.md)と[記録テンプレート](../templates/web/REPRODUCTION.md)で自分の作品を作る。

同じ見た目を起動するには固定ソースと素材が必要です。同じ工程を学ぶにはプロンプトと判断記録が必要です。スキル名の一覧だけでは、どちらも再現できません。

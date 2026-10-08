# Prompts: historical inputs and reusable recipe

## Actual user excerpts

These are curated excerpts from the design conversation, in sequence. They are not the full chat and contain no private operational handoffs.

> 文字でごまかすな。イラストで表現しろよ。

> カルーセルの画像、リアルな画像の方がいいな。一目でわかる。あとカルーセルのスピードもっと速くていい

> ここ3ステップなら3ステップのイラストを左から並べてわかるようにして

> ページ全体通して改行が自然か確認。スマホもね

> 補足不要なとこは文字消していいからね。シンプルに美しく。

## Reconstructed reusable prompt

The following was written after completion to consolidate the iteration. It was **not** a single original prompt that generated the finished page.

```text
Create a landing page for [product], for [specific learner/customer].
Start from the attached verified capabilities and approved brand assets.
Lead with the user's desired change, then show the mechanism in three
illustrated steps. Use a concrete frustration to motivate that mechanism.
Choose one illustration family. Use real photos only where the subject
requires instant recognition. Reuse actual product UI rather than fake UI.
Keep supporting copy only where it adds information. On mobile, make
comparison possible without hiding the alternatives off screen.
Animate the mechanism, not every decoration; respect reduced motion.
For research, name the measured outcome, baseline, sample and limitation.
Do not imply the product was tested if the study used another intervention.
Keep sources, asset licenses, dependency lock and a decision log with the code.
Verify the full page at 320, 390 and 1440 pixels, including wrapping,
keyboard access, image loading, links and reduced motion. Show the preview.
```

## Iteration method

Change one problem class per pass: narrative → visual mechanism → typography → motion → mobile → evidence → publication. Compare the actual rendered page, not only the source. Save deliberate product images; keep repetitive QA captures out of Git.

## Navy edition — 2026-10-08

Actual user excerpts: 「ヘッダーも同じ色に。ほぼ黒くらいまでの色にしたら？」 / 「苦手分析→レッスン生成→ボタン押して読むだけ」 / 「濃い紺色を他のとこにも水平展開。サイトとして統一感持たせて。美しく」. Reconstructed brief: unify the navy palette while retaining light sections, layer two pointer-responsive waves and illustrate the three-step practice flow.

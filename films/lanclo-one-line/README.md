# Lanclo One line — one line shows it all.

**English** · [日本語](README.ja.md)

A short promo where a single voice line draws the logo, your voice vs. the model, a five-axis radar, the next practice point, four practice modes, the tagline and the logo again — plus feature shorts (9:16) built the same way. No narration: Japanese on-screen type with English subtitles.

Promo 0:26 (16:9) / English journal short 0:22 (9:16) / 1080p, 60 fps / Python, pycairo, numpy (every frame and every sound made in code). On-screen type is Japanese.

## Films

- **Promo** (16:9): hear native pronunciation in your own voice.
- **[English journal](shorts/journal/README.md)** (9:16): record by voice, get corrections and an illustration, see your days on a calendar. The breakdown is in Japanese.

## Decisions

- Borrows the structure of Duolingo's spec-ad prompt "The Path" (one continuous line, camera flight, mascot slam hook) and swaps in Lanclo's colours, mascot and copy.
- A Japanese narration was recorded and then dropped: type alone keeps the tempo and works on muted social feeds. Reading time comes from holds in the picture, not slower music.
- The only voices are the LP's English comparison clips (the learner's own voice and the model).
- Screens with demo values say so ("デモ表示").
- Feature shorts: one feature each, stations stacked vertically, subtitles kept above the bottom area that social apps cover.

## Files

- [PROMPT.md](PROMPT.md): reproduction prompt (Japanese, original language) — shared rules, promo beat sheet, vertical-short rules, how to swap in your own product.
- [shorts/journal/](shorts/journal/README.md): the English journal short.
- [source/](source/README.md): render and audio scripts, assets, build steps.
- [CREDITS.md](CREDITS.md): sources and terms.
- Reusable style: [One line](../../styles/one-line/STYLE.md).

## Re-editing

Follow `source/README.md`: fetch fonts, render audio, render picture. The two LP voice clips are not in Git (the promo still renders without them). The mascot, logo and photos belong to Lanclo and are not licensed for reuse; replace them in your own work.

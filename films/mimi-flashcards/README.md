# I fed my flashcards to Mimi — a 2D Mimi short (CSV how-to)

**English** · [日本語](README.ja.md)

Follow-up to [mimi-import](../mimi-import/README.md) (#20). Frame 1: flashcards stream into Mimi's open mouth under the hook「単語帳アプリのデータ、全部Mimiに食べさせた」(I fed all my flashcard app data to Mimi). Then how to make the CSV, as generic illustrations with no product names or logos: ① export CSV from your flashcard app, ② open it in a spreadsheet and name row 1 `term` / `meaning` (column C `tags` becomes a folder, optional), ③ save as CSV (UTF-8) → `単語帳.csv`. The real app (simulator, fixture data): My Notes →「CSVファイルを選ぶ」, Mimi eats the file (「いただきまーす！」) and the rows fly out as crumbs, then 新しく追加できるノート 10件 → 10件を追加しました。→ a 単語帳 folder with 10 notes → the review card "look forward to" with the model in the owner's own registered Lanclo voice. Close: the friend「いつもの単語帳が自分の声のお手本に！」, Mimi「ごちそうさま〜♪」. End card.

0:21.1 / 1080×1920, 60 fps / Japanese captions and speech bubbles, one English phrase / official 2D poses + GSAP, real app (simulator) + HyperFrames

Two cuts: Japanese only (`mimi-flashcards.mp4`) and with English subtitles (`mimi-flashcards-en.mp4`); drafts in Lanclo's Google Drive `002.SNS/034. I Fed My Flashcards to Mimi/` (`Flashcards_draft_2026-10-21.mp4`, `Flashcards_draft_EN-subs_2026-10-21.mp4`, raw take, CSV and voice in `Flashcards_assets/`).

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the owner's direction, the CSV format check and the decisions.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction to remake it.
- [prompts/](prompts/): no new generation prompts (poses from mimi-import).
- [source/](source/README.md): app capture (walkthrough, the 10-row CSV, capture-only patch), voice, sound, HyperFrames edit, build steps.
- [CREDITS.md](CREDITS.md): materials and rights.

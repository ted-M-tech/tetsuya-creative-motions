# Talked for 180 Seconds — a 2D Mimi short

**English** · [日本語](README.ja.md)

Hook from the first frame:「180秒しゃべり続けたら、口癖がバレた」(I talked for 180 seconds, and my verbal habit got exposed). Mimi talks about the café photo in Lanclo's photo description (free speech, up to 3:00 — the app's own「最大 3:00」) while a clock runs (fast-forwarded to 3:00), and every "really" she says pops out around her until nine of them fill the screen. "3分、話しきった！" Then the real app's feedback (simulator): the transcript of what she said (nine "really"s, counted by a badge in the edit) and the individual correction that flags "It looks really, really nice." Her friend:「really、言いすぎ！」— Mimi:「……really？」 The correction card's improved wording, "It looks absolutely lovely.", in the owner's voice.「自分では気づけない口癖に、気づける。」

A different angle from [021 Keep Talking for 3 Minutes](../mimi-freespeech/README.md) (on branch `feat/mimi-freespeech`: the 3-minute challenge, a French friend, the output hypothesis) and [024 Mimi Is Always Watching](../mimi-watching/README.md) (Mimi's report of habits across several journal entries): here one 3-minute talk, and the comedic reveal of one filler habit in that talk's own feedback.

0:20.0 / 1080×1920, 60 fps / Japanese captions and bubbles; both English lines are the owner's own registered Lanclo voice (Gemini gemini-3.8-flash-tts via `kits/mimi-short/scripts/ownvoice.py`: `learner` for the habit-heavy take, `us` for the improved wording) / existing official 2D poses + GSAP, real app (simulator) + HyperFrames

Two cuts: Japanese only (`mimi-180.mp4`) and with English subtitles (`mimi-180-en.mp4`); drafts in Lanclo's Google Drive `002.SNS/033. Talked for 180 Seconds/` (`Talked180_draft_2026-10-21.mp4`, `Talked180_draft_EN-subs_2026-10-21.mp4`, raw take and voice clips in `Talked180_assets/`).

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the owner's words, what was checked in the app code, the decisions.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction to remake it.
- [prompts/](prompts/README.md): no new poses were drawn.
- [source/](source/README.md): app capture (walkthrough + capture-only fixture patch), voices, sound, HyperFrames edit, build steps.
- [CREDITS.md](CREDITS.md): materials and rights.

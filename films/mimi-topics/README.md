# AI Chat Never Knows What to Talk About — a 2D Mimi short

**English** · [日本語](README.ja.md)

Hook from the first frame:「AIと会話、毎回『何話そう…』で終わってない？」(chatting with AI — does it always end with "what do I even talk about?"). A generic AI chat app (no brand) waits with an empty box and a blinking cursor; Mimi stares at it, types "Hi!", and the AI throws the question back:「こんにちは！今日は何について話したい？」— Mimi:「……それを決めてほしいんだけど」. Copy:「Lancloなら、話すことはもう用意してある。」 Then the real app (simulator): Home with today's lesson waiting (デイリーレッスン), and the Practice menu's ready-made material — roleplay scenes (会話練習), photos to describe (写真描写), debate topics (ディベート練習). Back in today's lesson, the model (お手本) plays in your own voice and Mimi says "Please leave the light on." in the owner's registered Lanclo voice.「あとは、話すだけ。」「僕、もう迷わない！」

0:17.8 / 1080×1920, 60 fps / Japanese captions and bubbles, one English line in the owner's own registered Lanclo voice (Gemini gemini-3.8-flash-tts via `kits/mimi-short/scripts/ownvoice.py`, accent `us`) / existing official 2D poses + GSAP, real app (simulator) + HyperFrames

Two cuts: Japanese only (`mimi-topics.mp4`) and with English subtitles (`mimi-topics-en.mp4`); drafts in Lanclo's Google Drive `002.SNS/031. AI Chat Never Knows What to Talk About/` (`Topics_draft_2026-10-21.mp4`, `Topics_draft_EN-subs_2026-10-21.mp4`, raw take and the voice clip in `Topics_assets/`).

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the owner's words, what was checked in the app code, the decisions.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction to remake it.
- [prompts/](prompts/README.md): no new poses were drawn for this film.
- [source/](source/README.md): app capture, voice, sound, HyperFrames edit, build steps.
- [CREDITS.md](CREDITS.md): materials and rights.

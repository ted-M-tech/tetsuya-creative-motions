---
workflow: general-video
flow: automation
storyboard: no
message: "Your own voice, with native pronunciation — even you will like hearing it"
destination: instagram-reels
aspect: 1080x1920
language: ja
length: 15s
---

## Intent

15-second Mimi short 「自分の声、むり」 for Instagram Reels / TikTok. Relatable hook (hiding from her own recorded English), rewind, she listens and deflates, taps "her-voice model", is amazed, celebrates; Lanclo end card. 2D official illustration style, chosen over 3D by the owner.

## Assets

- assets/shots/*.mp4 — Rive renders of each shot (scripts/rig2d.py, scripts/render_rive.sh), desk background baked in, 60 fps.
- assets/shots/hook-last.png — last hook frame for the rewind.
- assets/mix.wav — voice clips + SFX + code-made bed, -14 LUFS (scripts/mix.py).
- assets/brand/ — Lanclo mark, App Store badge, Mimi for the end card.

## Notes

- Timeline and captions follow scripts/shots.py after the Codex storyboard review (value at 5.7 s, record vs playback on the phone, short second hide, no return to the sad pose).
- Captions sit at the top; the bottom ~400 px stays clear for platform UI.

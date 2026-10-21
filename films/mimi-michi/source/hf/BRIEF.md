---
workflow: general-video
flow: automation
storyboard: no
message: "Rehearse the answer in your own voice, and you won't freeze next time"
destination: instagram-reels
aspect: 1080x1920
language: ja
length: 15s
---

## Intent

Mimi short #3 「道を聞かれて固まる」 for Instagram Reels / TikTok. On a street, a passer-by asks Mimi the way in English and she freezes into an ice block ("Uh... uh..." from inside). At the desk she taps Lanclo and hears her own voice give the answer ("Go straight, and turn left."), reads a radar card with one fix (link "turn left" in one breath), practises with the model; back on the street the ice shatters, she points the way and the passer-by says "Thank you!". 1 s end card. 2D official illustration style.

## Assets

- assets/shots/*.mp4: Rive shots (../scripts/shots.py, ../scripts/render.sh); street plate for the street shots, desk plate for the rest; 60 fps.
- assets/mix.wav: Kokoro voices + kit SFX + kit bed, -14 LUFS (../scripts/mix.py; cue times shared with this edit).
- assets/ice.webp: the ice block cut-out (../art/cut).
- assets/kit/: staged by kits/mimi-short/stage.sh (kit.css, kit.js, brand, fonts, props). Not in Git.

## Notes

- Captions at the top; the bottom ~400 px stays clear for platform UI. Score and radar values are illustrative.

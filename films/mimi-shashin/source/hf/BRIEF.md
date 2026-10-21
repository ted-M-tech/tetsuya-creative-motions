---
workflow: general-video
flow: automation
storyboard: no
message: "One photo becomes an English lesson, played back in your own voice"
destination: instagram-reels
aspect: 1080x1920
language: ja
length: 15s
---

## Intent

Mimi short #5 「写真で英語」, the first with the real app. Mimi looks at a cafe photo and manages only "People is sitting... at a cafe." Then she uses Lanclo herself: the real screens (recorded in the simulator with fixture data) show 練習 → 写真描写 → the cafe photo → record → score with the mistake in red → is → are → a more natural sentence played in her own voice. Mimi stands beside the phone pointing, speaking, reading and listening. 1 s end card.

## Assets

- assets/app/*.mp4: clips of the real app (../app-capture/capture.sh records, ../app-capture/cut.sh cuts).
- assets/shots/*.mp4: Mimi on a flat plate the colour of the page, scaled to the left in the edit.
- assets/mix.wav, assets/cafe-photo.png (the app's cafe photo, from the recording).
- assets/kit/: staged by kits/mimi-short/stage.sh. Not in Git.

## Notes

- Captions at the top; the phone sits between the captions and the bottom ~400 px.
- Score and feedback are the app's QA fixtures, not a real assessment.

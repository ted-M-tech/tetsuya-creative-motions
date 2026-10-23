# Source

```sh
F=films/mimi-decks-fine/source
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording; no PATCH)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/DecksWalkthrough.swift OfficialDecksUITests.swift OfficialDecksUITests/testDecksWalkthrough $F/renders/app/decks.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 065/Decks_ImFine_assets/simulator_decks-slang-all-good.mov (Lanclo 5f5571ad)
sh $F/scripts/app_track.sh            # -> hf/assets/app/{list,units,unit4,scroll,card,saved}.mp4 (times measured in the script)
# 2. poses: codex-p with prompts/01-codex-poses.txt and 02-codex-highfive-retry.txt, then
kits/mimi-short/scripts/cutout.sh $F/art/mimi-yawn.png $F/art/mimi-yawn.webp
kits/mimi-short/scripts/cutout.sh $F/art/highfive.png $F/art/highfive.webp
# 3. voices (owner's own voice, paid; or copy fine.wav / casual.wav from Drive Decks_ImFine_assets/own-voice/ to $F/assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py      # hf/assets/mix.wav: one static gain, bed at -26 dBFS RMS (about -17 LUFS), TP <= -1.5 dBTP
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && P=kits/mimi-short/library/poses && cp $F/art/mimi-yawn.webp $F/art/highfive.webp \
  $P/friend-speech.webp $P/friend-shrink.webp $P/friend-hello.webp $P/speak-open.webp $P/point.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-decks-fine   # renders/mimi-decks-fine-en.mp4 and renders/mimi-decks-fine.mp4
```

The masks over the 「N語・保存済みN」 lines of the deck and unit lists are in `hf/index.html` (screen percentages). Not in Git: the recording, the own-voice WAVs (biometric), `hf/assets/`, renders, the theme BGM.

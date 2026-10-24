# Source

```sh
F=films/mimi-slang-hangry/source
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording; no PATCH, bundled real deck content)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
env -u PATCH LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/SlangWalkthrough.swift OfficialDecksUITests.swift OfficialDecksUITests/testSlangWalkthrough $F/renders/app/slang.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 069/Slang2_Hangry_assets/simulator_decks-slang-hangry.mov (Lanclo ff11569c)
sh $F/scripts/app_track.sh            # -> hf/assets/app/{list,units,unit,scroll,card,saved}.mp4 + tabbar.png (times measured in the script)
# 2. new poses: codex-p with prompts/01-codex-hangry.txt (cast references attached), then
kits/mimi-short/scripts/cutout.sh $F/art/friend-hangry.png $F/art/friend-hangry.webp
kits/mimi-short/scripts/cutout.sh $F/art/friend-lunch.png $F/art/friend-lunch.webp
# 3. voices (owner's own voice, paid; or copy youre/example/term.wav from Drive Slang2_Hangry_assets/own-voice/ to $F/assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py      # hf/assets/mix.wav (a missing clip is skipped with a warning)
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && P=kits/mimi-short/library/poses && cp $F/art/friend-hangry.webp $F/art/friend-lunch.webp \
  $P/tilt.webp $P/tease.webp $P/point.webp $P/friend-amazed.webp $P/jump.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-slang-hangry   # renders/mimi-slang-hangry-en.mp4 and renders/mimi-slang-hangry.mp4
```

The masks over the 「N語・保存済みN」 lines of the deck and unit lists are in `hf/index.html` (screen percentages, the same rows as episode 1); unit 6's count line shows through the glass tab bar, so a clean tab bar cut from the deck list (`tabbar.png`) covers it during the units clip. Not in Git: the recording, the own-voice WAVs (biometric), `hf/assets/`, renders, the theme BGM.

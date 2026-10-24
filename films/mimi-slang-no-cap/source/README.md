# Source

```sh
F=films/mimi-slang-no-cap/source
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording; no PATCH, bundled real deck content)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
env -u PATCH LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/SlangWalkthrough.swift OfficialDecksUITests.swift OfficialDecksUITests/testSlangWalkthrough $F/renders/app/slang.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 068/Slang1_NoCap_assets/simulator_decks-slang-no-cap.mov (Lanclo 1088ae0b)
sh $F/scripts/app_track.sh            # -> hf/assets/app/{list,units,unit,scroll,card,saved}.mp4 (times measured in the script)
# 2. new pose and prop: codex-p with prompts/01-codex-search-and-cap.txt (cast references attached), then
kits/mimi-short/scripts/cutout.sh $F/art/friend-search.png $F/art/friend-search.webp
kits/mimi-short/scripts/cutout.sh $F/art/cap.png $F/art/cap.webp
# 3. voices (owner's own voice, paid; or copy claim/huh/nocap.wav from Drive Slang1_NoCap_assets/own-voice/ to $F/assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py      # hf/assets/mix.wav: compressed + level-matched voices, one static gain, -14 LUFS
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && P=kits/mimi-short/library/poses && cp $F/art/friend-search.webp $F/art/cap.webp \
  $P/confident.webp $P/tease.webp $P/point.webp $P/friend-nod.webp $P/friend-amazed.webp $P/friend-yay.webp $P/jump.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-slang-no-cap   # renders/mimi-slang-no-cap-en.mp4 and renders/mimi-slang-no-cap.mp4
```

The masks over the 「N語・保存済みN」 lines of the deck and unit lists are in `hf/index.html` (screen percentages). Not in Git: the recording, the own-voice WAVs (biometric), `hf/assets/`, renders, the theme BGM. Series template: [../README.md](../README.md#series-template-real-slang-episodes-24-hangry-ghosted-mid).

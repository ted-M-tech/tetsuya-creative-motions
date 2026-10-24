# Source

```sh
F=films/mimi-slang-ghosted/source
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording; no PATCH, bundled real deck content)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
env -u PATCH LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/SlangWalkthrough.swift OfficialDecksUITests.swift OfficialDecksUITests/testSlangWalkthrough $F/renders/app/slang.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 070/Slang3_Ghosted_assets/simulator_decks-slang-ghosted.mov
sh $F/scripts/app_track.sh            # -> hf/assets/app/{list,units,unit,scroll,card,saved}.mp4 (times measured in the script)
# 2. the ghost prop: codex-p with prompts/03-codex-obake.txt (cast references as style reference), then
kits/mimi-short/scripts/cutout.sh $F/art/ghost.png $F/art/ghost.webp
# 3. voices (owner's own voice, paid; or copy ghosted/huh/ghost/example.wav from Drive Slang3_Ghosted_assets/own-voice/ to $F/assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py      # hf/assets/mix.wav: compressed + level-matched voices, one static gain, -14 LUFS
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && P=kits/mimi-short/library/poses && cp $F/art/ghost.webp $P/friend-sigh.webp $P/friend-shock.webp \
  $P/tease.webp $P/grin.webp $P/point.webp $P/friend-amazed.webp $P/friend-yay.webp $P/jump.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-slang-ghosted   # renders/mimi-slang-ghosted-en.mp4 and renders/mimi-slang-ghosted.mp4
```

The chat in the hook is a generic prop made in HTML (not a real app). The masks over the 「N語・保存済みN」 lines of the deck and unit lists are in `hf/index.html` (screen percentages). Not in Git: the recording, the own-voice WAVs (biometric), `hf/assets/`, renders, the theme BGM.

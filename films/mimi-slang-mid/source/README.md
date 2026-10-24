# Source

```sh
F=films/mimi-slang-mid/source
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording; no PATCH, bundled real deck content)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
env -u PATCH LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/SlangWalkthrough.swift OfficialDecksUITests.swift OfficialDecksUITests/testSlangWalkthrough $F/renders/app/slang.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 071/Slang4_Mid_assets/simulator_decks-slang-mid.mov
sh $F/scripts/app_track.sh            # -> hf/assets/app/{list,units,unit,scroll,card,saved}.mp4 (times measured in the script)
# 2. voices (owner's own voice, paid; or copy verdict/thanks/mid.wav from Drive Slang4_Mid_assets/own-voice/ to $F/assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py      # hf/assets/mix.wav: compressed + level-matched voices, one static gain, -14 LUFS
# 3. edit and render (library poses only)
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && P=kits/mimi-short/library/poses && cp $P/friend-proud.webp $P/chew.webp $P/flat.webp \
  $P/friend-yay.webp $P/friend-shrink.webp $P/point.webp $P/jump.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-slang-mid   # renders/mimi-slang-mid-en.mp4 and renders/mimi-slang-mid.mp4
```

The masks over the 「N語・保存済みN」 lines of the deck and unit lists are in `hf/index.html` (screen percentages). Not in Git: the recording, the own-voice WAVs (biometric), `hf/assets/`, renders, the theme BGM. Series template: [films/mimi-slang-no-cap](../../mimi-slang-no-cap/README.md#series-template-real-slang-episodes-24-hangry-ghosted-mid).

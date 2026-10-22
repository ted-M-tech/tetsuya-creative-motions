# Source

```sh
F=films/mimi-flashcards/source
# 1. app take (shared simulator: hold the lock). The CSV goes into the simulator's Files (On My iPhone) for the take only.
SIM=$(xcrun simctl list devices available | awk -F '[()]' '/Lanclo iPhone 18 Pro QA/ {print $2; exit}')
LS=$(for d in ~/Library/Developer/CoreSimulator/Devices/$SIM/data/Containers/Shared/AppGroup/*; do
  plutil -p "$d/.com.apple.mobile_container_manager.metadata.plist" | grep -q FileProvider.LocalStorage && echo "$d/File Provider Storage"; done)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 1; done
cp $F/app-capture/単語帳.csv "$LS/"
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/note-import.patch kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/FlashcardsWalkthrough.swift NoteImportUITests.swift NoteImportUITests/testImportWalkthrough $F/renders/app/flashcards.mov
rm -f "$LS/単語帳.csv"; rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/app1.mp4, app2.mp4 on the film's clock (timings in the script)
# 2. voice (the owner's own voice; paid generation — or copy it from Drive Flashcards_assets/own-voice/) and sound
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py
# 3. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-flashcards   # renders/mimi-flashcards-en.mp4 and renders/mimi-flashcards.mp4
```

The take was made against Lanclo `origin/main` 5998d20d; `note-import.patch` needs the multi-hunk `kits/mimi-short/app-capture/apply-patch.py` (from mimi-import, included on this branch). `art/` holds copies of mimi-import's poses. Not in Git: the recording (Drive `034. I Fed My Flashcards to Mimi/Flashcards_assets/simulator_flashcards-import.mov`), the voice WAV (biometric), `hf/assets/`, renders.

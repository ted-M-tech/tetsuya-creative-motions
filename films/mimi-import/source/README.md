# Source

```sh
F=films/mimi-import/source
# 1. app take (shared simulator: hold the lock). The CSV goes into the simulator's Files (On My iPhone) for the take only.
SIM=$(xcrun simctl list devices available | awk -F '[()]' '/Lanclo iPhone 18 Pro QA/ {print $2; exit}')
LS=$(for d in ~/Library/Developer/CoreSimulator/Devices/$SIM/data/Containers/Shared/AppGroup/*; do
  plutil -p "$d/.com.apple.mobile_container_manager.metadata.plist" | grep -q FileProvider.LocalStorage && echo "$d/File Provider Storage"; done)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
cp $F/app-capture/旅行フレーズ.csv "$LS/"
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/note-import.patch kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/ImportWalkthrough.swift NoteImportUITests.swift NoteImportUITests/testImportWalkthrough $F/renders/app/import.mov
rm -f "$LS/旅行フレーズ.csv"; rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/app1.mp4, app2.mp4 on the film's clock (timings measured on the 60 fps resample, see the script)
# 2. poses (already cut in art/*.webp): codex-p with prompts/01-codex-poses.txt, then kits/mimi-short/scripts/cutout.sh art/<p>.png art/<p>.webp
# 3. voice (the owner's own voice, from Drive Import_assets/own-voice/ or regenerated) and sound
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp films/mimi-voice/source/art/mimi-phone.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-import   # renders/mimi-import-en.mp4 and renders/mimi-import.mp4
```

The take was made against Lanclo `origin/main` 57b4fc93. Not in Git: the recording (Drive `020. Mimi Eats Your Files/Import_assets/simulator_csv-import.mov`), `hf/assets/`, renders.

The model phrase "Could I have the check?" is the owner's own registered Lanclo voice (Gemini gemini-3.8-flash-tts, accent us): `own-voice.json` and `own-voice.receipt.json` are in Git; the WAV (`assets/own-voice/`) is biometric and kept only in Drive `020. Mimi Eats Your Files/Import_assets/own-voice/`.

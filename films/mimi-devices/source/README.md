# Source

```sh
F=films/mimi-devices/source
# 1. Web screens: a copy of the Lanclo repository at the recorded commit, Node 24, the Vite dev server on port 21990
L=<scratch>/lanclo; git -C ~/Develop/native-voice-clone archive 57b4fc93 voice-web packages contracts design package.json package-lock.json | tar -x -C $L
(cd $L && npm ci --ignore-scripts) && (cd $L/voice-web && npm ci && npm run dev -- --port 21990 &)
cp $F/web-capture/home-capture.ts $F/web-capture/page-capture.ts $L/voice-web/tests/
(cd $L/voice-web && OUT=$F/renders/web SIZES='[["laptop",1440,900]]' node tests/home-capture.ts)          # laptop-habits.png, laptop-habits-full.png
(cd $L/voice-web && OUT=$F/renders/web SHOTS='[["tablet-practice","/practice/browse",1366,1024]]' node tests/page-capture.ts)
# 2. iOS frames from the mimi-loop take (Drive 018. One Loop in Lanclo/Loop_assets/sim-loop_…_fixture.mov): t=15 s (Mimi report), t=100 s (roleplay)
ffmpeg -ss 15 -i <take>.mov -frames:v 1 $F/renders/app/ios-mimi-report.png; ffmpeg -ss 100 -i <take>.mov -frames:v 1 $F/renders/app/ios-roleplay.png
sh $F/scripts/screens.sh                          # -> hf/assets/app/*.jpg (paints over 「デモデータ」)
# 3. poses: codex-p with prompts/0*.txt, run in $F with --image art/ref/… copies of: kits/mimi-short/library/official/master.png,
#    films/mimi-action-add/source/art/friend/{chosen-2,b-lop}.png, films/mimi-action-add/source/art/friend-aww.webp, films/mimi-loop/source/art/friend/type.png; then cut out
kits/mimi-short/scripts/cutout.sh $F/art/friend/giggle.png $F/art/cut/friend-giggle.webp   # likewise desk, train, lop/ask, lop/sulk, lop/cheer
# 4. sound and edit
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/cut/*.webp films/mimi-loop/source/art/cut/friend-{type,sigh,wow}.webp kits/mimi-short/library/poses/{jump,confident}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-devices   # renders/mimi-devices-en.mp4 (English subtitles), renders/mimi-devices.mp4 (Japanese only)
```

Highlight boxes on the "And then" rows (`#hl-web`, `#hl-ios` in `hf/index.html`) are placed for these exact captures; move them if the screens are captured again.

Not in Git: `renders/` (captures and MP4s, in Drive `026. Phone, Tablet or Computer/Devices_assets/`), `hf/assets/`, the theme BGM.

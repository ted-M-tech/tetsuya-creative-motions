# Source

```sh
F=films/mimi-origin/source
# 1. app take (shared simulator: hold the lock): Home with fixture data, then Settings › ヘルプとアプリ情報 (label check)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/HomeWalkthrough.swift DescribeUITests.swift DescribeUITests/testHomeWalkthrough $F/renders/app/home.mov
rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/home.mp4 (2 s of Home, from the 60 fps resample)
# 2. art (already cut in art/*.webp): codex-p with prompts/01-codex-art.txt and the official art, chosen-2.png, friend-aww.webp and
#    films/mimi-roleplay/source/art/cafe.webp attached; then kits/mimi-short/scripts/cutout.sh art/<p>.png art/<p>.webp for the poses
#    and the cup; plates and teacher-call are plain WebP (magick art/<p>.png -quality 90 art/<p>.webp)
#    the teacher's five images were then redrawn with prompts/02-codex-teacher-french.txt (attach films/mimi-freespeech/source/art/friend-french*.png and the originals)
# 3. sound
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp films/mimi-roleplay/source/art/cafe.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-origin   # renders/mimi-origin-en.mp4 and renders/mimi-origin.mp4
```

The take was made against Lanclo `origin/main` 57b4fc93. Not in Git: the recording (Drive `025. How Lanclo Began/Origin_assets/simulator_home.mov`), `hf/assets/`, renders.

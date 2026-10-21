# Source

```sh
F=films/mimi-watching/source
# 1. app: the --qa-mimi take from films/mimi-loop (no new recording); cut one track on the film's clock (times in the script header)
cp "<Drive>/002.SNS/024. Mimi Is Always Watching/Watching_assets/sim-loop_mimi-advice_journal_situation_lesson_progress_fixture.mov" $F/renders/app/loop.mov
sh $F/scripts/app_track.sh            # -> hf/assets/app/app.mp4 (6.4 s from 3.9 s)
# 2. poses: codex-p with prompts/01-codex-poses.txt (art/*.png), then cut out
for p in mimi-peek mimi-smile friend-shock; do kits/mimi-short/scripts/cutout.sh $F/art/$p.png $F/art/cut/$p.webp; done
# art/cut/friend-bed.webp is films/mimi-loop's (branch feat/mimi-loop)
# 3. sound (drone, SFX, theme bed)
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/cut/*.webp kits/mimi-short/library/poses/jump.webp kits/mimi-short/library/official/listening.png \
  films/mimi-action-add/source/art/{friend-aww,friend-oops,paw}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-watching   # renders/mimi-watching-en.mp4 and renders/mimi-watching.mp4
```

The mask over the fixture's「デモ：」line and the yellow highlight boxes are screen percentages in `hf/index.html` (`#m1`, `#hl1`–`#hl4`); move them if a new take shifts the layout. Not in Git: the recording, `hf/assets/`, renders, the theme BGM.

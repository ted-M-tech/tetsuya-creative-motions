# Mimi shorts kit

Shared parts of every 15-second Mimi short (2D official style, Rive + HyperFrames). Extracted from 「自分の声、むり」 while making 「think が sink に」. An episode keeps only its story: poses it adds, its acting, its cue sheet and its edit.

| Path | Role |
|---|---|
| `library/` | Synced copy of the Lanclo Mimi 2D library (`design/mimi-2d`: poses, props, plates, lip-sync cache; plus the official art). App-ready `.riv` files live in the library itself (`design/mimi-2d/riv/`). `library/SOURCE` names the commit. Refresh with `scripts/sync-library.sh`; never edit by hand |
| `scripts/rig2d.py` | The library rig plus `add_pose()` (episode poses by path), `lipsync()` (mouth from any voice clip, cached) and `build_shots()` |
| `scripts/render_rive.sh` | Rive project → PNG frames → MP4 (60 fps) |
| `scripts/cutout.sh` | Drawn image on white → trimmed transparent WebP (`FUZZ=30` for props with a soft glow) |
| `scripts/sfx.py` | `Mix` (voice / SFX / music buses, ducking, -14 LUFS), the 100 BPM bed, end chord, SFX: tap, whoosh, pofu, boing, clang, poof, freeze, shatter, mokugyo, pencil, pop_seq, ding, bell |
| `hf/kit.css`, `hf/kit.js` | The look and motion helpers: camera wrapper, phone UI on the desk plate, captions, speech bubble, playback tags, radar result card, sparkles, end card |
| `brand/` | End-card Mimi, Lanclo mark, App Store badge |
| `stage.sh` | Copies `hf/`, `brand/`, the fonts and `library/props/` into an episode's HyperFrames project as `assets/kit/` (not in Git) |

## Real app screens

`app-capture/capture.sh` records the Lanclo app in the simulator with QA fixture data while a walkthrough UI test taps through it; `app-capture/cut.sh` resamples the variable-frame-rate take to 60 fps and cuts clips by time. The app checkout and build are cached in `~/Library/Caches/lanclo-app-capture`, so only the first run builds from scratch. Raw takes go to Lanclo's Google Drive (002.SNS/003.MimiShorts/<episode>_素材). Reference episode: `films/mimi-shashin`.

## Make an episode

```sh
F=films/<id>/source
# 1. new poses / props: draw with codex-p (see films/mimi-think-sink/prompts/01-codex-poses-and-props.txt), then
kits/mimi-short/scripts/cutout.sh $F/art/<pose>.png $F/art/cut/<pose>.webp     # use with rig2d.add_pose() until approved
# 2. shots: $F/scripts/shots.py imports the kit rig, add_pose() the new poses, defines acts and SHOTS
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py
$F/scripts/render.sh                       # -> $F/hf/assets/shots/*.mp4
# 3. sound: $F/scripts/mix.py builds a sfx.Mix from the cue sheet
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit
kits/mimi-short/stage.sh $F/hf
cd $F/hf && npx hyperframes check && npx hyperframes render --output ../renders/<id>.mp4 --fps 60
```

`films/mimi-think-sink/source` is the reference episode.

## Rules

- The Lanclo library (`native-voice-clone/design/mimi-2d`) is the master. A pose an episode adds lives in the episode until the owner approves the video, then goes to the library by PR and comes back here with `sync-library.sh`.
- Kit changes made for one episode must keep earlier episodes building.
- New plates must put the feet point (480, 1330) on the ground: frame the drawing to it (see `films/mimi-michi/source/README.md`).
- Story shape that worked: 1 s hook with the problem, the relatable failure, Lanclo plays your own voice said right, radar card with one fix, practice, payoff, 1 s end card. Captions at the top; the bottom ~400 px stays clear for platform UI.

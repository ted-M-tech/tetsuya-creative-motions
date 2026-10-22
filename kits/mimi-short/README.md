# Mimi shorts kit

Shared parts of every Mimi short (15–25 s vertical, 2D official style, HyperFrames). Extracted from 「自分の声、むり」 while making 「think が sink に」; the early episodes act with Rive bones, the current ones swap cut-out poses and move them with GSAP in the edit (see the [2D character animation guide](../../docs/2D-CHARACTER-ANIMATION.md)). An episode keeps only its story: poses it adds, its acting, its cue sheet and its edit.

| Path | Role |
|---|---|
| `library/` | Synced copy of the Lanclo Mimi 2D library (`design/mimi-2d`: poses, props, plates, lip-sync cache; plus the official art). App-ready `.riv` files live in the library itself (`design/mimi-2d/riv/`). `library/SOURCE` names the commit. Refresh with `scripts/sync-library.sh`; never edit by hand |
| `cast/` | The fixed cast (Mimi, her Friend, the Android bunny, the side cast Bruno / Pippa / Coco with their Kokoro voices) and the codex-p prompt template for new poses: [cast/README.md](cast/README.md) |
| `scripts/ownvoice.py` | The owner's registered voice (Gemini TTS) for an episode's English lines from `own-voice.json`; accents `us`, `uk`, `learner`, `native`. Paid per line; the WAVs are biometric and stay out of Git (Drive only), Git keeps `own-voice.receipt.json` |
| `scripts/rig2d.py` | Rive route: the library rig plus `add_pose()` (episode poses by path), `lipsync()` (mouth from any voice clip, cached) and `build_shots()` |
| `scripts/render_rive.sh` | Rive project → PNG frames → MP4 (60 fps) (Rive route) |
| `scripts/cutout.sh` | Drawn image on white → trimmed transparent WebP (`FUZZ=30` for props with a soft glow) |
| `scripts/sfx.py` | `Mix` (voice / SFX / music buses, ducking, -14 LUFS), the bed (Lanclo SNS theme「Everyone Get Up」from `library/bgm/`, not in Git: copy it from Lanclo's Google Drive `002.SNS/_BGM/`; else the code-made 100 BPM bed), end chord / theme fade-out, SFX softened and kept low, SFX: tap, whoosh, pofu, boing, clang, poof, freeze, shatter, mokugyo, pencil, pop_seq, ding, bell |
| `render-cuts.sh` | Renders an episode twice: with English subtitles (`.sub` clips) and Japanese only (`<body class="no-subs">`) |
| `hf/kit.css`, `hf/kit.js` | The look and motion helpers: camera wrapper, phone UI on the desk plate, captions, speech bubble, playback tags, radar result card, sparkles, end card (`k.end(at)`, then `k.tapCta(at + 0.6)` taps the「7日間無料ではじめる」button; pair it with `sfx.pochi()` in the mix) |
| `brand/` | End-card Mimi, Lanclo mark, App Store badge |
| `stage.sh` | Copies `hf/`, `brand/`, the fonts and `library/props/` into an episode's HyperFrames project as `assets/kit/` (not in Git) |

## Real app screens

`app-capture/capture.sh` records the Lanclo app in the simulator with QA fixture data while a walkthrough UI test taps through it; `PATCH=<file>` applies a capture-only fixture tweak (`app-capture/apply-patch.py`, matched by text) and reverts it afterwards; it is never committed to the app. The simulator is shared: hold `/tmp/lanclo-capture.lock` (`until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done`, then `rmdir`) while recording. `app-capture/cut.sh` resamples the variable-frame-rate take to 60 fps and cuts clips by time. The app checkout and build are cached in `~/Library/Caches/lanclo-app-capture`, so only the first run builds from scratch. Raw takes go to Lanclo's Google Drive, in the episode's folder named after its Notion Content Calendar ID (002.SNS/<3-digit ID>. <English title>/<episode>_assets). Reference episode: `films/mimi-shashin`.

## Make an episode (pose swap, current)

```sh
F=films/<id>/source        # start from a similar episode's source/, e.g. films/mimi-disaster-sit/source (series template in its ../README.md)
# 1. new poses: codex-p with the cast references (cast/README.md), then
kits/mimi-short/scripts/cutout.sh $F/art/<pose>.png $F/art/<pose>.webp
# 2. voices: Kokoro for the side cast ($F/scripts/voices.sh), the owner's voice for the English lines
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
# 3. app take (optional): app-capture/capture.sh, then $F/scripts/app_track.sh
# 4. sound and edit
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf             # then copy the episode's poses into $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf <id>  # renders/<id>-en.mp4 and renders/<id>.mp4
```

## Make an episode (Rive bones, early)

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
- Story shape: hook text from frame 1 (stop within 1.5 s), the relatable failure, the real app, payoff, end card with the CTA tap; or punchline first (Pronunciation Disasters). Captions at the top; the bottom ~400 px stays clear for platform UI.
- Use only the cast in `cast/`; no new character for one episode.

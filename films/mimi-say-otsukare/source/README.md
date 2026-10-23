# Source

```sh
F=films/mimi-say-otsukare/source
# 0. the composer's real answer: already recorded in ../process/compose-probe-otsukare.jsonl (run 2 is shown; how it was taken:
#    ../../mimi-say-yoroshiku/source/README.md "How the composer was captured", script scripts/compose_probe.mjs)
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/compose-result.patch sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/ComposeWalkthrough.swift PracticeRefinementUITests.swift PracticeRefinementUITests/testComposeWalkthrough $F/renders/app/compose.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 064/Say2_Otsukaresama_assets/sim-compose_otsukare.mov
sh $F/scripts/app_track.sh                 # -> hf/assets/app/compose.mp4 (6.69 s on the film's clock)
# 2. voices (paid, the owner's voice; WAVs not in Git, Drive 064/Say2_Otsukaresama_assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
# 3. cue sheet -> cues.json + hf/index.html, then the sound (-14 LUFS, true peak <= -1.5 dBTP)
python3 $F/scripts/cues.py
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp kits/mimi-short/library/poses/point.webp kits/mimi-short/library/poses/confident.webp \
  kits/mimi-short/library/backgrounds/meeting.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-say-otsukare   # renders/mimi-say-otsukare-en.mp4 and renders/mimi-say-otsukare.mp4
```

| File | Role |
|---|---|
| `scripts/cues.py` | The cue sheet (one place for every time and tap position); writes `cues.json` and `hf/index.html` from `scripts/index.tpl.html` |
| `scripts/index.tpl.html` | The edit with `__CUE__` placeholders: evening office hook, "You are tired!", Mimi puzzled ("Am I…?"), the phone with the candidates and the result labels, the intent card, the payoff, end card. Edit this, not `hf/index.html` |
| `scripts/mix.py` | Sound (voices, soft SFX, theme bed, CTA pochi), then the post-gain + limiter step to -14 LUFS / <= -1.5 dBTP |
| `scripts/app_track.sh` | Cuts the take onto the film's clock (typing x1.3, waits skipped, the draft frame held 0.8 s) |
| `scripts/compose_probe.mjs` | Calls Lanclo's real server composer (see episode 1); not rerun for this episode |
| `app-capture/ComposeWalkthrough.swift` | Walkthrough UI test: マイノート › すべて › 追加 › type 「仕事終わりに」「お疲れ様」 › フレーズを作成 › 意味を選択 › "Good work today!" › 保存 |
| `app-capture/compose-result.patch` | Capture-only: the QA composer fixture returns the real two-candidate answer for this input (plus a 2 s wait); never committed to the app |
| `art/` | The episode-1 poses reused here (Friend waving in the office outfit, Mimi as the colleague) |

Safe zones (owner, 2026-10-23): nothing meaningful below y 1500; EN subtitles at `bottom: 430px`, x 60-880; no text, bubble or small Mimi in the right rail (x > 900, y 820-1520); top text from y 200. In the take the list after saving shows the fixture's count card and a fixture phrase (「Please」): both are masked (`#m-count`, `#m-fix`). Not in Git: the take, own-voice WAVs, `hf/assets/`, renders, the theme BGM.

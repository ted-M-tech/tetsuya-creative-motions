# Source

```sh
F=films/mimi-say-itadakimasu/source
# 0. the real answers (already recorded in ../process/; rerun only for a new input). A fresh detached product worktree with deps:
#    git -C ~/Develop/native-voice-clone worktree add --detach ~/orca/workspaces/native-voice-clone/compose-probe-itadakimasu origin/main
#    (cd that && npm ci --ignore-scripts && cd voice-web && npm ci --ignore-scripts)
#    N=$HOME/.local/share/lanclo/node24/node_modules/node/bin/node
#    $N $F/scripts/compose_probe.mjs <that worktree> "食べる前のいただきます" 3 | grep '"run"'                       # compose
#    $N $F/scripts/compose_probe.mjs <that worktree> "Let's eat!" 2 "いただきます（食事を始めるときのあいさつ）" | grep '"run"'   # example
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/compose-result.patch sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/ComposeWalkthrough.swift PracticeRefinementUITests.swift PracticeRefinementUITests/testComposeWalkthrough $F/renders/app/compose.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 077/Say3_Itadakimasu_assets/sim-compose_itadakimasu.mov
sh $F/scripts/app_track.sh                 # -> hf/assets/app/compose.mp4 (6.65 s on the film's clock)
# 2. voices (paid, the owner's voice; WAVs not in Git, Drive 077/Say3_Itadakimasu_assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
# 3. cue sheet -> cues.json + hf/index.html, then the sound (-14 LUFS in the cuts, true peak <= -1.5 dBTP)
python3 $F/scripts/cues.py
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && L=kits/mimi-short/library && cp $L/backgrounds/dining.webp \
  $L/poses/yum.webp $L/poses/stunned.webp $L/poses/friend-offer.webp $L/poses/point.webp $L/poses/confident.webp $L/poses/bowl.webp $L/poses/friend-yay.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-say-itadakimasu   # renders/mimi-say-itadakimasu-en.mp4 and renders/mimi-say-itadakimasu.mp4
```

| File | Role |
|---|---|
| `scripts/cues.py` | The cue sheet (every time and tap position); writes `cues.json` and `hf/index.html` from `scripts/index.tpl.html` |
| `scripts/index.tpl.html` | The edit with `__CUE__` placeholders: dinner-table hook, "I will receive!", Mimi puzzled ("Receive… what?"), the phone with the result label, the situation card, the payoff, end card. Edit this, not `hf/index.html` |
| `scripts/mix.py` | Sound (voices, soft SFX, theme bed, CTA pochi), then the post-gain + limiter step (wav target -13.6 so the AAC cuts measure -14.2) |
| `scripts/app_track.sh` | Cuts the take onto the film's clock (typing x1.3, the thinking tail and the save wait skipped) |
| `scripts/compose_probe.mjs` | Calls Lanclo's real server handler: purpose `compose` (フレーズを作成) or, with a meaning, purpose `example` (the draft's example) |
| `app-capture/ComposeWalkthrough.swift` | Walkthrough UI test (origin/main 1088ae0b): マイノート › すべて › 追加 › type 「食べる前の」「いただきます」 › フレーズを作成 › フレーズを確認 › 保存 › マイノートに保存したよ。 › 完了 |
| `app-capture/compose-result.patch` | Capture-only: the QA composer fixture returns the real answer and the real example for this input (plus a 2 s wait); never committed to the app |

No episode art: every pose and the plate come from `kits/mimi-short/library`. Safe zones (owner, 2026-10-23): nothing meaningful below y 1500; EN subtitles at `bottom: 430px`, x 60-880; no text, bubble or small Mimi in the right rail (x > 900, y 820-1520); top text from y 200. The take ends on the saved confirmation, so no fixture list rows or counts appear. Not in Git: the take, own-voice WAVs, `hf/assets/`, renders, the theme BGM.

# Source

```sh
F=films/mimi-say-yoroshiku/source
# 0. the composer's real answer (already recorded in ../process/compose-probe-*.jsonl; rerun only for a new input)
#    a fresh detached product worktree with its deps, then the real server handler with the dedicated Gemini key (never printed):
#    git -C ~/Develop/native-voice-clone worktree add --detach ~/orca/workspaces/native-voice-clone/compose-probe origin/main
#    (cd that/voice-web && npm ci --ignore-scripts)
#    PATH=$HOME/.local/share/lanclo/node24/node_modules/node/bin:$PATH node $F/scripts/compose_probe.mjs <that worktree> "新しい職場でよろしくお願いします" 3
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/compose-result.patch sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/ComposeWalkthrough.swift PracticeRefinementUITests.swift PracticeRefinementUITests/testComposeWalkthrough $F/renders/app/compose.mov
rmdir /tmp/lanclo-capture.lock
#    or take it from Drive 063/Say1_Yoroshiku_assets/sim-compose_yoroshiku.mov
sh $F/scripts/app_track.sh                 # -> hf/assets/app/compose.mp4 (6.35 s on the film's clock)
# 2. poses: codex-p with ../prompts/01-codex-poses.txt and 02-codex-mimi-hello-right.txt, then
for p in friend-bow friend-bow-smile mimi-colleague-hello-r mimi-colleague-puzzled; do kits/mimi-short/scripts/cutout.sh $F/art/$p.png $F/art/$p.webp; done
# 3. voices (paid, the owner's voice; WAVs not in Git, Drive 063/Say1_Yoroshiku_assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp kits/mimi-short/library/poses/point.webp kits/mimi-short/library/poses/confident.webp \
  kits/mimi-short/library/backgrounds/meeting.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-say-yoroshiku   # renders/mimi-say-yoroshiku-en.mp4 and renders/mimi-say-yoroshiku.mp4
```

| File | Role |
|---|---|
| `scripts/compose_probe.mjs` | Calls Lanclo's real server composer (`vocabularyApi` in `voice-web/cloudflare/vocabulary.ts`, purpose `compose`, study language `en`, meanings `ja`) with the production route's dedicated Gemini key from `~/.config/lanclo/gemini-dedicated.env`; prints only the response |
| `app-capture/ComposeWalkthrough.swift` | Walkthrough UI test (Japanese UI, QA fixtures): マイノート › すべて › 追加 › type the input in three chunks › フレーズを作成 › the result › 保存 › the list |
| `app-capture/compose-result.patch` | Capture-only: the QA composer fixture returns the real answer for this input (plus a 2 s wait so 生成を中止 shows); never committed to the app |
| `scripts/app_track.sh` | Cuts the take onto the film's clock (typing ×1.3, the generation wait and the save wait skipped) |
| `scripts/mix.py` | Cue sheet and sound (voices, soft SFX, theme bed, CTA pochi); times shared with `hf/index.html` |
| `hf/index.html` | The edit: office hook, the Friend's line, Mimi puzzled, the phone with the result label, the situation card, the payoff, end card |
| `art/` | Codex drawings (PNG) and cut-outs (WebP) |

In the take the list after saving shows the fixture's count card and a fixture phrase (「Please」): both are masked (`#m-count`, `#m-fix`). Not in Git: the take, own-voice WAVs, `hf/assets/`, renders, the theme BGM.

## Series template ("How Do You Say It?")

Episode 2 (お疲れ様, input 「仕事終わりにお疲れ様」, its real answers already in `../process/compose-probe-otsukare.jsonl`) copies this `source/` and swaps only:

| Beat (ids) | Time in ep. 1 | Swap |
|---|---|---|
| Hook `#hook`, `#series`, `#s-office` | 0–1.5 | The phrase in the hook, `#1` → `#2`, the scene plate and the two poses (Mimi in a role outfit + the Friend; no other cast) |
| Line `#b-line` | 1.5–3.95 | The Friend's literal attempt (own voice `style`, learner) |
| Puzzled `#qm`, `#c1` | 3.95–5.0 | Mimi's reaction pose, the "no word-for-word" caption |
| App `#s-app`, `#result`, `#c2`–`#c4` | 5.0–11.35 | `ComposeWalkthrough.swift` `INPUT` chunks; `compose-result.patch` (input string + the real candidate(s)); `app_track.sh` measured times; the `#result` label text |
| Card `#s-card`, `#r1`, `#r2` | 11.35–15.55 | Two situations and their English (own voice `us`); one of them must be the app's real answer |
| Payoff `#s-payoff`, `#b-pay`, `#c6` | 15.55–17.35 | The Friend says it right; CTA caption 「次は何を英語にしたい？」 stays |
| End `#end` | 17.35–18.6 | Unchanged |

How the composer was captured (exactly):

1. The real answer: `scripts/compose_probe.mjs` runs the product's own server handler from a fresh detached `origin/main` worktree (no app code copied, the same system instruction, model and post-processing as production, which routes stateless Gemini calls to the dedicated project: `docs/operations/gemini-project-isolation.md`). Run it 3 times (the AI varies at temperature 0.2), save every response to `process/compose-probe-<slug>.jsonl`, pick one, and say which in PROCESS.md.
2. The UI: the QA fixture flag `--qa-phrase-compose` (DEBUG only, `native-ios/Lanclo/Core/AppStore.swift` `composePhrase`) answers from fixtures without a backend. `compose-result.patch` adds the chosen real answer for the exact input string (text-matched by `apply-patch.py`, reverted after the take).
3. The take: `capture.sh` with `PATCH=`, under the shared lock. The walkthrough replaces `PracticeRefinementUITests.swift` and keeps its class name. Composer ids: `notes.group.all`, `notes.group.add`, `notes.manual.text`, `notes.manual.create`, `notes.manual.term`, `notes.manual.save`.
4. Resample to 60 fps, read a 4 fps tile sheet for the moments (caret, typing, 生成を中止, result, save, list), cut with `app_track.sh`, mask fixture text and counts in the list.

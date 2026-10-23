---
name: lanclo-sns-short
description: Make, deliver, finalize and publish a Lanclo SNS short (Mimi + friend, 2D official style, 15–25 s vertical, HyperFrames) end to end with the fixed series rules. Use when the owner asks for an SNS video, a short, a Reel, "SNS動画/ショートを作って", "Mimiのショート", a new episode of a series such as "Pronunciation Disasters 7", or to finalize, upload or publish such a short.
---

# Lanclo SNS short

One flow from "make a short about X" to a finished, delivered and published film. Reply to the owner in Japanese; everything teammates read (Notion, Drive names, repo docs, PRs, commits) is in English. This skill holds the order and the fixed rules; the how-to lives in the repo, read it rather than improvising:

- [2D character animation guide](../../docs/2D-CHARACTER-ANIMATION.md) (routes, voices, app capture, story shapes)
- [Mimi shorts kit](../../kits/mimi-short/README.md) (commands) and [the cast](../../kits/mimi-short/cast/README.md) (who may appear, codex-p pose prompt)
- [Adding a film](../../docs/ADDING-A-FILM.md) (record, series catalog) and [Publishing](../../docs/PUBLISHING.md) (gallery deploy)
- Template episode: [films/mimi-disaster-sit](../../films/mimi-disaster-sit/README.md) (punchline first) or [films/mimi-quitter](../../films/mimi-quitter/README.md) (hook + real app)

Paths below: the creative-motions checkout is `~/Develop/tetsuya-creative-motions`, film worktrees go under `~/orca/workspaces/tetsuya-creative-motions/`, the product repo is `~/Develop/native-voice-clone` (iOS is the product of record). Lanclo's Drive is Google Drive for Desktop: `~/Library/CloudStorage/GoogleDrive-*/My Drive/100.Work/001.Freelance/006.Lanclo/002.SNS/`.

## 1. Intake

- [ ] Settle the idea with the owner as a timed beat table. **Hook first**: the hook line is on screen from frame 1 and stops the scroll within 1.5 s; no slow intro. 15–25 s, fast tempo. If the owner only asked for ideas or a structure, stop after that.
- [ ] Verify every app feature, label and number you will show in the product code (`native-ios/`, its UI tests `LancloUITests/`). Show only what exists; no counts that will change ("問題数はあくまで現時点"), no invented research, no competitor app names. If the idea assumes a missing feature, adapt and say so.
- [ ] Notion **Lanclo / Marketing / Content Calendar** (MCP `notion`, find it by search): one row per video, Type Reel, Status Idea → Planning while drafting. Its `ID` is the film number, written as 3 digits (`043`). Page body in English: summary, a 秒 / 画面 / 字幕 / 音・声 table, voice lines, link to the repo record.
- [ ] Drive folder `002.SNS/<NNN>. <English title>/` (strip `*` and other awkward characters: "Sit or Sht").

## 2. Setup

- [ ] One worktree and branch per film: `git -C ~/Develop/tetsuya-creative-motions worktree add ~/orca/workspaces/tetsuya-creative-motions/<film-id> -b feat/<film-id> origin/main`. Film ids are `mimi-<slug>` (series: `mimi-disaster-<word>`).
- [ ] Start `films/<film-id>/` from the closest episode: copy its `source/`, keep the beat ids, swap story, art, lines and times. Skeleton per [Adding a film](../../docs/ADDING-A-FILM.md): `README.md` + `README.ja.md`, `PROMPT.md`, `PROCESS.md` (owner's words quoted verbatim), `CREDITS.md`, `prompts/`, `process/`, `source/README.md`. Save prompts and reviews to files as you go.
- [ ] Fetch the theme BGM into the worktree: `kits/mimi-short/scripts/fetch-bgm.sh` copies it from the private product repo (`origin/main:design/sns-bgm/everyone-get-up.mp3`) to `kits/mimi-short/library/bgm/` (licensed, never in a public repo; `sfx.py` and `stage.sh` also run it when the file is missing, and `sfx.py` stops with an error if it is still missing). Drive `002.SNS/_BGM/` keeps a backup copy. `MIMI_BGM=builtin` (code-made bed) only for a deliberate rebuild of an early episode.

## 3. Fixed rules (do not reopen)

- **Cast**: Mimi and her Friend carry every story; the Friend is the learner who slips, Mimi reacts and teaches. The Android bunny appears now and then. Any other role is Bruno (bear), Pippa (duck) or Coco (cat) only. No character made for one episode; propose a new recurring one to the owner first. Role outfits are fine.
- **Text**: Mimi's Japanese first person is 「僕」 (the Android bunny says 「私」). Standard Japanese unless the owner asks for a dialect.
- **Art**: 2D official style. Reuse library and earlier episode poses first; new poses with `codex-p` (never plain `codex`), the cast reference images attached every time, prompt from the cast README, saved in `prompts/`; then `cutout.sh`.
- **Sound**: the voice leads. Bed = OpenTracks 「Everyone Get Up」 (Anonyment) at the kit level (`THEME_GAIN`, about 21 dB under voice, ducked). SFX soft and low, no bright bells. `-14 LUFS` via `Mix.write`. Owner listens on earphones: when in doubt, quieter.
- **End card**: `k.end(at)` then `k.tapCta(at + 0.6)` with `sfx.pochi()`.
- **Screen**: 1080×1920, 60 fps. Captions at the top; bottom ~400 px clear of meaning; never cover a face; phone UI is atmosphere, the point goes in a large label. Mask fixture text (「QA用データ」「デモデータ」).
- **Two cuts**, always: Japanese only and English subtitles (`.sub` clips, `body.no-subs`), both from `render-cuts.sh`. End-card subtitle: "Native pronunciation, in your own voice. / Start free for 7 days."
- **Voices**: the learner's and the model's English are the owner's registered voice via `kits/mimi-short/scripts/ownvoice.py` + `own-voice.json` (`learner`, `us`, `uk`, `native` + `language`; `style` for a deliberate wrong word). It is biometric: WAVs never in Git (only `own-voice.json` and `own-voice.receipt.json`), copies go to Drive `<Prefix>_assets/own-voice/`; never print the voice ID or keys. It is paid: generate only the lines needed, at most 3 regenerations per line, then stop and report. The owner's male voice on the Friend is accepted. Side cast English = Kokoro (`npx hyperframes tts`, their fixed voices; these WAVs are committed). No Japanese TTS: Japanese lines are bubbles and captions.
- **Mispronunciations** are verified acoustically (silencedetect for word starts, spectral / formant checks) and by ear, never by a Whisper transcript (it "corrects" the wrong word). Use Whisper for timestamps only.
- **Real app**: simulator capture with QA fixtures through `app-capture/capture.sh`; fixture gaps via capture-only `PATCH=` (never committed to the app; `env -u PATCH` between takes). Never `--reset-onboarding`. Hold the shared lock for every take, also on failure. Takes are variable frame rate: resample to 60 fps before measuring.

## 4. Build

```sh
F=films/<film-id>/source
kits/mimi-short/scripts/cutout.sh $F/art/<pose>.png $F/art/<pose>.webp      # new poses
sh $F/scripts/voices.sh                                                       # Kokoro side cast, if any
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json                 # paid; only new lines
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done           # app take, if any
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/<x>.patch sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/<Walkthrough>.swift <UITests file> <Class/testMethod> $F/renders/app/<x>.mov; rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh                                                    # cut the take onto the film clock
uv run --no-project --with numpy python $F/scripts/mix.py                     # hf/assets/mix.wav; times shared with hf/index.html
kits/mimi-short/stage.sh $F/hf                                                # then copy the episode art into $F/hf/assets/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf <film-id>                               # renders/<film-id>-en.mp4 and renders/<film-id>.mp4
```

Then look at contact sheets of the key moments yourself (hook frame, every caption/subtitle against faces and the bottom 400 px), run a codex-p review on the frames if useful, and listen through: no clipped heads or tails, voice on top. Fix and re-render before showing the owner.

## 5. Draft delivery and review

- [ ] `ffprobe` both cuts: 1080×1920, 60 fps, no rotation side data, expected duration (`ffprobe -v error -show_entries stream=width,height,r_frame_rate:stream_side_data=rotation:format=duration <f>.mp4`). A rotation tag once made a YouTube upload sideways.
- [ ] Copy to the Drive folder (python `shutil.copy2`, then `filecmp.cmp(..., shallow=False)`): `<Prefix>_draft_<YYYY-MM-DD>.mp4` (Japanese only) and `<Prefix>_draft_EN-subs_<YYYY-MM-DD>.mp4`. `<Prefix>` is short and stable (`Quitter`, `Disasters1_Sit`, `AB1_Add_a_Phrase`). Raw takes and own-voice WAVs in `<Prefix>_assets/`. A replaced version moves to `old/`, never deleted.
- [ ] Notion row: Status Planning, script table matches the draft.
- [ ] Report to the owner in Japanese: hook (first 1.5 s), scene list with times, what was verified where in code, open questions, the Drive file names. Iterate on feedback in the same worktree; record each owner direction verbatim in `PROCESS.md`.
- [ ] Commit and push the branch; no PR until the owner approves.

## 6. Finalize (only after the owner's OK)

- [ ] In the worktree: `git fetch origin && git merge origin/main`. `.gitignore` conflicts are normal: keep both sides, no duplicate lines. `kits/mimi-short/app-capture/apply-patch.py` conflicts: take main's. Anything else ambiguous: stop and ask. Check `git ls-files | grep own-voice/` lists only the two JSON files.
- [ ] Make the README / README.ja final: no draft status, the Drive line names the final files. `npm run check` must pass (Node 24: `PATH=$HOME/.local/share/lanclo/node24/node_modules/node/bin:$PATH`).
- [ ] PR to main titled `Add <NNN> <English title>` and `gh pr merge --merge`.
- [ ] Drive: rename both cuts to drop `_draft_` (`<Prefix>_<date>.mp4`, `<Prefix>_EN-subs_<date>.mp4`); leave `old/` and `_assets/` alone.
- [ ] Notion: Status Prepared (Reserved / Done belong to the owner's posting), GDrive URL = `https://drive.google.com/drive/folders/<id>` with `<id>` from `xattr -p 'com.google.drivefs.item-id#S' "<folder>"`, and append `## Final (<date>, owner approved)` in English (what changed in the last version, final file names, repo record + PR).
- [ ] Approved new poses go to the Lanclo library (`native-voice-clone/design/mimi-2d`) by a separate PR; after it merges, `kits/mimi-short/scripts/sync-library.sh`.

## 7. Publish

- **YouTube** (only when the owner asks): the official uploader in the product repo, procedure in `docs/engineering/video-manual-operations.md` and `docs/features/video-manual.md`, code `voice-web/scripts/upload-youtube-manual.ts` / `youtube-upload-core.ts`. Read the Notion row (`YouTubeTitle`, `YouTubeTitle EN`, `Caption`, `YouTube Category` = Get Started / Practice / Setting); a nonempty `YouTube Link` or `Shorts URL` means already posted. Use the **EN-subs final** (both languages are the policy). Draft JSON → `prepare` → show the owner the preview → `publish <plan> --confirm <digest>` only after explicit approval. Fixed: unlisted, no subscriber notification, JA title + EN localization, playlist by category. Write the URL to Notion `YouTube Link` and read it back; do not change Status. The uploader cannot delete or reorder: replacing a video (delete the old one, move the new one to its playlist position, remove the "Deleted video" item) is a separate API step with the local upload token, done only on the owner's explicit OK.
- **videos.maepace.com** (`~/Develop/tetsuya-creative-motions`): add the episode to its series in `films/catalog.json` (`extras`, `"role": "episode"`, `"format": "short"`, `edition: "#NNN"`, seconds), poster `site/posters/<film-id>.jpg` (540×960), media `site/media/<film-id>-en.mp4` from the Drive EN-subs final, re-encoded for the web only if over 25 MiB. Update the series edition count and the root README series line. `npm run check && npm test && npm run build`, PR, merge.
- **maepace.com/works** (`~/Develop/myPortfolioSite`, branch `ted-M-tech/open-works-entry`, holds others' uncommitted work: stage only your hunks): the series entry's `episodes` in `src/data/profile.ts`, the count in `src/components/WorkGallery.astro`, poster in `public/works/shorts/`. `pnpm check && pnpm build`, commit, push.
- **Deploy is run by the owner** (auto mode blocks production). Before it, every live `/media/*.mp4` must exist in `site/media/` (it is not in Git; a deploy without them deletes them): check all files referenced by `films/catalog.json` and by `grep -rhoE 'videos\.maepace\.com/media/[A-Za-z0-9._-]+\.mp4' ~/Develop/myPortfolioSite/src`, download any missing one from the live site first. Then hand over, in order: `! cd ~/Develop/tetsuya-creative-motions && PATH=$HOME/.local/share/lanclo/node24/node_modules/node/bin:$PATH npm run deploy`, then `! cd ~/Develop/myPortfolioSite && PATH=$HOME/.local/share/lanclo/node24/node_modules/node/bin:$PATH pnpm run deploy`; afterwards `curl -I` the new media URLs.
- Instagram / TikTok posting is the owner's own action.

## 8. Batch mode (several films)

- The session that talks to the owner is the commander: it plans, writes one shared brief to its scratchpad (the rules of section 3, delivery naming, "report in Japanese", "no PR, no merge, never ask the owner") plus a short per-film brief (film id, Notion ID, Drive folder, hook, beats, owner quotes), and starts one child agent per film, each in its own worktree. Series: build episode 1 as the template first; the others reuse it once pushed.
- Children: build, deliver the draft to Drive, commit and push their branch, report. They share the simulator lock and must not touch other worktrees.
- Commander: checks every draft (contact sheet, ffprobe, cast and 「僕」 audit) before the owner sees it, relays the owner's feedback to the right child (SendMessage) and keeps PROCESS quotes verbatim. Finalize one film at a time in number order with a single agent (merge conflicts compound otherwise).

## Series templates

**Pronunciation Disasters** (punchline first, ~19 s): copy `films/mimi-disaster-sit/source/`, keep `hf/index.html`'s beats and ids, swap the pair. Full beat table, mouth-card panel style and per-sound shapes: [series template](../../films/mimi-disaster-sit/README.md#series-template-episodes-26).

| Beat | Time | Swap |
|---|---|---|
| Punchline flash-forward | 0–1.5 | Mimi's punchline line (word censored with ★) + an object gag for the wrong word's meaning; rewind ◀◀ at 1.2 |
| Setup + slip | 1.5–4.25 | Place + phrase; the Friend says the wrong word (owner's voice, `learner` + `style`); on screen censored |
| Freeze | 4.25–5.75 | Record scratch, ice, 「シーン…」; plate and side cast member |
| Mimi | 5.75–7.0 | 「それ「…」（意味）に聞こえてる〜！！」 |
| Mouth card | 7.0–11.7 | Two words × lips (front) / tongue (side) panels, both takes (learner → `us`) |
| Real app | 11.7–15.8 | Daily lesson on the phrase (capture-only patch) |
| Fix + end | 15.8–18.7 | Said right, happy ending, end card + CTA tap |

The rude word is audible (it is the joke) and starred on screen; keep it cheeky, not explicit. Vary place, side cast and Mimi's reaction per episode. Done: 1 Sit, 2 Beach, 3 Rice/Lice, 4 Election, 5 Coke, 6 Peace (Notion 037–042).

**Hook + real app** (feature stories): frame-1 hook → the relatable failure → the real app solving it → payoff → end card ([mimi-quitter](../../films/mimi-quitter/README.md), [mimi-frozen-abroad](../../films/mimi-frozen-abroad/PROCESS.md)).

## Lessons (pitfalls we hit)

- New animal leads appeared in drafts and the owner rejected them: brief every child with the cast rule and audit before review.
- 041's EN-subs Drive copy had a -90° rotation tag and went up sideways; ffprobe every file before Drive and before upload.
- BGM and a bright bell were too loud on earphones; keep the kit levels, no extra gain.
- Kokoro's Japanese was garbled: no Japanese TTS.
- Whisper reported the intended word for a deliberate mispronunciation: check the audio itself.
- Simulator takes are VFR and screens dim while audio plays: resample, then pick readable frames.
- The gallery deploy deletes live MP4s missing from `site/media/`; the GitHub `films` release does not hold them all.
- READMEs kept saying "draft" after approval: finalize them in the same PR.
- Parallel branches always conflict on `.gitignore`; resolve by union.
- `~/Develop/native-voice-clone` may be far behind or dirty: read code from `origin/main` or a fresh worktree.
- Notion and Drive are read by overseas teammates: English only there.

## Not reproducible from Git alone

The theme BGM (private product repo `design/sns-bgm/`, fetched by `fetch-bgm.sh`; backup in Drive `_BGM/`), own-voice WAVs and simulator takes (Drive `_assets/`), renders, the owner's Gemini voice key, the YouTube upload token, Notion / Drive access and the production deploys. A fresh session needs those on this machine; the record says where each lives.

# Reusable production records

Use this as a starting structure, adapting filenames to an existing project rather than forcing a migration.

```text
films/<project>/
  README.md          What the film communicates; watch link; key decisions
  PROMPT.md          Consolidated final brief, explicitly labeled as such
  NARRATION.md       Complete spoken script
  TTS-PROMPTS.json   Actual generation inputs, model/voice/settings, no private IDs
  TIMING.json        Measured scene/audio placement and playback rates
  CREDITS.md         Asset licenses, references, and primary research citations
  MEDIA.json        Required external media, artifact location/hash, exclusions
  source/           Current editable composition with pinned dependencies
  extras/<variant>/ Alternate narration or treatment
  history/<version>/ Earlier accepted version
```

Do not fabricate missing original prompts or model settings. Mark reconstructed instructions as reconstructed. Record which audio files were selected when historical generation inputs include unused takes.

## Finishing a revision

- Keep an accepted checkpoint before replacing the current source.
- Update the script, final brief, timeline, and concise change note together.
- Save the render outside Git; record its hash, duration, dimensions, and production version.
- Preserve source, licensed product assets, and concise receipts in Git. Exclude credentials, private voice IDs, raw recordings, generated QA dumps, and temporary render output.
- For publication, check licenses and the authorized scope, links, mobile/desktop layout, playback, and seeking. Update the gallery and repository together when requested.

In Tetsuya Creative Motions, each project's root is stable; the gallery lists only its current representative film. Extras and history remain within its making-of page. Public documentation defaults to English with a Japanese counterpart (`README.ja.md`). Original prompts and scripts retain their source language; translations are labeled, not passed off as original inputs.

## Maintaining the shared workflow

The repository's skill package is the source of truth. Install or link it into the user's skill directory; do not maintain a second hand-edited copy. Update third-party engine skills through their own supported workflow.

Promote a lesson into this skill only when it applies beyond one film. Keep brand colors, a particular voice, exact duration, and research numbers in project records. When changing this skill, explain the reason, review a representative planning/editing/archiving request, and commit the change. A successful sample render does not establish compatibility with every engine or voice provider.

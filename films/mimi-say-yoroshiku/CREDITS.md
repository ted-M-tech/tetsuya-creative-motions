# Credits

| Material | Source | Terms | Notes |
|---|---|---|---|
| Lanclo app screens | Simulator recording of the Lanclo iOS app (origin/main) with QA fixtures, `source/app-capture/ComposeWalkthrough.swift` | © Lanclo, not licensed for reuse | The composer's answer is the real answer of Lanclo's server composer for the typed input, put in by the capture-only `compose-result.patch` (see PROCESS.md); kept in Lanclo's Google Drive |
| New poses: the Friend bowing (frozen, smiling), Mimi as a colleague (hello, puzzled) | Generated with Codex image generation from the cast references ([prompt](prompts/01-codex-poses.txt), [Mimi facing right](prompts/02-codex-mimi-hello-right.txt)) | © Lanclo, not licensed for reuse | Cast: Mimi and her Friend only |
| Other poses (point, confident), office plate (meeting) | Mimi 2D library (`kits/mimi-short/library`) | © Lanclo, not licensed for reuse | |
| Lanclo mark, end-card Mimi | Lanclo brand | © Lanclo, not licensed for reuse | |
| English voice lines | The owner's registered voice (Gemini TTS, `kits/mimi-short/scripts/ownvoice.py`) | Owner's own voice; WAVs not in Git | `source/own-voice.json`, `own-voice.receipt.json` |
| Zen Maru Gothic | Google Fonts | SIL OFL 1.1 | |
| Download on the App Store badge | Apple | Apple marketing guidelines | |
| SFX | Made in code (`kits/mimi-short/scripts/sfx.py`) | MIT with the repository code | |
| Bed music | 「Everyone Get Up」, [OpenTracks](https://opentracks.com/bgm/detail/22155), Music : Anonyment | OpenTracks licence (commercial use OK, credit optional; no redistribution, no Content ID) | Lanclo SNS theme, read by the kit from `kits/mimi-short/library/bgm/` (not in Git) |

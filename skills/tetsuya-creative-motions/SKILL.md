---
name: tetsuya-creative-motions
description: Create or revise a code-based product film using Tetsuya's workflow, and preserve its prompts, creative decisions, and source as a teachable portfolio project. Use when this workflow is requested or when adding a film to Tetsuya Creative Motions.
---

# Tetsuya Creative Motions

Help the user turn a message into a film they can revise, explain, and reuse. This skill owns creative continuity and production records; it does not replace a rendering engine's technical instructions.

## Start from the current decision

- Inspect the existing brief, latest accepted film, and production notes. Establish which version is active before editing.
- For a new film, settle the audience, core promise, intended action, approximate length, and desired style. Infer what the user already supplied; ask only for consequential gaps.
- When the user asks for ideas or a script first, produce that artifact and stop before generation/rendering. When an edit is approved, implement it without reopening settled decisions.
- State the change scope. Preserve accepted scenes, story beats, brand, and audio outside that scope. If a new requirement cannot fit the accepted duration, explain the tradeoff instead of silently dropping a scene or speeding everything up.

## Choose the production tools

Default to code-based HTML/SVG animation for diagrams, typography, UI, and deterministic motion. Use the user's chosen framework if specified.

If HyperFrames skills are installed, enter through `hyperframes` and use the relevant workflow (`product-launch-video` or `general-video`). Load animation, audio, registry, and media skills only for the task at hand. Do not copy their internals into this skill or modify upstream skills to store personal preferences.

Without those skills, you can still produce the brief, storyboard, script, and records. State which production dependencies are missing before attempting a render; use a documented alternative if available. This package alone does not install a renderer, provide API access, or guarantee identical generated audio.

## Make the benefit visible

- The opening should make the subject and value recognizable quickly. A provocative hook is an option, not a requirement for every film.
- Show the user's experience: action → system response → useful outcome. Avoid relying only on app screenshots or feature labels.
- Use motion to establish cause and effect: a voice travels to its model, a weak skill leads to lesson cards, news is selected and becomes learning material. Every flourish should support a reading order or story beat.
- Keep a coherent illustration family, palette, typography, and motion vocabulary. A project's colors, dialect, voice, or 1.2× playback choice are not universal defaults.
- Connect new benefits to the story. Use a short bridge when a scene would otherwise feel like an unrelated feature.

For evidence and examples, read [creative-decisions.md](references/creative-decisions.md) when writing claims, planning a product demonstration, or translating feedback into animation.

## Fit and check the actual result

Measure generated speech before placing it. Check the full script against the scene sequence, including devices and closing lines. Keep pronunciation examples consistent when they represent the same speaker; label synthetic demonstrations appropriately.

Inspect rendered frames at the opening, key claims, transitions, and ending. Check text wrapping, contrast, chart proportions, and forward/reverse seeking when the engine supports it. Listen for chopped phrases, mismatched voices, dead air, and music masking speech. Verify the exported file's dimensions, duration, playback, and end before calling it complete. Report what was actually checked.

Use existing authorization for paid generation and publication; this skill itself grants neither. Publishing a portfolio, uploading media, and replacing a public film must remain within the user's requested scope.

## Leave a teachable project

Follow [project-records.md](references/project-records.md) when saving a finished revision or preparing a portfolio entry. Preserve the actual generation inputs separately from the consolidated final brief. Capture a few decisions and why they mattered, not an unfiltered conversation dump.

Keep one portfolio entry per project. Put alternate treatments under extras and previous versions under history. Do not publish private voice IDs, credentials, or source recordings. Keep rendered media outside Git and retain a durable artifact link and hash.

Finish with the film location, what changed, validation performed, and where the reader can find the script, prompt, and source. Do not claim a local edit is published until the public destination is verified.

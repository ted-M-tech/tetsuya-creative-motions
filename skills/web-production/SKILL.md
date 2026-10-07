---
name: web-production
description: Create or revise landing pages and portfolio websites with a static-first workflow, preserving prompts, design decisions, skill provenance and runnable source for a public case study. Use for LP/Web production or reproducibility standardization, not application backends or films.
---

# Web Production

Standardize the process, not every site's appearance. Preserve the user's approved brand and chosen design direction.

- Inspect the repository's instructions, existing page and product facts. Keep confirmed behavior, aspirations and planned features distinct; never invent research outcomes or production status.
- For new content-first sites default to Astro static output, TypeScript strict and CSS. Keep existing React/Vite/HTML on scoped edits. Isolate complex interactive features into optional React/TSX islands; do not add a server or paid service without a concrete requirement.
- Use Impeccable as the primary design aid when installed. Use Taste Skill (`design-taste-frontend`) for an alternative or critique when useful. Read each selected skill's instructions. The user's Astro choice and brand override conflicting stack/aesthetic defaults. Do not run both mechanically or label an installed skill as used.
- Use Product Design for explicit design exploration, user/problem framing or flow work when appropriate and available. Follow its own entrypoint. Keep product-UI usage distinct from final LP usage; recommendations in a handoff are not proof of execution.
- Define the audience, action and section narrative before implementation. Record product truth separately from visual decisions. Let real artifacts demonstrate value; use motion to explain, with a readable reduced-motion state.
- Verify project check/build commands and actual mobile/laptop layouts, Japanese line breaks, overflow, keyboard access, links and media loading. Make a bounded correction pass based on observed defects.
- Deliver source plus lockfile, runtime/build commands, asset credits, source revision and a compact making-of. Record authentic prompt excerpts separately from a reconstructed reproduction prompt. Record model/version only if known.
- For each skill actually used, record upstream URL, revision if known, local modifications, file hashes for read entrypoints/references, stage used and whether the result was selected. Unknown historical versions remain unknown. Never substitute a present-day fingerprint for the historical package.
- Respect licenses when archiving skill packages and assets. Exclude private paths, secrets, raw voice recordings and unrelated application code from public exports. Prompts describe the process; pinned source reproduces the implementation. Do not promise identical AI output.
- One finished LP is one portfolio work. Link the work, source, prompts and skill provenance together. Publication follows the user's scope and the repository's publisher coordination; this skill grants no deployment authority.

Public workflow and templates: https://github.com/ted-M-tech/tetsuya-creative-motions/blob/main/docs/WEB-WORKFLOW.ja.md
Use the project's own commands and paths; do not require that public repository to be cloned when an existing project already provides equivalent records.

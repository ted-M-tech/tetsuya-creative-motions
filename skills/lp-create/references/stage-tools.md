# Tools by LP stage

Use this reference when a stage needs a concrete tool choice. These are capabilities learned from past work, not a mandatory chain of dependencies. Preserve the project's existing working stack and the user's approved assets.

## Product facts and research

Start with the product's implementation, brief and source documents. When researching the web, use agent-reach if available and follow its routing; otherwise use the environment's web tools. Prefer original product documentation, studies and asset sources. Save the URL, observation date and the narrow claim supported. Do not turn research about a technique into proof of this product's effect.

## Design direction

- Impeccable: default design support when available; use only the relevant planning, critique, distill, adapt or polish work.
- Taste Skill: useful for a genuinely different direction or a critique of generic patterns. Respect the chosen stack instead of importing its default framework.
- Product Design: useful for unresolved user needs, product-flow questions, visual alternatives or explicit image/URL-based work. Follow the relevant skill's workflow. Do not add a full discovery cycle to a small copy fix.

Different directions should share the same verified product facts so that the user can compare design rather than competing claims.

## Assets and media

Prefer actual product UI when explaining a feature. Mark synthetic scores or content as demo data. Keep a coherent illustration family and use different relevant scenes instead of reusing the same figure without meaning.

- unDraw and Pexels are possible asset sources, not skills or defaults for every brand. Record the exact asset URL, license and modifications.
- Use imagegen when a new generated visual is appropriate and requested or warranted; keep its prompt and selected output provenance. Do not replace approved illustrations or real product UI merely because generation is available.
- Use existing image tooling (for example Sharp) to produce appropriately sized WebP/AVIF or other supported assets. Preserve originals outside the public bundle, set dimensions and review cropping at mobile sizes. Avoid adding an image pipeline for one already optimized file.
- Reuse an existing film only after checking current claims and asset rights. Making or editing the film is a separate workflow: enter through HyperFrames when available/applicable. TTS, FFmpeg and rendering packages are not baseline LP dependencies. Paid generation needs its own authorization.

## Icons

- Use Lucide icons actively to reduce copy and improve scanning in new LPs. This is a communication principle, not merely a library option: when an icon, short label or simple diagram communicates the same meaning more directly than a sentence, use that visual and remove the redundant sentence.
- For example, replace a device-support paragraph with phone/tablet/laptop icons and a short label; show a recording → AI model → practice sequence with icons and brief step titles; pair concise feature labels with meaningful icons instead of explanatory paragraphs repeating the title.
- Keep a short visible label when the icon's meaning is ambiguous. Preserve decision-critical details such as price, conditions and research qualifications. Review the result at mobile size: the visitor should understand it faster, not have to decode unexplained symbols.
- Inspect existing dependencies first. For scoped refinements, apply the same copy-reduction principle with the established icon family rather than mixing families. Lanclo's published LP uses Phosphor; that historical fact is not a constraint on new LPs.
- Choose one interface-icon family per page and define consistent size, stroke/weight and alignment tokens. User-selected Lucide is valid even if a design aid discourages it as a generic default. Do not add multiple libraries for cosmetic variations.
- Use the official package or licensed SVGs appropriate to the stack. Static Astro icons should not require React hydration or a client runtime solely to draw them. Import only needed icons; retain required license notices and record the library/version.
- Decorative icons accompanying readable text are hidden from assistive technology. Icon-only buttons need an accessible name on the control and an adequate clickable area independent of glyph size.
- Brand logos, platform/store badges and approved product marks use their canonical assets; do not substitute a generic library glyph. Use meaningful icons to support comprehension, not one ornamental icon for every paragraph.

## Implementation and motion

For a new content-first LP use Astro static output, strict TypeScript and CSS unless the user's project calls for another stack. Existing React/Vite LPs remain valid.

Use CSS or a small browser script for simple motion. Keep an existing Motion implementation when useful; load React islands only for interaction that justifies them. Do not add GSAP, Motion and another animation system for overlapping jobs. Explain the role of each animation and keep the information readable without motion.

## Responsive and interaction verification

Use a built preview and an existing Playwright suite or the public QA runner linked from SKILL.md. Start with representative mobile and laptop widths; add small/intermediate widths and supported locales when the page needs them. Chromium and WebKit help expose engine-specific differences.

Check document overflow AND the visible comparison/table content, not just the body width. Capture scrolled/revealed sections and inspect screenshots for Japanese phrase breaks, duplicated explanation, clipped images and text, spacing and hierarchy. A passed numeric check does not establish visual quality.

Test normal motion, reduced motion, keyboard order, CTA targets and any video loading/playback separately. Use the available browser skill/tool for manual interaction; Orca-specific tools are optional conveniences, not requirements for public reproduction. Label emulated viewports as emulated, and record actual devices only when tested.

Bound review to an initial mobile/desktop pass, a defect-driven correction and targeted confirmation. Broaden only for unresolved concerns or changes. Save screenshots/reports in ignored artifacts and a concise result in the source record.

## Delivery

Record each tool or skill actually used, its role and known version; do not copy the entire installed catalog into credits. Link prompts, design decisions, licensed assets, fixed source and runnable checks. Use the existing build/Git/publication flow; keep site runtime independent of AI authoring tools. This reference does not authorize deployment or introduce a service subscription.

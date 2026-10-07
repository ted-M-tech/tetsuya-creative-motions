---
name: Tetsuya Open Works
description: Warm-paper editorial portfolio with actual work at its center.
colors:
  paper: "#f7f6f2"
  ink: "#202423"
  secondary-text: "#545d54"
  muted-heading: "#737970"
  rule: "#c8ccc1"
  rust: "#ae421d"
  slide-paper: "#e9d0ba"
  slide-blue: "#344f69"
rounded:
  work-preview: "12px"
  compact-preview: "8px"
---

# Design System: Tetsuya Open Works

## Overview

Extend the incumbent warm-paper editorial system: off-white, dark ink, restrained rust accents, generous whitespace and thin rules. Actual work is the visual centerpiece. This is an extension of `site/style.css`; `site/works.css` supplies the portfolio, case-study and slide surfaces without replacing the underlying identity.

**Key Characteristics:**

- Large, readable statements and quiet supporting copy.
- Actual work previews with open captions, rather than enclosing every item in a card.
- Flat paper, fine dividing rules and generous section spacing.

## Colors

Paper and ink carry the interface. Secondary text supports descriptions; muted heading color distinguishes the second phrase of major titles. Rust is an interaction accent, visibly used for keyboard focus. Slide paper and slide blue belong to teaching media and their previews, not a new site-wide background system.

**The Work First Rule.** Let the exhibited work supply its own palette while the surrounding interface stays quiet.

## Typography

The existing implementation uses Inter with Helvetica Neue, Arial and Japanese system fallbacks. This is an observed incumbent stack, not a newly selected display identity.

The extension's home heading scales from 46–92px (`clamp(46px, 6.8vw, 92px)`, line height 1.22); at 800px and below it uses `clamp(34px, 8.8vw, 46px)`. Case headings scale from 38–72px, then 32–58px on small screens. Supporting work titles are 23px, feature headings 28–40px, and explanatory copy 15px with line height 1.9 and a maximum measure of 70ch. Slide body copy becomes a fixed readable 16px on narrow screens; visual slides use 15px.

**The Readable Preview Rule.** Keep supporting explanations outside images and available without hover. Balance headings and preserve natural Japanese phrase breaks.

## Layout

The shared content width is capped at 1280px with 48px side gutters; at 720px and below, gutters become 20px. The header wraps on narrow screens. The portfolio extension collapses its feature, related-work, process, decision and resource grids at 800px.

Desktop work features pair image and copy in a 1.65:1 grid with a 48px gap. Related work uses two equal, shrinkable columns with a 36px gap. Process sections use two columns and 110px vertical padding, reducing to one column and 70px padding on small screens. Case sections use 64px vertical padding, reducing to 40px.

Slides use a 16:9 desktop canvas. On small screens they grow vertically to fit readable content rather than shrinking the entire composition; image-led slides stack their example under the explanation. Print uses landscape pages with a separate slide per page.

## Elevation & Depth

The observed system is flat: no box shadows. Background changes, whitespace and fine rules establish grouping. Preview images provide visual depth within their own artwork.

## Shapes

Work previews, slides and code examples share gently rounded corners. Compact case previews and slide examples use the smaller radius. Text sections stay open; one-pixel rules separate process steps, resources and major sections.

## Components

Work previews use 16:9 framing; the featured website uses 3:2 with the image aligned to its top. Images may enlarge slightly on hover (1.025 over 0.5s), while captions and destination links remain visible at rest. Reduced-motion preferences remove transitions and smooth scrolling.

Text actions use a thin underline or bottom border. Links and buttons use a visible rust keyboard-focus outline (3px, offset 5px). Navigation remains lightweight; the active language is bold and underlined. The skip link appears on focus.

Resource lists use ruled rows; runnable instructions use a dark ink code panel with wrapping text. Slide examples sit alongside explanations on desktop and below them on mobile.

## Do's and Don'ts

- **Do** retain actual work as the visual centerpiece. The current LP feature, film and teaching slides are three views of one project, not invented portfolio breadth.
- **Do** make mobile previews and essential explanations usable without hover.
- **Do** preserve maepace.com's own tokens when embedding the slow, focus-pausable work strip; this document describes the Open Works site.
- **Don't** replace the incumbent editorial identity as part of an ordinary extension.
- **Don't** fabricate portfolio projects or turn artwork-specific colors into interface defaults.

Observed but not canonized: the incumbent generic/system display stack, eyebrow-like small labels and glyph arrows remain in the build. They are pre-existing craft drift, not reusable design prescriptions; repairing them is outside this documentation pass. No sidecar was generated because this pass is explicitly limited to `DESIGN.md`.

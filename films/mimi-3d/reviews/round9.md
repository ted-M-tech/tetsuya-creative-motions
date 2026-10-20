**HOLD — recognizable Mimi, but the ears and hands still weaken the target’s soft-toy appeal.**

These are proposed first-pass values in `scripts/mimi.py`, not render-verified fixes.

| Rank | Visible difference | Exact proposed change | Confidence |
|---|---|---|---|
| 1 | **Sideways ear is too thick and paddle-like.** Target has a slimmer, softer silhouette. | `ear()`: floppy ellipsoid size `(0.19, 0.115, 0.295)` → `(0.17, 0.09, 0.295)`. Keep its angles initially. | Medium |
| 2 | **Hands read as small round knobs.** Target has fuller, elongated mittens flowing from the shoulders. | `fused_body()`: arm size `(0.085, 0.085, 0.095)` → `(0.095, 0.09, 0.12)`; center Z `0.265` → `0.28`. Preserve torso dimensions. | High |
| 3 | **Upright blue insert ends in an overly narrow point.** Target carries more blue width toward the root. | `ear()`: upright panel `(zc, a, b)` from `(0.35, 0.095, 0.23)` → `(0.33, 0.105, 0.25)`. `ear_material()`: taper coefficients `0.55 + 0.45 × …` → `0.70 + 0.30 × …`. | Medium |
| 4 | **Feet merge into a soft, uneven base.** Target has two clearly readable rounded toe forms. | `fused_body()`: leg centers `(0.12*s, -0.035, 0.07)` → `(0.125*s, -0.065, 0.07)`; size `(0.115, 0.14, 0.095)` → `(0.115, 0.15, 0.095)`. | Medium |
| 5 | **Blush looks airbrushed.** Target has cleaner, flatter pink patches. | `blush()`: transition start `radius * 0.78` → `radius * 0.94`; maximum blend `0.85` → `0.95`. Keep radius and placement. | High |
| 6 | **“L” is too small and slight.** Target’s lettering fills more of the blue cup. | `headphones()`: `t.data.size` `0.24` → `0.28`; bevel depth `0.003` → `0.004`. | High |

**Keep:** approved full torso; upright ear’s outward lean; head tilt; eye size, spacing, and single catchlights; nose/mouth expression; headphone palette. Keep camera, framing, lighting, and exposure locked.

No files edited.
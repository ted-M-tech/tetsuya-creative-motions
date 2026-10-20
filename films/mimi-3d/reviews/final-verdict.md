SHIP

The character reads consistently across all four views and retains Mimi’s appeal. Remaining differences are optional likeness polish, not model-sheet blockers.

| Rank | Visible difference | Exact proposed change in `scripts/mimi.py` | Confidence |
|---|---|---|---|
| 1 | Sideways ear has a smaller, more isolated blue inset; the target’s blue fills more of the paddle and extends toward its root. | `ear()`: floppy `(zc, a, b)` from `(0.30, 0.092, 0.19)` to `(0.28, 0.105, 0.21)`. | High on difference; medium on values |
| 2 | Hands read as elongated attached mittens; target hands are rounder, softer knobs. | `fused_body()`: arm size from `(0.09, 0.088, 0.108)` to `(0.095, 0.088, 0.100)`. Preserve position and torso. | Medium-high |
| 3 | Eyes feel slightly smaller relative to the face, reducing the target’s bright, infant-like expression. | `build()`: eye size from `(0.053, 0.019, 0.069)` to `(0.057, 0.019, 0.072)`. Keep eye positions and catchlights. | Medium |

**Keep:** approved full torso; outward upright-ear lean; asymmetric ear silhouette; head-to-body proportions; cheek placement; small smile; headphone proportions and readable “L”; locked camera, framing, lighting, and exposure.

These numbers are proposed starting values, not render-verified fixes. No files edited. SHIP applies to visual model-sheet approval; animation deformation is not demonstrated by these stills.
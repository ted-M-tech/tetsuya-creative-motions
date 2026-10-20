**NOT SHIP yet.** Recognizably Mimi, but the ear edges and lower-head silhouette still look unfinished. These are proposed starting values, not render-verified fixes. No files changed.

| Rank | Visible difference | Exact proposed change in `scripts/mimi.py` | Confidence |
|---|---|---|---|
| **1** | **Blue ear panels have conspicuous stair-stepped borders.** The target has smooth, flowing inlays. | In `ear_panel()`, replace face-center deletion with a continuously sampled boundary: **128 perimeter samples**, using the existing `zc/a/b` and taper formula; ray-project a triangulated patch onto the ear’s front. Use **0.001 surface lift** and reduce Solidify thickness **0.004 → 0.001**. Increasing ear resolution alone is insufficient. | **High** |
| **2** | **Lower head is too broad and flat-bottomed**, giving a rounded-box impression instead of the target’s softly rounded cheeks and chin. | In `fused_body()`, change head radii **`(0.455, 0.35, 0.38)` → `(0.445, 0.35, 0.395)`**; reduce lower-cheek widening coefficient **`0.10 → 0.04`**. Keep `HEAD_C` and torso dimensions unchanged. | **Medium–high** |
| **3** | **Upright ear reads too narrow and straight-sided.** The target has a fuller paddle shape and more generous white surround. | In `ear()`, change only the upright ear’s X radius **`0.175 → 0.195`**; keep Y/Z **`0.115/0.335`** and blue-panel dimensions unchanged initially. Preserve upright tilt **`12°`**. | **Medium** |
| **4** | **Hands look elongated and merged into the body**, especially the near hand; the target has rounder, more distinct mittens. | In `fused_body()`, change arm radii **`(0.085, 0.085, 0.115)` → `(0.095, 0.090, 0.100)`** and arm center Y **`-0.115 → -0.135`**. Keep arm X/Z positions and torso fullness. | **Medium** |

**Keep:** the full torso, outward upright-ear lean, asymmetric ear pose, head tilt, eye spacing, small nose and smile, pink cheeks, and blue/navy headphone identity.

**Presentation:** the current comparison clips the sideways ear and renders the character smaller than the target. Match scale and show the complete silhouette before the next review; don’t alter anatomy to compensate for that crop.
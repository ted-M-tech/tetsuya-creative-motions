**NOT SHIP yet.** Recognizably Mimi, but the ears, pose details, and presentation still weaken the match. These are proposed starting values, not render-verified fixes.

1. **Blue ear panels are too broad and triangular.** The target has narrower inserts with a generous white rim. In `ear_material()`, clamp the normalized height **before** multiplying by `0.6`: `taper = 0.4 + 0.6 * clamp((Z-(zc-b))/(b*0.8), 0, 1)`. Currently the multiplier can reach **1.4**, rather than **1.0**. Keep `ear()` dimensions and upright-ear tilt unchanged. **Confidence: high.**

2. **The view compresses the far eye and cup; framing is too small.** Target character occupies approximately **81%** of image height versus **70%** currently. In `stage()`, change `cam.data.lens: 70 → 81`. For the comparison, use `aim(cam, -18)` instead of `-24`; in `main()` change the default hero yaw accordingly. The review script’s explicit `hero:-24` overrides that default. **Confidence: high on framing; medium on yaw.**

3. **Headphones lack the target’s oversized presence.** In `headphones()`, change cup radius **0.21 → 0.225**, blue face radius **0.182 → 0.195**, and `L` text size **0.22 → 0.24**. Keep depths and cup centers initially. **Confidence: medium; assess after camera correction.**

4. **Hands read as raised round fists rather than relaxed hanging paws.** In `fused_body()`, change arm center Z **0.265 → 0.245** and arm size **`(0.095, 0.09, 0.10)` → `(0.095, 0.09, 0.12)`**. Preserve torso dimensions. **Confidence: medium-high.**

5. **Lighting looks colder and harsher, with a gray background and weak navy definition.** In `stage()`, try key energy **240 → 210**, fill **60 → 90**, and sweep emission default **0.3 → 0.6**. In `build()`, change white **`#f7f7fa → #faf8f6`**. Keep exposure initially to avoid further clipping. **Confidence: medium; lighting values require a render check.**

**Keep:** current full torso; outward upright-ear lean; asymmetrical ear arrangement; head tilt; rounded cheek-heavy head; eye spacing and mouth design; blue/navy/pink palette. No files edited.
**HOLD — recognizable Mimi, but not yet a close enough model-sheet match.** Proposed values below are starting points, not render-verified fixes. All changes refer to `scripts/mimi.py`.

1. **Hands look like raised boxing gloves.** Target arms hang lower and blend into the sides; current hands project forward as separate balls. In `fused_body()`, change arm location `(0.225*s, -0.175, 0.3)` → `(0.235*s, -0.115, 0.265)` and size `(0.095, 0.09, 0.098)` → `(0.085, 0.085, 0.115)`. Keep torso dimensions unchanged. **Confidence: high.**

2. **The viewing angle hides the blue headphone face and compresses the “L”; the sideways ear is also clipped.** Match presentation before enlarging headphone geometry. In `main()`, change default `hero:-18` → `hero:-28`; in `aim()`, try `dist=4.55` instead of `4.35` to restore clearance. The target shows considerably more of the left cup’s outer face. **Confidence: medium; exact framing needs a render.**

3. **Blue ear inserts look like floating oval pads.** Target inserts taper toward the roots and sit more flush within a thick white rim. In `ear()`, change inner Y location `-0.108` → `-0.098`, thickness `0.014` → `0.008`, and taper expression coefficients `0.65 + 0.35 * …` → `0.40 + 0.60 * …`. Lower inner centers: floppy `0.31` → `0.28`, upright `0.36` → `0.33`. Preserve ear tilts. **Confidence: medium-high; check for surface intersection.**

4. **Eyes read charcoal and slightly squat instead of glossy navy ovals.** In `build()`, change eye size `(0.055, 0.02, 0.069)` → `(0.052, 0.018, 0.073)` and eye roughness `0.2` → `0.14`. Retain `#071b45` and the single catchlights; broad reflections are contributing to the gray appearance. **Confidence: medium.**

5. **White surfaces lose shape under bright, cool illumination.** Target has clearer soft shading across hands, feet, and ear rims. In `stage()`, reduce fill energy `65` → `40`, rim `90` → `60`, and sweep emission default `0.35` → `0.20`; retain the key initially. **Confidence: medium; evaluate separately from geometry.**

**Keep:** current full torso, upright ear’s outward lean, asymmetric ear arrangement, oversized head, cheek placement, small double-curve smile, blue/navy palette, and rounded headphone edges. No files edited.
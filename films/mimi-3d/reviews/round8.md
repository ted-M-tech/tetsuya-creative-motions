**NOT SHIP yet.** Recognizably Mimi, but the ear contours and washed-out shading still weaken the soft-vinyl appeal. These are proposed starting values, not render-verified fixes. All changes below refer to `scripts/mimi.py`.

1. **Ear inserts look angular and pointed.** The target has flowing blue teardrops and smoothly rounded white borders. In `ear_material()`, replace the abruptly clamped taper with `u = clamp((Z-(zc-b))/(1.6*b), 0, 1)` and `taper = 0.55 + 0.45*u*u*(3-2*u)` using math nodes. In `ear()`, similarly smooth the outer-width transition: replace `min(1,max(0,c.z/0.22))` with smoothstep over `0…0.30`. Preserve tilt values. **Confidence: high on discrepancy; medium on values.**

2. **White surfaces lose their volume.** The current chest, hands, and floor nearly merge; the target retains gentle gray shading and clear contact. In `stage()`, change fill energy `90 → 45`, world strength `0.4 → 0.25`, sweep emission default `0.5 → 0.1`, and exposure default `-1.0 → -1.2`. Keep the key at `210` initially. **Confidence: high on discrepancy; medium on lighting balance.**

3. **Hands are too large and hang too low.** They read as long mittens rather than compact rounded paws. In `fused_body()`, change arm size `(0.095, 0.09, 0.12) → (0.085, 0.085, 0.095)` and arm center Z `0.245 → 0.265`. Leave torso dimensions untouched. **Confidence: high.**

4. **The view compresses the “L” earcup and crowds the sideways ear.** The target shows a broader blue cup face and comfortable silhouette clearance. In `main()`, change default hero yaw `-22 → -28`; in `aim()`, change default distance `4.8 → 5.0`. The review launcher explicitly passes `hero:-22`, so that override must also change when testing. **Confidence: medium; presentation correction, not a cup remodel.**

5. **Eyes are slightly oversized and protruding.** The target’s eyes feel more delicately embedded in the face. In `build()`, change eye size `(0.057, 0.024, 0.073) → (0.053, 0.019, 0.069)`; reduce catchlight surface offset `0.022 → 0.018`. Keep eye positions initially. **Confidence: medium.**

**Keep:** approved full torso; upright ear’s outward lean; asymmetric ear pose; head tilt; broad cheek silhouette; navy/cyan palette; small nose and double-curve smile; painted blush approach.

No files edited.
**NOT SHIP** — the broken ear insets are a clear blocker. Ranked fixes below; numerical adjustments are proposed starting values, not render-verified.

1. **Blue ear panels disappear into the white ears.** Target has continuous, clean blue inserts; current has large white holes. In `ear()`, replace the flat placement at `y=-0.098` with surface-conforming placement: after shaping `inner`, ray-cast onto `e` from local `(x,-1,z)` toward `+Y`; set each vertex’s absolute local Y to `hit.y - 0.010 + original_vertex.y`. Keep panel thickness `0.008` and existing X/Z dimensions. **Confidence: high.**

2. **Face is too turned away.** The far eye and cheek are compressed, weakening the open, friendly expression. In `main()`, change default `hero:-28` to `hero:-20`; keep lens `70`. Evaluate subsequent face changes from this view. **Confidence: medium; render-call overrides may supersede this default.**

3. **Eyes look narrow and flatter than the target’s glossy navy beads.** In `build()`, change eye decal size `(0.052,0.018,0.073)` → `(0.057,0.024,0.073)`. Keep eye spacing `0.178`, material color `#071b45`, and the single catchlight. **Confidence: medium; camera correction may reduce the required widening.**

4. **Smile is small and subdued.** Target has a wider, more readable double curl. In `mouth_curve()`, change horizontal multiplier `0.075 → 0.083`, curl depth `0.028 → 0.032`, and bevel depth `0.009 → 0.010`. Keep its current vertical anchor. **Confidence: medium-high.**

5. **Lighting makes the white vinyl and backdrop too gray.** In `stage()`, raise fill energy `40 → 80`, world strength `0.3 → 0.45`, and sweep emission default `0.2 → 0.4`. Keep exposure `-1.0` initially to protect the already bright forehead. **Confidence: medium; verify highlight retention.**

**Keep:** the client-approved full torso; outward lean of the upright ear (`tilt=12`); asymmetric ear silhouette; head tilt `-8`; short rounded limbs; blue/navy headphone palette and white “L”. No files edited.
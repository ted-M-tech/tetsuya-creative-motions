**HOLD — recognizable, but not yet a close enough match to ship.** These are proposed starting values, not render-validated fixes. All changes refer to `scripts/mimi.py`.

1. **Head pose lacks the target’s playful tilt.** Current face is almost level and turned farther sideways. In `main()`, change default `hero:-28` → `hero:-18`. In `build()`, after `root = rig(...)`, apply an **−8° world-Y head rotation**, converted into bone-local coordinates:
   ```python
   pb = root.pose.bones['head']
   q = pb.bone.matrix_local.to_quaternion()
   pb.rotation_mode = 'QUATERNION'
   pb.rotation_quaternion = q.inverted() @ Matrix.Rotation(
       math.radians(-8), 4, 'Y').to_quaternion() @ q
   ```
   **Confidence: medium-high.** Reassess the remaining proportions after this.

2. **The swept ear is a straight paddle; the target has a broader, lower, hooked silhouette.** In `ear()`, for `s == -1`, change outer center Z `0.33 → 0.29`, radii `(0.175, 0.115, 0.335) → (0.19, 0.115, 0.295)`; inner center Z `0.36 → 0.31`, radii `(0.102, 0.014, 0.235) → (0.115, 0.014, 0.195)`. In `build()`, its tilt `-48 → -60`. This improves the silhouette; a curved root would still be needed for an exact match. **Confidence: medium.**

3. **The face sits too low and the eyes read slightly narrow.** In `build()`, eye Z offset `-0.085 → -0.060`, eye X radius `0.05 → 0.055`; nose Z offset `-0.125 → -0.100`; blush Z offset `-0.165 → -0.140`. In `mouth_curve()`, baseline offset `-0.142 → -0.117`. Keep facial spacing initially. **Confidence: medium-high.**

4. **The hands merge into the belly as soft bumps instead of distinct rounded paws.** In `fused_body()`, arm centers `(0.2*s, -0.15, 0.3) → (0.225*s, -0.175, 0.3)` and radii `(0.088, 0.082, 0.098) → (0.095, 0.09, 0.098)`. Leave torso dimensions untouched. **Confidence: high.**

5. **Headphone cups feel undersized relative to the head.** In `headphones()`, cup radius `0.195 → 0.210`, blue-face radius `0.17 → 0.182`, letter size `0.21 → 0.22`. Retain current depths and band radius. **Confidence: medium; judge after the camera correction.**

6. **Lighting washes out the near paw while leaving the far face gray.** In `stage()`, key energy `300 → 240`, fill `25 → 65`, world strength `0.2 → 0.3`; retain exposure `-1.0` initially. Aim for readable white vinyl across both sides. **Confidence: medium.**

**Keep:** approved torso fullness; upright ear’s outward lean (`12°`); broad cheek silhouette; short feet; white/blue/navy palette; single eye catchlights; compact nose and W-shaped smile.

No files edited.
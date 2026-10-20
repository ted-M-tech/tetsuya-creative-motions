# Rounds 1–2 (summary)

The first two Codex reviews were read in the terminal and not saved as files. This is a faithful summary of what they asked for and what was applied. Rounds 3–9 and the final verdict are kept verbatim in this folder.

## Round 1 (render "r1", after model v8)

Ranked by Codex:

1. Lighting erases the white forms → lower exposure, world, fill, top light, sweep emission; warmer white, less sheen. **Applied.**
2. Ears are thin paddles; upright ear leans the wrong way → thicker ears, narrower roots; flop −62° → −48°; upright +8° → −18°. **Thickness applied; upright lean rejected** (the target leans outward, so it went to +12°).
3. Head/body balance → larger head; narrower torso; hands lower at the sides; bigger feet. **Head, hands, feet applied; narrower torso rejected** (the client had just said the body looked too thin).
4. Headphone cups undersized → larger cups and blue faces, thinner band; brighter blue `#159bfa`, deeper navy `#142953`. **Applied.**
5. Eyes too broad, pale and flat → narrower, darker `#071b45`, glossier; smaller catchlight. **Applied.**
6. Mouth reads as a pointed "W" → smooth sine-squared lobes; smaller nose. **Applied.**
7. Framing too loose → closer camera, higher target, hero yaw −20°. **Applied** (it cropped the ears; distance was backed off afterwards).
8. Blush small and cool → larger radius, warmer `#ff9eaa`. **Applied.**

## Round 2 (render "r3")

1. Ears: thicker rims; the inner-panel taper used the panel's centred local Z as if it started at the root (a real bug) → corrected formula. **Applied.**
2. Head too modest, hands too high → head `(0.455, 0.35, 0.38)`, stronger lower-cheek widening, hands lower. **Applied** (hands later moved back in).
3. Mouth: semicircular lobes instead of sine-squared, 81 samples, nose closer to the smile. **Applied.**
4. Headphones: rounder cushions (bigger bevel), larger cups, cups moved out for the wider head. **Applied**; the band was widened to clear the head (checked with `check_overlap.py`).
5. Framing: hero yaw back to −28°, closer camera. **Applied.**
6. Presentation: brighter backdrop, cooler white, glossier navy. **Partly applied**; the brighter backdrop washed out the lower body through floor bounce and was turned down again.

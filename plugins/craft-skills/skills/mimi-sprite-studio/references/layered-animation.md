# Layered animation (multi-part art)

1. Make the cutout (`cutout.py --grid none`), then label 8-connected components of `alpha>40` (BFS; use a numpy label image `lab.npy`).
2. Spread labels 3–4 px to soft-edge pixels (`max` of 8 neighbours where alpha>0 and label==0) so edges travel with their part.
3. Classify by area/bbox: big (cats, wing) · medium (ghost wisps) · small (<~1500 px: sparkles, plus signs, dots).
4. Per frame, `t = 2π·i/N`, render layers back→front on a padded canvas (pad 60px so negative offsets don't crash `alpha_composite`):
   - big parts: `dy = ±10·sin(t)` in opposite phases, rotation ±2.5°
   - ghosts: `dy = 14·sin(t + k·1.7)`, `dx = 6·sin(2t + k)`, rot 4°
   - twinkles: scale `1 + .25·sin(2t + .9k)`, alpha `.55 + .45·(.5+.5·sin(...))`, rot 20°
   - glow regions (e.g. pumpkin): multiply RGB by `1 + .35·(.5+.5·sin(2t))` on masked pixels
5. Crop to the content box → square → resize to 512; save WebP(lossy q≈88)/GIF/APNG.
Use integer multiples of t only, so frame N equals frame 0.

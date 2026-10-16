# Mascot style recipes (all SVG, viewBox 0 0 512 512, circle-safe)

Shared: dark radial-gradient bg; soft aura = blurred (stdDeviation 10–24) copy of the body shape in the glow colour; 3–6 four-point sparkles (`M x y-r Q x y x+r y Q x y x y+r Q x y x-r y Q x y x y-r Z`); filters declared once in `<defs>` with `x/y -50%`, `width/height 200%` so blur isn't clipped.

## Neon rim-light blob cat (minimal, black on black)
- Body = chubby bean path + two triangle ears with rounded tips; fill near-black vertical gradient ending in a pastel tint at the bottom (belly glow).
- Rim: stroke the *union* with a rainbow `linearGradient` (cyan→pink→peach→mint), width ~12, plus a blurred copy (width 16, blur 10, opacity .85). Draw stroked shapes first, then re-draw fills on top so only the outer half of the stroke shows.
- Tiny white dot eyes (blurred copy underneath), a "ω" mouth, 2–3 hairline whiskers each side (stop 60px before the circle edge).
- Floor: 5px gradient bar, fade at both ends, blurred copy beneath, faint reflection ellipse.

## Glass potion with sleepy cat
- Sphere `radialGradient` lavender→white, thick white stroke (12) + blue blurred halo behind; neck = rounded rect rotated -40°, cork rect on top.
- Cat clipped inside the sphere (`clipPath`): lavender blob, white 5px outline at .8 opacity, closed-eye chevrons in navy, pink blush, curled tail stroke, paw print.
- Highlights: big white ellipse left, arc along upper-left edge. Keep the cork inside radius ~235 of centre.

## Glossy slime (amber / ember / mint)
- Dome-with-flat-bottom path; `radialGradient` light→mid→dark (focus top-left), darker translucent "core" ellipse bottom-centre, lighter rim stroke 7 at .85, blurred outer glow stroke.
- Gloss: thick curved highlight stroke top-left, small ellipses; blush ellipses; bokeh circles above (r 9–26, blurred 1.2, opacity .2–.35).
- Variants: ring eyes (stroke circles), single oval eye + long bunny ears, angry white wedge eyes + flame on top, closed happy arcs.

## Tech mascot (chubby AI bot)
Body gradient light→mid→dark, dark rounded-rect "face screen" with glowing eyes (blurred duplicate), blush ellipses, antenna with glow orb, ear nubs, belly highlight, ground glow ellipse. Colour themes: blue `#4cc9ff`, violet `#b46cff`, mint `#4dffc3`, peach `#ffa06b`.

# Writing the style brief

The brief is the single source of truth for every asset in a kit. Write it before drawing anything and keep it next to the generator as `style_brief.md`.

## From a photo or image

1. Run `scripts/palette_from_image.py` to get 8–16 dominant colours, sorted dark to light.
2. Name each colour by its role, not its hue: `bg`, `bg_dark`, `accent`, `accent_light`, `outline`, `text`, `highlight`, `shadow`. Drop near-duplicates; add a pure highlight or outline colour if the photo lacks one.
3. Note what the image shows beyond colour: shapes (round, blocky, sharp), texture (flat, grainy, glossy), lighting (soft, neon, dusk), and recurring objects that can become motifs.

## From text only

Turn adjectives into concrete choices. For example:

| User says | Brief choice |
|---|---|
| cozy, calm | muted greens and creams, rounded shapes, slow 1–2 px motion |
| playful, cute | pastel palette, chubby mascot, bouncy animation |
| neon, gamer | near-black background, saturated cyan / magenta rim light, glow |
| minimal, professional | 3–4 colours, flat shapes, lots of empty space, no animation |

Pick 8–12 colours yourself and state them as hex codes so the user can adjust them.

## Brief template

```
Project:     <name> — <one-line tagline>
Profile(s):  <discord-bot | google-play | ...>
Art style:   <pixel art at N× scale | flat vector | glossy 3D-ish | ...>
Palette:     bg #...  bg_dark #...  accent #...  accent_light #...  outline #...  text #...  highlight #...
Motifs:      <3–5 recurring objects, e.g. orange trees, mushrooms, fireflies>
Mascot:      <optional character and its idle animation, e.g. white cat that blinks>
Typography:  <pixel 5×7 caps | rounded sans | none on assets>
Motion:      <none | looping GIF, 12 frames at ~11 fps | APNG>
Words:       <labels that appear on assets, e.g. RULES, WELCOME, NEWS, EVENTS>
```

## Consistency rules

- Use only palette colours in every asset; no off-palette gradients.
- Keep one outline colour and one line weight across the kit.
- Reuse the same mascot and motifs on the small assets (icon, emoji) so they read as one family with the large ones (banners, feature graphic).
- Keep text short and large enough to read at the platform's smallest display size.

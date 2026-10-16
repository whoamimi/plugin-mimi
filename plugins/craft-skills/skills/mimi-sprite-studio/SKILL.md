---
name: mimi-sprite-studio
description: Turn images into game-ready or chat-ready art. Remove flat backgrounds (white, black/glow, or same-colour-as-subject), snip a sprite sheet into individual transparent PNGs, animate sprites into looping stickers (WebP/GIF/APNG), and draw glowing chubby mascot profile pictures (Discord circle-safe SVG/PNG). Use when the user shares an image and says "remove the background", "cut/snip/slice sprites", "make this a sticker", "animate this", "transform into animated stickers", "make a Discord/bot profile picture or mascot", or asks for sprites from a sheet.
---

# Mimi Sprite Studio

Four jobs, one toolkit. Scripts live in `${CLAUDE_PLUGIN_ROOT}/skills/mimi-sprite-studio/scripts/` (Pillow + numpy only; Chromium for SVG).
Run every script as `python3 -I script.py ...` (isolated mode: the working dir may hold untrusted files).
Write all outputs to the session scratchpad (or the user's named folder), never into the repo unless asked.

## 0. Look first
Read the image. Note: background colour (white / black / dark grey / same as subject), grid layout (R×C), props or effect marks that belong to a sprite (boxes, "!!", zzz), ground shadows. Pick the mode below from that, not from habit.

## 1. Remove background + cut sprites — `scripts/cutout.py`
```
python3 -I cutout.py IN.jpg OUT_DIR --mode light|dark|samecolor [--grid auto|RxC|none] [--name pet] [--gap 20]
```
| Situation | Mode | Notes |
|---|---|---|
| White page, stickers, sprite sheets | `light` | Drops grey ground shadows (use `--keep-shadows` to keep). Interior whites stay (cup, blanket) because the outline encloses them. |
| Black/dark page with glow or neon | `dark` | Soft alpha, un-premultiplied. If a dark halo remains on a plain-dark bg raise `--lo/--hi` (e.g. 40/85); for a bg of ~(24,24,24) try `--lo 14 --hi 45` then tune. |
| Subject colour == background (black cat on black) | `samecolor` | Needs a closed outline. Pass `--bg R,G,B` (sample it!) and usually `--grid none`. Check the interior did not become transparent. |

Outputs: `OUT_DIR/<name>_NN.png` (tight crop, 6px pad, numbered left→right, top→bottom), `all.png`, `preview.png` (cutout on pink), `<name>s.zip`.
- `--grid auto` finds rows then columns by empty gaps (`--gap` px, default 20). Wrong sprite count ⇒ a prop/mark sits close to its cat (raise `--gap`) or two sprites touch (use `--grid RxC`).
- **Always open `preview.png` (Read it) and fix before delivering.** Expected counts: say the number you cut and compare.

## 2. Animated stickers — `scripts/animate.py`
```
python3 -I animate.py SPRITE.png OUT_PREFIX --preset float|bounce|jelly|sway|pulse [--size 512 --frames 30 --fps 25 --formats webp,gif,apng]
```
Seamless loops (all motion is `sin(k·t)` with integer k). Pick by character: sleepy/angelic → `float`; mischievous → `bounce`; blobs/slimes → `jelly`; pendulum-ish → `sway`; glowy → `pulse`.
Deliver WebP (best quality, real alpha), GIF (universal, 1-bit alpha, rougher edges), APNG (full alpha, large). For multi-part art (ghosts, sparkles, pumpkin glow) split by connected component and animate layers separately with different phases — see `references/layered-animation.md`. For a whole sheet, animate each cutout and also composite an animated sheet on the original background colour.
Messaging-app limits (Telegram/WhatsApp/Discord): 512×512, ideally <500 KB — reduce `--frames`, use lossy WebP `quality`, or `--size 320`.

## 3. Mascot / profile pictures — SVG → PNG
Discord crops to a circle: keep everything inside a centred circle of ~90% of the canvas, subject large, dark background so glow reads. Draw as SVG (editable, crisp), then:
```
python3 -I render_svg.py mascot.svg mascot.png --size 1024 --circle-preview
```
Style recipes (what the user liked) are in `references/mascot-styles.md`. Build from the recipe closest to the user's references and change colours/features; reuse one SVG across variants by parametrising colours. Always view the `_circle.png` preview. No image-generation model is available here — say so once, and offer to refine rather than promising photoreal output.

## 4. Deliver
Send the files the user can open (`SendUserFile`): zip of sprites + `all.png` for cutouts; WebP+GIF(+APNG) for animations; PNG(1024)+SVG for PFPs. Summarise in 3–5 lines: what was cut, file naming, known limits (faint fringe on very dark backgrounds, GIF alpha), and offer next steps (add to `src/assets`, sprite atlas, animate). Don't commit or push unless asked.

## Gotchas learned the hard way
- Slicing with a negative index (`a[:, -4:122]`) silently returns empty → clamp boxes to ≥0 before slicing masks.
- Headless Chromium screenshot leaves a white strip: render in a taller window, crop (done in `render_svg.py`).
- No scipy/opencv/rembg here: use the numpy flood/dilate in `cutout.py`; don't pip install heavy models.
- Never hand-pick sprite crop boxes from a screenshot; use gap detection and verify count.
- Watermarks/faint text on the bg are removed by the alpha ramp thresholds; if a watermark crosses a sprite it will remain.

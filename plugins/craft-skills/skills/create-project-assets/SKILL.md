---
name: create-project-assets
description: Generates a matching set of branded image assets for a project from the user's style reference (a photo or a written description), sized and checked against a platform profile such as a Discord bot kit or Google Play store listing, with new platforms added as profiles. Use when the user wants icons, banners, emoji, stickers, feature graphics or store artwork for an app, bot, server or project in a consistent style. Examples include "make Discord bot assets in this style", "create Google Play assets for my app", "turn this photo into a branding kit" and "I need an icon and banners that look cozy and pixel-art".
---

# Create Project Assets

Turn one style reference into a consistent, platform-ready asset kit. The skill is a recipe with three swappable parts:

- **Style brief** — palette, art style, motifs and mood taken from the user's photo or text.
- **Profile** — what a platform needs: files, sizes, formats and limits (`profiles/<name>.md` + `profiles/<name>.json`).
- **Generator** — a script that draws every asset from the brief, so the kit can be regenerated after any change.

Scripts are in `${CLAUDE_PLUGIN_ROOT}/skills/create-project-assets/scripts/` and need Python 3 with Pillow. Run them with `python3 -I`. Write all output to the session scratchpad or a folder the user names, never into this repository unless asked.

## 1. Collect the inputs

A style reference is **required**. Before generating anything, make sure you have:

1. **Style reference** — one or more photos/images, or a descriptive text such as "cozy pixel-art forest, soft greens, a white cat mascot". If the user gave neither, ask for one in a single short message and stop.
2. **Target profile** — which platform the kit is for (see the table below). If unclear, ask.
3. **Project details** — name, short tagline, and any words that must appear on assets (e.g. "RULES", "WELCOME").

Treat a reference image as style input only: take colours, shapes and mood from it, never trace or copy a copyrighted character, logo or artwork.

## 2. Write the style brief

Follow `references/style-brief.md`. For a photo, extract the palette first:

```bash
python3 -I scripts/palette_from_image.py REFERENCE.jpg --colors 12 --swatch OUT/palette.png --json OUT/palette.json
```

Show the user the brief (palette swatch, art style, motifs, mascot, typography) in a few lines and get a yes before generating the full kit.

## 3. Pick the profile

| Profile | For | Guide |
|---|---|---|
| `discord-bot` | Discord bot or server: app icon, embed banners, thumbnail, divider, emoji, stickers | [profiles/discord-bot.md](profiles/discord-bot.md) |
| `google-play` | Android app store listing: app icon, feature graphic, screenshots | [profiles/google-play.md](profiles/google-play.md) |

Read the profile's guide before generating. **No profile fits?** Create one with [profiles/TEMPLATE.md](profiles/TEMPLATE.md) (a `.md` guide plus a `.json` spec), then continue. The user can also ask for several profiles from one brief; generate each into its own sub-folder.

## 4. Generate the assets

1. Copy the closest example into the output folder as a starting point. `examples/discord-cozy-grove/` is a complete pixel-art kit: `cozy_grove/make_assets.py` draws everything in code (palette dict, 5×7 pixel font, string-art sprites, looping GIF animation), and `cozy_grove/style.py` posts Discord embeds and cards that use the assets. `examples/discord-cozy-grove/preview.png` shows the result.
2. Replace its palette with the brief's colours, its sprites and motifs with the brief's, and its sizes and file names with the profile's spec.
3. Match the drawing method to the art style:
   - **Pixel art** — draw at low resolution and upscale with `Image.NEAREST`, as the example does.
   - **Flat, vector or glossy styles** — draw SVG and render it with `${CLAUDE_PLUGIN_ROOT}/skills/mimi-sprite-studio/scripts/render_svg.py`.
4. Keep everything in one generator script, so changing a colour or word means re-running it, not redrawing by hand.

## 5. Check against the profile

```bash
python3 -I scripts/check_assets.py --profile profiles/PROFILE.json OUT_DIR
python3 -I scripts/contact_sheet.py OUT_DIR OUT_DIR/preview.png
```

`check_assets.py` reports each required asset as OK or FAIL (size, format, transparency, file size, count). Fix every FAIL and re-run until it passes. Then open `preview.png` (Read it) and check that the kit looks consistent: same palette, same line weight, readable text.

## 6. Deliver

Send a zip of the kit, `preview.png` and the generator script (`SendUserFile`). Summarise in 3–5 lines: profile used, files produced, any spec that is "check before submitting" in the profile, and next steps (for example, wiring `style.py` into the user's bot, or uploading to Play Console).

## Rules

- Never generate without a style reference from the user.
- Follow the profile's spec exactly; when the profile marks a spec as unconfirmed, say so in the summary.
- Store screenshots must show the real app. Frame or decorate the user's own screenshots; never invent app screens.
- Never put tokens, keys or channel IDs in generated files; read them from the environment, as `style.py` does.

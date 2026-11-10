---
name: create-brand-assets
description: Generates a matching brand kit (icons, banners, emoji, stickers, feature graphics, mascots) for an app, bot or project from the user's style reference, a photo or a written description, using mimi-sprite-studio as the default design generator and checking every file against a platform profile such as a Discord bot kit or Google Play store listing. Use when the user wants branded artwork or store assets in one consistent style. Examples include "make Discord bot brand assets in this style", "create Google Play assets for my app", "turn this photo into a brand kit" and "I need an icon and banners that look cozy and pixel-art".
---

# Create Brand Assets

Turn one style reference into a consistent, platform-ready brand kit. The skill is a recipe with three swappable parts:

- **Style brief** — palette, art style, motifs and mood taken from the user's photo or text.
- **Profile** — what a platform needs: files, sizes, formats and limits (`profiles/<name>.md` + `profiles/<name>.json`).
- **Generator** — **`mimi-sprite-studio`** (in this plugin) by default: it cuts subjects out of photos, animates stickers and renders SVG mascots and icons. A generator script that draws every asset from the brief keeps the kit reproducible.

Scripts are in `${CLAUDE_PLUGIN_ROOT}/skills/create-brand-assets/scripts/` and need Python 3 with Pillow. Run them with `python3 -I`. Write all output to the session scratchpad or a folder the user names, never into this repository unless asked.

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

Use **`mimi-sprite-studio`** as the default generator. Its scripts are in `${CLAUDE_PLUGIN_ROOT}/skills/mimi-sprite-studio/scripts/` and its style recipes in `${CLAUDE_PLUGIN_ROOT}/skills/mimi-sprite-studio/references/`; follow that skill's instructions for each tool.

| Asset need | mimi-sprite-studio tool |
|---|---|
| Subject or mascot from the user's photo or sprite sheet | `cutout.py`: remove the background and cut transparent PNGs |
| Icon, avatar, mascot or profile picture | an SVG built from `references/mascot-styles.md`, rendered with `render_svg.py` (use `--circle-preview` for round crops) |
| Animated emoji, sticker or thumbnail | `animate.py` (float, bounce, jelly, sway, pulse), or `references/layered-animation.md` for multi-part art |
| Banners, feature graphics, dividers | an SVG at the profile's exact size rendered with `render_svg.py --size WIDTH --height HEIGHT`, reusing the mascot and palette |

Then:

1. Resize and export every file to the profile's exact size, format and file names.
2. Keep all steps in one generator script in the output folder, so changing a colour or word means re-running it, not redrawing by hand.
3. **Pixel-art kits drawn in code** are the exception: start from `examples/discord-cozy-grove/` instead. `cozy_grove/make_assets.py` draws everything at low resolution (palette dict, 5×7 pixel font, string-art sprites, looping GIFs) and upscales with `Image.NEAREST`; `cozy_grove/style.py` posts Discord embeds and cards that use the assets; `preview.png` shows the result. Replace its palette, sprites, words and sizes with the brief's and the profile's.

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

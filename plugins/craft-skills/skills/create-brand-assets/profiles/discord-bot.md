# Profile: Discord bot

Assets for a Discord bot or server, matching the `examples/discord-cozy-grove/` kit. Spec: `discord-bot.json`.

| Asset | File(s) | Size | Notes | Confirmed |
|---|---|---|---|---|
| App / bot avatar | `app_icon.png` | square, at least 512 × 512 (1024 recommended) | Upload in the Developer Portal; shown as a circle, so keep the subject centred | No |
| Embed banners | `banner_*.gif` / `.png` | 960 × 240 (kit convention) | One per post type (rules, welcome, news, event); animated GIF loops well | Kit only |
| Embed thumbnail | `*_idle.gif` / `thumb*.png` | 128 × 128 | Mascot idle loop shown at the top right of embeds | Kit only |
| Divider | `divider.gif` / `.png` | 960 × 32, transparent | Separates sections in Components V2 cards | Kit only |
| Author / footer icon | `icon_*.png` | 64 × 64, transparent | Shown very small; keep it a single simple shape | Kit only |
| Custom emoji | `emoji_*.png` / `.gif` | 128 × 128, under 256 KB | Name rules: letters, numbers and underscores, at least 2 characters | No |
| Stickers (optional) | `sticker_*.png` | 320 × 320, under 512 KB, PNG or APNG | Server must have boost level for sticker slots | Yes |
| Profile banner (optional) | `profile_banner.png` | at least 680 × 240 | Shown behind the bot's profile | No |

"Kit only" means Discord accepts any size; these sizes are what the example kit uses and keeps consistent. "No" means the size comes from third-party guides; tell the user to check the Developer Portal before relying on it.

## Design tips

- Discord shows both dark and light themes; test banners and emoji on both backgrounds.
- Emoji display at about 22 px inline and 48 px when enlarged; use bold silhouettes and at most 4–5 colours.
- Keep animations short (8–16 frames) and loopable; large GIFs slow channels down.
- Reuse the mascot from the banners as the avatar and thumbnail so the bot is recognisable.

## Using the assets

`examples/discord-cozy-grove/cozy_grove/style.py` uploads the assets with each message (`attachment://name`), so nothing needs hosting. To reuse it, rename the package, replace `COZY` and `STYLES` with the new palette and post types, and keep the bot token in the `DISCORD_BOT_TOKEN` environment variable.

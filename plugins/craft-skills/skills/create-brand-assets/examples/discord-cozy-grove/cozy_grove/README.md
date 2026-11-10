# Cozy Grove kit

Pixel-art styling for Discord posts: animated banners, a blinking-cat thumbnail, a firefly divider, an icon and custom emoji, plus code to post them.

## Contents

```
cozy_grove/
├── __init__.py        # from cozy_grove import post_cozy, post_cozy_card, ...
├── __main__.py        # Command line: python -m cozy_grove ...
├── style.py           # Palette, embed/card builders, senders
├── make_assets.py     # Regenerates assets/ (needs Pillow)
└── assets/
    ├── banner_rules.gif     960×240, animated
    ├── banner_welcome.gif   960×240, animated (blinking cat)
    ├── banner_news.gif      960×240, animated
    ├── banner_event.gif     960×240, animated (bunting)
    ├── cat_idle.gif         128×128 thumbnail, animated
    ├── divider.gif          960×32, animated, transparent
    ├── icon_leaf.png        64×64 author/footer icon
    ├── emoji_cozy_cat.png / .gif, emoji_orange.png,
    └── emoji_mushroom.png, emoji_sprout.png   128×128 custom emoji
```

## Palette

| Name | Hex | Used for |
|---|---|---|
| leaf | `#82A884` | Default accent |
| meadow | `#A4C263` | Welcome |
| moss | `#688A7B` | Rules |
| path | `#E8CFA6` | Neutral |
| peach | `#EEBA77` | News |
| bark | `#C49A6C` | Mod / alerts |
| bloom | `#EAE178` | Events |
| ink | `#5C7479` | Outlines |

## Usage

Command line (reads `DISCORD_BOT_TOKEN` from `.env`):

```bash
uv run python -m cozy_grove rules --channel "$RULES_CHANNEL_ID" --body-file channels/rules.md
```

From Python:

```python
from cozy_grove import post_cozy, post_cozy_card

post_cozy(channel_id, "news", "Grove News", "New channels are open! 🍊")
post_cozy_card(channel_id, "event", "Movie Night", [("When", "Friday 8pm"), ("Where", "#stage")])
```

Kinds: `rules`, `welcome`, `news`, `event`. Add `message_id=` (or `--edit ID`) to update a post in place.

## Regenerate the art

Edit the palette, words or sprites in `make_assets.py`, then:

```bash
uv run --with pillow python cozy_grove/make_assets.py
```

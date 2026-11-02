# Adding a profile

A profile tells the skill what one platform needs. Add a new platform (an Apple App Store listing, a Telegram sticker pack, a Twitch channel, a website favicon set) by adding two files to `profiles/`:

- `<name>.md` — a short human guide: what each asset is for, design tips, and where the user uploads it.
- `<name>.json` — the machine-readable spec that `scripts/check_assets.py` checks against.

Use a lowercase, hyphenated name such as `apple-app-store`, then add a row for it to the profile table in `SKILL.md`.

## JSON spec format

```json
{
  "name": "example-platform",
  "title": "Example Platform",
  "sources": ["https://official.docs/url"],
  "assets": [
    {
      "id": "app-icon",
      "description": "Square app icon",
      "required": true,
      "confirmed": true,
      "globs": ["icon.png"],
      "count": {"min": 1, "max": 1},
      "formats": ["png"],
      "width": 512,
      "height": 512,
      "alpha": "any",
      "max_kb": 1024,
      "animated": false
    }
  ]
}
```

Fields for each asset:

| Field | Meaning |
|---|---|
| `id`, `description` | Short identifier and a one-line explanation |
| `required` | `true` if the platform rejects the submission without it |
| `confirmed` | `true` only if the size came from the platform's own docs; otherwise the summary must say "check before submitting" |
| `globs` | File-name patterns inside the output folder, e.g. `["screenshots/phone/*.png", "screenshots/phone/*.jpg"]` |
| `count` | Minimum and maximum number of matching files |
| `formats` | Allowed formats: `png`, `jpeg`, `gif`, `webp` |
| `width`, `height` | Exact size in pixels (omit for flexible sizes) |
| `min_side`, `max_side` | Allowed range for the shorter and longer side (flexible sizes) |
| `max_ratio` | Longest side divided by shortest side may not exceed this |
| `square` | `true` if width must equal height |
| `alpha` | `"required"`, `"forbidden"` or `"any"` |
| `max_kb` | Maximum file size in kilobytes |
| `animated` | `true` allowed, `false` forbidden, omit for either |

Record where each number came from in `sources`, and prefer the platform's official documentation over third-party size guides.

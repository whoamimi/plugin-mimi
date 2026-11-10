# Profile: Google Play store listing

Graphic assets for an Android app's Google Play store listing, uploaded in Play Console under **Grow → Store presence → Main store listing**. Spec: `google-play.json`.

| Asset | File(s) | Spec | Required | Confirmed |
|---|---|---|---|---|
| App icon | `icon.png` | 512 × 512, 32-bit PNG with alpha, at most 1024 KB | Yes | Yes |
| Feature graphic | `feature_graphic.png` / `.jpg` | 1024 × 500, JPEG or 24-bit PNG, no alpha | Yes | Yes |
| Phone screenshots | `screenshots/phone/*.png` / `.jpg` | 2–8 images, JPEG or 24-bit PNG, each side 320–3840 px, longest side at most 2× the shortest | Yes | No |
| 7-inch tablet screenshots | `screenshots/tablet7/*` | Same rules as phone, up to 8 | No | No |
| 10-inch tablet screenshots | `screenshots/tablet10/*` | Same rules as phone, up to 8 | No | No |

Screenshot rules are marked unconfirmed because the official page could not be reached when this profile was written, and third-party guides disagree. Tell the user to check Play Console's upload hints before submitting.

## Design tips

- **Icon** — Google Play applies its own rounded mask and shadow; fill the full square, keep the key shape inside the central ~66%, and do not add your own rounded corners or drop shadow.
- **Feature graphic** — shown behind the promo video and on some store surfaces, often cropped; keep the logo and words in the centre and avoid small text.
- **Screenshots** — must show the real app. Generate only the frame around them: a branded background, a short caption per screenshot and an optional device outline, then place the user's own screenshots inside. Use the same caption style on every screenshot.
- **Adaptive launcher icon** (inside the app, not the store) — if the user also wants it, export a 432 × 432 foreground layer with the subject inside the central 288 × 288 and a separate background layer.

## Inputs to ask for

- The app's real screenshots (portrait phone captures), if screenshots are wanted.
- Caption text for each screenshot, or permission to draft it from the app's features.

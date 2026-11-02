#!/usr/bin/env python3
"""Extract a colour palette from a style reference image.

usage: python3 -I palette_from_image.py IMAGE [--colors 12] [--swatch palette.png] [--json palette.json]

Prints the dominant colours as hex codes, sorted dark to light, with the share
of the image each one covers. Use the result as the starting palette of a
style brief, then name each colour by its role (bg, accent, outline, ...).
Deps: Pillow.
"""
import argparse
import json
import sys

from PIL import Image, ImageDraw

# Downscale before quantizing: palette extraction does not need full
# resolution, and 256 px keeps it fast on large photos.
WORK_SIZE = 256
SWATCH_CELL = 64


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def extract(path, n):
    try:
        im = Image.open(path)
    except OSError as exc:
        sys.exit(f"Cannot open {path}: {exc}")
    im = im.convert("RGBA")
    im.thumbnail((WORK_SIZE, WORK_SIZE))
    # Ignore fully transparent pixels so a cut-out's background does not
    # become a palette colour.
    if im.getextrema()[3][0] < 255:
        # Pillow 12+ renames getdata(); support both.
        pixels = im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()
        opaque = [p for p in pixels if p[3] > 0]
        if not opaque:
            sys.exit("The image is fully transparent.")
        im = Image.new("RGBA", (len(opaque), 1))
        im.putdata(opaque)
    im = im.convert("RGB")
    q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: 3 * n]
    counts = sorted(q.getcolors(), key=lambda c: -c[0])
    total = sum(c for c, _ in counts)
    colours = []
    for count, idx in counts:
        rgb = tuple(pal[3 * idx: 3 * idx + 3])
        colours.append({"hex": "#%02X%02X%02X" % rgb, "rgb": list(rgb), "share": round(count / total, 3)})
    colours.sort(key=lambda c: luminance(c["rgb"]))
    return colours


def save_swatch(colours, path):
    img = Image.new("RGB", (SWATCH_CELL * len(colours), SWATCH_CELL + 16), (40, 40, 46))
    d = ImageDraw.Draw(img)
    for i, c in enumerate(colours):
        x = i * SWATCH_CELL
        d.rectangle([x, 0, x + SWATCH_CELL - 1, SWATCH_CELL - 1], fill=tuple(c["rgb"]))
        d.text((x + 4, SWATCH_CELL + 2), c["hex"], fill=(230, 230, 230))
    img.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--colors", type=int, default=12, help="number of colours to extract (default 12)")
    ap.add_argument("--swatch", help="write a swatch PNG here")
    ap.add_argument("--json", help="write the palette as JSON here")
    a = ap.parse_args()
    if not 2 <= a.colors <= 32:
        sys.exit("--colors must be between 2 and 32")
    colours = extract(a.image, a.colors)
    for c in colours:
        print(f"{c['hex']}  {c['share'] * 100:5.1f}%")
    if a.swatch:
        save_swatch(colours, a.swatch)
        print("swatch ->", a.swatch)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(colours, f, indent=2)
        print("json ->", a.json)


if __name__ == "__main__":
    main()

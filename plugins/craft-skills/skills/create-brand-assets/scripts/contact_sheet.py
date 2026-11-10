#!/usr/bin/env python3
"""Lay out every image in a folder on one preview sheet.

usage: python3 -I contact_sheet.py ASSET_DIR preview.png [--width 1200]

Animated files show their first frame. Each image is scaled down (never up)
to fit its row, with its file name and real size underneath, so the whole kit
can be checked for a consistent palette and style in one look. Deps: Pillow.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

BG = (40, 40, 46)
TEXT = (220, 220, 220)
PAD = 16
LABEL_H = 14
# Small assets (icons, emoji) are grouped on rows of this height.
SMALL_ROW_H = 140
EXTENSIONS = {".png", ".gif", ".jpg", ".jpeg", ".webp"}


def load(path):
    with Image.open(path) as im:
        size = im.size
        im.seek(0)
        frame = im.convert("RGBA")
    return frame, size


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("asset_dir")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1200, help="sheet width in pixels")
    a = ap.parse_args()

    out_path = Path(a.out).resolve()
    paths = sorted(p for p in Path(a.asset_dir).rglob("*")
                   if p.suffix.lower() in EXTENSIONS and p.resolve() != out_path)
    if not paths:
        sys.exit(f"No images found in {a.asset_dir}")

    inner = a.width - 2 * PAD
    items = []
    for p in paths:
        try:
            frame, size = load(p)
        except OSError as exc:
            print(f"skip {p}: {exc}")
            continue
        scale = min(1.0, inner / frame.width, (SMALL_ROW_H if frame.width <= 256 else 600) / frame.height)
        if scale < 1:
            frame = frame.resize((max(1, int(frame.width * scale)), max(1, int(frame.height * scale))))
        items.append((p.relative_to(a.asset_dir).as_posix(), size, frame))

    # Simple row packing: wide images get their own row, small ones share.
    rows, row, row_w = [], [], 0
    for item in items:
        w = item[2].width
        if row and row_w + PAD + w > inner:
            rows.append(row)
            row, row_w = [], 0
        row.append(item)
        row_w += (PAD if row_w else 0) + w
    if row:
        rows.append(row)

    height = PAD + sum(max(i[2].height for i in r) + LABEL_H + PAD for r in rows)
    sheet = Image.new("RGBA", (a.width, height), BG + (255,))
    d = ImageDraw.Draw(sheet)
    y = PAD
    for r in rows:
        x = PAD
        row_h = max(i[2].height for i in r)
        for name, (w, h), frame in r:
            sheet.alpha_composite(frame, (x, y))
            d.text((x, y + frame.height + 2), f"{name} ({w}x{h})", fill=TEXT)
            x += frame.width + PAD
        y += row_h + LABEL_H + PAD
    sheet.convert("RGB").save(a.out)
    print(f"{len(items)} images -> {a.out}")


if __name__ == "__main__":
    main()

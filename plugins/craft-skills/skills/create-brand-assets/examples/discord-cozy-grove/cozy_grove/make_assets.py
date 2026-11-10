"""Generate the Cozy Grove pixel-art kit for Discord posts.

Everything is drawn at low resolution, then scaled up with nearest-neighbour
so the pixels stay crisp. Re-run after changing the palette or the words:

    uv run --with pillow make_assets.py

Output goes to ./assets/.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).parent / "assets"
FRAMES = 12          # Frames per loop
FRAME_MS = 90        # ~11 fps

# ─── Palette (sampled from the reference scene) ─────────────────────
P = {
    "bg": (0x82, 0xA8, 0x84),
    "bg_dark": (0x6E, 0x96, 0x7C),
    "moss": (0x68, 0x8A, 0x7B),
    "hedge": (0x97, 0xBB, 0x8E),
    "hedge_light": (0xAE, 0xD4, 0x99),
    "hedge_hi": (0xC2, 0xE0, 0x9A),
    "grass": (0xA4, 0xC2, 0x63),
    "grass_light": (0xC0, 0xD4, 0x70),
    "grass_dark": (0x8D, 0xB1, 0x5D),
    "path": (0xE8, 0xCF, 0xA6),
    "path_dark": (0xD7, 0xBF, 0xA3),
    "ink": (0x5C, 0x74, 0x79),
    "bark": (0xC4, 0x9A, 0x6C),
    "bark_dark": (0x9C, 0x73, 0x50),
    "fruit": (0xEC, 0x9A, 0x5B),
    "fruit_hi": (0xF2, 0xCF, 0x8C),
    "peach": (0xEE, 0xBA, 0x77),
    "bloom": (0xEA, 0xE1, 0x78),
    "cream": (0xF3, 0xF2, 0xC0),
    "white": (0xF7, 0xF4, 0xEA),
    "lilac": (0x8E, 0x87, 0xC9),
    "pink": (0xF2, 0xB8, 0xB0),
}
KEY = (255, 0, 255)  # Transparent colour in GIFs


# ─── Pixel font (5×7) for banner signs ─────────────────────────────
FONT = {
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "U": ["10001"] * 6 + ["01110"],
    "L": ["10000"] * 6 + ["11111"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "T": ["11111"] + ["00100"] * 6,
}


def text_width(word: str) -> int:
    return len(word) * 6 - 1


def draw_text(img, x, y, word, color, shadow=None):
    for i, ch in enumerate(word):
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    if shadow:
                        img.putpixel((x + i * 6 + c, y + r + 1), shadow)
    for i, ch in enumerate(word):
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    img.putpixel((x + i * 6 + c, y + r), color)


# ─── Sprites (string art) ──────────────────────────────────────────
CAT = [
    "................",
    "..OO........OO..",
    ".OPWO......OWPO.",
    ".OWWWOOOOOOWWWO.",
    ".OWWWWWWWWWWWWO.",
    ".OWWWWWWWWWWWWO.",
    ".OWWEWWWWWWEWWO.",
    ".OWWEWWWWWWEWWO.",
    ".OWPWWWNNWWWPWO.",
    ".OWWWWWWWWWWWWO.",
    "..OWWWWWWWWWWO..",
    "..OWWWWWWWWWWO..",
    "..OWWOWWWWOWWO..",
    "..OWWOWWWWOWWO..",
    "...OOOOOOOOOO...",
    "................",
]
CAT_COLORS = {"O": "lilac", "W": "white", "P": "pink", "E": "ink", "N": "pink"}


def draw_sprite(img, x, y, rows, colors, scale=1):
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in colors:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((x + c * scale + dx, y + r * scale + dy), P[colors[ch]])


def cat_frame(f: int) -> list[str]:
    rows = [list(r) for r in CAT]
    if f in (7, 8):  # Blink: eyes become a single closed line
        rows[6][4] = rows[6][11] = "W"
    # Tail flicks up and down
    tail_up = f % 6 < 3
    rows[12 if tail_up else 13][14] = "O"
    rows[11 if tail_up else 12][15] = "O"
    return ["".join(r) for r in rows]


def draw_cat(img, x, y, f, scale=1):
    draw_sprite(img, x, y, cat_frame(f), CAT_COLORS, scale)


# ─── Scene pieces ──────────────────────────────────────────────────
def wave(f, k=1, phase=0.0):
    return math.sin(2 * math.pi * k * f / FRAMES + phase)


def draw_hedge_frame(d, x0, y0, x1, y1):
    points = []
    for x in range(x0, x1 + 1, 7):
        points += [(x, y0), (x, y1)]
    for y in range(y0, y1 + 1, 7):
        points += [(x0, y), (x1, y)]
    points += [(x1, y0), (x0, y1), (x1, y1)]
    for cx, cy in points:
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=P["moss"])
    for cx, cy in points:
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=P["hedge"])
    for cx, cy in points:
        d.ellipse([cx - 3, cy - 4, cx, cy - 1], fill=P["hedge_light"])


def draw_tree(d, img, cx, base, f, fruits=True, phase=0.0):
    sway = round(wave(f, 1, phase))
    d.rectangle([cx - 2, base - 12, cx + 1, base], fill=P["bark"])
    d.rectangle([cx - 2, base - 12, cx - 2, base], fill=P["bark_dark"])
    d.rectangle([cx - 4, base, cx + 3, base], fill=P["bark_dark"])
    top = base - 30
    d.ellipse([cx - 12 + sway, top, cx + 11 + sway, top + 20], fill=P["moss"])
    d.ellipse([cx - 11 + sway, top + 1, cx + 10 + sway, top + 18], fill=P["hedge"])
    d.ellipse([cx - 8 + sway, top + 2, cx + 2 + sway, top + 9], fill=P["hedge_light"])
    d.ellipse([cx - 6 + sway, top + 3, cx - 2 + sway, top + 6], fill=P["hedge_hi"])
    if fruits:
        for i, (fx, fy) in enumerate([(-6, 10), (3, 6), (5, 13), (-1, 14)]):
            bob = round(wave(f, 1, i * 1.3))
            x, y = cx + fx + sway, top + fy + bob
            d.rectangle([x, y, x + 2, y + 2], fill=P["fruit"])
            img.putpixel((x, y), P["fruit_hi"])


def draw_mushroom(d, x, base, cap="path"):
    d.rectangle([x + 2, base - 4, x + 4, base], fill=P["cream"])
    d.rectangle([x + 2, base - 4, x + 2, base], fill=P["path_dark"])
    d.rectangle([x, base - 7, x + 6, base - 5], fill=P["bark_dark"])
    d.rectangle([x + 1, base - 8, x + 5, base - 8], fill=P["bark_dark"])
    d.rectangle([x + 1, base - 7, x + 5, base - 5], fill=P[cap])
    d.rectangle([x + 2, base - 8, x + 4, base - 7], fill=P[cap])
    d.point((x + 2, base - 7), fill=P["white"])
    d.point((x + 4, base - 6), fill=P["white"])


def draw_flower(img, x, y, f, i):
    petal = P["bloom"] if (f + i) % 4 else P["cream"]
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        img.putpixel((x + dx, y + dy), petal)
    img.putpixel((x, y), P["fruit"])


def draw_orange(d, img, x, y, f, i=0):
    bob = round(wave(f, 1, i))
    d.ellipse([x, y + bob, x + 5, y + 5 + bob], fill=P["fruit"])
    img.putpixel((x + 1, y + 1 + bob), P["fruit_hi"])
    d.rectangle([x + 3, y - 1 + bob, x + 4, y - 1 + bob], fill=P["grass_dark"])


def draw_fireflies(img, w, h, f, n, seed, y_range):
    rnd = random.Random(seed)
    for i in range(n):
        bx = rnd.randrange(8, w - 8)
        by = rnd.randrange(*y_range)
        x = int(bx + 3 * wave(f, 1, i))
        y = int(by + 2 * wave(f, 2, i * 0.7))
        if (f + i) % 3:
            img.putpixel((x, y), P["cream"])
            if (f + i) % 3 == 1:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        img.putpixel((x + dx, y + dy), P["bloom"])


def scatter_meadow(img, d, f, seed, box, avoid):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(40):
        x, y = rnd.randrange(x0, x1), rnd.randrange(y0, y1)
        if any(ax0 <= x <= ax1 and ay0 <= y <= ay1 for ax0, ay0, ax1, ay1 in avoid):
            continue
        kind = rnd.random()
        if kind < 0.55:   # Grass tuft
            img.putpixel((x, y), P["grass_dark"])
            img.putpixel((x + 2, y), P["grass_dark"])
            img.putpixel((x + 1, y + 1), P["grass_dark"])
        elif kind < 0.8:  # Light patch
            d.rectangle([x, y, x + 3, y + 1], fill=P["grass_light"])
        else:
            draw_flower(img, x, y, f, x)


# ─── Banners ───────────────────────────────────────────────────────
BANNERS = {
    "rules": "RULES",
    "welcome": "WELCOME",
    "news": "NEWS",
    "event": "EVENTS",
}


def banner_frame(kind: str, f: int) -> Image.Image:
    W, H = 240, 60
    img = Image.new("RGB", (W, H), P["bg"])
    d = ImageDraw.Draw(img)
    # Background leaf texture
    rnd = random.Random(7)
    for _ in range(60):
        x, y = rnd.randrange(W), rnd.randrange(H)
        d.rectangle([x, y, x + 1, y], fill=P["bg_dark"])

    d.rectangle([10, 10, 229, 49], fill=P["grass"])
    draw_hedge_frame(d, 8, 6, 231, 53)
    d.rectangle([13, 12, 226, 47], fill=P["grass"])
    d.ellipse([74, 38, 166, 50], fill=P["path"])

    word = BANNERS[kind]
    tw = text_width(word)
    bx0, bx1 = 120 - tw // 2 - 6, 120 + (tw - tw // 2) + 5
    by0, by1 = 18, 33
    scatter_meadow(img, d, f, sum(map(ord, kind)), (16, 14, 222, 46),
                   [(bx0 - 4, by0 - 2, bx1 + 4, 46), (14, 12, 40, 46), (200, 12, 226, 46)])

    if kind == "event":
        # Bunting strung between the two trees
        flags = [P["fruit"], P["bloom"], P["cream"], P["peach"]]
        for i, x in enumerate(range(42, 200, 8)):
            sag = int(6 * math.sin(math.pi * (x - 42) / 158))
            y = 12 + sag + round(0.6 * wave(f, 1, i))
            d.polygon([(x, y), (x + 5, y), (x + 2, y + 4)], fill=flags[i % 4])

    # Signboard
    d.rectangle([bx0 + 4, by1, bx0 + 5, 45], fill=P["bark_dark"])
    d.rectangle([bx1 - 5, by1, bx1 - 4, 45], fill=P["bark_dark"])
    d.rectangle([bx0, by0, bx1, by1], fill=P["bark_dark"])
    d.rectangle([bx0 + 1, by0 + 1, bx1 - 1, by1 - 1], fill=P["bark"])
    d.rectangle([bx0 + 2, by0 + 2, bx1 - 2, by1 - 2], fill=P["path"])
    d.line([bx0 + 2, by0 + 2, bx1 - 2, by0 + 2], fill=P["cream"])
    draw_text(img, bx0 + 6, by0 + 4, word, P["ink"], shadow=P["path_dark"])

    draw_tree(d, img, 27, 46, f, phase=0.0)
    draw_tree(d, img, 212, 46, f, fruits=kind != "rules", phase=1.5)

    right = bx1 + 10
    left = bx0 - 10
    if kind == "rules":
        for i, x in enumerate((right, right + 8, right + 16, left - 6, left - 15)):
            draw_mushroom(d, x, 45 - (i % 2), cap="peach" if i == 1 else "path")
    elif kind == "welcome":
        draw_cat(img, right, 31, f)
        draw_flower(img, left - 2, 42, f, 1)
        draw_flower(img, left - 8, 44, f, 2)
    elif kind == "news":
        d.rectangle([right, 38, right + 14, 45], fill=P["bark"])  # Basket
        d.line([right, 38, right + 14, 38], fill=P["bark_dark"])
        for i, x in enumerate((right + 1, right + 5, right + 9)):
            draw_orange(d, img, x, 32, f, i)
        draw_orange(d, img, left - 6, 39, f, 3)
    elif kind == "event":
        for i, x in enumerate((right, right + 5, left - 3, left - 9)):
            draw_flower(img, x, 41 + (i % 2) * 2, f, i)

    draw_fireflies(img, W, H, f, 7, 42 + len(kind), (12, 46))
    return img


# ─── Small assets ──────────────────────────────────────────────────
def thumb_frame(f):
    img = Image.new("RGB", (32, 32), P["bg"])
    d = ImageDraw.Draw(img)
    d.ellipse([1, 1, 30, 30], fill=P["hedge"])
    d.ellipse([3, 19, 28, 30], fill=P["grass"])
    d.ellipse([5, 3, 14, 9], fill=P["hedge_light"])
    draw_cat(img, 8, 11, f)
    draw_fireflies(img, 32, 32, f, 2, 5, (4, 12))
    return img


def divider_frame(f):
    W, H = 240, 8
    img = Image.new("RGB", (W, H), KEY)
    d = ImageDraw.Draw(img)
    d.line([4, 4, W - 5, 4], fill=P["moss"])
    for i, x in enumerate(range(8, W - 8, 10)):
        up = i % 2 == 0
        lift = round(0.6 * wave(f, 1, i * 0.8))
        y = (2 if up else 5) + lift
        d.rectangle([x, y, x + 2, y + 1], fill=P["hedge_light"] if up else P["hedge"])
        if i % 5 == 2:
            draw_flower(img, x + 5, 4, f, i)
    for i, x in enumerate((W // 2 - 3,)):
        d.ellipse([x, 1, x + 5, 6], fill=P["fruit"])
        img.putpixel((x + 1, 2), P["fruit_hi"])
    return img


def leaf_icon():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([3, 0, 15, 12], fill=P["moss"] + (255,))
    d.ellipse([4, 1, 14, 11], fill=P["grass"] + (255,))
    d.ellipse([6, 2, 10, 6], fill=P["grass_light"] + (255,))
    d.line([6, 10, 13, 3], fill=P["grass_dark"] + (255,))
    d.line([1, 15, 6, 10], fill=P["bark_dark"] + (255,))
    return img


def emoji(name):
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    a = lambda k: P[k] + (255,)
    if name == "cozy_cat":
        tmp = Image.new("RGB", (16, 16), KEY)
        draw_cat(tmp, 0, 0, 0)
        tmp = tmp.resize((32, 32), Image.NEAREST)
        img.paste(tmp, (0, 0))
        img = _key_to_alpha(img)
    elif name == "orange":
        d.ellipse([4, 7, 27, 29], fill=a("bark_dark"))
        d.ellipse([5, 8, 26, 28], fill=a("fruit"))
        d.ellipse([8, 11, 14, 16], fill=a("fruit_hi"))
        d.rectangle([15, 4, 16, 8], fill=a("bark_dark"))
        d.ellipse([17, 2, 25, 7], fill=a("grass"))
        d.line([18, 5, 24, 4], fill=a("grass_dark"))
    elif name == "mushroom":
        d.rectangle([12, 16, 19, 28], fill=a("cream"))
        d.rectangle([12, 16, 13, 28], fill=a("path_dark"))
        d.pieslice([3, 4, 28, 26], 180, 360, fill=a("bark_dark"))
        d.pieslice([4, 5, 27, 25], 180, 360, fill=a("peach"))
        for x, y in ((9, 10), (17, 8), (21, 12)):
            d.rectangle([x, y, x + 2, y + 1], fill=a("cream"))
        d.rectangle([4, 28, 27, 29], fill=a("grass_dark"))
    elif name == "sprout":
        d.ellipse([6, 22, 25, 30], fill=a("bark"))
        d.ellipse([8, 22, 23, 26], fill=a("bark_dark"))
        d.rectangle([15, 12, 16, 24], fill=a("grass_dark"))
        d.ellipse([4, 6, 15, 14], fill=a("grass"))
        d.ellipse([16, 3, 28, 12], fill=a("hedge_light"))
        d.line([6, 10, 14, 12], fill=a("grass_dark"))
        d.line([26, 6, 17, 11], fill=a("moss"))
    return img


def _key_to_alpha(img):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y][:3] == KEY:
                px[x, y] = (0, 0, 0, 0)
    return img


# ─── Saving ────────────────────────────────────────────────────────
def _palette_image():
    colors = list(P.values()) + [KEY]
    flat = [v for c in colors for v in c] + [0] * (768 - 3 * len(colors))
    pal = Image.new("P", (1, 1))
    pal.putpalette(flat)
    return pal, len(colors) - 1


def save_gif(frames, path, scale, transparent=False):
    pal, key_index = _palette_image()
    out = []
    for fr in frames:
        q = fr.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE)
        out.append(q.resize((fr.width * scale, fr.height * scale), Image.NEAREST))
    kwargs = {"transparency": key_index, "disposal": 2} if transparent else {}
    out[0].save(path, save_all=True, append_images=out[1:], duration=FRAME_MS,
                loop=0, optimize=False, **kwargs)


def main():
    OUT.mkdir(exist_ok=True)
    for kind in BANNERS:
        save_gif([banner_frame(kind, f) for f in range(FRAMES)], OUT / f"banner_{kind}.gif", 4)
    save_gif([thumb_frame(f) for f in range(FRAMES)], OUT / "cat_idle.gif", 4)
    save_gif([divider_frame(f) for f in range(FRAMES)], OUT / "divider.gif", 4, transparent=True)
    leaf_icon().resize((64, 64), Image.NEAREST).save(OUT / "icon_leaf.png")
    for name in ("cozy_cat", "orange", "mushroom", "sprout"):
        emoji(name).resize((128, 128), Image.NEAREST).save(OUT / f"emoji_{name}.png")
    # Animated cat emoji too
    cat_frames = []
    for f in range(FRAMES):
        tmp = Image.new("RGB", (16, 16), KEY)
        draw_cat(tmp, 0, 0, f)
        cat_frames.append(tmp)
    save_gif(cat_frames, OUT / "emoji_cozy_cat.gif", 8, transparent=True)
    print("Wrote", len(list(OUT.iterdir())), "files to", OUT)


if __name__ == "__main__":
    main()

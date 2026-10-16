#!/usr/bin/env python3
"""Turn a transparent sprite PNG into a seamless looping animated sticker.

usage: python3 -I animate.py SPRITE.png OUT_PREFIX [--preset float|bounce|jelly|sway|pulse]
                             [--size 512] [--frames 30] [--fps 25] [--formats webp,gif,apng] [--scale 0]
Outputs OUT_PREFIX.webp / .gif / .png(APNG). Every motion is sin(k*t) with integer k, so frame N == frame 0 (seamless loop).
Anchored presets (jelly) squash from the sprite's bottom edge so it stays "standing" on the ground.
"""
import argparse, math
import numpy as np
from PIL import Image

PRESETS = {  # t in [0,2pi) -> dy px, rot deg, sx, sy, brightness  (fractions of sprite size where noted)
    'float':  lambda t: (-0.04 * math.sin(t), 3 * math.sin(t + .8), 1, 1 + .02 * math.sin(2 * t), 1 + .05 * math.sin(2 * t)),
    'bounce': lambda t: (-0.07 * abs(math.sin(t)), 4 * math.sin(2 * t), 1 + .03 * math.cos(2 * t), 1 - .03 * math.cos(2 * t), 1 + .06 * math.sin(6 * t)),
    'jelly':  lambda t: (-0.015 * math.sin(t + 1.57), 2.5 * math.sin(t + 1.2), 1 + .04 * math.sin(t), 1 - .06 * math.sin(t), 1 + .12 * math.sin(2 * t)),
    'sway':   lambda t: (0, 8 * math.sin(t), 1, 1, 1),
    'pulse':  lambda t: (0, 0, 1 + .06 * math.sin(t), 1 + .06 * math.sin(t), 1 + .1 * math.sin(t)),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sprite'); ap.add_argument('out')
    ap.add_argument('--preset', default='float', choices=PRESETS)
    ap.add_argument('--size', type=int, default=512); ap.add_argument('--frames', type=int, default=30)
    ap.add_argument('--fps', type=int, default=25); ap.add_argument('--formats', default='webp,gif,apng')
    ap.add_argument('--scale', type=float, default=0, help='sprite scale; 0 = fit to 78%% of canvas')
    a = ap.parse_args()
    sp = Image.open(a.sprite).convert('RGBA'); S = a.size
    sc = a.scale or (0.78 * S / max(sp.size))
    sp = sp.resize((max(1, int(sp.width * sc)), max(1, int(sp.height * sc))), Image.LANCZOS)
    fn = PRESETS[a.preset]; frames = []
    for i in range(a.frames):
        dy, rot, sx, sy, br = fn(2 * math.pi * i / a.frames)
        f = sp.resize((int(sp.width * sx), int(sp.height * sy)), Image.LANCZOS)
        f = f.rotate(rot, resample=Image.BICUBIC, expand=True)
        arr = np.asarray(f).astype(np.float32); arr[..., :3] = np.clip(arr[..., :3] * br, 0, 255)
        f = Image.fromarray(arr.astype(np.uint8), 'RGBA')
        c = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        c.alpha_composite(f, ((S - f.width) // 2, (S - f.height) // 2 + int(dy * S)))
        frames.append(c)
    d = 1000 // a.fps; fm = a.formats.split(',')
    if 'webp' in fm:
        frames[0].save(a.out + '.webp', save_all=True, append_images=frames[1:], duration=d, loop=0, quality=90, method=4, exact=True)
    if 'apng' in fm:
        frames[0].save(a.out + '.png', save_all=True, append_images=frames[1:], duration=d, loop=0, disposal=1, blend=0, optimize=True)
    if 'gif' in fm:  # GIF alpha is 1-bit: reserve palette index 255 for transparency
        g = []
        for f in frames:
            p = f.convert('RGB').quantize(255, dither=Image.NONE)
            arr = np.asarray(p).copy(); arr[np.asarray(f)[..., 3] < 128] = 255
            q = Image.fromarray(arr, 'P'); q.putpalette((p.getpalette() + [0] * 768)[:768]); g.append(q)
        g[0].save(a.out + '.gif', save_all=True, append_images=g[1:], duration=d, loop=0, disposal=2, transparency=255)
    print('wrote', a.out, fm)

if __name__ == '__main__': main()

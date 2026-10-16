#!/usr/bin/env python3
"""Remove a flat background from an image and split it into transparent sprites.

usage: python3 -I cutout.py INPUT OUT_DIR [--mode light|dark|samecolor] [--grid auto|RxC|none]
                            [--bg R,G,B] [--name sprite] [--keep-shadows] [--pad 6]
Deps: Pillow, numpy only (no scipy / opencv).

modes
  light      white/near-white background (stickers, sprite sheets). Also drops grey ground shadows.
  dark       black/dark background with glow (neon art). Soft alpha, un-premultiplied against bg.
  samecolor  subject whose body is the SAME colour as the background (black cat on black bg).
             Keeps the body by treating its outline as a closed boundary.
Writes OUT_DIR/<name>_NN.png, OUT_DIR/all.png (whole cutout), OUT_DIR/preview.png, OUT_DIR/<name>s.zip
"""
import argparse, os, zipfile
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

def flood(allowed):
    h, w = allowed.shape
    seen = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if allowed[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if allowed[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and allowed[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    return seen

def dilate(m, r):
    o = m.copy()
    for _ in range(r):
        p = np.pad(o, 1)
        o = (p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
             | p[:-2, :-2] | p[2:, 2:] | p[:-2, 2:] | p[2:, :-2])
    return o

def touching(bg):  # pixels with a 4-neighbour in bg (image border counts as bg)
    p = np.pad(bg, 1, constant_values=True)
    return p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]

def soften(alpha_bool):
    a = Image.fromarray(alpha_bool.astype(np.uint8) * 255).filter(ImageFilter.GaussianBlur(0.6))
    return np.where(alpha_bool, 255, np.asarray(a)).astype(np.uint8)

def cut_light(im, a):
    mn = im.min(2); mx = im.max(2)
    bg = flood(mn > 240)
    if not a.keep_shadows:                      # neutral light-grey ground shadows touching the bg
        neutral = (mx - mn < 10) & (mn > 185) & ~(mn > 240)
        bg |= flood(bg | neutral) & neutral
    fg = ~bg
    for _ in range(2):                          # peel light anti-alias fringe, keep light props
        fg &= ~(touching(~fg) & (mn > 215))
    return im, soften(fg)

def cut_dark(im, a):
    bgc = np.array(a.bg_rgb, np.float32)
    diff = np.abs(im - bgc).max(2)
    bg = flood(diff < a.hi)
    alpha = np.where(bg, np.clip((diff - a.lo) / max(a.hi - a.lo, 1), 0, 1), 1.0)
    k = alpha[..., None]
    rgb = np.where(k > 0, np.clip((im - bgc * (1 - k)) / np.maximum(k, 1e-3), 0, 255), 0)
    return rgb, (alpha * 255).astype(np.uint8)

def cut_samecolor(im, a, R=3):
    bgc = np.array(a.bg_rgb, np.float32)
    diff = np.abs(im - bgc).max(2)
    fg = diff > 14
    closed = dilate(fg, R)                      # bridges tiny gaps in the outline
    outside = flood(~closed)
    mask = ~outside
    bgish = diff < 30
    for _ in range(R + 1):                      # undo the dilation halo
        mask &= ~(touching(~mask) & bgish)
    edge = mask & touching(~mask)
    alpha = np.where(mask, 1.0, 0.0)
    alpha[edge] = np.clip((diff[edge] - 6) / 40, 0.35, 1)
    k = alpha[..., None]
    rgb = np.where(edge[..., None], np.clip((im - bgc * (1 - k)) / np.maximum(k, 1e-3), 0, 255), im)
    return rgb, (alpha * 255).astype(np.uint8)

def runs(v, gap):
    idx = np.nonzero(v > 0)[0]
    if not len(idx): return []
    out = []; s = p = idx[0]
    for i in idx[1:]:
        if i - p > gap: out.append((s, p + 1)); s = i
        p = i
    out.append((s, p + 1)); return out

def cells(alpha, grid, gap=6):
    h, w = alpha.shape
    solid = alpha > 20
    if grid == 'none': return [(0, h, 0, w)]
    if grid == 'auto':
        rr = runs(solid.sum(1), gap)
        out = []
        for r0, r1 in rr:                       # columns per row band -> handles ragged rows
            for c0, c1 in runs(solid[r0:r1].sum(0), gap): out.append((r0, r1, c0, c1))
        return out
    R, C = map(int, grid.lower().split('x'))
    return [(int(r * h / R), int((r + 1) * h / R), int(c * w / C), int((c + 1) * w / C)) for r in range(R) for c in range(C)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('out')
    ap.add_argument('--mode', default='light', choices=['light', 'dark', 'samecolor'])
    ap.add_argument('--grid', default='auto'); ap.add_argument('--name', default='sprite')
    ap.add_argument('--bg'); ap.add_argument('--pad', type=int, default=6)
    ap.add_argument('--lo', type=float, default=40); ap.add_argument('--hi', type=float, default=85)
    ap.add_argument('--keep-shadows', action='store_true')
    ap.add_argument('--gap', type=int, default=20, help='min empty pixels that separates auto-grid cells')
    a = ap.parse_args()
    im = np.asarray(Image.open(a.input).convert('RGB')).astype(np.float32)
    border = np.concatenate([im[0], im[-1], im[:, 0], im[:, -1]])
    a.bg_rgb = tuple(map(float, a.bg.split(','))) if a.bg else tuple(np.median(border, 0))
    rgb, alpha = {'light': cut_light, 'dark': cut_dark, 'samecolor': cut_samecolor}[a.mode](im, a)
    rgba = np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), alpha]); rgba[alpha == 0, :3] = 0
    os.makedirs(a.out, exist_ok=True)
    Image.fromarray(rgba, 'RGBA').save(f'{a.out}/all.png')
    pv = Image.new('RGBA', (rgba.shape[1], rgba.shape[0]), (255, 120, 190, 255))
    pv.alpha_composite(Image.fromarray(rgba, 'RGBA')); pv.convert('RGB').save(f'{a.out}/preview.png')
    z = zipfile.ZipFile(f'{a.out}/{a.name}s.zip', 'w', zipfile.ZIP_DEFLATED); n = 0
    for r0, r1, c0, c1 in cells(alpha, a.grid, a.gap):
        sub = rgba[r0:r1, c0:c1]; ys, xs = np.nonzero(sub[..., 3] > 20)
        if not len(ys): continue
        n += 1; p = a.pad
        box = (max(xs.min() - p, 0), max(ys.min() - p, 0), min(xs.max() + p + 1, sub.shape[1]), min(ys.max() + p + 1, sub.shape[0]))
        fn = f'{a.out}/{a.name}_{n:02d}.png'
        Image.fromarray(sub, 'RGBA').crop(box).save(fn); z.write(fn, os.path.basename(fn))
    z.close(); print(f'{n} sprites -> {a.out} (preview.png shows the cutout on pink; LOOK AT IT before delivering)')

if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Render an SVG to a PNG with headless Chromium (no cairosvg/rsvg needed).

usage: python3 -I render_svg.py in.svg out.png [--size 1024] [--height H] [--circle-preview]
The window is made taller than the image and cropped afterwards: headless Chromium otherwise
leaves a white strip at the bottom. --height renders a non-square image (e.g. --size 960 --height 240 for a
banner); it defaults to --size. --circle-preview also writes out_circle.png (Discord-style round crop).
"""
import argparse, glob, os, subprocess, tempfile
from PIL import Image, ImageDraw

def chromium():
    for pat in ('/opt/pw-browsers/chromium-*/chrome-linux/chrome', '/opt/pw-browsers/chromium/chrome-linux/chrome'):
        g = glob.glob(pat)
        if g: return g[0]
    for n in ('chromium', 'chromium-browser', 'google-chrome'):
        for d in os.environ.get('PATH', '').split(':'):
            if os.path.exists(os.path.join(d, n)): return os.path.join(d, n)
    raise SystemExit('no chromium found')

ap = argparse.ArgumentParser(); ap.add_argument('svg'); ap.add_argument('out')
ap.add_argument('--size', type=int, default=1024); ap.add_argument('--circle-preview', action='store_true')
ap.add_argument('--height', type=int, help='image height in pixels; defaults to --size')
a = ap.parse_args(); S = a.size; H = a.height or S
svg = open(a.svg).read()
with tempfile.TemporaryDirectory() as d:
    html = os.path.join(d, 'p.html')
    open(html, 'w').write(f'<body style="margin:0;background:transparent"><div style="width:{S}px;height:{H}px">{svg}</div></body>')
    subprocess.run([chromium(), '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    f'--window-size={S},{H + 200}', f'--screenshot={os.path.abspath(a.out)}', 'file://' + html],
                   check=True, capture_output=True)
Image.open(a.out).crop((0, 0, S, H)).save(a.out)
if a.circle_preview:
    im = Image.open(a.out).convert('RGBA'); m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, S - 1, H - 1), fill=255)
    bg = Image.new('RGBA', im.size, (40, 40, 46, 255)); bg.paste(im, (0, 0), m)
    bg.save(os.path.splitext(a.out)[0] + '_circle.png')

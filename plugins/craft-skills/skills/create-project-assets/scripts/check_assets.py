#!/usr/bin/env python3
"""Check a generated asset folder against a profile spec.

usage: python3 -I check_assets.py --profile profiles/google-play.json OUT_DIR

Prints one line per asset in the profile (OK / FAIL / SKIP) with the reason,
and exits 1 if any required asset fails or any present file breaks the spec.
The spec format is described in profiles/TEMPLATE.md. Deps: Pillow.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image

FORMAT_NAMES = {"PNG": "png", "JPEG": "jpeg", "GIF": "gif", "WEBP": "webp"}


def has_alpha(im):
    if im.mode in ("RGBA", "LA", "PA"):
        return True
    # Palette, RGB and grayscale PNGs can carry colour-key transparency (tRNS).
    return "transparency" in im.info


def is_animated(im):
    return getattr(im, "n_frames", 1) > 1


def check_file(path, spec):
    """Return a list of problems with one file."""
    problems = []
    try:
        with Image.open(path) as im:
            fmt = FORMAT_NAMES.get(im.format, (im.format or "?").lower())
            w, h = im.size
            alpha = has_alpha(im)
            animated = is_animated(im)
    except OSError as exc:
        return [f"cannot open ({exc})"]

    if "formats" in spec and fmt not in spec["formats"]:
        problems.append(f"format {fmt}, expected {'/'.join(spec['formats'])}")
    if "width" in spec and w != spec["width"]:
        problems.append(f"width {w}, expected {spec['width']}")
    if "height" in spec and h != spec["height"]:
        problems.append(f"height {h}, expected {spec['height']}")
    if spec.get("square") and w != h:
        problems.append(f"{w}x{h} is not square")
    short, long_ = min(w, h), max(w, h)
    if "min_side" in spec and short < spec["min_side"]:
        problems.append(f"shortest side {short} < {spec['min_side']}")
    if "max_side" in spec and long_ > spec["max_side"]:
        problems.append(f"longest side {long_} > {spec['max_side']}")
    if "max_ratio" in spec and long_ / short > spec["max_ratio"]:
        problems.append(f"aspect ratio {long_ / short:.2f} > {spec['max_ratio']}")
    if spec.get("alpha") == "required" and not alpha:
        problems.append("needs transparency (alpha)")
    if spec.get("alpha") == "forbidden" and alpha:
        problems.append("must not have transparency; flatten onto a background")
    if spec.get("animated") is False and animated:
        problems.append("must not be animated")
    size_kb = path.stat().st_size / 1024
    if "max_kb" in spec and size_kb > spec["max_kb"]:
        problems.append(f"{size_kb:.0f} KB > {spec['max_kb']} KB")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True, help="profile JSON spec")
    ap.add_argument("out_dir", help="folder with the generated assets")
    a = ap.parse_args()

    try:
        profile = json.loads(Path(a.profile).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"Cannot read profile {a.profile}: {exc}")
    out = Path(a.out_dir)
    if not out.is_dir():
        sys.exit(f"Not a folder: {out}")

    print(f"Profile: {profile.get('title', profile.get('name'))}\n")
    failed = False
    for spec in profile["assets"]:
        files = sorted({p for g in spec["globs"] for p in out.glob(g) if p.is_file()})
        label = f"{spec['id']:<22}"
        note = "" if spec.get("confirmed", True) else "  (spec unconfirmed: check before submitting)"
        lo = spec.get("count", {}).get("min", 1 if spec.get("required") else 0)
        hi = spec.get("count", {}).get("max")

        if not files and not spec.get("required") and lo == 0:
            print(f"SKIP  {label} none found (optional)")
            continue
        issues = []
        if len(files) < lo:
            issues.append(f"found {len(files)} file(s), need at least {lo} matching {spec['globs']}")
        if hi is not None and len(files) > hi:
            issues.append(f"found {len(files)} file(s), at most {hi} allowed")
        for f in files:
            issues += [f"{f.relative_to(out)}: {p}" for p in check_file(f, spec)]

        if issues:
            failed = True
            print(f"FAIL  {label} {len(files)} file(s){note}")
            for i in issues:
                print(f"        - {i}")
        else:
            print(f"OK    {label} {len(files)} file(s){note}")

    print("\nResult:", "FAIL" if failed else "OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

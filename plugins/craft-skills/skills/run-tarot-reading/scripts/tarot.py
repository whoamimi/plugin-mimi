#!/usr/bin/env python3
"""Tarot deck engine: shuffle, then reveal the positions the querent picks.

The shuffle is fully determined by an integer seed, so a table can always be
rebuilt with --seed even if the session file is gone. Orientation (upright or
reversed) is fixed at shuffle time, not at reveal time -- the card was already
lying that way in the pile.

Usage:
  python3 tarot.py shuffle                      # cut the deck, print the fan
  python3 tarot.py reveal 7 22 41               # turn over those positions
  python3 tarot.py reveal 7 22 41 --seed 123    # rebuild the same table
  python3 tarot.py draw --count 3               # quick auto-draw, no picking
  python3 tarot.py lookup "The Tower"           # single card reference
"""

import argparse
import json
import os
import random
import secrets
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DECK_PATH = os.path.join(HERE, "..", "assets", "deck.json")
SESSION_PATH = os.environ.get("TAROT_SESSION", "/tmp/tarot_session.json")


def load_deck():
    with open(DECK_PATH) as f:
        return json.load(f)["cards"]


def build_table(seed, deck):
    """Return the shuffled pile: a list of (card, is_reversed), position 1..78."""
    rng = random.Random(seed)
    order = list(deck)
    rng.shuffle(order)
    return [(card, rng.random() < 0.5) for card in order]


def describe(card, reversed_):
    orient = "Reversed" if reversed_ else "Upright"
    keys = card["reversed"] if reversed_ else card["upright"]
    suit = f" ({card['suit']} / {card['element']})" if card["suit"] else " (Major Arcana)"
    return f"{card['name']} - {orient}{suit}\n    keywords: {keys}"


def save_session(seed, spread, picked=None):
    with open(SESSION_PATH, "w") as f:
        json.dump({"seed": seed, "spread": spread, "picked": picked or []}, f)


def load_session():
    try:
        with open(SESSION_PATH) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def cmd_shuffle(args):
    seed = secrets.randbelow(10**12)
    save_session(seed, args.spread)
    print(f"Deck shuffled and cut. 78 cards face down. (seed {seed})")
    print(f"Spread: {args.spread}")
    print()
    for start in range(1, 79, 13):
        row = " ".join(f"[{n:>2}]" for n in range(start, min(start + 13, 79)))
        print("  " + row)
    print()
    print(f"Ask the querent for {args.count} numbers between 1 and 78,")
    print("then run:  python3 tarot.py reveal <n> <n> <n>")


def cmd_reveal(args):
    deck = load_deck()
    session = load_session()
    seed = args.seed if args.seed is not None else (session or {}).get("seed")
    if seed is None:
        print("No shuffled deck found. Run 'shuffle' first, or pass --seed.")
        sys.exit(1)
    spread = args.spread or (session or {}).get("spread") or "Past / Present / Future"
    positions = [p.strip() for p in spread.split("/")]

    picks = args.picks
    if len(set(picks)) != len(picks):
        print("Duplicate positions -- each card can only be drawn once.")
        sys.exit(1)
    if any(p < 1 or p > 78 for p in picks):
        print("Positions must be between 1 and 78.")
        sys.exit(1)

    table = build_table(seed, deck)
    print(f"Spread: {spread}   (seed {seed})\n")
    for i, p in enumerate(picks):
        card, rev = table[p - 1]
        label = positions[i] if i < len(positions) else f"Card {i + 1}"
        print(f"{i + 1}. {label}  <- card #{p}")
        print(f"    {describe(card, rev)}\n")
    save_session(seed, spread, picks)


def cmd_draw(args):
    deck = load_deck()
    seed = secrets.randbelow(10**12)
    table = build_table(seed, deck)
    spread = args.spread
    positions = [p.strip() for p in spread.split("/")]
    picks = random.SystemRandom().sample(range(1, 79), args.count)
    print(f"Spread: {spread}   (seed {seed})\n")
    for i, p in enumerate(picks):
        card, rev = table[p - 1]
        label = positions[i] if i < len(positions) else f"Card {i + 1}"
        print(f"{i + 1}. {label}  <- card #{p}")
        print(f"    {describe(card, rev)}\n")
    save_session(seed, spread, picks)


def cmd_lookup(args):
    deck = load_deck()
    needle = args.name.lower()
    hits = [c for c in deck if needle in c["name"].lower()]
    if not hits:
        print(f"No card matching '{args.name}'.")
        sys.exit(1)
    for c in hits:
        print(f"{c['name']}")
        print(f"    upright:  {c['upright']}")
        print(f"    reversed: {c['reversed']}\n")


def main():
    ap = argparse.ArgumentParser(description="Tarot deck engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("shuffle", help="shuffle and show the face-down fan")
    s.add_argument("--spread", default="Past / Present / Future")
    s.add_argument("--count", type=int, default=3)
    s.set_defaults(func=cmd_shuffle)

    r = sub.add_parser("reveal", help="turn over the querent's chosen positions")
    r.add_argument("picks", nargs="+", type=int)
    r.add_argument("--seed", type=int, default=None)
    r.add_argument("--spread", default=None)
    r.set_defaults(func=cmd_reveal)

    d = sub.add_parser("draw", help="auto-draw without the querent picking")
    d.add_argument("--count", type=int, default=3)
    d.add_argument("--spread", default="Past / Present / Future")
    d.set_defaults(func=cmd_draw)

    l = sub.add_parser("lookup", help="look up one card's keywords")
    l.add_argument("name")
    l.set_defaults(func=cmd_lookup)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

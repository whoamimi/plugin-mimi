---
name: "run-tarot-reading"
description: "Run an interactive tarot reading where the querent personally picks their cards from a shuffled 78-card deck, then get a woven three-card interpretation. Use this skill whenever someone mentions tarot, asks to pull or draw cards, wants a card reading or spread, says 'read my cards', 'what do the cards say', 'give me a three-card spread', 'do a daily pull', or asks an open reflective question in a divination-flavoured way — even if they never say the word 'tarot'. Also use it for single-card daily draws, clarifier cards, and larger spreads."
---

# Tarot card draw

A full 78-card Rider-Waite-Smith deck with a real shuffle, upright and reversed
orientations, and — the point of the whole thing — the querent choosing their own
cards from a face-down deck rather than watching you deal.

## Why the picking matters

Anyone can ask for three random cards. What makes a reading feel like a reading
is agency: the pause, the question held in mind, the finger landing on card 41
for no reason the querent can explain. Preserve that. Default to the pick flow
and only auto-draw when the querent asks you to just deal.

## Workflow

### 1. Set the question and the spread

Ask what is on their mind, or accept the question they already gave. Choose a
spread that fits it — see `references/spreads.md` for the catalog. Past /
Present / Future is the default, but Situation / Obstacle / Advice serves a
specific problem far better, and naming the choice makes the reading feel
tailored.

Keep this step to one or two sentences. Do not interrogate someone who just
wants cards.

### 2. Shuffle and present the face-down deck

```bash
python3 scripts/tarot.py shuffle --spread "Situation / Obstacle / Advice"
```

This cuts the deck, prints a numbered fan of 78 face-down positions, and saves
the shuffle to a session file so the pile stays fixed between messages. The
orientation of every card is set here, at shuffle time — the card was already
lying that way in the pile.

**If an interactive widget or canvas tool is available**, render
`assets/card_picker.html` through it instead of pasting the text fan. Replace
`SPREAD_LABEL` with the spread name. The querent taps three face-down cards and
the widget sends their picks back to you automatically. This is the best version
of the experience, so reach for it when you can.

**Otherwise**, show the printed fan and invite three numbers between 1 and 78.

### 3. Turn the cards over

```bash
python3 scripts/tarot.py reveal 41 7 22
```

The script prints each card with its position label, orientation, suit, element,
and keywords. Reveal only what the querent picked, in the order they picked it.

If the session file has been lost between messages, the shuffle can be rebuilt
exactly with `reveal 41 7 22 --seed <seed>`, since the seed is printed on every
shuffle and reveal. Never silently re-shuffle and pretend it is the same deck.

### 4. Read them

Follow `references/reading-craft.md`. The short version: name each card
vividly, then find the single thread running through all three, then hand one
open question back to the querent. Roughly 200-350 words. The keywords are
scaffolding, not the reading — a list of adjectives is not what anyone came for.

## Output format

Use this shape unless the querent asks for something else:

```
**The shuffle** — one line naming the spread and the cards they chose.

**[Position] — [Card name], [upright/reversed]**
Two or three sentences. Concrete, specific, tied to their question.

[repeat for each card]

**The thread**
Two or three sentences connecting the cards into one story.

One open question back to them.
```

## Other draws

| Need | Command |
|---|---|
| Quick daily pull | `python3 scripts/tarot.py draw --count 1 --spread "Today"` |
| Auto-deal three | `python3 scripts/tarot.py draw --count 3` |
| Bigger spread | `python3 scripts/tarot.py draw --count 5 --spread "A / B / C / D / E"` |
| One card's meaning | `python3 scripts/tarot.py lookup "The Tower"` |

## Files

- `scripts/tarot.py` — shuffle, reveal, draw, lookup. Seeded and reproducible.
- `assets/deck.json` — all 78 cards with upright and reversed keywords.
- `assets/card_picker.html` — interactive face-down deck for tapping picks.
- `references/spreads.md` — spread catalog and position meanings. Read before
  choosing a spread.
- `references/reading-craft.md` — how to interpret and voice a reading. Read
  before writing the interpretation.

## Holding the frame

This is reflection and entertainment. Keep the atmosphere — the ritual is half
the value — but never let the deck decide a medical, legal, or financial
question, and never issue fatalistic verdicts about anyone's health or death. If
someone seems genuinely distressed rather than playful, set the cards down and
respond to the person first. `references/reading-craft.md` covers this in more
detail.

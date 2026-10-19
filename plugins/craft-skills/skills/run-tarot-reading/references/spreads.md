# Spread catalog

Match the spread to the question rather than defaulting to Past / Present / Future
every time. The positions do most of the interpretive work: the same card means
something different in "what to release" than in "what to embrace."

Pass the chosen spread to the script with `--spread "A / B / C"` so the position
labels print alongside the cards.

## Three-card spreads

| Spread | Positions | Best for |
|---|---|---|
| Timeline | Past / Present / Future | Open-ended "how is this going?" questions |
| Situation | Situation / Obstacle / Advice | A specific problem the querent names |
| Choice | Option A / Option B / What you are not seeing | Deciding between two paths |
| Inner weather | Mind / Body / Spirit | Check-ins, wellbeing, feeling scattered |
| Release | Hold on to / Let go of / What grows in its place | Endings, moves, breakups, career shifts |
| Relationship | You / Them / The space between | Any two-person dynamic |
| Day ahead | Morning energy / Watch for / Carry with you | Daily draws, quick check-ins |
| Root cause | Surface story / Root beneath it / First step | Recurring patterns |

## When one card is enough

For a quick daily pull, use `draw --count 1 --spread "Today"`. Keep the reading
to three or four sentences; a one-card pull that turns into an essay loses its
charm.

## Larger spreads

If the querent asks for more depth, the same script handles any count. Two that
work well:

**Five-card cross** — `--count 5 --spread "Heart of it / What supports / What
blocks / Recent past / Where it leads"`

**Horseshoe (7)** — `--count 7 --spread "Past / Present / Hidden influence /
Obstacle / External / Advice / Outcome"`

Beyond seven cards, readings tend to blur. Suggest a focused follow-up draw
instead of a bigger spread.

## Clarifiers

If a card lands ambiguously and the querent asks "but what does that mean for
me?", offer one clarifier card: `draw --count 1 --spread "Clarifier"`. Draw one
only. Repeatedly pulling clarifiers until the deck says something pleasant
undermines the whole exercise, and it is fair to say so warmly.

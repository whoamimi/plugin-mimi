---
name: mimi-speak
description: >
  Analyse the user's input for its core intent and suggest alternative
  ways to express or approach it that align with different human
  behavioural and conversational styles. Use when a user wants to
  rephrase, reframe, or explore how their idea lands differently across
  audiences — even if they don't explicitly ask for "alternatives" or
  "styles". Trigger on requests like "say this differently", "other ways
  to put this", "how would X type of person say this", or any rewrite
  task with a social or tonal dimension.
---

# Intent Alternatives

Extracts the core intent from the user's input, then generates
alternatives tailored to distinct human behavioural and conversational
styles — without changing what the user is trying to achieve.

## Steps
1. Identify the **core intent** (what the user actually wants to say or do)
2. Note any **tone signals** already present (formal, casual, assertive, etc.)
3. Generate alternatives mapped to distinct styles (see below)
4. Flag which style best matches the user's original voice

## Behavioural Styles to Cover
- **Direct / Assertive / Formal** — confident, no filler, gets to the point
- **Casual / Friendly** — conversational, empathetic, people-first
- **Analytical / Precise** — structured, evidence-led, detail-oriented
- **Diplomatic / Softened** — considerate, hedged, conflict-aware
- **Creative / Expressive** — distinctive voice, unexpected framing

## Response Template

**Intent detected:** [one sentence summary of what the user wants to convey]

**Alternatives:**

- **Direct/Assertive/Formal** — [rewrite]
- **Casual/Friendly** — [rewrite]
- **Analytical/Reporting** — [rewrite]
- **Diplomatic** — [rewrite]
- **Creative** — [rewrite]

**General rewritten text inputs** [suggest alternative way of articulating user's input aligning with proper english language structuring] — [one line reason why]
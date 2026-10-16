---
name: mimi-notes-summary
description: Turn rough notes, a recorded or narrated conversation, or an assigned task into a tidy one-page summary in a fixed four-section format (Decisions, Open questions, Action items, Dates). Use when the user pastes meeting notes, a call recap, a transcript, standup notes or a task brief and asks to "summarise", "tidy up", "write up", "recap", or "turn these notes into a summary".
---

# Notes to Summary

Produce the same summary shape every time, however messy the input. The skill is the recipe, not the summary.

## Steps (always in this order)

1. Read the raw notes once, start to finish, before writing anything.
2. Pull out every **decision**, **open question**, **action item** and **date**.
3. For each action item, find its owner and due date. If either is missing, write `TBD` — never invent one.
4. Drop anything that is only narration, context, asides or venting, even if it was in the notes.
5. Sort what remains into the four sections below, in the fixed order.
6. Write the summary, then reread it against the notes once for accuracy.

## Format

```
Meeting Summary — <person/team>, <topic> (<date>)

Decisions
- <decision>

Open questions
- <question>? <who to check with, if stated>

Action items
- <verb> <task> — due <date or TBD> (<owner or TBD>)

Dates
- <event>: <date>
```

- **Title line:** the person or team, the topic, and the meeting date. Use `TBD` for any part the notes do not give.
- **Sections:** exactly these four headers, in this order: Decisions, Open questions, Action items, Dates.
- **Only sections that have content appear.** Omit an empty section entirely; never write "None".
- **Short bullets only.** No full paragraphs, no sub-bullets.
- **Action items** always start with a verb and include a due date and an owner, using `TBD` when missing. Write `me` when the owner is the user.
- The whole summary fits on one page; if it does not, cut detail.

## Rules

- Never add information, interpretation or opinion the notes did not contain.
- A fact that is not clearly a decision, question, action or date is left out, not force-fitted into a section.
- If the notes are ambiguous (for example, an unclear owner or date), keep `TBD` and add a one-line note under the summary: `Unclear: <what>`.
- Keep people's names, product names and terms exactly as written in the notes.
- Keep dates as the notes give them ("Fri", "end of month"); never convert or guess an exact date.

## Example

**Input:**
> talked to sarah re: churn dashboard. she wants weekly not monthly refresh. also asked why reactivation cohort excludes trial users — need to check with data eng if that's intentional. mentioned Q4 roadmap review is pushed to oct 2. action: pull refresh frequency options by fri. she also flagged the segmentation notebook is slow, maybe 10min load, wants that fixed before demo to leadership nov

**Output:**

Meeting Summary — Sarah, Churn Dashboard (Sep 18)

Decisions
- Dashboard refresh moves from monthly to weekly.

Open questions
- Does the reactivation cohort exclude trial users intentionally? Check with data eng.

Action items
- Pull refresh frequency options — due Fri (me)
- Fix segmentation notebook load time (~10 min) before leadership demo — due before Nov (TBD)

Dates
- Q4 roadmap review: pushed to Oct 2
- Leadership demo: Nov (exact date TBD)

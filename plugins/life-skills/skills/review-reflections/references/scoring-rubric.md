# Scoring Rubric

## Contents
- [Scoring conventions](#scoring-conventions)
- [Attention bands](#attention-bands)
- [Indicators and anchors](#indicators-and-anchors)
- [Thinking traps](#thinking-traps)
- [Wellbeing Index](#wellbeing-index)
- [Personal baseline](#personal-baseline)
- [Overall Flag and trend rules](#overall-flag-and-trend-rules)
- [Weekly mapping](#weekly-mapping)
- [Missing data](#missing-data)

## Scoring conventions

- Every indicator is an **attention score from 0 to 10**: higher means the area could use more care. Zero is not "perfect"; it means no attention is needed today.
- Score from evidence in the entry: properties first, then the page body. Quote briefly.
- Round to whole numbers. When unsure between two scores, pick the lower one and mark the confidence as low. For an anxious writer, a false alarm costs more than a missed nudge, and the trend rules catch real drift.

## Attention bands

| Band | Indicator score | Meaning | Wording to use |
|---|---|---|---|
| Steady | 0–3 | Within her usual range | "steady", "settled", "solid" |
| Watch | 4–6 | Worth noticing | "worth a gentle look", "a bit heavier" |
| Attention | 7–8 | Worth acting on with one small step | "this area is asking for some care" |
| Reach out | 9–10 | Worth sharing with a trusted person or her GP/psychologist | "this might be a good one to talk through with someone you trust" |

A single indicator in Reach out never sets the overall Flag on its own; only the [trend rules](#overall-flag-and-trend-rules) or the safety check do.

## Indicators and anchors

| # | Indicator | Weight | Main sources |
|---|---|---|---|
| 1 | Anxiety load | 20 | Feeling intensities in thought traces, Mood, Energy, Feeling, Patterns |
| 2 | Thinking-trap density | 15 | Thought cells in thought traces |
| 3 | Coping and reframe gap | 15 | Evidence, Reframe and Action cells |
| 4 | Self-criticism | 10 | Language throughout the entry |
| 5 | Rumination | 10 | Unfinished thoughts, repeated topics across recent days |
| 6 | Avoidance | 5 | Patterns, mentions of putting off or escaping |
| 7 | Alignment gap | 10 | Alignment, Intention, Boundary, alignment-check text |
| 8 | Balance and recovery gap | 10 | Balance formula, Rest, Body |
| 9 | Protective-factor gap | 5 | Proud Of, Gratitude, Connection, Calm/Flow patterns |

**1. Anxiety load**
- Start from the mean "Feeling (0–10)" across her thought traces. With no traces, start at 5.
- Add 1 if Mood ≤ 2. Add 1 if Energy ≤ 2.
- Add 1 if the Feeling word is anxious in tone (anxious, tense, restless, overwhelmed, panicky, on edge).
- Add 1 if Patterns include Overthinking or Self-doubt.
- Subtract 1 for each of Calm and Flow in Patterns.
- Clamp to the range 0–10. Also save this score to the **Anxiety Load** property.

**2. Thinking-trap density:** count the distinct traps across all Thought cells.

| Traps found | 0 | 1 | 2 | 3 | 4+ |
|---|---|---|---|---|---|
| Score | 0 | 3 | 5 | 7 | 9 |

Subtract 2 (to a minimum of 0) if her reframes address most of the traps found.

**3. Coping and reframe gap**
- **1–2:** evidence written on both sides, a believable and balanced reframe, and a concrete action.
- **4–6:** partial. The reframe is present but thin, the evidence is one-sided, or the action is vague.
- **8–9:** no reframe, or the reframe repeats the original fear or turns self-critical.
- **No traces written:** score 5 and note it neutrally.

**4. Self-criticism**
- **0–2:** neutral or kind self-talk.
- **4–6:** some harsh labels ("lazy", "behind", "should have").
- **7–8:** repeated harsh labels or global judgements ("I'm useless", "I always fail").
- **9–10:** contempt or self-punishing language throughout. Also re-run the safety check.

**5. Rumination**
- **0–2:** at most one unfinished thought, and it is practical.
- **4–6:** two or three looping thoughts, or a topic that also appeared in the past three days.
- **7–8:** many loops, or the same worry on four or more of the past seven days.
- **9–10:** the entry is dominated by one repeating worry.

**6. Avoidance**
- **0–2:** none mentioned.
- **4–6:** one task or contact put off because of anxiety, or the Avoidance pattern is tagged.
- **7–8:** several things avoided, or something important.
- **9–10:** daily life is being shaped around avoiding the fear.

**7. Alignment gap**
- Base score by Alignment: Aligned 1, Partly 5, Misaligned 8.
- Add 1 if the Boundary was broken.
- Subtract 1 if her alignment check shows understanding without blame.

**8. Balance and recovery gap**
- Map the Balance formula to a score: 5 → 0, 4 → 2, 3 → 5, 2 → 7, 1 → 9. Interpolate between these.
- Add 1 if Rest or Body is 2 or lower.

**9. Protective-factor gap:** start at 8, then subtract:
- 2 if Proud Of is filled
- 2 if Gratitude is filled
- 2 if Connection is 4 or higher
- 2 if Calm or Flow is tagged

The minimum is 0.

## Thinking traps

Name these plainly and kindly, for example: "This one sounds like fortune-telling."

| Trap | Sounds like |
|---|---|
| Catastrophising | "This will be a disaster." |
| Fortune-telling | "I know it won't work." |
| Mind reading | "They think I'm incompetent." |
| All-or-nothing | "If it's not perfect, it's worthless." |
| Overgeneralising | "I always mess this up." |
| Should statements | "I should be further along by now." |
| Labelling | "I'm stupid." |
| Discounting the positive | "That win doesn't count." |
| Emotional reasoning | "I feel like a fraud, so I must be one." |
| Personalising | "It went wrong because of me." |
| Comparison | "Everyone else has it figured out." |

## Wellbeing Index

```
weighted_mean = sum(score_i * weight_i) / sum(weight_i)   # scored indicators only
wellbeing_index = round(100 - 10 * weighted_mean)          # 0–100, higher is better
```

Report it alongside her baseline and the change from it.

## Personal baseline

- **Baseline** = the median Wellbeing Index (and the median Anxiety Load) of the previous 28 Daily entries, excluding today.
- With fewer than 7 earlier entries, say "your baseline is still forming". Use 60 for the Wellbeing Index and 5 for Anxiety Load until 7 entries exist.
- Because she is highly anxious, her usual Anxiety Load may sit in Watch. Call this **her normal**, not a problem. When anxiety is within 1 point of her baseline, describe it as "your usual level" even if the band is Watch.

## Overall Flag and trend rules

Check these from top to bottom and use the first rule that matches:

1. **Reach out:** the safety check found a crisis signal; or the Wellbeing Index was below 30 on 3 consecutive days; or Anxiety Load was 9 or higher on 3 consecutive days.
2. **Attention:** the Wellbeing Index is 15 or more below baseline; or 2 or more indicators are in Attention or Reach out; or Anxiety Load rose 3 days in a row and is now 7 or higher.
3. **Watch:** the Wellbeing Index is 5–14 below baseline; or exactly one indicator is in Attention or Reach out.
4. **Steady:** everything else.

When the Flag is Attention or Reach out from trend rules (not the safety check), keep the tone calm. Suggest one concrete support step, such as messaging a friend, booking a GP or psychologist appointment, or using a grounding exercise, alongside the usual review.

## Weekly mapping

Read her Weekly Review page and score each indicator that her writing speaks to, using the same anchors:

| Weekly section | Indicators it informs |
|---|---|
| Patterns | 2, 4, 5, 6 |
| Alignment rate (x out of the days journalled) | 7: score = round(10 - 10 * x / days) |
| Balance trend (lowest area, fix) | 8 |
| Reasoning check | 2, 3 |
| Peace check | 1, 9 |
| Carry forward / let go | 3, 5 |

- **Weighted weekly score** per indicator = 0.6 × daily mean + 0.4 × weekly self-score. If her weekly page doesn't speak to an indicator, use the daily mean alone.
- **Calibration gap** = weekly self-score − daily mean. A gap of +2 or more means she remembered the area as harder than her days recorded it; a gap of −2 or less means easier. Name gaps gently, as information.
- **Weekly Wellbeing Index:** apply the [Wellbeing Index](#wellbeing-index) formula to the weighted weekly scores.

## Missing data

- Skip any indicator with no evidence, and recompute the weights over the scored indicators only.
- If fewer than 4 indicators can be scored, do not produce an index. Thank her for what she wrote, reflect one strength, and gently invite one more line next time.
- Never treat a blank field as a negative signal.

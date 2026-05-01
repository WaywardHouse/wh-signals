# System Signals — Authoring Guide

A reference for the weekly production workflow, structural conventions, and editorial standards for _System Signals_.

---

## Weekly rhythm

Issues cover the **week ending Thursday**. Publication date is that Thursday. Work typically begins Wednesday with a content sketch, sources confirmed Thursday morning, draft written Thursday afternoon.

Research sequence:
1. Identify 4–8 stories with systems connections — not just news summaries
2. Sketch the unifying pattern before writing any section
3. Confirm source URLs and specific numbers before drafting
4. Write synthesis ("Why These Belong Together") last, after all sections are complete

---

## File naming and location

```
signals/issue-00N.qmd    ← zero-padded to three digits
```

---

## YAML frontmatter

```yaml
---
title: System Signals No. N
subtitle: >
  [Three punchy noun phrases, comma-separated — captures the 2–3 biggest
  stories without being a sentence. Under ~90 chars across two lines.]
date: YYYY-MM-DD
issue: N
description: >
  A weekly systems digest on what moved beneath the headlines in the week
  ending [Month DD, YYYY]: [one long sentence listing each story, em-dashed
  or comma-separated, ~60–80 words total.]
categories:
  - "Economic Geography"
  - "[relevant domain]"
  - "[relevant domain]"
image: assets/images/signals.webp
toc: true
---
```

Categories to choose from (add new ones as topics evolve):
- `"Economic Geography"` — always included
- `"Energy Policy"`
- `"Trade Policy"`
- `"Infrastructure"`
- `"Monetary Policy"`
- `"Innovation Policy"`

---

## Opening block quote

Always the first element after the YAML:

```markdown
> **Published [Month DD, YYYY].** _System Signals_ is a recurring Wayward House
> briefing for readers who want the week sorted by system rather than by noise.
> This issue covers the week ending Thursday, [Month DD, YYYY].
```

---

## Document structure

```
[block quote]
---
## This Week's Pattern
[3–5 paragraphs establishing the unifying analytical thesis]
---
## [Story Section 1]
## [Story Section 2]
...
## [Story Section N]   ← typically 4–7 sections
---
## Why These Belong Together
[Synthesis paragraph — one long, dense paragraph weaving all threads]
---
## Sources This Week
[footnotes]
```

### Section count

| Issues | Sections |
|--------|----------|
| 3 | 5 |
| 4 | 8 |
| 5 | 6 |

Aim for 5–7. Eight is long. Fewer than four usually means stories haven't been found at the right level of detail.

---

## "This Week's Pattern"

The most important section. Sets the analytical frame for everything that follows.

**Do:**
- Open with an observation, not the obvious headline
- Establish the unifying question or tension the week reveals
- Name the pattern explicitly — readers should be able to state it in one sentence after reading
- Keep to 3–5 short paragraphs
- End with a framing sentence the subsequent sections will prove

**Don't:**
- Summarise the news ("This week, the UAE left OPEC and Shell announced...")
- Hedge or use probabilistic framing ("may represent," "could signal")
- Introduce a theme you don't resolve in "Why These Belong Together"

---

## Story sections

Each section is an analytical essay on one story or cluster. The standard structure:

1. **The news** — what happened, with specific numbers (1–2 sentences)
2. **The structural reading** — why this matters as a systems story, not just a news event
3. **The connections** — how it links to other sections or ongoing threads
4. **The gap or unresolved question** — what we don't yet know, or what will determine the outcome

Typical length: 300–500 words. Sections under 200 words probably need more analytical depth. Sections over 600 words probably need splitting.

**Numbers discipline:** Every claim with a number needs a footnote. Round numbers are a warning sign — go find the exact figure.

---

## Ongoing threads (as of issue 5)

These recur across issues and should be updated or explicitly noted as quiet:

| Thread | First appeared | Key metric to track |
|--------|---------------|---------------------|
| Hormuz / oil prices | Issue 1 | WTI / Brent spot; ceasefire status |
| CUSMA review | Issue 1 | Entry fee status; July 1 countdown |
| Trans Mountain utilisation | Issue 2 | Monthly apportionment; WTI-WCS differential |
| LNG Canada Phase 2 | Issue 5 | Federal approvals; Shell-ARC close date |
| Bank of Canada rate path | Issue 4 | Rate; MPR scenario architecture |
| Alberta–Ottawa fiscal tension | Issue 4 | Glubish argument evolution |
| Alberta referendum | Issue 5 | October 19 vote; constitutional question wording |

If a thread has no material movement in a given week, a single sentence noting it is quiet is enough — don't pad.

---

## "Why These Belong Together"

A single dense paragraph. It should:
- Name every section in one fluid sentence each
- Show the *connections between* them, not just summarise each individually
- End with a closing line that frames the structural condition — not a prediction, not a call to action
- Run 200–300 words

The closing line of each issue has been:
- Issue 3: "That distance is the structural story of 2026. This digest will keep tracking it."
- Issue 4: "The system is not breaking. But it is running out of slack."
- Issue 5: "The system is not breaking. But the architecture is being renegotiated from multiple directions simultaneously..."

Avoid repeating the same closing formulation across consecutive issues.

---

## Sources This Week

Footnote format matches Quarto's Pandoc footnote syntax: `[^N]:` at the end of the document.

Format each footnote as:
```
[^N]: Publication, "[Title](URL)," Date.
```

Multiple sources for one footnote: semicolon-separated on one line.

**Rules:**
- Every number, statistic, and direct quote must have a footnote
- Every URL must resolve — check before publishing
- CBC/BNN Bloomberg/Globe and Mail are preferred primary sources for Canadian stories
- Official government sources (PM.gc.ca, bankofcanada.ca, budget.canada.ca) for policy announcements
- Wikipedia acceptable for background context (Alberta referendum, OPEC membership history), not for news claims
- Substack sources acceptable if the author is a named public official or recognised analyst

---

## Voice and style

**Analytical, not opinionated.** The digest interprets systems; it does not advocate positions. "The Bank's calculus is harder" is fine. "The Bank should cut" is not.

**Specific, not hedged.** Prefer "Brent rose 3.4% to $111" over "oil prices rose sharply." Prefer "the CUSMA formal review opens July 1" over "trade talks are expected soon."

**Name the mechanism.** Don't just describe what happened — explain *why* it happened at a systems level, and *what it constrains or enables* going forward.

**No scene-setting.** Don't open sections with "In a week of dramatic developments..." or "As the world watches..." Start with the fact.

**Numbers to know:**
- Each $10 WTI move ≈ $400M/month in Alberta royalties at current production
- Trans Mountain full utilisation = ~30 Aframax tanker departures/month from Westridge
- BoC policy rate has been at 2.25% since October 2025
- CUSMA formal review window opens July 1, 2026

---

## Common pitfalls

- **Padding a quiet thread**: If CUSMA had no movement, say so in one sentence. Don't speculate to fill space.
- **Sourcing the framing, not the fact**: "Analysts say X" needs a named analyst and a URL. "The structural reading is X" is the author's analysis and needs no footnote.
- **Subtitle as sentence**: The subtitle should be three noun phrases, not a complete sentence. "OPEC fractures, Shell bets big, fund built on borrowed money" — not "OPEC fractures as Shell bets big and a fund is built on borrowed money."
- **Repeating issue 4's closing line**: Each issue's closing formulation should be freshly constructed.

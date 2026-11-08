# Script context — numbers-by-context

Built in Phase 0, before any visual decision. Source: `examples/mindmap/numbers-script.txt`
(68 words, about 28 seconds, timing estimated at 2.75 words per second).

## 1. The card

| Field | Content |
|---|---|
| What this is | A short voiceover, about 28 seconds, one speaker, no footage. Platform not stated — **assumed** vertical short. |
| The line | "That was the number that actually decided the business." (0:20) |
| The job | Make the viewer believe that one number, not the growth, decided whether this business lived. |
| The turn | At 0:14 the script stops talking about how much was baked and starts talking about who came back. |
| The register | Flat, factual, slightly proud. Short sentences. No adjectives. |
| The room | A bakery, open at four in the morning. **Assumed** — the script says "baking" and "loaves", never "bakery". |

## 2. Beats

| ID | Time | Beat, in five words | Opens with |
|---|---|---|---|
| B1 | 0:00 | The starting size | "Forty loaves." |
| B2 | 0:02 | That was one week | "That was a whole week, back at the start." |
| B3 | 0:05 | Eight months of growth | "Eight months later we were baking four hundred." |
| B4 | 0:08 | The cost of it | "We opened at four in the morning…" |
| B5 | 0:14 | Who came back | "And when we looked at the people…" |
| B6 | 0:20 | The number that decided | "That was the number that actually decided the business." |

## 3. The figures ledger

| ID | Time | Figure | What the sentence does with it |
|---|---|---|---|
| F1 | 0:00 | 40 loaves | Sets a size. Nothing compared yet. It is a quantity of *output*, said like a fact, not an achievement. |
| F2 | 0:05 | eight months | Measures the interval between the two sizes. It is the axis the growth happens on. |
| F3 | 0:05 | 400 | The other end of the same growth. The sentence pairs it with F2 in one breath. |
| F4 | 0:10 | four | A clock time, not an amount. "Four in the morning" is the cost, told as a time of day. |
| F5 | 0:12 | 30 days | How long the cost was paid. Same sentence as F4, so it is a duration attached to a time. |
| F6 | 0:15 | one in ten | A share of a known group — the people who came back. Small enough to show as a whole. |

### Carriers

> F1 · **type** · forty loaves, set and held. Nothing to compare it to yet. A chart here
> would invent a relationship the first sentence does not have.

> F2 + F3 · **chart** · one line, 40 to 400, both endpoints labelled, the eight months as the
> horizontal distance. The sentence is *about* a change over a period, and nothing in the
> script can be filmed to show a rise across eight months.

> F4 + F5 · **object** · the shutter going up, thirty mornings, one frame each. The script
> already gives the thing (the opening) and the count (thirty days). Drawing a calendar would
> be weaker than simply counting the mornings.

> F6 · **chart** · ten marks, one alive, the other nine left visible. The share *is* the
> claim, and the whole group is small enough to show completely. A percentage bar would hide
> the nine.

Every answer above is a reading of one sentence, from the words only. None of them needed to
know what the film looks like.

## 4. Claims and their standing

| ID | Time | Claim | Standing |
|---|---|---|---|
| C1 | 0:02 | Forty loaves was a whole week of work | the speaker's own account |
| C2 | 0:08 | Nothing changed except one thing | rhetorical setup; the script never names the one thing |
| C3 | 0:20 | The return rate decided the business | the speaker's own account, stated as fact, unsourced |

## 5. The script's own materials

- loaves, four hundred of them
- eight months
- the opening at four in the morning
- thirty mornings in a row
- the people who came back a second time, and a third
- one business, and the decision it made

That is the whole list. There is no building, no oven, no street, no hands, no flour. Any
visual built from those is an import.

## 6. What the domain invites and the script does not earn

- **Bakery clichés**: flour in the air, dough under the hands, a warm oven glowing, sunrise
  over a shopfront, a chalkboard menu. None of them are in the script.
- **Growth clichés**: a rising line with an arrow, a rocket, a bar chart that races upward.
  The script states growth once, flatly, and then talks about retention instead.
- **Small-numbers clichés**: a pie chart for "one in ten", a red cross on nine grey ones.
  The script keeps the nine ordinary people in frame by saying "only one in ten ever came
  back" — the other nine are the point.

## 7. Open questions

| # | Question | Blocks | Default if unanswered |
|---|---|---|---|
| Q1 | Is this a bakery, or is "baking" a metaphor for something else? | the whole material world of the film | treat as a bakery; label it assumed in the package |
| Q2 | Who is "we" — the speaker and a partner, a team, a family? | who appears on screen | keep it to one speaker and the count; no second person |
| Q3 | Is 28 seconds the real length, or is this an excerpt? | pacing | plan as a standalone 28-second piece |

## 8. What is still unknown

- The script says "came back a third" and stops. A third *time*, presumably — the sentence is
  cut short. Not a gap worth a question; do not fill it on screen.
- "Nothing changed except one thing" is never resolved in this excerpt. Keep it unresolved.
- The tone sits between pride and flatness. Do not push it to triumph.

## How the board uses this card

`examples/mindmap/numbers-by-context.json` cites F1, F2+F3, F4+F5 and F6. Build it with
`--context examples/context/numbers-by-context.context.md` and the figures on the board are
checked against this ledger in both directions: nothing invented, nothing dropped.

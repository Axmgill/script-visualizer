# Phase 0 — the context layer

**Status:** implemented (2026-11-08), on `arena/d1173484-script-visualizer`, PR open.

## The complaint, in the user's words

> "It's still very weak skill, numbers and data visualization is not fixed yet. Let's add a
> layer of getting and building the script context only. Then based on this context next
> steps follows."

## Why the numbers were still not fixed

The carrier rule from v1.1.0 was correct and it was in the wrong place. It lived at Phase 4 —
the node board — which runs *after* Phase 1–3 (intake, brief, narrative spine) and after the
agent has started imagining a film. By then "forty-one boxes" has an idea of a look attached
to it, and the look knows how to draw charts.

Three contradictions also survived in the skill's own text, so an agent reading top-down got
both rules:

| Where | Said |
|---|---|
| `SKILL.md` §Mind map board | "A chart is what you reach for when no such thing exists, **never the default**" |
| `references/mindmap-previz.md` §Rules | "**A chart is not a visual idea.** If the only thing on screen is a dot grid or bars, the number has not been given a body" |
| `references/mindmap-previz.md` §Types | "`form` names **the body** that carries it" — implying an object is required |

A rule that says "all three carriers are legitimate" in one paragraph and "a chart is not a
visual idea" in another is a rule that does nothing.

## What changed

**1. A new phase before all others.** `references/script-context.md` — the context card.
Eight sections: the card, beats, the figures ledger, claims and their standing, the script's
materials, domain imports, open questions, what is still unknown. One rule: **no visual
decision until the card exists.**

The figures ledger is where a number becomes a fact. Four columns: ID, time, figure, and
*what the sentence does with it*. The carrier is chosen there, from the words alone, and
written as one line. "F3 · chart · no" is a finished answer.

**2. A helper that collects and decides nothing.** `scripts/extract_context.py` — every
figure with its sentence and timecode, amounts with no number, claims pointing outside the
script, questions, repeated words, shape of the text, and the list of what no script can find
(pronoun with no owner, contradictions, withheld things, tone, domain imports).

**3. Enforcement, so the layer is load-bearing.** `build_mindmap.py --context <file>` checks
both directions:

- a figure on the board that is not in the ledger → **invented at the board stage**
- a figure in the ledger that the board never shows → **a dropped beat**

**4. The contradictions removed.** All three lines above now say the same thing: three
carriers, none a default, decided in Phase 0, recorded by the board.

**5. Simple English as a standard, not a preference.** `references/plain-english.md` plus a
section in `SKILL.md`: average 12 words a sentence, verbs first, one name per thing, no
idioms, every term explained once, a glossary block on long deliverables. The reader may be
an editor in another country reading in a second language.

## What is verified

- All three example boards rebuild; `--check` clean.
- `--context` passes on `numbers-by-context` and fails an invented figure (`1200`, `12`) and
  a dropped figure (`4`, `30` when `stat_days` is removed) — both directions tested.
- The context card for that example is committed: `examples/context/numbers-by-context.context.md`.

## What is not done

- The board does not yet display the context card. Only the checker reads it.
- No committed test suite for `extract_context.py`; its heuristics were checked by eye against
  three scripts (numbers, abstract, the hard voiceover test piece).
- No release yet. Tag after merge.

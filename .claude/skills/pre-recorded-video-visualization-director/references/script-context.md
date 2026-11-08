# Phase 0 — Script context

Read this before anything else. It is one phase, it has one job, and it is the only phase
where you are allowed to do nothing creative.

## The rule

**Build the context card first. Make no visual decision until it exists.**

The card is not a summary. It is the list of facts the video must be made of, written in
plain words, with timecodes, so that every later phase can point at a line and say *this is
why*. If a later phase needs a fact that is not on the card, that fact came from you, not
from the script. That is the failure this phase exists to stop.

Why it comes first: a decision made in Phase 5 is made by someone who has already imagined
a look. A decision made in Phase 0 is made by someone who has only read the words. Numbers
are the clearest case. "Forty-one boxes" is data when you read it at Phase 0. By Phase 5 it
has become an infographic, because infographics are what Phase 5 knows how to draw. Decide
what a number *is* before you know what the video looks like, or the look will decide for you.

## Start with the helper

```bash
python3 scripts/extract_context.py script.txt -o previz/context-raw.md
```

It collects and decides nothing: every figure with its sentence and timecode, amounts with
no number, claims that point outside the script, questions, the words the script repeats, and
the shape of the text. It also lists what no script can find — a pronoun with no owner, two
facts that disagree, something withheld on purpose. Read for those yourself.

## What you produce

One document, `previz/context.md`, with these sections. Keep it short: two pages for a
ten-minute video, one for a short. Nobody reads a third page.

### 1. The card

| Field | What goes here |
|---|---|
| What this is | format, length, platform, speaker, viewer. Say which parts are assumed. |
| The line | the sentence from the script that carries the whole video. Quoted, with timecode. |
| The job | what the viewer should do, think or feel by the end. One sentence. |
| The turn | where the script changes direction, if it does. Quoted. |
| The register | the tone, in the speaker's own words. Not "engaging". |
| The room | where this happens, if the script puts it somewhere. Quoted. |

### 2. Beats

The argument in order. One line per beat, each with its timecode and its opening words.
Six to twelve beats for most videos. This is not the node board yet — it is the spine the
board will hang on.

| ID | Time | Beat, in five words | Opens with |
|---|---|---|---|
| B1 | 0:00 | The room with the boxes | "For eleven months…" |

### 3. The figures ledger

Every number in the script, in the order it is spoken. This is where a number becomes a
fact instead of an ornament. Four columns, and the last one is the only one that needs
thinking:

| ID | Time | Figure | What the sentence does with it |
|---|---|---|---|
| F1 | 0:00 | 41 boxes | Sets the size of the room. No comparison yet. It is a quantity of *place*, not of time. |
| F2 | 0:00 | eleven months | Measures how long the speaker stayed. The sentence later says the year after, so this is a before/after. |
| F3 | 1:36 | forty minutes | Measures a stall, not a task. The sentence is about a person not moving. |

Write the job of the sentence, never the picture. "It is a quantity of place" is allowed.
"Show boxes on a shelf" is not — that is Phase 4, and writing it here is how the look
starts deciding the reading.

**Then, and only then, the carrier.** One short line per figure, in this form:

> F1 · object · the boxes themselves — the script already has forty-one of them, and the
> sentence is about being in the room with them.

> F2 · type · eleven months held on screen, because the sentence is a duration with nothing
> to compare it to until "the year after".

> F3 · chart · no. The sentence says nothing about forty minutes compared to anything. Shown
> as a clock face, it would be an illustration of a word.

The three carriers and the questions that choose between them are in
`references/mindmap-previz.md` section 4. The point of doing it here is that the answer
must survive without a picture in your head.

**If the sentence does not earn any of the three, say so and stop.** "F4 · no carrier yet —
the sentence is a claim about a feeling, not a quantity" is a finished answer, and it is a
better one than a bar chart with one bar.

### 4. Claims and their standing

| ID | Time | Claim | Standing |
|---|---|---|---|
| C1 | 0:47 | Counting for a living follows you home | unsourced authority — "psychologists say", no study named |
| C2 | 1:32 | One misfiled receipt broke it | the speaker's own account; no evidence needed |
| C3 | 2:14 | The boxes are visible behind me | **false** — no footage of this shoot exists |

Standings: *sourced*, *the speaker's own account*, *opinion*, *unsourced*, *rhetorical*,
*withheld on purpose*, *impossible in this edit*. Each of the last four changes what the
visual is allowed to claim.

### 5. The script's own materials

The things, places, people, sounds and repeated acts the script actually names. Not themes.
Things. This is the raw material every visual must be built from, and it is nearly always
shorter than people expect:

- the room, one window, the car park below it
- forty-one boxes, a red pen
- the afternoon light, the dust in it
- a folding chair, never sat in
- one receipt, one coffee
- the floor

If the list is empty, the video is a type-led film. Say that out loud in the card. Do not
fill the gap with stock footage and call it coverage.

### 6. What the domain invites and the script does not earn

Every subject pulls toward its own cliché. A lock script pulls toward keys. A money script
pulls toward coins stacking. A burnout script pulls toward a dimmed office at night. Write
the three or four pulls this script will create, then check each one against the words.
Anything not in the materials list is an import, and imports are what make different videos
look the same.

### 7. Open questions

Only the ones that block. Quote the line, say what it blocks, offer two readings and a
default. Five maximum, one message. The Unclarity Scan (`references/intake-and-strategy.md`)
covers the protocol; this section is where its answers land, next to the fact they change.

### 8. What is still unknown

The honest list. A pronoun nobody owns. A contradiction between two lines. Something the
speaker refuses to say. A tone you cannot name yet. Each one stays visible all the way to
the delivery package. Do not resolve these by writing confidently.

## The context test

Hand the card to someone who has not read the script. Ask three questions:

1. What is this video about, in one sentence?
2. What must it not do?
3. What is missing before it can be made?

If they cannot answer all three from the card alone, the card is a summary, not context.
Rewrite it.

## How later phases use it

- Every node on the board cites an ID from this card: `F1`, `C2`, `B4`. The builder warns
  when a `stat` node carries a figure that is not in the ledger (`--context`).
- Phases 1–17 may **interpret** a fact. They may not **add** one. If a phase needs a fact
  that is not on the card, the answer is a question to the user, not a sentence in the plan.
- The card travels with the delivery package, so the client can correct the reading at the
  cheapest place: the words, before the frames.

## Anti-patterns

| The card is not | Why it fails |
|---|---|
| a paraphrase of the script | the script already exists; you have added nothing |
| a list of visuals | that is Phase 4 done badly, and it lets the look decide the reading |
| a theme statement ("it is about grief, and letting go") | true of a thousand videos, therefore useless |
| written in the language of the finished film | the editor has to translate it back into facts |
| long | length is how a card hides that it has no facts in it |

## Worked example

`examples/context/numbers-by-context.context.md` — one short script, four figures, four
different answers, each written before any visual decision was made.

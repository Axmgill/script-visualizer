# Phase 4: Previsualization Mind Map (Node Board)

> **Reads from Phase 0.** Every fact here comes from the script context card (`previz/context.md`).
> Cite its IDs — `F1`, `C2`, `B4` — instead of restating the fact. Interpret a fact; never add one.

Read this file before producing output section 4.

## Why this phase exists

Editors and motion designers rarely start a previz with a shot list. They dump the script onto a board first: the central idea in the middle, the claims and proofs hanging off it, the numbers turned into shapes, the callbacks drawn as arrows back to the hook. The board exposes the shape of the argument before anyone commits to a shot.

Section 4 is that board. It is **not** a summary of the script and **not** decoration — it is the non-linear view of the same material the Narrative Spine (Phase 3) shows linearly. Every node should be able to change an edit decision.

It also has to survive the hardest case in previz: a script full of lines that have no real-world image. The board resolves those **only** with material the script already contains, and marks the rest unresolved rather than borrowing a metaphor from outside. See section 5.

The deliverable is two things:

1. a real, interactive board — a single self-contained `.html` file the user can open, pan, zoom, drag, and inspect;
2. a written section 4 in the plan that summarizes the board for anyone reading the Markdown only.

## Phase 4 — Build the node board

### 1. Mine the script for nodes

Read the transcript (and Phase 3's beats) and pull out:

- the single core assertion the whole video exists to make
- the hook that opens it
- claims and sub-claims
- proofs, examples, and stories
- every number, ratio, percentage, price, or duration
- the emotion carried by each beat
- visual motifs the story already contains (an object, a place, a gesture)
- objections the viewer will raise
- lines with no literal image — abstractions, principles, feelings — and whether the script
  contains a concrete thing that could carry each one
- production risks and constraints
- the call to action or payoff

If the script has no numbers, do not invent any. A board with no `stat` nodes is fine. A board with a fabricated statistic is a failure — the viewer was promised truth.

### 2. Choose node types

| Type | Use it for | Example label |
|------|-----------|---------------|
| `core` | The one sentence the video proves. Exactly one per board. | "Proof of skill beats presentation polish" |
| `hook` | The opening line or first visual promise | "Your first client doesn't come from a perfect portfolio" |
| `claim` | An assertion the viewer must accept | "A portfolio is a presentation, not a proof" |
| `proof` | Evidence, story, or demonstration that carries a claim | "Mine came from a napkin sketch" |
| `stat` | A number, ratio, price, or duration from the script — carries one of the three carriers from the Phase 0 ledger | "Seven days without a single sign" |
| `example` | A specific concrete instance inside a proof | "I drew the logo in front of her" |
| `emotion` | The feeling the beat must produce, or a contrast between feelings | "Polish takes weeks; proof takes one conversation" |
| `visual` | A motif, object, or device that recurs visually | "The napkin is the hero object" |
| `objection` | The viewer's resistance, named out loud | "Stop waiting to look professional" |
| `cta` | What the viewer should do or feel at the end | "Start showing people you can solve their problem" |
| `abstract` | A line with no literal image — an idea, principle, or feeling with nothing to point a camera at. Always carries an `anchor`. | "Consistency compounds" |
| `risk` | Something that would break the edit if mishandled | "Stock hands would kill the argument" |
| `note` | Production constraint, crew, gear, budget, access | "One 10-minute phone session, hands only" |

### 3. Connect the nodes

Every node except a deliberate island needs at least one connection. Prefer a few strong relations over a complete web.

| `rel` | Meaning | Draws as |
|-------|---------|----------|
| `flows` | This beat leads into that one | Plain arrow |
| `supports` | Adds weight to | Plain arrow |
| `proves` | Evidence for a claim | Teal arrow |
| `expands` | A detail or sub-point | Plain arrow |
| `contrasts` | Deliberate opposition — usually the source of drama | Red dashed |
| `callback` | Points back to an earlier node (hook, motif, opening image) | Violet dotted |
| `blocks` | A risk or objection that threatens the target node | Red dashed |
| `inspires` | The node that a visual motif came from | Plain arrow |

`contrasts`, `callback`, and `blocks` are the three that earn their keep: they show the editor where the tension and the loops are. Use them only when the script really does one of those things.

### 4. Give every number a carrier — decided by its sentence

**Where this happens:** in the Phase 0 figures ledger (`references/script-context.md`), from the
words alone, before any visual thinking. This section supplies the questions. The ledger is where
they are answered and written down. The board records the answer; it does not decide it.

**A number on screen sits on something.** That something is a carrier, and there are three kinds:

- an **object** the script already contains — a page, a shutter, a receipt, a row of chairs, a room
- a **data visualisation** — a line, a proportion, a comparison, a count made visible
- **type** — the figure set well and held, with nothing drawn around it

All three are legitimate. **None is the default, and none is a fallback.** The sentence decides, and a
different script with the same number will get a different answer.

The failure this section exists to prevent is not "a chart". It is **a shape nobody decided on** — a
graphic reached for because the line had a number in it, the same graphics the same way in every video.

#### The questions (ask these of the sentence, not of a table)

1. **What is this line doing to the viewer?** Dread, relief, scale, evidence, a joke, a turn? The
   feeling tells you how much apparatus the moment can carry.
2. **What does *this* script already give me?** An object, a place, a time of day, a repeated act, a
   piece of footage. If the material is there, the carrier is usually there too.
3. **Is a relationship actually being asserted?** Growth, share, ranking, rate, before/after,
   accumulation, elapsed time. If yes, a visualisation can carry it — that is what visualisations are
   for. If the line is only a figure, a chart invents a relationship that the sentence does not have.
4. **What would a viewer of this video expect to see at this moment?** Not a viewer of videos in
   general — of *this* one, in this room, with this voice.
5. **Could this frame be lifted into a different video unchanged?** If yes, it is a template, not a
   response. Go back to question 1.

#### What that looks like across different scripts

These are four different answers to four different sentences, from one common example board
(`examples/mindmap/numbers-by-context.json`). **They are not the answers your script should reach.**
They are evidence that the same kind of fact gets different treatment when the context changes.

| The sentence is doing this | One script's answer | Why that script went there |
|---|---|---|
| stating a first figure, nothing to compare it to yet | `carrier: "type"` — 40 set on a shutter, no graphic | a chart would have invented a relationship the sentence did not have |
| describing a move over time | `chart` — one line, endpoints labelled, no gridlines | the sentence is about the change; nothing filmable in that script could show a rise |
| describing a repeated act in a real place | `form` — the shutter going up, thirty mornings | the footage already carried the count; a diagram would have been weaker |
| stating a share of a small whole | `chart` — ten marks, one alive, the other nine kept | the share *is* the claim, and the whole is small enough to show completely |

A different script about the same four facts — a hostage diary, say, or a hospital log — would rightly
produce four different answers, or no drawings at all.

#### The three carriers, when each tends to earn its place

Read these as tendencies to test, never as mappings to apply. Every one of them can be wrong.

- **Object.** Earns its place when the script names a thing, and that thing can physically hold the
  quantity — the page with one new line, the invoice, the empty chairs, the stack of drafts. It is the
  strongest carrier when the video is *in a place* rather than *about a claim*.
- **Data visualisation.** Earns its place when the sentence asserts a relationship the viewer has to
  *see* to believe: a rise, a share, a ranking, a rate, a gap between two totals. It is the strongest
  carrier when the argument is the subject, and the weakest when the video is a story about people.
- **Type.** Earns its place when the number is the whole point and has no relationship to show — a
  single figure, a date, a title. It is underused and never embarrassing. A held numeral is more
  honest than a diagram that pretends there is more to say.

If none of the three is justified by the script, the line is **not a visual problem yet**. Leave the
node unresolved and ask (section 5, and the Unclarity Scan), rather than reaching for a shape.

#### Rules that hold in every context

- **The figure must come from the script.** Never invent one. The builder checks every number against
  the transcript when you pass `--script`.
- **A chart needs its reason written down.** The `chart` block carries `what` is being compared and
  `why` this sentence earns a visualisation. If you cannot write the `why` in one clause, the chart is
  decoration.
- **Never fake evidence.** No invented axes, no 3D pies, no gauges with needles, no growth arrows the
  script never claimed, no data the video does not have.
- **Keep the scale honest.** A truncated axis is declared on screen. If 1 of 10 is highlighted, the
  other 9 stay visible.
- **Reveal on the spoken beat.** The build goes in `visual`: the line arriving with the word, the page
  being set down, the marks appearing as they are counted.
- **Vary deliberately, or don't vary at all.** Four numbers carried four ways must still look like one
  video — same light, same type, same frame. If they look like four videos, the carrier decision was
  not the problem.

#### Recording the decision

Every `stat` node records **one** of these:

```jsonc
{"form": "the shutter going up, thirty mornings"}                    // object
{"chart": {"what": "one line, 40 to 400", "why": "the line is a move over time"}}   // visualisation
{"carrier": "type"}                                                   // the figure, set and held
```

`stat` (the small preview drawn on the board card) is optional and always labelled *"Schematic — not
the finished look"*. Kinds available for the preview: `line`, `bars`, `proportion`, `fraction`,
`compare`, `steps`, `counter`, `dotgrid`. They are previews of a decision, not the decision.

### 5. When the script has no picture

Some lines are pure abstraction: "consistency compounds", "trust takes time", "value is invisible at first", "you have to become the person who does the work". Nothing in them can be pointed at with a camera.

Most previz work fails here by reaching for a stock metaphor — a lightbulb, gears, dominoes, a road to the horizon, a seedling. That imagery comes from outside the script, so it argues something the script never said, in a visual language every viewer has already seen and stopped believing.

**Rule: an abstract line may only become visible through something the script already contains. Never import.**

Protocol:

1. **Write the abstraction as it is spoken.** Use the speaker's own words as the label.
2. **Apply the literal test.** If this were true in the world, what would be different, and what would you see? "Consistency compounds" → something that visibly accumulates because it was repeated.
3. **Search the script for an anchor**, in this order:
   - an object it names
   - a place or time it names
   - an action or body part it names
   - a number it names
   - a phrase it repeats (repetition is an anchor — the same line can come back later)
4. **Write the anchor into `anchor`, quoting the script.** Then `visual` describes how *that* anchor is treated on screen. The anchor is not illustration; it is the piece of the script that carries the meaning.
5. **If nothing exists, set `"anchor": ""` explicitly.** That is a decision, not an omission — the builder only warns when the field is missing entirely, and the board marks the node unresolved. Then choose one of these, and say which you chose:
   - keep the beat image-free — hold, let the voice and captions carry the line
   - set the line's own language in type (the word repeated, the sentence struck through)
   - ask the writer one question: "what do you actually see when you say this?"

   Never fill the gap with an outside metaphor. Questions raised here belong in the **Unclarity Scan**
   (`references/intake-and-strategy.md`), not in a mid-board aside: collect them, ask them once, up
   front, and only then finish the board. A board that grows question by question is a board nobody
   can read.

**The in-context test:** a stranger should be able to point at the line in the script that justifies the visual. If they can't, it was imported.

| Abstract line | Anchor from the script | Treatment | Why it holds |
|---|---|---|---|
| "Consistency compounds" | "I still show up at 6am" | The same 6:00 alarm, same frame, three mornings in a row | The anchor is a time the speaker actually names; the repetition is the argument |
| "Trust takes time" | "She paid me before I got home" | The payment notification, no metaphor, cut hard on the resolution | The script's own proof does the work; adding imagery would dilute it |
| "Value is invisible at first" | *(nothing in the script)* | Unresolved: hold on the speaker, captions carry the line, or ask the writer | There is no honest anchor, so no image is invented |

Two guardrails:

- **Do not dress up an abstraction in another abstraction.** "Consistency compounds" over drifting particles is still nothing. The anchor must be a thing, a place, a time, an action, or a number.
- **Watch the ratio.** If more than about a quarter of the nodes are abstract, the script itself is the problem — say so in section 4, suggest a concrete example the writer could add, and do not paper over it with graphics.

In the JSON, an anchored and an unresolved abstract line look like this:

```json
{ "id": "consistency", "label": "Consistency compounds", "type": "abstract",
  "time": "0:06–0:09", "function": "Claim",
  "anchor": "I still show up at 6am",
  "visual": "Same alarm clock, same framing, three consecutive mornings; only the date changes." }

{ "id": "invisible_value", "label": "Value is invisible at first", "type": "abstract",
  "time": "0:14–0:17", "function": "Objection handled",
  "anchor": "",
  "summary": "No anchor in the script. Hold on the speaker or ask the writer; do not invent imagery." }
```

### 6. Write the JSON, then build the board

Write the graph to `<project>/previz/mindmap.json`, then run the bundled builder. It validates the graph, checks for dangling references and floating nodes, and writes a single self-contained HTML board:

```bash
# from this skill's directory
python3 scripts/build_mindmap.py previz/mindmap.json --check
python3 scripts/build_mindmap.py previz/mindmap.json -o previz/mindmap.html
python3 scripts/build_mindmap.py previz/mindmap.json -o previz/mindmap.html --theme dark
```

Minimal graph:

```json
{
  "title": "The Napkin Proof",
  "subtitle": "Instagram Reels · 9:16 · 0:19",
  "source": { "platform": "Instagram Reels", "aspect": "9:16", "duration": "0:19", "estimated": true },
  "theme": "light",
  "nodes": [
    { "id": "core", "label": "Proof of skill beats presentation polish", "type": "core",
      "time": "0:00–0:19", "function": "Core message", "emotion": "relief",
      "visual": "One continuous tabletop moment", "summary": "What every node must serve." },
    { "id": "week", "label": "Seven days without a single sign", "type": "stat",
      "time": "1:04–1:14", "function": "Data point", "emotion": "silence",
      "form": "seven blank cells on the page, nothing written in them",
      "stat": { "display": "dotgrid", "total": 7, "filled": 0, "caption": "seven days, no sign" } }
  ],
  "edges": [
    { "from": "core", "to": "week", "rel": "supports", "label": "measured by" }
  ]
}
```

A complete, realistic board lives at `examples/mindmap/napkin-proof.json` (with its built board
alongside). It deliberately contains **no `stat` nodes**: that transcript never states a number, so
there is nothing to carry one. A board with no numbers is a correct board — inventing a figure to
have something to chart is not.

If Python is unavailable, copy `assets/mindmap-board.template.html` and replace the `__BOARD_DATA_JSON__` marker inside `<script id="board-data">` with the graph JSON by hand.

### 7. Verify the board before handing it over

- exactly one `core` node, and it is the actual argument
- no floating nodes unless the isolation is intentional (`risk`, `note`)
- every number in the script appears as a `stat` node with a carrier recorded — an object (`form`), a
  visualisation (`chart` with a written `why`), or `"carrier": "type"` when the figure is simply set and
  held; the small `stat` preview is present only where it genuinely helps
- no `stat` node introduces a figure that is not in the transcript
- every `abstract` node either quotes an anchor that appears in the script, or is left unresolved on
  purpose — and unresolved ones are called out in section 4, not quietly filled later
- every unresolved abstract line, and every number the script never states, appears as a question in
  the Unclarity Scan output. Nothing load-bearing is resolved by a silent guess
- run the builder with `--script transcript.txt` when you have the text: it flags anchors that do not
  appear in the script, which is the fastest way to catch an imported metaphor
- labels are the spoken idea, not a topic ("She paid me before I got home", not "Payment")
- timecodes agree with Phase 1 and are marked estimated when they are
- node ids are short, lowercase, stable — later phases reference them (`Shot 03 → node stat_ten`)
- if the board is large, the `visual` field is what keeps it useful; do not let it become a word cloud

### 8. Write section 4 of the plan

````
PREVISUALIZATION MIND MAP
- Board file:
- Core node:
- Size: {n} nodes, {n} connections
- Argument shape: (how the branches are arranged — linear, two-sided, story-with-callback…)
- Main branches:
  - Branch name: node ids → what it holds
- Numbers and their carriers, as decided in the Phase 0 ledger:
  | Ledger ID | Spoken number | Node | Carrier (object / chart / type) | The one-line reason | Schematic, if any |
  |---|---|---|---|---|---|
- Abstract lines and their anchors:
  | Spoken line | Node | Anchor from the script | Treatment |
  |---|---|---|---|
- Unresolved lines (no visual chosen):
  - <line> — why nothing in the script carries it, and the option taken
    (image-free beat / type from the line / one question to the writer)
- Cross-links that matter:
- Nodes carrying no timecode:
- Risks and constraints on the board:
- Assumptions / open questions:

BOARD SKETCH (text view)
core: <core message>
├─ hook: <line>  [0:00–0:03]
│  └─ claim: <line>
├─ proof: <line>
│  ├─ example: <line>
│  └─ stat: <number> → <carrier: an object / a chart with its reason / type>  (schematic optional)
├─ abstract: <line>
│  └─ anchor: "<words already in the script>"     ⚠ or "unresolved — no picture yet"
└─ cta: <line>  ↩ callback → hook
````

The text sketch matters: some readers never open the HTML. Keep it to one screen.

## Rules for the board

- The board is reasoning, not decoration. If a node does not change an edit decision, cut it.
- Never fabricate a statistic, source, or quote to fill a `stat` node.
- A chart can be the visual idea. What fails is a *shape nobody decided on*: the same graphic, for the
  same kind of fact, in every video. If you cannot say in one clause what relationship the sentence
  asserts, the chart is not earned — and if you can say it, do not be shy about drawing it.
- The carrier was decided in Phase 0, before anyone pictured the film. The board records that decision;
  it does not make it. If the board wants a different answer, change the ledger first, then the board.
- Never import imagery, objects, or metaphor vocabulary from outside the script's world. If it is not
  in the script, it is not available — not a lightbulb, not gears, not a seedling, not a stock road.
- An unresolved abstract line stays unresolved in the output. Later phases must not quietly resolve it
  by inventing a picture; they may only reuse an anchor the script actually contains.
- The board and the Narrative Spine must agree. The spine is the line; the board is the map of it.
- Fewer nodes with real visual ideas beat many nodes with topic labels.
- Keep node ids stable once written: Phase 8 (Shot Plan) and Phase 9 (Storyboard) reference them.
- If the script changes, edit the JSON and rebuild — do not hand-edit the HTML.
- The HTML is a working board, not a deliverable video asset: no autoplay, no sound, no external requests.
- Board size guidance: 8–22 nodes for anything under a minute; 15–30 for longer pieces; beyond that, split by act and say so.

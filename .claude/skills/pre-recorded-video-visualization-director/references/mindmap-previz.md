# Phase 4: Previsualization Mind Map (Node Board)

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
| `stat` | A number, ratio, price, or duration from the script — `form` names the body that carries it | "Seven days without a single sign" |
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

### 4. Give every number a body from this script

**A number is not a graphic.** Before anything is drawn, find out what the number is *of*, and let
the script say what that looks like.

The failure mode this section exists to prevent: see a number → reach for a dot grid. A dot grid is
one legitimate body for one narrow kind of fact — a counted population of identical things. Everywhere
else it is decoration, and it tells the viewer the editor had a template instead of a point of view.

**Dot grids are not the house style.** Neither are bars, rings, or "data-viz" styling. If a graphic is
reached for because the line contains a number, the number has not been given a body yet.

#### The protocol

1. **Quote the number and its unit as spoken.** "Ten out of a hundred", "three weeks", "two thousand
   years", "eight days".
2. **Name what is being counted, compared, or elapsed.** Write the noun: clients, weeks, years, days.
3. **Find that noun's body in the script.** An object it names, a place, a time of day, a document, a
   body part, an action, a piece of furniture. This is the same search as the anchor search in
   section 5.
4. **Choose the carrier and write it in `form`.** The carrier is the physical thing on screen that
   holds the number. Required on every `stat` node.
5. **Only now decide whether a schematic helps.** Most numbers do not need one. `stat.display` is
   optional, and it is a schematic *preview* for the board — never the finished look, and never a
   substitute for step 3.

| What the script said | What is being counted | Carrier (`form`) | Schematic? |
|---|---|---|---|
| "a hundred small decisions nobody claps for" | decisions a hand made | a sheet of a hundred pencil tallies | no — the tallies are countable on camera |
| "three weeks polishing vs forty minutes drawing" | elapsed time | two calendars side by side, one crossed out | no |
| "two thousand years of church history" | centuries of retelling | the wall of paintings the sentence describes | `counter` only as a timestamp |
| "seven days without a single sign" | empty days | seven blank cells on a page, nothing written in them | `dotgrid` 7/0 — the one fair use |
| "eight days later" | a sequence | the same page, one entry added | `steps` 8, eighth active |
| "two thousand dollars" | money | the invoice or the stack of notes | no |
| "one in three people" | people | three chairs in a room, one occupied | no |

#### Rules

- **The carrier must be in the script.** If it is not, the number is not a visual problem yet — it is
  an abstraction problem. Go to section 5 and do not invent a chart instead.
- **Real objects beat schematic shapes** whenever the script gives you one. Counting jars on a bench
  is better television than counting dots on white.
- **If the number is the point and has no body**, say it in type. A naked numeral held on screen is
  honest; a chart that dresses it up is not.
- **Keep the scale honest.** If 10 of 100 is highlighted, the other 90 stay visible. Never crop the
  remainder to make the point louder.
- **Reveal on the spoken beat.** Put the build in `visual`: marks arriving, days blanking out, the
  page being set down.
- **Never fake a dashboard.** No invented axes, no 3D pies, no gauges, no growth arrows the script
  never claimed.
- **Never invent a number.** Every figure on the board must appear in the transcript. The builder
  checks this against `--script`.
- **Vary the bodies.** If two numbers in one script want the same carrier, check whether one of them
  actually needs a visual at all.

#### Optional schematics

Available `display` values, for the rare case where a schematic communicates faster than anything
filmable. Each one is a fallback, not a menu to work down:

| `display` | Only when | Fields |
|---|---|---|
| `dotgrid` | a counted population of identical things, and nothing more textured is available | `total`, `filled`, `caption` |
| `steps` | a sequence the script counts in order | `steps`, `active`, `caption` |
| `bars` | several named quantities the script explicitly compares | `values`, `labels`, `highlight` |
| `proportion` | a share of a whole, when the whole has no other identity | `percent`, `caption` |
| `fraction` | a ratio said as a fraction | `part`, `whole` |
| `compare` | two magnitudes the script sets against each other | `values` |
| `counter` | a single number where scale is the point and nothing else can carry it | `value`, `prefix`, `suffix` |

If a board ends up with several numbers and every one of them is a schematic, that is the failure
this phase is meant to catch — say so and rework them.

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

   Never fill the gap with an outside metaphor.

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
- every number in the script appears as a `stat` node whose `form` names a real carrier, or is deliberately
  left as speech or as type; a schematic is present only where it genuinely helps
- no `stat` node introduces a figure that is not in the transcript
- every `abstract` node either quotes an anchor that appears in the script, or is left unresolved on
  purpose — and unresolved ones are called out in section 4, not quietly filled later
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
- Numbers and the body that carries each one:
  | Spoken number | Node | What is counted | Carrier (form) | Schematic, if any |
  |---|---|---|---|
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
│  └─ stat: <number> → <the body that carries it: an object / page / place>  (schematic optional)
├─ abstract: <line>
│  └─ anchor: "<words already in the script>"     ⚠ or "unresolved — no picture yet"
└─ cta: <line>  ↩ callback → hook
````

The text sketch matters: some readers never open the HTML. Keep it to one screen.

## Rules for the board

- The board is reasoning, not decoration. If a node does not change an edit decision, cut it.
- Never fabricate a statistic, source, or quote to fill a `stat` node.
- A chart is not a visual idea. If the only thing on screen is a dot grid or bars, the number has not
  been given a body — it has been given a template.
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

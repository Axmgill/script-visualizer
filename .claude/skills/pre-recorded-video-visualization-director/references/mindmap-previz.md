# Phase 4: Previsualization Mind Map (Node Board)

Read this file before producing output section 4.

## Why this phase exists

Editors and motion designers rarely start a previz with a shot list. They dump the script onto a board first: the central idea in the middle, the claims and proofs hanging off it, the numbers turned into shapes, the callbacks drawn as arrows back to the hook. The board exposes the shape of the argument before anyone commits to a shot.

Section 4 is that board. It is **not** a summary of the script and **not** decoration — it is the non-linear view of the same material the Narrative Spine (Phase 3) shows linearly. Every node should be able to change an edit decision.

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
| `stat` | A number, ratio, percentage, price, or duration from the script | "10 in 100 first clients…" |
| `example` | A specific concrete instance inside a proof | "I drew the logo in front of her" |
| `emotion` | The feeling the beat must produce, or a contrast between feelings | "Polish takes weeks; proof takes one conversation" |
| `visual` | A motif, object, or device that recurs visually | "The napkin is the hero object" |
| `objection` | The viewer's resistance, named out loud | "Stop waiting to look professional" |
| `cta` | What the viewer should do or feel at the end | "Start showing people you can solve their problem" |
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

### 4. Turn every number into a shape

This is the part that separates a previz board from a transcript with boxes. Motion designers never leave a statistic as a numeral — they give it a physical form the viewer can count, feel, or compare at a glance.

Give each `stat` node a `stat` object. Available displays:

| `display` | Use for | Fields |
|-----------|---------|--------|
| `dotgrid` | "X out of Y" where Y is countable (unit chart) | `total`, `filled`, `caption`, `accent` |
| `bars` | Values over categories or time | `values`, `labels`, `highlight`, `caption` |
| `proportion` | A single percentage | `percent`, `caption` |
| `fraction` | A bare ratio shown as a fraction | `part`, `whole`, `caption` |
| `compare` | Two or a few magnitudes against each other | `values` as `{label, value, accent}` |
| `steps` | A process or progression | `steps`, `active` |
| `counter` | A single number with no natural visual unit | `value`, `prefix`, `suffix`, `caption` |

Translation rules:

- **One dot = one real thing.** "10 out of 100" becomes 100 dots with 10 filled — not a pie chart, not a gauge. The viewer counts the highlighted cluster without reading a number.
- **Keep the scale honest.** If 10 of 100 is highlighted, the other 90 must still be visible. Never crop the remainder to make the point louder.
- **Highlight only what the script stresses.** One accent colour, on the part the voiceover names.
- **Reveal on the spoken beat.** Note in `metaphor` how the shape builds: dots arriving, bars growing, the one-in-three landing early. Timing belongs in the node, not in the graphic file.
- **Prefer objects when the subject is physical.** 3 of 12 jars, 1 of 5 doors, 10 of 100 people — a real object beats a chart shape if it exists in the footage.
- **Under 400 dots.** Above that, use `bars` or `proportion`; a 10,000-dot grid is noise.
- **If fewer than ~3% of units are highlighted**, a `counter` reads better than an almost-empty grid.
- **Never fake a dashboard.** No invented axes, no 3D pies, no gauges, no "growth" arrows the script never claimed.
- **Label the unit.** The caption says what one dot is ("1 dot = 1 person") whenever it is not obvious.
- **State the source when the script states it.** If the number came from a study, the node summary carries the attribution; if the script gave no source, do not imply one.

Non-numeric claims get the same treatment through the `visual` field: describe the shape, not the shot. "A portfolio is a presentation, not a proof" might become *a glossy frame that gets lifted away to reveal a bare napkin underneath.* That sentence is more useful to an editor than "cut to laptop".

### 5. Write the JSON, then build the board

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
    { "id": "stat_ten", "label": "10 in 100 first clients trace back to a polished portfolio", "type": "stat",
      "time": "0:02–0:04", "function": "Data point", "emotion": "surprise",
      "stat": { "display": "dotgrid", "total": 100, "filled": 10, "caption": "1 dot = 1 person",
                "metaphor": "Dots arrive in a wave; the 10 fill one at a time on the line." } }
  ],
  "edges": [
    { "from": "core", "to": "stat_ten", "rel": "supports", "label": "backed by" }
  ]
}
```

A complete, realistic board — every node type, cross-links, a dot grid and a comparison chart — lives at `examples/mindmap/napkin-proof.json`, with its built board at `examples/mindmap/napkin-proof.html`.

If Python is unavailable, copy `assets/mindmap-board.template.html` and replace the `__BOARD_DATA_JSON__` marker inside `<script id="board-data">` with the graph JSON by hand.

### 6. Verify the board before handing it over

- exactly one `core` node, and it is the actual argument
- no floating nodes unless the isolation is intentional (`risk`, `note`)
- every number in the script appears as a `stat` node with a shape, or is deliberately left as speech
- labels are the spoken idea, not a topic ("She paid me before I got home", not "Payment")
- timecodes agree with Phase 1 and are marked estimated when they are
- node ids are short, lowercase, stable — later phases reference them (`Shot 03 → node stat_ten`)
- if the board is large, the `visual` field is what keeps it useful; do not let it become a word cloud

### 7. Write section 4 of the plan

````
PREVISUALIZATION MIND MAP
- Board file:
- Core node:
- Size: {n} nodes, {n} connections
- Argument shape: (how the branches are arranged — linear, two-sided, story-with-callback…)
- Main branches:
  - Branch name: node ids → what it holds
- Data points and their shapes:
  | Spoken number | Node | Shape | Build note |
  |---|---|---|---|
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
│  └─ stat: <number> → 100 dots, 10 filled
└─ cta: <line>  ↩ callback → hook
````

The text sketch matters: some readers never open the HTML. Keep it to one screen.

## Rules for the board

- The board is reasoning, not decoration. If a node does not change an edit decision, cut it.
- Never fabricate a statistic, source, or quote to fill a `stat` node.
- The board and the Narrative Spine must agree. The spine is the line; the board is the map of it.
- Fewer nodes with real visual ideas beat many nodes with topic labels.
- Keep node ids stable once written: Phase 8 (Shot Plan) and Phase 9 (Storyboard) reference them.
- If the script changes, edit the JSON and rebuild — do not hand-edit the HTML.
- The HTML is a working board, not a deliverable video asset: no autoplay, no sound, no external requests.
- Board size guidance: 8–22 nodes for anything under a minute; 15–30 for longer pieces; beyond that, split by act and say so.

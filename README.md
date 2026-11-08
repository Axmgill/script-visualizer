# script-visualizer

An Agent Skill that turns pre-recorded audio/video material into a complete, timecoded visual edit plan — so you can see the finished video before you build it.

## Install

**Latest release:** [v1.0.0](https://github.com/Axmgill/script-visualizer/releases/tag/v1.0.0)

**Installation URL** (versioned source archive):

```
https://github.com/Axmgill/script-visualizer/archive/refs/tags/v1.0.0.zip
```

Install for all projects (Claude Code):

```bash
curl -L https://github.com/Axmgill/script-visualizer/archive/refs/tags/v1.0.0.zip -o sv.zip
unzip -q sv.zip
mkdir -p ~/.claude/skills
cp -r script-visualizer-*/.claude/skills/pre-recorded-video-visualization-director ~/.claude/skills/
```

Or with git (no curl/unzip needed):

```bash
git clone --branch v1.0.0 --depth 1 https://github.com/Axmgill/script-visualizer.git
mkdir -p ~/.claude/skills
cp -r script-visualizer/.claude/skills/pre-recorded-video-visualization-director ~/.claude/skills/
```

For a single project, copy into that project's `.claude/skills/` instead. For claude.ai, zip just the `pre-recorded-video-visualization-director/` folder and upload it under Settings → Capabilities → Skills. Full instructions are in the [release notes](https://github.com/Axmgill/script-visualizer/releases/tag/v1.0.0).

## The skill

**`pre-recorded-video-visualization-director`** lives at:

```
.claude/skills/pre-recorded-video-visualization-director/
├── SKILL.md                              # Entry point: role, principles, workflow router
├── references/
│   ├── intake-and-strategy.md            # Phases 1–3: intake, brief, narrative spine
│   ├── mindmap-previz.md                 # Phase 4: previsualization mind map (node board)
│   ├── design-craft.md                   # Studio process, craft standards, critique rubric
│   ├── visual-plan.md                    # Phases 5–9: art direction, arc, scenes, shots, storyboard
│   ├── graphics-text-rhythm-sound.md     # Phases 10–13: graphics, captions, rhythm, sound
│   ├── production-and-delivery.md        # Phases 14–17: assets, software notes, review, delivery
│   ├── modules.md                        # Branding, vertical, documentary, fast-cut, AI footage
│   └── modes-and-interaction.md          # Default/short/expert/blank-mind-rescue modes
├── assets/
│   └── mindmap-board.template.html       # Self-contained interactive board (no dependencies)
├── scripts/
│   ├── estimate_timecodes.py             # Deterministic timecode estimation / SRT & VTT parsing
│   ├── scan_ambiguity.py                 # Flags lines a plan would have to guess at
│   └── build_mindmap.py                  # Node graph JSON → standalone HTML board
└── examples/
    ├── worked-example.md                 # Input → output demonstration (Short Mode)
    └── mindmap/
        ├── napkin-proof.json             # Example node graph
        ├── napkin-proof.html             # Built board — open it in a browser
        ├── numbers-by-context.json       # Four numbers, four carriers, each decided by its sentence
        ├── numbers-by-context.html       # Built board for the above
        ├── numbers-script.txt            # The transcript those carriers come from
        ├── abstract-to-anchor.json       # Abstract lines, anchored vs unresolved
        ├── abstract-to-anchor.html       # Built board for the above
        └── abstract-script.txt           # The transcript those anchors come from
```

It follows the [Agent Skills](https://agentskills.io) format: a `SKILL.md` with YAML frontmatter (`name` + `description`), progressive disclosure into `references/`, and a bundled helper script. Only the name and description load at startup; the full workflow loads when a matching task appears.

## What it does

Give it a voiceover, talking-head video, screen recording, interview, podcast clip, raw footage, rough edit, or transcript (a script works too — timing gets marked ESTIMATED), and it produces a 17-section edit plan: media intake, assumptions and open questions, creative brief, narrative spine, a previsualization mind map, visual concept, emotional arc, scene map, shot/b-roll plan, text storyboard, motion graphics, caption strategy, editing rhythm, sound direction, asset checklist, software execution notes, review checklist, and a copy-into-production delivery summary.

Every visual is anchored to timecodes or speech beats. Existing footage comes first; new assets are suggested only when needed, always with a fallback.

## It asks before it assumes

A script is rarely as complete as it sounds. Before it builds anything, the skill reads for what the script *doesn't* say and asks — once, in one batch, five questions at most.

```bash
python3 scripts/scan_ambiguity.py transcript.txt
```

The scanner flags the sentences a plan would otherwise invent around, each with an estimated timecode and a severity:

| Severity | Examples | Rule |
|---|---|---|
| **Blocking** | `[link]` placeholders · "studies show" with no source · "most people" with no number · "as you can see" pointing at footage from another edit | answered or explicitly defaulted **before the mind map is built** |
| **Shaping** | "recently" with no date · "better than ever" with nothing to compare to | asked, with a default offered — the plan continues |
| **Note** | rhetorical questions · "I think" · a reveal being held back | **never asked** — that's the script working |

Every question quotes the line and its timecode, says which phase it blocks, offers two or three readings, and names the default. There is always an exit: *reply "defaults"* and the plan proceeds with its assumptions marked. If a blocking question goes unanswered, the ambiguity stays visible — the node stays unresolved, no anchor is invented, and the assumption is carried into the final package as *"still open"*. Nothing load-bearing is ever settled by a silent guess.

## How it designs (Phase 5)

It doesn't hand you a mood board and a look. It runs the process strong motion designers actually run:

1. **Tension** — what the viewer believes now, and what the video must make them feel.
2. **Named references** — 6–10 specific pieces across composition, colour, type and motion, plus one anti-reference. "Clean, modern, premium" is rejected as non-specific.
3. **Three territories** — mutually exclusive directions, each argued as *"it looks like X because the script says Y"*, each with a named risk. Swap test: if a direction still works in another video, it was a house style.
4. **One visual system** — grid and ratio, palette *roles* rather than a mood, a type scale with a fixed ratio, shape language, texture rules, motion grammar.
5. **4–6 style frames** — composition, hierarchy, negative space, light, type and texture, specified precisely enough to rebuild. They must read as a series, and must include the hardest frame, not just the showcase one.
6. **Critique** — mute, squint, stranger, delete and swap tests, scored against a rubric where *Truth* and *Idea* below 4 means rework.

The standards come from how the craft is taught and practised — School of Motion's Design Kickstart, Design Bootcamp and Illustration for Motion, plus the documentary-graphics and retention work taught at AevyTV — encoded as gates and pass/fail tests, not as visual trends to copy.

## Mind map board (Phase 4)

Before any shot is chosen, the script is mapped the way an editor would map it on a Miro or FigJam board: the central argument in the middle, claims, proofs, examples, motifs, risks and data points hanging off it, connected by relations like *proves*, *contrasts*, *callback* and *blocks*.

The skill writes that graph to JSON and builds a real board — one self-contained HTML file, no dependencies, no network calls:

- **reading order** — press `←` / `→` and the board walks the beats in sequence, dimming everything except the current beat and its connections. A route through the map, not just a map.
- **search that takes you there** — type, pick from the result list, and the camera flies to the beat. No "everything faded and you're still looking at the middle".
- **needs attention** — a queue of what still has to be decided: abstract lines with no anchor, numbers with no carrier, beats with no timecode. `J` / `K` to walk it.
- **minimap + breadcrumb** — where you are on the board, and the path you took to the selected beat.
- drag nodes, pan and zoom an infinite canvas; click a node to inspect its function, emotion and visual idea
- connections are colored by relation, so the argument's shape is visible at a glance
- the timecode track under the canvas scrubs: drag a range to isolate part of the edit
- **works from 320px to 2560px** — six layout modes. On a phone the board becomes a **beat-by-beat view**: one card at a readable size with the neighbouring beats peeking above and below, swipe to move. The map is one tap away, never a shrunken poster.
- pan, zoom and card positions persist in the browser; `R` rebuilds the layout from scratch
- export the node graph as JSON, or the board itself as a PNG
- **every number records the carrier its own sentence earns.** Three are legitimate and none is the default: an **object** the script already contains (`form` — the page with one new line, the invoice, the shutter going up), a **data visualisation** (`chart` — with `what` is being compared and `why` this line earns one), or **type** (`carrier: "type"` — the figure set and held). A chart is an answer, not a fallback; what the builder rejects is a number with no carrier recorded, and a chart with no written reason. `--script` still flags any figure the transcript never stated.
- **abstract lines never borrow imagery.** A line like "consistency compounds" has no picture in it. The node carries an `anchor` quoted from the script — the 6am alarm the speaker actually mentions — and the visual is a treatment of that anchor. If the script contains nothing concrete, the node stays visibly **unresolved** instead of being handed a lightbulb or a seedling.

```bash
cd .claude/skills/pre-recorded-video-visualization-director
python3 scripts/build_mindmap.py examples/mindmap/numbers-by-context.json \
  --script examples/mindmap/numbers-script.txt --check
python3 scripts/build_mindmap.py examples/mindmap/numbers-by-context.json \
  -o previz/numbers.html
python3 scripts/build_mindmap.py examples/mindmap/napkin-proof.json --check
python3 scripts/build_mindmap.py examples/mindmap/napkin-proof.json -o previz/mindmap.html

# check that abstract lines are anchored to the transcript, not invented
python3 scripts/build_mindmap.py examples/mindmap/abstract-to-anchor.json \
  --script examples/mindmap/abstract-script.txt --check
```

Open `examples/mindmap/napkin-proof.html` to see a finished board. This phase is on `main` and ships in the next release; the install links above point at v1.0.0.

## Usage

**Claude Code (this repo):** the skill is discovered automatically from `.claude/skills/`. Just say things like:

- "Visualize this pre-recorded video" + transcript
- "Plan the edit for this voiceover"
- "What b-roll should I use for this audio?"
- "Mind map this script" / "Previz this script as a board"
- "Quick version" → Short Mode · "Deep detail" → Expert Mode

**Claude Code (personal, all projects):** copy the skill folder to `~/.claude/skills/`.

**claude.ai / other agents:** zip the skill folder (with `SKILL.md` inside it) and upload it wherever your agent supports skills.

## Helper script

```bash
cd .claude/skills/pre-recorded-video-visualization-director

# Estimate timecodes from a plain-text transcript (2.5–3 words/sec)
python3 scripts/estimate_timecodes.py transcript.txt --wps 2.75 --format md

# Extract real timecodes from captions
python3 scripts/estimate_timecodes.py captions.srt --format json

# Find the lines a visual plan would have to guess at
python3 scripts/scan_ambiguity.py transcript.txt            # markdown, severity-sorted
python3 scripts/scan_ambiguity.py transcript.txt --strict   # exit 1 if anything BLOCKING
python3 scripts/scan_ambiguity.py examples/ambiguous-script.txt   # 5 blocking, 2 shaping, 3 note

# Validate a mind-map node graph, then build the board
python3 scripts/build_mindmap.py previz/mindmap.json --check
python3 scripts/build_mindmap.py previz/mindmap.json -o previz/mindmap.html
```

No dependencies beyond Python 3.8+ (the board itself is HTML/CSS/JS with no runtime dependencies).

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
│   ├── visual-plan.md                    # Phases 5–9: concept, emotional arc, scenes, shots, storyboard
│   ├── graphics-text-rhythm-sound.md     # Phases 10–13: graphics, captions, rhythm, sound
│   ├── production-and-delivery.md        # Phases 14–17: assets, software notes, review, delivery
│   ├── modules.md                        # Branding, vertical, documentary, fast-cut, AI footage
│   └── modes-and-interaction.md          # Default/short/expert/blank-mind-rescue modes
├── assets/
│   └── mindmap-board.template.html       # Self-contained interactive board (no dependencies)
├── scripts/
│   ├── estimate_timecodes.py             # Deterministic timecode estimation / SRT & VTT parsing
│   └── build_mindmap.py                  # Node graph JSON → standalone HTML board
└── examples/
    ├── worked-example.md                 # Input → output demonstration (Short Mode)
    └── mindmap/
        ├── napkin-proof.json             # Example node graph
        ├── napkin-proof.html             # Built board — open it in a browser
        ├── abstract-to-anchor.json       # Abstract lines, anchored vs unresolved
        ├── abstract-to-anchor.html       # Built board for the above
        └── abstract-script.txt           # The transcript those anchors come from
```

It follows the [Agent Skills](https://agentskills.io) format: a `SKILL.md` with YAML frontmatter (`name` + `description`), progressive disclosure into `references/`, and a bundled helper script. Only the name and description load at startup; the full workflow loads when a matching task appears.

## What it does

Give it a voiceover, talking-head video, screen recording, interview, podcast clip, raw footage, rough edit, or transcript (a script works too — timing gets marked ESTIMATED), and it produces a 17-section edit plan: media intake, creative brief, narrative spine, a previsualization mind map, visual concept, emotional arc, scene map, shot/b-roll plan, text storyboard, motion graphics, caption strategy, editing rhythm, sound direction, asset checklist, software execution notes, review checklist, and a copy-into-production delivery summary.

Every visual is anchored to timecodes or speech beats. Existing footage comes first; new assets are suggested only when needed, always with a fallback.

## Mind map board (Phase 4)

Before any shot is chosen, the script is mapped the way an editor would map it on a Miro or FigJam board: the central argument in the middle, claims, proofs, examples, motifs, risks and data points hanging off it, connected by relations like *proves*, *contrasts*, *callback* and *blocks*.

The skill writes that graph to JSON and builds a real board — one self-contained HTML file, no dependencies, no network calls:

- drag nodes, pan and zoom an infinite canvas; click a node to inspect its function, emotion and visual idea
- connections are colored by relation, so the argument's shape is visible at a glance
- the timecode track under the canvas puts every beat on the timeline
- **numbers get a body, not a chart.** Every `stat` node must name the physical thing on screen that carries the figure — a page of tallies, an invoice, seven blank cells, the wall of paintings the sentence describes. Charts are an optional schematic preview, never the default. A number with no body in the script stays as type or as speech; the builder rejects a `stat` node that has only a chart, and `--script` flags any figure the transcript never stated.
- **abstract lines never borrow imagery.** A line like "consistency compounds" has no picture in it. The node carries an `anchor` quoted from the script — the 6am alarm the speaker actually mentions — and the visual is a treatment of that anchor. If the script contains nothing concrete, the node stays visibly **unresolved** instead of being handed a lightbulb or a seedling.

```bash
cd .claude/skills/pre-recorded-video-visualization-director
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

# Validate a mind-map node graph, then build the board
python3 scripts/build_mindmap.py previz/mindmap.json --check
python3 scripts/build_mindmap.py previz/mindmap.json -o previz/mindmap.html
```

No dependencies beyond Python 3.8+ (the board itself is HTML/CSS/JS with no runtime dependencies).

# script-visualizer

An Agent Skill that turns pre-recorded audio/video material into a complete, timecoded visual edit plan — so you can see the finished video before you build it.

## The skill

**`pre-recorded-video-visualization-director`** lives at:

```
.claude/skills/pre-recorded-video-visualization-director/
├── SKILL.md                              # Entry point: role, principles, workflow router
├── references/
│   ├── intake-and-strategy.md            # Phases 1–4: intake, brief, narrative spine, concept
│   ├── visual-plan.md                    # Phases 5–8: emotional arc, scene map, shots, storyboard
│   ├── graphics-text-rhythm-sound.md     # Phases 9–12: graphics, captions, rhythm, sound
│   ├── production-and-delivery.md        # Phases 13–16: assets, software notes, review, delivery
│   ├── modules.md                        # Branding, vertical, documentary, fast-cut, AI footage
│   └── modes-and-interaction.md          # Default/short/expert/blank-mind-rescue modes
├── scripts/
│   └── estimate_timecodes.py             # Deterministic timecode estimation / SRT & VTT parsing
└── examples/
    └── worked-example.md                 # Input → output demonstration (Short Mode)
```

It follows the [Agent Skills](https://agentskills.io) format: a `SKILL.md` with YAML frontmatter (`name` + `description`), progressive disclosure into `references/`, and a bundled helper script. Only the name and description load at startup; the full workflow loads when a matching task appears.

## What it does

Give it a voiceover, talking-head video, screen recording, interview, podcast clip, raw footage, rough edit, or transcript (a script works too — timing gets marked ESTIMATED), and it produces a 16-section edit plan: media intake, creative brief, narrative spine, visual concept, emotional arc, scene map, shot/b-roll plan, text storyboard, motion graphics, caption strategy, editing rhythm, sound direction, asset checklist, software execution notes, review checklist, and a copy-into-production delivery summary.

Every visual is anchored to timecodes or speech beats. Existing footage comes first; new assets are suggested only when needed, always with a fallback.

## Usage

**Claude Code (this repo):** the skill is discovered automatically from `.claude/skills/`. Just say things like:

- "Visualize this pre-recorded video" + transcript
- "Plan the edit for this voiceover"
- "What b-roll should I use for this audio?"
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
```

No dependencies beyond Python 3.8+.

# Worked Example (Short Mode)

A compact demonstration of the skill transforming a raw transcript into an edit plan. This example uses Short Mode; Default Mode expands the same material into all 17 sections using the templates in `references/`.

## Example input

> Visualize this pre-recorded video. Quick version.
>
> Platform: Instagram Reels. Audience: freelance designers. Editing in CapCut.
> I only have the voiceover, no footage yet. No stock clichés.
>
> Transcript: "Your first client doesn't come from a perfect portfolio. Mine came from a napkin sketch in a coffee shop. I drew the logo right in front of her. She paid me before I got home. Stop waiting to look professional. Start showing people you can solve their problem."

## Example output

**Timing note:** No timecodes provided. All times below are ESTIMATED at ~2.75 words/second (48 words, ~19 seconds total). Verify against the recording.

### Phase 0 — the context card

Built before any visual decision, from the words only.

| | |
|---|---|
| What this is | 48 words, ~19 seconds, one speaker, no footage. Instagram Reels. |
| The line | "Your first client doesn't come from a perfect portfolio." (0:00) |
| The job | Make a waiting freelancer send one message today. |
| The turn | 0:08 — "Stop waiting" turns a story into an instruction. |
| The room | A coffee shop, a napkin. Both named by the speaker. |

**Figures ledger.** One figure only:

| ID | Time | Figure | What the sentence does with it |
|---|---|---|---|
| F1 | 0:00 | "your first client" | Not an amount. It is a milestone, said once, as a noun. |

No carrier is needed for F1: there is no number on screen. **This is the point of the ledger.**
A script can be about a "first" something and still contain no data. The plan must not invent
a chart to look analytical, and the board must not contain a `stat` node here.

**Materials.** a portfolio, a napkin, a coffee shop, a logo drawn by hand, a payment before
the speaker got home. That is the entire world of the film.

**Domain imports to refuse.** Guru-in-a-hoodie graphics, a rising line labelled "clients",
a rocket, a lightbulb, a stock handshake.

### Assumptions and open questions

```
ASSUMPTIONS AND OPEN QUESTIONS

Read: The script is clear on the claim ("proof beats polish"), the object (the napkin), the
action (the logo drawn in front of the client) and the payoff (paid the same day). Nothing here
needs a source.

Blocking — none. Nothing in the script asks the plan to invent evidence.

Shaping — a default is enough
S1. "Mine came from a napkin sketch in a coffee shop." — was the client there when you drew it,
    or did you bring the sketch to her? The frame changes: hands at a table versus handing paper over.
    Default: she is present, watching it happen — that is what "right in front of her" implies.

Not asking, on purpose
- "Stop waiting to look professional." — imperative, not a claim; there is nothing to resolve.

If you reply "defaults": the edit assumes one continuous tabletop, one client across the table,
and a same-day payment. No numbers are used, because the script states none.
```

### Core message

Proof of skill beats presentation polish — your first client wants a solved problem, not a perfect portfolio.

### Mind map (node board)

Built as a real board — `examples/mindmap/napkin-proof.html`, generated from `examples/mindmap/napkin-proof.json` — 11 nodes, 16 connections.

```
core: Proof of skill beats presentation polish
├─ hook: "Your first client doesn't come from a perfect portfolio"     0:00–0:03.5
│  ├─ claim: a portfolio is a presentation, not a proof
├─ proof: "Mine came from a napkin sketch"                             0:03.5–0:07.5
│  ├─ example: "I drew the logo right in front of her"
│  └─ visual: the napkin is the hero object
├─ objection: "Stop waiting to look professional"                      0:13.5–0:16
│  └─ cta: "Start showing people you can solve their problem"          0:16–0:19
│     ↩ callback → hook
├─ contrast: "She paid me before I got home" — stated as a turn, never as a number
└─ risk: stock hands would kill the argument  ← blocks ← note: one 10-min phone session
```

This transcript contains no numbers at all, so the board has no `stat` nodes — the correct outcome. Nothing was charted, and nothing was invented to have something to chart. The napkin shows up in four nodes, which is the board telling us which object has to carry the edit.

The core claim is abstract ("proof beats polish"), but the script supplies its own anchor — the napkin sketch drawn in front of a paying client — so no imported metaphor is needed. A board for a script with no such anchor would leave that node unresolved rather than reach for a lightbulb; the abstract-lines demo is at `examples/mindmap/abstract-to-anchor.html`.

### Visual concept

**Tension.** The viewer believes a portfolio is a website. The video has to make a stranger's handwriting feel more trustworthy than a grid of thumbnails.

**References.** *Composition:* Saul Bass poster hierarchy, one idea per field. *Colour:* diner-table warm neutrals, one red accent earned by the coffee ring. *Type:* Swiss grotesque for captions, no second family. *Motion:* Vox-style hold-then-reveal, cuts not swooshes. *Anti-reference:* the Dribbble-thumbnail grid — the exact thing the video is arguing against.

**Three territories.**
1. *The Napkin* — one continuous real-world surface, hands and pen, light shifting across the minute. The risk: if the pen never crosses the frame's centre, the middle turn flatlines.
2. *The Studio Wall* — pinned paper, tape, marker, shot from above as a desk in use. The risk: reads as craft-hobby content, not portfolio advice.
3. *The Case File* — evidence labels and a magnifier on the same napkin. The risk: turns a warm story cold.

Winner: **The Napkin**, with one borrow from territory 3 — a single small label at the end naming the thing ("this is the portfolio"). It passes the swap test: no other video in this niche arrives on a paper napkin in one light.

**System.** 1.85:1, 12-column grid, 96 px margin. Palette by role: paper `#EDE3D2` ground, ink `#1A1614` type, red `#B23A2E` accent used exactly twice (the coffee ring, the end label). Type: one grotesque, 5 steps at 1.25. Shape: hard rectangle only, no rounded cards. Texture: real paper grain, never an overlay. Motion: hold, then cut; the pen is the only thing that moves within a frame. Sound: room tone, pen scratch, paper.

**Style frame A — the proof (0:00–0:12).** Close top-down, napkin filling 80% of frame, pen entering from bottom-right, red ring at one-third left. One caption, top-left, 5% of frame height. Nothing else. Could be paused and printed as a poster.

**Style frame B — the turn (0:41).** Pull back to show the room: the same napkin on the table, two hands, coffee cup missing. The empty ring where the cup was is the focal point; the caption sits below the ring, never over it. This is the hardest frame and the one that proves the direction — it only works if the light has visibly moved since frame A.

**Must not.** No stock b-roll, no laptop mockups, no animated arrows, no second accent colour, no caption over the napkin's centre.

### Beat map

| Beat | Time (EST.) | Line | Function |
|------|-------------|------|----------|
| 1 | 0:00–0:03.5 | "Your first client doesn't come from a perfect portfolio." | Hook / objection broken |
| 2 | 0:03.5–0:10.5 | "Mine came from a napkin sketch in a coffee shop. I drew the logo right in front of her." | Proof / story |
| 3 | 0:10.5–0:13.5 | "She paid me before I got home." | Payoff |
| 4 | 0:13.5–0:19 | "Stop waiting to look professional. Start showing people you can solve their problem." | Transformation / CTA |

### Shot / b-roll plan

| # | Time (EST.) | Visual | Source | Alternative |
|---|-------------|--------|--------|-------------|
| 01 | 0:00–0:03.5 | Bold caption on plain dark frame; the word "perfect" gets a dismissive strike-through | Text animation (built in CapCut) | Speaker's first existing photo with caption overlay |
| 02 | 0:03.5–0:07.5 | Close-up: pen drawing on an actual napkin, coffee cup edge in frame | Self-shot phone b-roll, 2 takes, top-down | User's own real napkin sketch held up to camera (photo works) |
| 03 | 0:07.5–0:10.5 | Same napkin, hand slides it across table toward a second person's hands | Same phone session | Freeze on sketch + subtle push-in |
| 04 | 0:10.5–0:13.5 | Phone notification mock: "Payment received" | Simple graphic overlay | Big kinetic caption "PAID" on black |
| 05 | 0:13.5–0:19 | Return to napkin sketch, slow push-in; CTA captions land line-by-line | Reuse shot 02 footage | Static sketch photo with punch-in on "solve their problem" |

New-shoot burden: one 10-minute phone session at a table (hands only, no faces — consistent with "no fake AI faces / no stock" constraints). Everything else is text/graphics built in the editor.

### Editing rhythm

- 0:00–0:03.5: hold on hook caption; strike-through lands exactly on "perfect."
- 0:03.5–0:10.5: two cuts only; let the drawing hand move — motion carries retention.
- 0:10.5–0:13.5: hard cut + 0.3s beat of silence before "She paid me" for impact.
- 0:13.5–0:19: slow down; captions land per phrase, final line holds 1.5s past VO end.

### Graphics / text plan

- Full word-level captions, bold sans, white with black stroke, centered in middle 60% of the 9:16 frame (clear of Reels UI top ~10% / bottom ~25% — assumed safe zones).
- Emphasis words: "napkin sketch" (highlight), "paid" (scale punch), "Stop" / "Start" (color contrast pair).
- One graphic only: payment notification at 0:10.5. No other decoration.

### Asset list

- Have: voiceover, transcript.
- Need: 2 phone clips of napkin drawing (or 1 photo of a real sketch), payment-notification overlay, caption styling.
- Missing: nothing blocking — the photo alternative unblocks the whole edit.
- Music: low-key lo-fi bed at ~85 BPM, ducked −12 dB under voice, cuts out at 0:10.5.

### Next action

Record the 10-minute napkin b-roll session (or photograph an existing sketch), then drop the voiceover into CapCut and place the five shots against the beat map.

---

## What Default Mode would add

The full 17-section package: Media Intake Summary, Creative Brief, per-beat Narrative Spine with meaning/emotion/priority, a full Phase 4 board with every node type and data point shaped, full Visual Concept, second-by-second Emotional Arc, Scene Map with transitions and risks, per-shot safe-zone and lens notes, frame-by-frame Text Storyboard, timed Motion Graphics Plan, complete Caption Strategy, section-level Rhythm Plan, Sound Direction with sync points, full Asset Checklist, CapCut execution notes, Review Checklist, and the 15-point Final Delivery Package.

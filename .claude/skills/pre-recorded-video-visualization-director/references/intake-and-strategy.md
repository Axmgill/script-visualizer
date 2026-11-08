# Phases 1–3: Intake and Strategy

> **Reads from Phase 0.** Every fact here comes from the script context card (`previz/context.md`).
> Cite its IDs — `F1`, `C2`, `B4` — instead of restating the fact. Interpret a fact; never add one.

Read this file before producing output sections 1–3. Follow the output templates exactly. Phase 4 (the previsualization mind map) is in `references/mindmap-previz.md`.

## Input schema

Use whatever the user provides. If something is missing, make reasonable assumptions and label them.

- **PRE-RECORDED MEDIA** — Voiceover, interview, talking head, screen recording, raw footage, podcast clip, or existing edit.
- **TRANSCRIPT** — Exact words spoken, with timecodes if available.
- **DURATION** — Total length of the pre-recorded media or target final length.
- **PLATFORM** — TikTok, Instagram Reels, YouTube Shorts, LinkedIn, X, website, client presentation, internal training, etc.
- **ASPECT RATIO** — Default to 9:16 vertical for short-form social video. Use 16:9 horizontal for YouTube long-form, presentations, or client work unless specified.
- **TARGET AUDIENCE** — Who the video is for.
- **CREATIVE GOAL** — What the viewer should feel, understand, remember, or do.
- **TONE** — Energetic, calm, emotional, funny, serious, inspiring, raw, polished, cinematic, documentary, corporate, educational, etc.
- **VISUAL STYLE** — Handheld documentary, natural light, Arri Amira feel, 35mm lens, cinematic realism, fast-cut, MTV/TikTok energy, clean motion graphics, minimal text, bold captions, etc.
- **BRAND GUIDELINES** — Logo usage, colors, typography, safe zones, tone of voice, prohibited elements, sponsor/partner requirements.
- **AVAILABLE ASSETS** — Existing footage, b-roll, photos, logos, music, sound effects, screen recordings, AI-generated clips, captions, graphics, etc.
- **CONSTRAINTS** — No stock clichés, no fake-looking AI faces, no excessive transitions, must include logo, must fit platform UI safe zones, must be editable in Premiere Pro / After Effects / CapCut, etc.
- **EDITING SOFTWARE** — Adobe Premiere Pro, Adobe After Effects, CapCut, DaVinci Resolve, Final Cut Pro, etc.

## Phase 1 — Media Intake and Timecode Map

First, understand the pre-recorded material.

Do this:

- Read the transcript or described media.
- Identify the spoken segments.
- Break the audio/video into timecoded blocks.
- Mark pauses, emphasis words, emotional peaks, key statements, and natural cut points.
- If no timecodes are provided, estimate them based on normal speaking pace: approximately 2.5 to 3 words per second for conversational voiceover. When a transcript file exists, prefer `scripts/estimate_timecodes.py`; otherwise estimate inline. Mark all such timecodes ESTIMATED.
- Identify whether the source is: voiceover only, talking head only, interview, screen recording, raw footage, podcast clip, rough edit, or mixed media.

Output template:

```
MEDIA INTAKE SUMMARY
- Source type:
- Total estimated duration:
- Core message:
- Main speaker/subject:
- Emotional tone of delivery:
- Key spoken moments:
- Natural pause points:
- Words/phrases that deserve visual emphasis:
- Missing information:
- Assumptions made:
```

## Before Phase 2 — The Unclarity Scan

Read the script once for meaning, then read it again for what it *does not* say. A plan built on a
guess produces frames built on a fiction; a question costs ten seconds.

```
python3 scripts/scan_ambiguity.py transcript.txt
```

The helper flags candidate lines with timecodes and a severity — it cannot judge them, and it never
answers anything. You apply the protocol below.

### What counts as unclear, and must be asked

1. **Unfinished material** — placeholders, TODOs, `[link]`, "coming soon", "insert name here".
2. **Unsupported authority** — "studies show", "experts say", "they say", "everyone knows", with no
   source anywhere in the material.
3. **A quantity with no number** — "most people", "thousands of them", "a huge amount". The plan
   cannot design a figure the script never states.
4. **Media from another edit** — "as you can see", "the chart below", "like this one". If that
   footage or graphic is not in the package, the sentence has no visual and no meaning.
5. **A claim that fights another line** — two statements that cannot both be true, or a claim the
   video's own evidence undercuts. Only a human read finds these; the helper cannot.
6. **A missing handle** — no call to action, or a call to action pointing at something never named.
7. **A production fact the plan cannot invent** — rights to footage, paintings or music; a runtime
   cap; aspect ratio and platform; brand colours; whether a person on camera may be shown.
8. **Whose story it is** — first person with no identified speaker, or a "we" that could mean the
   speaker, the audience, or a whole industry.

### What is not unclear, and must never be asked

- Rhetorical questions, irony, deliberate mystery, a reveal being held back on purpose.
- An opinion marked as an opinion ("I think", "for me", "my guess").
- Anything the script answers two lines later.
- Anything the user's own brief or constraints already fix.
- Tone, audience or platform when the material or the brief already implies them.

Asking about these is worse than not asking: it tells the user the skill wasn't listening.

### Three severities

| Severity | What it changes | What you do |
|---|---|---|
| **BLOCKING** | the claim, the spine, or an anchor | must be answered or explicitly defaulted **before Phase 4** |
| **SHAPING** | a design or edit choice — a date, a baseline, a palette, a pace | ask, propose a default, and continue if it goes unanswered |
| **NOTE** | wording, hedge, or the script's own voice | never ask; mention at delivery only if it matters |

### How to ask

- **Batch it.** One message, blocking first, **five questions maximum** — seven in a whole session.
  Never drip-feed one question per turn.
- **Quote the sentence**, with its timecode. A question about "the tone" is unanswerable; a question
  about a specific line is answerable in three words.
- **Name what it blocks.** "This decides whether Phase 4 gets an anchor or an unresolved node."
- **Offer two or three candidate readings**, not an open field. The user corrects a guess far faster
  than they compose an answer.
- **Always attach the default**: "if you'd rather not decide, I'll treat it as X and mark it."
- **Offer the exit**: *"Reply 'defaults' and I'll build with the assumptions named."*
- **Ask once, up front.** After that, run to the end without interrupting unless a genuinely new
  blocker appears — no mid-plan quizzes.

### Never silently choose

If a blocking question goes unanswered you may still proceed, but the ambiguity must stay visible:

- the mind-map node stays `unresolved` with no invented `anchor` (see `mindmap-previz.md`);
- every frame that depends on the guess is labelled with the assumption;
- the assumption is carried into Phase 17.

A plan that names its guess is usable. A plan that hides one is a trap for whoever builds it.

### Output template

```
ASSUMPTIONS AND OPEN QUESTIONS

Read: <one or two lines on what the script is already clear about>

Blocking — answer these, or I default
B1. "<quoted line>"
    Timecode: <0:42, ESTIMATED if derived>
    Unclear: <what it cannot resolve to>
    Blocks: <Phase 3 claim / Phase 4 anchor / Phase 8 shot / Phase 14 rights>
    Options: (a) <reading> — <consequence for the plan>
             (b) <reading> — <consequence>
    If unanswered: <the exact default, and what stays marked unresolved>

Shaping — a default is enough
S1. "<quoted line>" (1:12) — <question>. Default: <default>.

Not asking, on purpose
- "<quoted line>" — rhetorical; the plan will not answer it.
- "<quoted line>" — already marked as the speaker's opinion.

If you reply "defaults": <one paragraph stating exactly what the plan will assume>
```

If the user's first message already answers everything, do not perform the questions — show the
template once with "answered" against each item, then move straight into Phase 2.

## Phase 2 — Creative Brief for the Pre-Recorded Video

Convert the raw material into a clear creative brief.

Output template:

```
CREATIVE BRIEF
- Video title/working title:
- Core message in one sentence:
- Target audience:
- Platform:
- Aspect ratio:
- Final duration target:
- Tone:
- Visual style:
- Emotional goal:
- Viewer takeaway:
- Call to action, if any:
- Brand constraints:
- Production constraints:
- Style references, if any:
```

## Phase 3 — Narrative Spine from the Recorded Audio

Do not invent a new story unless needed. Build the narrative from what was already recorded.

Do this:

- Divide the transcript into beats.
- Label each beat by function. Common beat functions: Hook, Problem, Promise, Context, Explanation, Proof, Example, Emotion, Transformation, Objection handled, Call to action, Payoff, Closing note.
- For each beat, identify the exact script line or time range, what the viewer needs to understand, what the viewer needs to feel, why this beat matters, and how long it should occupy on screen.

Output template:

```
NARRATIVE SPINE
Beat 1:
- Time range:
- Script line(s):
- Function:
- Meaning:
- Emotion:
- Visual purpose:
- Edit priority:

Beat 2:
...
```

Continue for all beats.

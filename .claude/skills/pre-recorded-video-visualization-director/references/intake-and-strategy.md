# Phases 1–4: Intake and Strategy

Read this file before producing output sections 1–4. Follow the output templates exactly.

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

## Phase 4 — Visual Concept for the Edit

Create the overall visual world for the pre-recorded video. This is not about shooting a new film unless b-roll is required. This is about how the existing recording will be presented.

Define: visual theme; use of original footage; use of b-roll; use of motion graphics; use of text/captions; use of archival or supporting media; camera feel if new b-roll is needed; lighting/color mood; editing energy; graphic style; sound atmosphere.

Output template:

```
VISUAL CONCEPT
- Concept title:
- One-line visual idea:
- How the original recording is used:
- How b-roll supports the message:
- How graphics support clarity:
- Camera style for any new/support footage:
- Lighting style:
- Color palette:
- Mood:
- Editing rhythm:
- Graphic style:
- Sound/music direction:
- Why this concept fits the recorded audio:
```

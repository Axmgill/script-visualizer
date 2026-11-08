# Modes and Interaction Style

## Interaction style

- Be supportive but not vague.
- Be direct but not cold.
- If the user is stuck, give options instead of only asking questions.
- If the user gives a partial transcript, expand it into a workable edit plan.
- If the user says "I don't know," provide three possible visual directions.
- If the user says "make it simpler," reduce it to a basic edit map.
- If the user says "make it more creative," push into unexpected but relevant visual metaphors.
- If the user says "this feels generic," replace clichés with specific, grounded, human details.
- Use short paragraphs and clear headings.
- Avoid overwhelming the user with unnecessary theory.
- Always connect suggestions back to the recorded audio.
- When you build the Phase 4 board, present the HTML file itself, not just a summary of it. Say what it is in one line: "Open this in a browser — drag the nodes, click one to see its visual idea."
- Offer one next move on the board ("want me to add the second stat, or merge the two proof branches?"), never a menu of five.

## Default output order

Unless the user requests otherwise, return the result in this order:

1. Media Intake Summary
2. Creative Brief
3. Narrative Spine
4. Previsualization Mind Map (node board)
5. Visual Concept
6. Emotional Arc
7. Scene Map
8. Shot / B-Roll Plan
9. Text Storyboard
10. Motion Graphics Plan
11. Caption and Text Strategy
12. Editing Rhythm Plan
13. Sound and Music Direction
14. Asset Checklist
15. Software Execution Notes
16. Review Checklist
17. Final Pre-Recorded Video Visualization Package

## Short Mode

Trigger: the user asks for a quick version. Compress the output to:

- Core message
- Mini mind map (core node + 5–8 connected nodes, built as a board if the user has a project folder) — including any abstract line and the anchor from the script that carries it, or a clear "no picture yet" note
- Visual concept
- Beat map
- Shot/b-roll plan
- Editing rhythm
- Graphics/text plan
- Asset list
- Next action

## Expert Mode

Trigger: the user asks for deep detail. Expand each phase with:

- alternative concepts
- visual references
- camera movement options
- transition options
- pacing variations
- A/B hook ideas
- retention risks
- emotional triggers
- production tradeoffs
- backup assets if primary visuals are unavailable

## Blank-Mind Rescue Mode

Trigger: the user seems confused, stuck, or unable to continue. Activate automatically.

Do this:

- Reduce the task to one small decision.
- Offer 3 simple choices.
- Use concrete examples.
- Avoid abstract questions.
- Give a starting sentence the user can react to.

Example:

> You do not need to solve the whole edit. Pick one opening visual:
> A) Start on the speaker's face with a bold caption.
> B) Start on hands doing the action while the voiceover plays.
> C) Start on a black screen with one powerful spoken word.
> Which one feels easiest?

## Example trigger commands

The user may invoke this skill with phrases such as:

- "Visualize this pre-recorded video"
- "Plan the edit for this voiceover"
- "Turn this transcript into a visual edit map"
- "Help me storyboard this recorded video"
- "What b-roll should I use for this audio?"
- "Make a caption and graphics plan for this recording"
- "I have a recorded video, help me see the final edit"
- "Map this voiceover to visuals"
- "Mind map this script"
- "Previz this script as a board"
- "Show me the structure of this script like a Miro board"
- "Build a production plan from this pre-recorded clip"

## Working on the board

The Phase 4 board is a living object, not a one-time diagram. Expect the user to react to it.

- **They want it rearranged:** drag positions live in the HTML; the JSON export from the board (`E`) gives coordinates to write back into `previz/mindmap.json`.
- **They want a node added, split, or cut:** edit the JSON, rebuild, and say which node ids changed.
- **They disagree with the argument's shape:** that is the useful conversation. A board where every claim hangs off one unproven assertion is worth flagging out loud.
- **A line is still unresolved:** do not solve it with a metaphor. Offer the two honest moves — name a concrete thing from their script that carries the line, or keep the beat image-free — and ask which they prefer only if the script truly gives nothing.
- **They ask for a visual anyway:** say plainly what it would cost. An image the script never justified argues something the script did not say, and the board is where that is cheapest to catch.
- **The script changes:** rebuild from the JSON rather than hand-editing the HTML, and note which downstream sections are now stale.
- **They only want the text version:** give the board sketch from section 4 and skip the HTML; do not pretend the file was built if it was not.

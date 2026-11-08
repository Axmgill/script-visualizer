#!/usr/bin/env python3
"""Scan a script or transcript for lines that cannot be visualised without a question.

Part of the pre-recorded-video-visualization-director skill (Phase 1, the
Unclarity Scan). It does not answer anything and it does not fix anything: it
finds the sentences a visual plan would have to guess at, quotes them with an
estimated timecode, and hands them to the agent as questions for the user.

Categories (severity in brackets):

  placeholder           TBD, [link], insert, XXX, your name       [BLOCKING]
  unsourced-authority   "studies show", "experts say", "they say"  [BLOCKING]
  implied-evidence      "as you can see", "the chart below"        [BLOCKING]
  unstated-figure       "most people", "thousands of them"         [BLOCKING]
  vague-time            "recently", "these days", "at some point"  [SHAPING]
  comparative-no-baseline "more than ever", "better than ever"     [SHAPING]
  deictic-opener        sentence opens with This/That/It/Which     [NOTE]
  question-in-script    a question mark                            [NOTE]
  hedge                 "I think", "probably", "sort of"           [NOTE]

BLOCKING items change the argument, the spine or an anchor, so they must be
answered or explicitly defaulted before the mind map (Phase 4) is built.
SHAPING items change a design or edit choice and can proceed on a stated
default. NOTE items are the script's own voice: they are reported so nobody
"fixes" a rhetorical question or a deliberate hedge, and they are never asked.

Usage:
  python3 scan_ambiguity.py transcript.txt
  python3 scan_ambiguity.py transcript.txt --format json --max 5
  python3 scan_ambiguity.py transcript.txt --strict   # exit 1 if BLOCKING found

No third-party dependencies. Python 3.8+.
"""

import argparse
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # leave the skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:  # captions carry real timecodes; reuse the Phase 1 parser instead of guessing
    from estimate_timecodes import parse_srt, parse_vtt
except Exception:  # pragma: no cover - the helper is optional
    parse_srt = parse_vtt = None

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])[\u201d\"')\]]*\s+")

# (key, label, severity, compiled regex, why it matters, question template)
DETECTORS = [
    (
        "placeholder",
        "placeholder text",
        "BLOCKING",
        re.compile(
            r"\b(?:TBD|TBC|XXX|insert (?:link|name|here)|your (?:link|name) here|coming soon)\b"
            r"|\[[^\]]{1,40}\]|\{\{[^}]{1,40}\}\}",
            re.IGNORECASE,
        ),
        "unfinished copy reaches the edit and becomes a caption nobody can ship.",
        "What should this say on screen, and in the voiceover?",
    ),
    (
        "unsourced-authority",
        "unsourced authority",
        "BLOCKING",
        re.compile(
            r"\b(studies|research|science|data|surveys?)\s+(show|shows|says|say|proves?|suggests?|found)\b"
            r"|\b(experts|scientists|researchers|historians|scholars|psychologists|doctors)\s+"
            r"(say|says|agree|believe|found|have found|warn|insist)\b"
            r"|\b(they|people)\s+say\b|\bwe(?:'re| are) told\b|\bit is said\b"
            r"|\baccording to (?:many|some|most)\b|\beveryone knows\b"
            r"|\bno one (?:tells|teaches|warns) you\b",
            re.IGNORECASE,
        ),
        "the plan would either invent the evidence or lean on a claim the video cannot show.",
        "You say <quote> — is there a source the visuals may cite, or should the plan treat this "
        "as your opinion and avoid implying evidence?",
    ),
    (
        "implied-evidence",
        "points at media the edit may not have",
        "BLOCKING",
        re.compile(
            r"\b(as|and) you can see\b|\byou(?:'ll| will)? see (?:here|below|in a second)\b"
            r"|\blook at this\b|\bwatch this\b"
            r"|\bin this (?:video|image|frame|chart|graphic|screenshot)\b"
            r"|\b(?:the|this) (?:chart|graph|image|screenshot|table|slide) (?:below|above|here)\b"
            r"|\bas (?:shown|I showed|we showed)\b|\blike this one\b",
            re.IGNORECASE,
        ),
        "the line was written for another edit; if that footage is gone, the sentence has no visual and no meaning.",
        "For <quote> — does that footage or graphic still exist, or was this written for a different cut?",
    ),
    (
        "unstated-figure",
        "quantity with no number",
        "BLOCKING",
        re.compile(
            r"\b(most|many|a lot of|lots of|countless|millions|billions|thousands|hundreds|dozens)"
            r"\s+(?:of\s+)?(?:the\s+)?(people|users|viewers|creators|writers|students|companies|"
            r"businesses|men|women|kids|teams|founders|artists|us|them)\b"
            r"|\b(millions|billions|thousands|hundreds|dozens|countless)\s+of\b"
            r"|\bthe majority of\b|\ba (?:huge|large|growing) (?:number|amount|share)\b",
            re.IGNORECASE,
        ),
        "a number cannot be designed if the script never states it, and a chart here would be invented.",
        "Is there a real figure for <quote>, or should the frame carry the idea without a number?",
    ),
    (
        "vague-time",
        "vague time reference",
        "SHAPING",
        re.compile(
            r"\b(recently|lately|these days|back then|at some point|a while ago|"
            r"in recent years|not long ago|nowadays)\b",
            re.IGNORECASE,
        ),
        "time on screen means something: a date, a span, or a deliberate blur.",
        "For <quote> — do you want a real date on screen, a span, or should it stay deliberately vague?",
    ),
    (
        "comparative-no-baseline",
        "comparison with nothing to compare to",
        "SHAPING",
        re.compile(r"\b(more than ever|than ever before|better than ever|worse than ever)\b", re.IGNORECASE),
        "a comparison needs a baseline before a frame can show one.",
        "For <quote> — compared to what, specifically? Or should the line stay as feeling, with no graphic?",
    ),
    (
        "deictic-opener",
        "opens on a word that points backwards",
        "NOTE",
        re.compile(r"^(this|that|it|these|those|which|such)\b", re.IGNORECASE),
        "usually resolved by the previous line — check the antecedent before designing, do not ask by reflex.",
        None,
    ),
    (
        "question-in-script",
        "question in the script",
        "NOTE",
        re.compile(r"\?$"),
        "questions are often rhetorical; the plan must not answer them on the viewer's behalf.",
        None,
    ),
    (
        "hedge",
        "hedge",
        "NOTE",
        re.compile(
            r"\b(I think|I guess|I suppose|probably|maybe|sort of|kind of|apparently|"
            r"seems like|it seems|or something|somehow|might be|I feel like)\b",
            re.IGNORECASE,
        ),
        "hedges carry the speaker's stance; they are voice, not a gap in the material.",
        None,
    ),
]

SEVERITY_ORDER = {"BLOCKING": 0, "SHAPING": 1, "NOTE": 2}


def fmt_ts(seconds):
    seconds = int(round(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def strip_timecodes(text):
    """Remove SRT/VTT cue numbers, arrows and tags so only speech remains."""
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*WEBVTT.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}", "", text)
    text = re.sub(r"<[^>]{1,20}>", "", text)
    return text


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]


def count_words(sentence):
    return len(re.findall(r"[A-Za-z0-9']+", sentence))


def scan(sentences, wps, sentence_pause, per_category=3, times=None, total_seconds=None):
    """Return findings with start times and the preceding sentence.

    ``times`` (one entry per sentence) supplies real caption timecodes; without it
    every timecode is estimated from word count at ``wps``.
    """
    findings = []
    seen = set()
    elapsed = 0.0
    previous = ""
    for index, sentence in enumerate(sentences):
        real = times[index] if times is not None and index < len(times) else None
        start = real if real is not None else elapsed
        if real is None:
            elapsed += count_words(sentence) / wps + sentence_pause
        for key, label, severity, pattern, why, question in DETECTORS:
            match = pattern.search(sentence)
            if not match:
                continue
            key_dedupe = (key, sentence.lower())
            if key_dedupe in seen:
                continue
            seen.add(key_dedupe)
            findings.append(
                {
                    "id": None,
                    "category": key,
                    "label": label,
                    "severity": severity,
                    "sentence_index": index,
                    "start": round(start, 2),
                    "timecode": fmt_ts(start),
                    "quote": sentence,
                    "matched": match.group(0),
                    "context": previous,
                    "why": why,
                    "ask": question,
                }
            )
        previous = sentence

    # keep the first few of each category so one repeated tic cannot flood the list
    if per_category > 0:
        kept, tally = [], {}
        for finding in sorted(findings, key=lambda f: f["sentence_index"]):
            tally[finding["category"]] = tally.get(finding["category"], 0) + 1
            if tally[finding["category"]] <= per_category:
                kept.append(finding)
        findings = kept

    findings.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["sentence_index"]))
    counters = {"BLOCKING": 0, "SHAPING": 0, "NOTE": 0}
    for finding in findings:
        counters[finding["severity"]] += 1
        finding["id"] = f"{finding['severity'][0]}{counters[finding['severity']]}"
    if total_seconds is None:
        total_seconds = elapsed
    return findings, round(total_seconds, 2), counters


def render_markdown(findings, counters, total_seconds, source, wps):
    lines = ["# Unclarity scan", ""]
    real = source.lower().endswith((".srt", ".vtt"))
    timing = "real caption timecodes" if real else f"ESTIMATED at {wps} wps"
    lines.append(f"Source: `{source}` · duration ≈ {fmt_ts(total_seconds)} ({timing})")
    lines.append("")
    verdict = (
        f"{counters['BLOCKING']} blocking, {counters['SHAPING']} shaping, {counters['NOTE']} note"
    )
    lines.append(f"**Verdict:** {verdict}")
    lines.append("")
    if counters["BLOCKING"]:
        lines.append(
            "Ask the blocking questions before Phase 4. If the user does not answer, proceed only "
            "with a stated default, and keep the affected line visibly unresolved on the board."
        )
    elif findings:
        lines.append(
            "Nothing blocks the argument. Ask at most the shaping questions, with a default offered "
            "for each, then build."
        )
    else:
        lines.append("Nothing flagged. Build, and do not invent questions to look thorough.")
    lines.append("")

    for severity, heading in (
        ("BLOCKING", "Blocking — answer or default before the mind map"),
        ("SHAPING", "Shaping — ask, but a default is enough to proceed"),
        ("NOTE", "Note — the script's own voice, never ask"),
    ):
        group = [f for f in findings if f["severity"] == severity]
        if not group:
            continue
        lines.append(f"## {heading}")
        lines.append("")
        for finding in group:
            lines.append(f"### {finding['id']} · {finding['timecode']} · {finding['label']}")
            lines.append("")
            lines.append(f"> {finding['quote']}")
            lines.append("")
            if finding["context"]:
                lines.append(f"*Previous line:* {finding['context']}")
                lines.append("")
            lines.append(f"**Why it matters:** {finding['why']}")
            lines.append("")
            if finding["ask"]:
                ask = finding["ask"].replace("<quote>", f"“{finding['matched']}”")
                lines.append(f"**Ask:** {ask}")
                lines.append("")
                if severity == "BLOCKING":
                    lines.append(
                        "**If unanswered:** no invented evidence, no chart, no number — mark the "
                        "anchor unresolved and say so in the delivery package."
                    )
                else:
                    lines.append("**If unanswered:** state the assumption and continue.")
                lines.append("")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "This scan is a prompt generator, not a verdict. Deliberate ambiguity (a rhetorical "
        "question, a held-back fact, a plain opinion) is the script working, not a defect — leave "
        "it alone and never ask about it."
    )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("input", help="Transcript or script (.txt/.md/.srt/.vtt) or - for stdin")
    parser.add_argument("--wps", type=float, default=2.75, help="Words per second (default 2.75)")
    parser.add_argument(
        "--sentence-pause", type=float, default=0.3, help="Pause between sentences (default 0.3)"
    )
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--max", type=int, default=0, help="Cap findings shown (0 = all)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when any BLOCKING finding exists (useful in a pipeline)",
    )
    args = parser.parse_args(argv)

    if args.input == "-":
        raw = sys.stdin.read()
        source = "stdin"
    else:
        with open(args.input, "r", encoding="utf-8") as handle:
            raw = handle.read()
        source = args.input

    sentences, times, total_seconds = [], [], None
    lower = args.input.lower()
    if args.input != "-" and parse_srt and lower.endswith((".srt", ".vtt")):
        blocks = parse_vtt(raw) if lower.endswith(".vtt") else parse_srt(raw)
        if blocks:
            for block in blocks:
                block_sentences = split_sentences(block["text"])
                words = sum(count_words(s) for s in block_sentences) or 1
                spoken = 0
                for sentence in block_sentences:
                    sentences.append(sentence)
                    times.append(round(block["start"] + (spoken / words) * max(block["end"] - block["start"], 0), 2))
                    spoken += count_words(sentence)
            total_seconds = blocks[-1]["end"]
    if not sentences:
        sentences = split_sentences(strip_timecodes(raw))
        times = None

    findings, total_seconds, counters = scan(
        sentences, args.wps, args.sentence_pause, times=times, total_seconds=total_seconds
    )

    if args.max > 0:
        findings = findings[: args.max]

    if args.format == "json":
        payload = {
            "source": source,
            "sentences": len(sentences),
            "estimated_seconds": total_seconds,
            "timecodes": "caption" if source.lower().endswith((".srt", ".vtt")) else "estimated",
            "counts": counters,
            "findings": findings,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(findings, counters, total_seconds, source, args.wps))

    if args.strict and counters["BLOCKING"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

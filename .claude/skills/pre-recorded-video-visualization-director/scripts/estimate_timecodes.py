#!/usr/bin/env python3
"""Estimate or extract a timecoded block map from a transcript.

Part of the pre-recorded-video-visualization-director skill (Phase 1).

Inputs:
  - Plain text (.txt / .md / stdin): timing is ESTIMATED from word count at
    --wps words per second (default 2.75, the midpoint of the 2.5-3 wps
    conversational range). Sentence ends add a small pause; blank lines add
    a longer beat.
  - SubRip (.srt) or WebVTT (.vtt): REAL timecodes are parsed and preserved.

Outputs a block map as Markdown (--format md, default) or JSON
(--format json). Blocks are split on sentence boundaries, then merged or
split toward --target-block-words so blocks stay usable as edit beats.

Usage:
  python3 estimate_timecodes.py transcript.txt --wps 2.75 --format md
  python3 estimate_timecodes.py captions.srt --format json
  cat transcript.txt | python3 estimate_timecodes.py - --format md

No third-party dependencies. Python 3.8+.
"""

import argparse
import json
import re
import sys

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])[\u201d\"')\]]*\s+")
SRT_TIME = re.compile(
    r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*"
    r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})"
)
VTT_TIME = re.compile(
    r"(?:(\d{1,2}):)?(\d{2}):(\d{2})[.,](\d{1,3})\s*-->\s*"
    r"(?:(\d{1,2}):)?(\d{2}):(\d{2})[.,](\d{1,3})"
)


def word_count(text):
    return len(re.findall(r"\S+", text))


def fmt_ts(seconds):
    """Format seconds as M:SS.d (tenths), the working precision of an edit plan."""
    minutes = int(seconds // 60)
    secs = seconds - minutes * 60
    return f"{minutes}:{secs:04.1f}"


def split_sentences(paragraph):
    parts = SENTENCE_SPLIT.split(paragraph.strip())
    return [p.strip() for p in parts if p.strip()]


def rebalance(sentences, target_words):
    """Merge tiny sentences and split huge ones toward target block size."""
    blocks = []
    buf = ""
    for sentence in sentences:
        candidate = (buf + " " + sentence).strip() if buf else sentence
        if buf and word_count(candidate) > target_words * 1.5:
            blocks.append(buf)
            buf = sentence
        else:
            buf = candidate
    if buf:
        blocks.append(buf)

    final = []
    for block in blocks:
        words = block.split()
        if len(words) <= target_words * 2:
            final.append(block)
            continue
        # Split oversized run-on blocks at the target size.
        for i in range(0, len(words), target_words):
            final.append(" ".join(words[i : i + target_words]))
    return final


def estimate_blocks(text, wps, sentence_pause, paragraph_pause, target_words):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    blocks = []
    clock = 0.0
    for para in paragraphs:
        sentences = split_sentences(para.replace("\n", " "))
        for chunk in rebalance(sentences, target_words):
            duration = word_count(chunk) / wps
            blocks.append(
                {
                    "start": round(clock, 1),
                    "end": round(clock + duration, 1),
                    "text": chunk,
                    "words": word_count(chunk),
                    "estimated": True,
                }
            )
            clock += duration
            # Small breath after a sentence-final punctuation mark.
            if re.search(r"[.!?][\u201d\"')\]]*$", chunk):
                clock += sentence_pause
        clock += paragraph_pause
    return blocks


def _hms(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000.0


def parse_srt(text):
    blocks = []
    for chunk in re.split(r"\n\s*\n", text.strip()):
        lines = chunk.strip().splitlines()
        for i, line in enumerate(lines):
            match = SRT_TIME.search(line)
            if match:
                g = match.groups()
                blocks.append(
                    {
                        "start": round(_hms(*g[0:4]), 1),
                        "end": round(_hms(*g[4:8]), 1),
                        "text": " ".join(l.strip() for l in lines[i + 1 :] if l.strip()),
                        "estimated": False,
                    }
                )
                break
    return blocks


def parse_vtt(text):
    blocks = []
    for chunk in re.split(r"\n\s*\n", text.strip()):
        lines = chunk.strip().splitlines()
        for i, line in enumerate(lines):
            match = VTT_TIME.search(line)
            if match:
                h1, m1, s1, ms1, h2, m2, s2, ms2 = match.groups()
                blocks.append(
                    {
                        "start": round(_hms(h1 or 0, m1, s1, ms1), 1),
                        "end": round(_hms(h2 or 0, m2, s2, ms2), 1),
                        "text": " ".join(l.strip() for l in lines[i + 1 :] if l.strip()),
                        "estimated": False,
                    }
                )
                break
    return blocks


def render_markdown(blocks, timing_note):
    lines = [
        "# Timecoded Block Map",
        "",
        f"Timing: {timing_note}",
        "",
        "| # | Start | End | Words | Text |",
        "|---|-------|-----|-------|------|",
    ]
    for i, block in enumerate(blocks, 1):
        text = block["text"].replace("|", "\\|")
        lines.append(
            f"| {i:02d} | {fmt_ts(block['start'])} | {fmt_ts(block['end'])} "
            f"| {block.get('words', word_count(block['text']))} | {text} |"
        )
    if blocks:
        lines += ["", f"Total duration: {fmt_ts(blocks[-1]['end'])}"]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("input", help="Transcript file (.txt/.md/.srt/.vtt) or - for stdin")
    parser.add_argument("--wps", type=float, default=2.75,
                        help="Words per second for estimation (default 2.75; range 2.5-3)")
    parser.add_argument("--sentence-pause", type=float, default=0.3,
                        help="Seconds of pause after each sentence (default 0.3)")
    parser.add_argument("--paragraph-pause", type=float, default=0.7,
                        help="Extra seconds of pause between paragraphs (default 0.7)")
    parser.add_argument("--target-block-words", type=int, default=18,
                        help="Preferred words per block (default 18)")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    args = parser.parse_args(argv)

    if args.wps <= 0:
        parser.error("--wps must be positive")

    if args.input == "-":
        text = sys.stdin.read()
        ext = ".txt"
    else:
        try:
            with open(args.input, encoding="utf-8-sig") as handle:
                text = handle.read()
        except OSError as exc:
            parser.error(str(exc))
        ext = "." + args.input.rsplit(".", 1)[-1].lower() if "." in args.input else ".txt"

    if not text.strip():
        parser.error("input is empty")

    if ext == ".srt" or SRT_TIME.search(text):
        blocks = parse_srt(text)
        timing_note = "REAL timecodes parsed from SRT."
    elif ext == ".vtt" or text.lstrip().startswith("WEBVTT"):
        blocks = parse_vtt(text)
        timing_note = "REAL timecodes parsed from WebVTT."
    else:
        blocks = estimate_blocks(
            text, args.wps, args.sentence_pause, args.paragraph_pause,
            args.target_block_words,
        )
        timing_note = (
            f"ESTIMATED at {args.wps:g} words/second "
            f"(+{args.sentence_pause:g}s per sentence, "
            f"+{args.paragraph_pause:g}s per paragraph). Verify against the recording."
        )

    if not blocks:
        parser.error("no transcript blocks found")

    if args.format == "json":
        print(json.dumps({"timing": timing_note, "blocks": blocks}, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(blocks, timing_note))
    return 0


if __name__ == "__main__":
    sys.exit(main())

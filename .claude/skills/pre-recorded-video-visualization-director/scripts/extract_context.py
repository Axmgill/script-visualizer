#!/usr/bin/env python3
"""Pull the raw material out of a script, so the agent can build context before anything else.

Part of the pre-recorded-video-visualization-director skill (Phase 0, Script
Context). It decides nothing. It does not choose visuals, carriers, colours or
shots. It only collects what the script actually contains, in one place, with
timecodes, so the agent reads it once instead of guessing across seventeen
phases.

What it collects:

  figures      every number in the script — digits and number words — with the
               sentence it sits in and the word it counts
  amounts      vague quantities ("most people", "thousands") with no figure
  outside      claims that point outside the script: unsourced authority,
               media that may not exist, placeholders
  questions    questions in the script, with a reminder that most are the voice
               working and must not be answered
  vocabulary   the words the script repeats — the materials it gives you
  shape        length, sentence length, where the script is dense or thin
  unseen       the things this tool cannot see, listed so the agent reads for
               them: pronoun antecedents, contradictions, withheld things, tone

Usage:
  python3 extract_context.py script.txt
  python3 extract_context.py script.txt --json        # machine-readable
  python3 extract_context.py script.txt --wps 2.6     # slower speaker

No third-party dependencies. Python 3.8+.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_ambiguity import count_words, fmt_ts, split_sentences, strip_timecodes  # noqa: E402

WPS = 2.75
SENTENCE_PAUSE = 0.3
PARAGRAPH_PAUSE = 0.7

DIGIT = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?![\w])")
NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    "hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000,
    "half": 0.5, "third": 0.33, "quarter": 0.25, "twice": 2, "double": 2, "triple": 3,
}
VAGUE = re.compile(
    r"\b(most|many|some|few|several|a lot|loads|plenty|hundreds|thousands|millions|"
    r"billions|dozens|majority|minority|almost all|nearly all|the vast majority)\b",
    re.I,
)
AUTHORITY = re.compile(
    r"\b(studies|study|research|researchers|scientists|experts|psychologists|"
    r"economists|doctors|surveys|statistics|data shows|figures show|reportedly)\b",
    re.I,
)
MEDIA = re.compile(
    r"\b(as you can see|you can see|behind me|in the (wide|close)[- ]?(shot|up)|"
    r"the (chart|graph|screen|slide|image|photo|clip|footage) (below|above|here)|"
    r"watch this|look at this|this picture|this image|this footage)\b",
    re.I,
)
PLACEHOLDER = re.compile(
    r"(\[[^\]]*\]|\{[^}]*\}|TBD|TBC|TODO|XXX|insert (?:link|name|handle|url|date)|"
    r"your (?:name|handle|url)|link below|linked below|in the description|"
    r"full breakdown|link in bio)",
    re.I,
)
STOP = set("""a about above after again all am an and any are as at be because been before
being below between both but by can did do does doing down during each few for from further
had has have having he her here hers herself him himself his how i if in into is it its itself
just me more most my myself no nor not now of off on once only or other our ours ourselves out
over own same she should so some such than that the their theirs them themselves then there these
they this those through to too under until up very was we were what when where which while who
whom why will with would you your yours yourself yourselves just like really thing things got get
like time know said say going want one""".split())

SHAPE = re.compile(r"[.!?]\s|[.!?]$")


def sentences_with_times(text, wps=WPS):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, t = [], 0.0
    for pi, para in enumerate(paras):
        for s in split_sentences(para):
            dur = max(0.6, count_words(s) / wps)
            out.append({"text": s, "start": t, "end": t + dur, "paragraph": pi})
            t += dur + SENTENCE_PAUSE
        t += PARAGRAPH_PAUSE
    return out, t


def unit_after(sentence, match_end):
    """The word the figure counts: "eleven months", "forty boxes", "four in the afternoon"."""
    tail = re.split(r"[,;:.!?—]", sentence[match_end:match_end + 44])[0]
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", tail)
    skip = {"the", "a", "an", "of", "in", "at", "per", "on", "for", "and", "to", "later", "or"}
    out = []
    for w in words:
        low = w.lower()
        if low in skip:
            continue
        if low in STOP:
            break
        out.append(w)
        break
    return " ".join(out)


# A compound like "four hundred" or "twenty-two" is one figure, not three.
COMPOUND = re.compile(
    r"\b((?:" + "|".join(NUMBER_WORDS) + r")[\s-]+(?:hundred|thousand|million|billion))\b",
    re.I,
)
HYPHEN_NUM = re.compile(
    r"\b(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)[-\s]"
    r"(one|two|three|four|five|six|seven|eight|nine)\b",
    re.I,
)
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
UNITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
         "six": 6, "seven": 7, "eight": 8, "nine": 9}
RATIO = re.compile(
    r"\b((?:one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:in|out of|per)\s+"
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|\d+))\b",
    re.I,
)
WORDNUM = re.compile(r"\b(" + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + r")\b", re.I)
# These read as ordinary words, not amounts.
NOT_A_FIGURE = re.compile(
    r"(one (thing|another|other|day|night|of|more|side|half)|no one|any one|"
    r"every one|some one|the one|(a|the|next) (second|third) time|"
    r"(second|third|quarter|half) (time|day|place|half)|a quarter (past|to))",
    re.I,
)


def figures(sents):
    rows = []
    for s in sents:
        text = s["text"]
        taken = []

        def free(a, b):
            return all(b <= x or a >= y for x, y in taken)

        def add(a, b, label, digits=False):
            if not free(a, b):
                return
            taken.append((a, b))
            rows.append({
                "time": fmt_ts(s["start"]),
                "_at": a,
                "figure": label,
                "unit": "" if not digits else unit_after(text, b),
                "sentence": text,
            })

        for m in HYPHEN_NUM.finditer(text):
            if not free(m.start(), m.end()):
                continue
            value = TENS[m.group(1).lower()] + UNITS[m.group(2).lower()]
            taken.append((m.start(), m.end()))
            rows.append({"time": fmt_ts(s["start"]), "_at": m.start(),
                         "figure": str(value), "unit": unit_after(text, m.end()),
                         "sentence": text})
        for m in RATIO.finditer(text):
            if NOT_A_FIGURE.search(m.group(1)):
                continue
            add(m.start(), m.end(), " ".join(m.group(1).split()))
        for m in COMPOUND.finditer(text):
            words = re.findall(r"[A-Za-z]+", m.group(1).lower())
            value = 0
            for w in words:
                v = NUMBER_WORDS.get(w, 0)
                value = value + v if v >= 1000 else (value or 1) * v if v >= 100 else value + v
            add(m.start(), m.end(), str(value) if value else m.group(1),
                digits=True)
        for m in DIGIT.finditer(text):
            add(m.start(), m.end(), m.group(1), digits=True)
        start_of_sentence_rows = len(rows)
        for m in WORDNUM.finditer(text):
            if NOT_A_FIGURE.search(text[max(0, m.start() - 12):m.end() + 16]):
                continue
            w = m.group(1).lower()
            after = text[m.end():m.end() + 22].lower()
            if w in ("third", "quarter"):
                if not re.match(r"\s+(of|the)\b", after):
                    continue
            elif w == "half":
                if not re.match(r"\s+(of|the|a|an)\b", after):
                    continue
            elif w in ("twice", "double", "triple"):
                if not re.match(r"\s+(as|the|its|what)\b", after):
                    continue
            add(m.start(), m.end(), w, digits=True)
        rows[start_of_sentence_rows:] = sorted(
            rows[start_of_sentence_rows:], key=lambda r: r["_at"])
    for r in rows:
        r.pop("_at", None)
    return rows


def collect(text, sents):
    amounts, outside, questions = [], [], []
    for s in sents:
        t = fmt_ts(s["start"])
        for m in VAGUE.finditer(s["text"]):
            amounts.append({"time": t, "phrase": m.group(1), "sentence": s["text"]})
            break
        for m in AUTHORITY.finditer(s["text"]):
            outside.append({"time": t, "kind": "unsourced authority",
                            "phrase": m.group(1), "sentence": s["text"]})
            break
        for m in MEDIA.finditer(s["text"]):
            outside.append({"time": t, "kind": "points at media",
                            "phrase": m.group(1), "sentence": s["text"]})
            break
        for m in PLACEHOLDER.finditer(s["text"]):
            outside.append({"time": t, "kind": "placeholder",
                            "phrase": m.group(1), "sentence": s["text"]})
            break
        if "?" in s["text"]:
            questions.append({"time": t, "sentence": s["text"]})
    return amounts, outside, questions


def vocabulary(text, limit=24):
    counts, first_line = {}, {}
    for i, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"[A-Za-z][A-Za-z'-]+", line):
            w = m.group(0).lower()
            if len(w) < 4 or w in STOP:
                continue
            counts[w] = counts.get(w, 0) + 1
            first_line.setdefault(w, i)
    rows = [{"word": w, "times": c, "line": first_line[w]}
            for w, c in counts.items() if c > 1]
    rows.sort(key=lambda r: (-r["times"], r["word"]))
    return rows[:limit]


def shape(text, sents):
    words = count_words(text)
    lens = [count_words(s["text"]) for s in sents]
    longest = max(sents, key=lambda s: count_words(s["text"])) if sents else None
    return {
        "words": words,
        "sentences": len(sents),
        "paragraphs": len([p for p in re.split(r"\n\s*\n", text) if p.strip()]),
        "mean_sentence": round(sum(lens) / len(lens), 1) if lens else 0,
        "longest": {"words": count_words(longest["text"]) if longest else 0,
                    "time": fmt_ts(longest["start"]) if longest else "0:00",
                    "sentence": longest["text"] if longest else ""},
    }


def build(text, wps=WPS):
    clean = strip_timecodes(text)
    sents, total = sentences_with_times(clean, wps)
    figs = figures(sents)
    amounts, outside, questions = collect(clean, sents)
    return {
        "words": count_words(clean),
        "seconds": round(total),
        "wps": wps,
        "figures": figs,
        "amounts": amounts,
        "outside": outside,
        "questions": questions,
        "vocabulary": vocabulary(clean),
        "shape": shape(clean, sents),
        "sentences": [{"time": fmt_ts(s["start"]), "text": s["text"]} for s in sents],
    }


def render_markdown(d, source):
    L = []
    a = L.append
    a("# Script context — raw material")
    a("")
    a(f"**Source:** `{source}` · {d['words']} words · about "
      f"{d['seconds'] // 60}:{d['seconds'] % 60:02d} at {d['wps']} words per second (ESTIMATED)")
    a("")
    a("This page only collects. It makes no visual decision. Read it, fill in the last")
    a("column, and let every later step point back to an ID here.")
    a("")

    a("## 1. Every figure")
    a("")
    if d["figures"]:
        a("| ID | Time | Figure | Counts | The sentence | What the sentence does with it |")
        a("|---|---|---|---|---|---|")
        for i, f in enumerate(d["figures"], 1):
            sent = f["sentence"].replace("|", "/")
            if len(sent) > 90:
                sent = sent[:87].rstrip() + "…"
            a(f"| F{i} | {f['time']} | {f['figure']} | {f['unit'] or '—'} | {sent} | — |")
        a("")
        a("The last column is yours. Write one short line: what the sentence is doing with the")
        a("number. Not a picture yet. A job description. The carrier comes after that line, in")
        a("`references/script-context.md`.")
    else:
        a("No figures in this script. Nothing to draw. Do not add any.")
    a("")

    a("## 2. Amounts with no number")
    a("")
    if d["amounts"]:
        for x in d["amounts"]:
            a(f"- **{x['time']}** · “{x['phrase']}” · {x['sentence'][:120]}")
        a("")
        a("The script says *how many* without saying *a number*. These are questions for the")
        a("writer, or an honest “unnamed amount” on screen. Never a made-up figure.")
    else:
        a("None.")
    a("")

    a("## 3. Claims that point outside the script")
    a("")
    if d["outside"]:
        a("| Time | Kind | Words | Sentence |")
        a("|---|---|---|---|")
        for x in d["outside"]:
            sent = x["sentence"].replace("|", "/")
            if len(sent) > 90:
                sent = sent[:87].rstrip() + "…"
            a(f"| {x['time']} | {x['kind']} | “{x['phrase']}” | {sent} |")
        a("")
        a("Each of these is a place where a visual plan would invent something: a study, a shot,")
        a("a link. They go to the user as questions, once, with a default.")
    else:
        a("None found. Check by eye anyway.")
    a("")

    a("## 4. Questions the script asks")
    a("")
    if d["questions"]:
        for q in d["questions"]:
            a(f"- **{q['time']}** · {q['sentence']}")
        a("")
        a("Most of these are the script working, not a gap. **Do not answer them on screen.**")
    else:
        a("None.")
    a("")

    a("## 5. The script's own vocabulary")
    a("")
    a("Words the script repeats. These are materials: objects, places, acts, people. If a")
    a("visual is not built from these, it is built from somewhere else.")
    a("")
    if d["vocabulary"]:
        a("| Word | Times | First line |")
        a("|---|---|---|")
        for v in d["vocabulary"]:
            a(f"| {v['word']} | {v['times']} | {v['line']} |")
    else:
        a("No word repeats. That itself is a problem worth noticing: the script may be all")
        a("abstraction, with nothing in it to film.")
    a("")

    s = d["shape"]
    a("## 6. Shape")
    a("")
    a(f"- {s['words']} words · {s['sentences']} sentences · {s['paragraphs']} paragraphs")
    a(f"- mean sentence: {s['mean_sentence']} words")
    if s["longest"]["words"]:
        a(f"- longest: {s['longest']['words']} words at {s['longest']['time']} — “{s['longest']['sentence'][:100]}”")
    a("")

    a("## 7. What this tool cannot see")
    a("")
    a("Read the script for these yourself. No script can find them:")
    a("")
    a("- **A pronoun with no owner.** “She signed off on every one of them.” Who is she?")
    a("- **Two facts that disagree.** A date said twice, two ways.")
    a("- **Something the script says it will not tell you.** That is a promise, not a gap.")
    a("- **The tone.** Dry, angry, tired, delighted. Only reading finds this.")
    a("- **What the domain invites and the script does not earn.** A script about locks will")
    a("  pull you toward keys. Check whether the script ever says key.")
    a("")
    a("Every one of those belongs in the context card, not in a later guess.")
    a("")
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="Collect script context. Decide nothing.")
    p.add_argument("source")
    p.add_argument("--wps", type=float, default=WPS)
    p.add_argument("--json", action="store_true")
    p.add_argument("-o", "--out")
    args = p.parse_args(argv)

    text = open(args.source, encoding="utf-8").read()
    d = build(text, args.wps)
    body = json.dumps(d, indent=2, ensure_ascii=False) if args.json else render_markdown(d, args.source)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(body)
        print(f"wrote {args.out} · {len(d['figures'])} figures · {len(d['outside'])} outside claims")
    else:
        print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())

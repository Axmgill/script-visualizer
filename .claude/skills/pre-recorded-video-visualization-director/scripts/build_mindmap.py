#!/usr/bin/env python3
"""Build a self-contained previsualization mind-map board from a node graph.

Part of the pre-recorded-video-visualization-director skill (Phase 4).

The board is a single HTML file with no dependencies: nodes can be dragged,
the canvas pans and zooms, connections are drawn as curves, data points render
their metaphor graphic, and the timecode track sits under the canvas.

Usage
-----
    # Validate only
    python3 scripts/build_mindmap.py nodes.json --check

    # Build a board next to the JSON
    python3 scripts/build_mindmap.py nodes.json

    # Build somewhere specific
    python3 scripts/build_mindmap.py nodes.json -o previz/mindmap.html

    # Dark board
    python3 scripts/build_mindmap.py nodes.json --theme dark

    # Check that abstract lines are anchored to material in the transcript
    python3 scripts/build_mindmap.py nodes.json --script transcript.txt --check

Input format
------------
{
  "title": "The Napkin Proof",
  "subtitle": "Instagram Reels · 0:19 · 9:16",
  "source": {"platform": "Instagram Reels", "aspect": "9:16",
             "duration": "0:19", "estimated": true},
  "theme": "light",
  "nodes": [
    {
      "id": "core",
      "label": "Proof of skill beats presentation polish",
      "type": "core",
      "time": "0:00-0:19",
      "function": "Core message",
      "emotion": "relief",
      "visual": "One continuous real-world tabletop moment",
      "summary": "What the whole edit has to prove.",
      "form": "",     # type "stat": the physical thing on screen that carries the number (or "")
      "chart": null,  # type "stat": OR a data visualisation, as {"what": ..., "why": ...}
      "carrier": "",  # type "stat": OR "type" when the figure is simply set and held
      "stat": null,   # type "stat": OPTIONAL schematic preview of the form or chart
      "x": 0, "y": 0
    }
  ],
  "edges": [
    {"from": "core", "to": "hook", "rel": "flows", "label": "opens with"}
  ]
}

Node types: core, hook, claim, proof, stat, example, emotion, visual,
objection, cta, risk, note, abstract.

An "abstract" node is a line with no literal image. Its `anchor` must quote
something the script already contains (an object, place, time, action, number
or repeated phrase); the visual is a treatment of that anchor, never an
imported metaphor. Set "anchor": "" to mark a line deliberately unresolved —
the board will show it as having no picture yet.
Relation types: supports, proves, expands, contrasts, callback, blocks,
flows, inspires.
A number on screen is carried by something. There are three carriers and the
script decides which one: an object it names ("form"), a data visualisation
("chart": {"what": what is being compared, "why": why a chart serves this
line}), or type alone ("carrier": "type", with the treatment in "visual").
A chart is a legitimate answer, not a fallback — what is rejected is a shape
chosen with no reason. The builder requires a reason ("why") next to every
chart, and requires every figure to exist in the script.

Stat display kinds (optional preview, never the finished look): dotgrid,
bars, line, proportion, fraction, compare, steps, counter.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

PLACEHOLDER = "__BOARD_DATA_JSON__"

NODE_TYPES = {
    "core", "hook", "claim", "proof", "stat", "example",
    "emotion", "visual", "objection", "cta", "risk", "note", "abstract",
}

# Words too common to prove that an anchor came from the script.
ANCHOR_STOPWORDS = {
    "the", "and", "that", "this", "with", "from", "they", "them", "their",
    "when", "what", "which", "your", "youre", "have", "has", "had", "was",
    "were", "will", "would", "could", "should", "about", "into", "over",
    "than", "then", "there", "these", "those", "been", "being", "because",
    "just", "like", "more", "most", "some", "such", "very", "only", "also",
    "does", "doesnt", "didnt", "isnt", "arent", "cant", "dont", "wont",
}

REL_TYPES = {
    "supports", "proves", "expands", "contrasts",
    "callback", "blocks", "flows", "inspires",
}

STAT_KINDS = {
    "dotgrid", "dots", "bars", "line", "chart", "proportion", "progress",
    "fraction", "ratio", "compare", "steps", "counter",
}

DEFAULT_TEMPLATE = (
    Path(__file__).resolve().parent.parent / "assets" / "mindmap-board.template.html"
)


class ValidationError(Exception):
    pass


def load_graph(path: Path) -> Dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationError(f"cannot read {path}: {exc}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"{path} is not valid JSON (line {exc.lineno}, column {exc.colno}): {exc.msg}"
        ) from exc

    if not isinstance(data, dict):
        raise ValidationError("the JSON root must be an object with 'nodes' and 'edges'")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValidationError("'nodes' must be a non-empty array")

    edges = data.get("edges", [])
    if edges is None:
        edges = []
    if not isinstance(edges, list):
        raise ValidationError("'edges' must be an array")

    data["edges"] = edges
    return data


def normalize_id(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def anchor_terms(anchor: str) -> List[str]:
    """Words in an anchor that must be traceable back to the script."""
    words = re.findall(r"[a-z0-9']+", anchor.lower())
    return [w for w in words if len(w) >= 4 and w not in ANCHOR_STOPWORDS]


def anchor_in_script(anchor: str, script_words: set, script_text: str) -> bool:
    """Loose containment check: an anchor word (or its stem) appears in the script."""
    terms = anchor_terms(anchor)
    if not terms:
        return True
    for term in terms:
        if term in script_words or term in script_text:
            return True
        stem = term[:5]
        for word in script_words:
            if len(word) >= 4 and (word.startswith(stem) or stem.startswith(word[:5])):
                return True
    return False


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
        "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def number_words(value: float) -> str:
    """Spell a whole number the way a script might say it (up to 9,999)."""
    n = int(value)
    if n < 20:
        return ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + (("-" + ONES[ones]) if ones else "")
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        return ONES[hundreds] + " hundred" + ((" and " + number_words(rest)) if rest else "")
    if n < 10000:
        thousands, rest = divmod(n, 1000)
        return number_words(thousands) + " thousand" + ((" " + number_words(rest)) if rest else "")
    return str(n)


def number_in_script(value: float, script_text: str, digits: set) -> bool:
    if isinstance(value, float) and not value.is_integer():
        return str(value) in script_text
    n = int(value)
    if str(n) in digits:
        return True
    if n == 0:
        return True
    words = number_words(n)
    spellings = {words}
    if words.startswith("one "):
        spellings.add(words[4:])          # "hundred" for "one hundred"
        spellings.add("a " + words[4:])   # "a hundred"
    return any(re.search(r"\b" + re.escape(w) + r"\b", script_text) for w in spellings)


def stat_numbers(node: Dict[str, Any]) -> List[float]:
    """Every figure a stat node puts on screen."""
    stat = node.get("stat") or {}
    out: List[float] = []
    for key in ("value", "total", "filled", "percent", "part", "whole"):
        v = stat.get(key)
        if isinstance(v, (int, float)) and v != 0:
            out.append(v)
    # `values` are relative bar heights on a schematic, not spoken claims — skip them.
    seen, unique = set(), []
    for v in out:
        if v not in seen:
            seen.add(v)
            unique.append(v)
    return unique


def check_numbers(nodes: List[Dict[str, Any]], script_text: str) -> List[str]:
    warnings: List[str] = []
    digits = set(re.findall(r"\d+(?:\.\d+)?", script_text))
    for node in nodes:
        if not isinstance(node, dict) or str(node.get("type", "")).lower() != "stat":
            continue
        for value in stat_numbers(node):
            if not number_in_script(value, script_text.lower(), digits):
                warnings.append(
                    f"node '{normalize_id(node.get('id'))}': the figure {value:g} does not appear in the "
                    "script \u2014 an invented number is the same failure as an invented anchor"
                )
    return warnings


def _norm_figure(token: str) -> str:
    """'41,000' -> '41000', '4.0' -> '4'. Keeps comparison simple."""
    t = token.replace(",", "").strip()
    try:
        v = float(t)
    except ValueError:
        return t.lower()
    return f"{v:g}"


def _figures_from_text(text: str) -> List[str]:
    """Reuse the Phase 0 extractor so both sides read figures the same way."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from extract_context import NUMBER_WORDS, figures as extract_figures  # noqa: WPS433
    except Exception:
        return []
    sents = [{"text": line, "start": 0.0}
             for line in re.split(r"(?<=[.!?])\s+|\n", text) if line.strip()]
    out: List[str] = []
    for row in extract_figures(sents):
        out.append(_norm_fig_token(row["figure"], NUMBER_WORDS))
    return [f for f in out if f]


def _norm_fig_token(token: str, number_words: Dict[str, float]) -> str:
    """'forty' -> '40', 'one in ten' -> '1:10', '400' -> '400'."""
    tok = token.strip().lower()
    if not tok:
        return ""
    if " in " in tok or " out of " in tok or " per " in tok:
        parts = re.split(r"\s+(?:in|out of|per)\s+", tok)
        return ":".join(_norm_fig_token(p, number_words) for p in parts if p)
    if re.fullmatch(r"\d[\d,]*(?:\.\d+)?", tok):
        return _norm_figure(tok)
    if tok in number_words:
        v = number_words[tok]
        return f"{int(v)}" if v >= 1 and float(v).is_integer() else f"{v:g}"
    return tok


def spoken_figures(node: Dict[str, Any]) -> List[str]:
    """The figures a stat node states to the viewer (not its schematic internals)."""
    out: List[str] = []
    stat = node.get("stat") or {}
    if isinstance(stat, dict):
        for key in ("value", "percent", "part", "whole"):
            v = stat.get(key)
            if isinstance(v, (int, float)) and v != 0:
                out.append(_norm_figure(f"{v:g}"))
    for key in ("label", "title", "text", "figure", "value"):
        v = node.get(key)
        if isinstance(v, str):
            for tok in _figures_from_text(v):
                out.append(tok)
            for tok in re.findall(r"\d[\d,]*(?:\.\d+)?", v):
                out.append(_norm_figure(tok))
    seen, unique = set(), []
    for v in out:
        if v and v not in seen:
            seen.add(v)
            unique.append(v)
    return unique


def ledger_figures(context_text: str) -> List[str]:
    """Read the Phase 0 figures ledger: the '| F1 | 0:00 | 41 boxes | ... |' rows."""
    section = context_text
    for start_marker in ("### 3. The figures ledger", "## 3. The figures ledger",
                         "Figures ledger", "figures ledger"):
        if start_marker in context_text:
            section = context_text.split(start_marker, 1)[1]
            break
    section = re.split(r"\n#{2,3} ", section, maxsplit=1)[0]
    out: List[str] = []
    for line in section.splitlines():
        if not re.match(r"\s*\|\s*F\d+\b", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        cell = cells[2]
        found = _figures_from_text(cell)
        if not found:
            found = [_norm_figure(t) for t in re.findall(r"\d[\d,]*(?:\.\d+)?", cell)]
        out.extend(found)
    return out


def check_context(nodes: List[Dict[str, Any]], context_text: str) -> List[str]:
    """The board may interpret the context card. It may not add to it."""
    warnings: List[str] = []
    ledger = ledger_figures(context_text)
    if not ledger:
        warnings.append(
            "the context file has no readable figures ledger (rows like '| F1 | 0:00 | 41 boxes | ... |') "
            "\u2014 the context check cannot run"
        )
        return warnings

    board: List[str] = []
    for node in nodes:
        if isinstance(node, dict) and str(node.get("type", "")).lower() == "stat":
            for fig in spoken_figures(node):
                board.append(fig)

    def covered(fig: str, pool: List[str]) -> bool:
        """A share '1:10' covers its own parts, and its parts cover it."""
        if fig in pool:
            return True
        if ":" in fig:
            return all(part in pool for part in fig.split(":") if part)
        return any(fig in tok.split(":") for tok in pool if ":" in tok)

    ledger_set, board_set = set(ledger), set(board)
    for node in nodes:
        if not isinstance(node, dict) or str(node.get("type", "")).lower() != "stat":
            continue
        for fig in spoken_figures(node):
            if not covered(fig, ledger):
                warnings.append(
                    f"node '{normalize_id(node.get('id'))}': the figure {fig} is on the board but "
                    "not on the Phase 0 figures ledger \u2014 a number that appears after the context "
                    "card came from the plan, not from the script"
                )
    missing = [f for f in ledger if not covered(f, board)]
    if missing:
        warnings.append(
            "the context ledger records figures the board never shows: "
            + ", ".join(dict.fromkeys(missing))
            + " \u2014 either the board is missing a beat, or the ledger has something it cannot carry"
        )
    return warnings


def check_anchors(nodes: List[Dict[str, Any]], script_text: str) -> List[str]:
    warnings: List[str] = []
    words = set(re.findall(r"[a-z0-9']+", script_text.lower()))
    for node in nodes:
        if not isinstance(node, dict):
            continue
        if str(node.get("type", "")).lower() != "abstract":
            continue
        anchor = str(node.get("anchor") or "").strip()
        if not anchor:
            continue
        if not anchor_in_script(anchor, words, script_text.lower()):
            warnings.append(
                f"node '{normalize_id(node.get('id'))}': the anchor \"{anchor}\" does not appear to come "
                "from this script \u2014 drive-by metaphors from outside the script's world are "
                "the thing this phase exists to prevent"
            )
    return warnings


def validate(data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Return (errors, warnings). Errors stop the build; warnings do not."""
    errors: List[str] = []
    warnings: List[str] = []

    nodes = data["nodes"]
    ids: Dict[str, Dict[str, Any]] = {}

    for index, node in enumerate(nodes):
        where = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{where}: must be an object")
            continue

        node_id = normalize_id(node.get("id"))
        if not node_id:
            errors.append(f"{where}: missing 'id'")
            continue
        if node_id in ids:
            errors.append(f"{where}: duplicate id '{node_id}'")
            continue
        ids[node_id] = node

        label = node.get("label") or node.get("title") or node.get("text")
        if not label or not str(label).strip():
            errors.append(f"node '{node_id}': missing 'label'")
        elif len(str(label)) > 140:
            warnings.append(
                f"node '{node_id}': label is {len(str(label))} chars — keep it under ~110 "
                "so the card stays readable"
            )

        node_type = str(node.get("type", "note")).lower().strip()
        if node_type not in NODE_TYPES:
            warnings.append(
                f"node '{node_id}': unknown type '{node_type}' — rendered as 'note'. "
                f"Known types: {', '.join(sorted(NODE_TYPES))}"
            )

        if "time" in node and node["time"] and not re.search(r"\d:\d{2}", str(node["time"])):
            warnings.append(
                f"node '{node_id}': time '{node['time']}' has no M:SS pattern — "
                "the timecode track will skip it"
            )

        stat = node.get("stat")
        if stat is not None:
            if not isinstance(stat, dict):
                warnings.append(f"node '{node_id}': 'stat' should be an object")
            else:
                kind = str(stat.get("display") or stat.get("kind") or "counter").lower()
                if kind not in STAT_KINDS:
                    warnings.append(
                        f"node '{node_id}': unknown stat display '{kind}' — "
                        f"use one of {', '.join(sorted(STAT_KINDS))}"
                    )
                if kind in ("dotgrid", "dots"):
                    total = stat.get("total", 100)
                    filled = stat.get("filled", 0)
                    if not isinstance(total, int) or total < 1:
                        warnings.append(f"node '{node_id}': dotgrid 'total' should be a positive integer")
                    elif total > 400:
                        warnings.append(
                            f"node '{node_id}': dotgrid total {total} exceeds 400 — "
                            "a grid that size reads as texture; find a real carrier or say the number in type"
                        )
                    if not isinstance(filled, int):
                        warnings.append(f"node '{node_id}': dotgrid 'filled' should be an integer")
                    elif isinstance(total, int) and 0 <= filled <= total and total >= 20:
                        ratio = filled / total
                        if 0 < ratio < 0.03:
                            warnings.append(
                                f"node '{node_id}': only {filled}/{total} dots are highlighted — "
                                "at card size that reads as empty; say the figure in type instead"
                            )

        if "anchor" in node and node["anchor"] is not None and not isinstance(node["anchor"], str):
            errors.append(f"node '{node_id}': 'anchor' must be a string")

        if node_type == "stat":
            form = str(node.get("form") or "").strip()
            chart = node.get("chart")
            has_chart = isinstance(chart, dict) and bool(chart)
            carrier = str(node.get("carrier") or "").strip().lower()
            type_only = carrier in {"type", "type-only", "typographic", "text"}

            if chart is not None and not isinstance(chart, dict):
                errors.append(
                    f"node '{node_id}': 'chart' must be an object like "
                    '{"what": "clients, Jan to Dec", "why": "the line says the count moved"}'
                )
                has_chart = False

            if not form and not has_chart and not type_only:
                errors.append(
                    f"node '{node_id}': this number has no carrier recorded. Say what it sits on \u2014 an "
                    "object from the script ('form'), a data visualisation ('chart') with the reason it "
                    "earns one, or \"carrier\": \"type\" when the honest answer is the figure set and held. "
                    "Any of the three can be right; what fails is a shape nobody decided on"
                )

            if has_chart:
                what = str(chart.get("what") or "").strip()
                why = str(chart.get("why") or "").strip()
                if not what:
                    errors.append(
                        f"node '{node_id}': the 'chart' block needs 'what' \u2014 what is being compared "
                        "or shown (a curve, a share, two totals, a count, a span)"
                    )
                if not why:
                    errors.append(
                        f"node '{node_id}': the 'chart' block needs 'why' \u2014 the part of the sentence "
                        "that makes a visualisation the right answer here. A chart with no reason is the "
                        "failure this rule exists to catch, not the chart itself"
                    )

            if node.get("stat") is not None and not isinstance(node.get("stat"), dict):
                errors.append(f"node '{node_id}': 'stat' is an optional preview and must be an object")
            if node.get("form") is not None and not isinstance(node.get("form"), str):
                errors.append(f"node '{node_id}': 'form' must be a string")

        if node_type == "abstract":
            anchor = str(node.get("anchor") or "").strip()
            if not anchor:
                # "anchor": "" is a deliberate decision; a missing key is usually an oversight.
                if "anchor" not in node:
                    warnings.append(
                        f"node '{node_id}' is abstract with no 'anchor' field. If the script really "
                        "contains nothing concrete, set \"anchor\": \"\" to mark it deliberately "
                        "unresolved; otherwise quote the thing in the script that carries the line"
                    )
            elif not str(node.get("visual") or "").strip():
                warnings.append(
                    f"node '{node_id}' has an anchor but no 'visual' \u2014 say how the anchor is treated on screen"
                )

        for key in ("visual", "summary", "emotion", "function"):
            if key in node and node[key] is not None and not isinstance(node[key], str):
                errors.append(f"node '{node_id}': '{key}' must be a string")

    stat_nodes = [n for n in nodes if isinstance(n, dict) and str(n.get("type", "")).lower() == "stat"]
    displays: Dict[str, List[str]] = {}
    for node in stat_nodes:
        display = (node.get("stat") or {}).get("display") if isinstance(node.get("stat"), dict) else None
        if display:
            displays.setdefault(str(display).lower(), []).append(normalize_id(node.get("id")))
    for display, display_ids in displays.items():
        if len(display_ids) > 1:
            warnings.append(
                f"nodes {', '.join(display_ids)} all use the '{display}' schematic \u2014 two different "
                "facts should not share one body unless the script repeats the same kind of count"
            )
    if len(stat_nodes) >= 2 and len(displays) and sum(len(v) for v in displays.values()) == len(stat_nodes):
        warnings.append(
            "every number in this board is drawn as a diagram. That is fine if the script really is about "
            "these relationships \u2014 check each line earns it, and that at least one of them is not "
            "better carried by an object the script already names (section 4 of mindmap-previz.md)"
        )

    core_nodes = [n for n in nodes if isinstance(n, dict) and str(n.get("type", "")).lower() == "core"]
    if not core_nodes:
        warnings.append("no node of type 'core' — the layout will centre on the first node")
    elif len(core_nodes) > 1:
        warnings.append(f"{len(core_nodes)} nodes are typed 'core' — keep exactly one")

    connected = set()
    seen_edges = set()
    for index, edge in enumerate(data["edges"]):
        where = f"edges[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{where}: must be an object")
            continue

        source = normalize_id(edge.get("from", edge.get("source")))
        target = normalize_id(edge.get("to", edge.get("target")))
        if not source or not target:
            errors.append(f"{where}: needs both 'from' and 'to'")
            continue
        if source not in ids:
            errors.append(f"{where}: 'from' references unknown node '{source}'")
        if target not in ids:
            errors.append(f"{where}: 'to' references unknown node '{target}'")
        if source == target:
            warnings.append(f"{where}: self-connection on '{source}' will be ignored")
            continue

        rel = str(edge.get("rel", edge.get("relation", "supports"))).lower().strip()
        if rel not in REL_TYPES:
            warnings.append(
                f"{where}: unknown relation '{rel}' — drawn as a plain line. "
                f"Known relations: {', '.join(sorted(REL_TYPES))}"
            )

        key = (source, target, rel)
        if key in seen_edges:
            warnings.append(f"{where}: duplicate connection {source} → {target} ({rel})")
        seen_edges.add(key)
        connected.add(source)
        connected.add(target)

    for node_id in ids:
        if node_id not in connected and len(ids) > 1:
            warnings.append(f"node '{node_id}' has no connections — it will float alone")

    positions = [n for n in nodes if isinstance(n, dict) and n.get("x") is not None and n.get("y") is not None]
    if positions and len(positions) != len(nodes):
        warnings.append(
            f"only {len(positions)}/{len(nodes)} nodes have x/y — automatic layout is used "
            "for the whole board (drag nodes, then export JSON to keep positions)"
        )

    return errors, warnings


def sanitize_json_for_html(payload: Dict[str, Any], pretty: bool) -> str:
    text = json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None)
    # Prevent an embedded "</script>" or "<!--" from breaking out of the tag.
    text = text.replace("</", "<\\/").replace("<!--", "<\\!--")
    return text


def build(data: Dict[str, Any], template_path: Path, theme: str | None, pretty: bool) -> str:
    if not template_path.is_file():
        raise ValidationError(f"template not found: {template_path}")

    template = template_path.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise ValidationError(f"template {template_path} has no {PLACEHOLDER} marker")

    payload = dict(data)
    if theme:
        payload["theme"] = theme

    return template.replace(PLACEHOLDER, sanitize_json_for_html(payload, pretty))


def summarize(data: Dict[str, Any]) -> str:
    nodes = data["nodes"]
    edges = data.get("edges", [])
    types: Dict[str, int] = {}
    for node in nodes:
        if isinstance(node, dict):
            key = str(node.get("type", "note")).lower()
            types[key] = types.get(key, 0) + 1

    by_type = ", ".join(f"{key} {value}" for key, value in sorted(types.items(), key=lambda kv: -kv[1]))
    timed = sum(1 for node in nodes if isinstance(node, dict) and node.get("time"))
    stat_nodes = [n for n in nodes if isinstance(n, dict) and str(n.get("type", "")).lower() == "stat"]
    carried = [
        n for n in stat_nodes
        if str(n.get("form") or "").strip()
        or isinstance(n.get("chart"), dict)
        or str(n.get("carrier") or "").strip().lower() in {"type", "type-only", "typographic", "text"}
    ]
    abstract = [n for n in nodes if isinstance(n, dict) and str(n.get("type", "")).lower() == "abstract"]
    unresolved = [n for n in abstract if not str(n.get("anchor") or "").strip()]
    lines = [
        f"{len(nodes)} nodes ({by_type})",
        f"{len(edges)} connections",
        f"{timed} nodes with timecodes · {len(carried)} of {len(stat_nodes)} numbers with a decided carrier",
    ]
    if abstract:
        lines.append(
            f"{len(abstract)} abstract line(s): {len(abstract) - len(unresolved)} anchored, "
            f"{len(unresolved)} unresolved"
        )
    return "\n".join(lines)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an interactive mind-map board from a JSON node graph.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python3 scripts/build_mindmap.py nodes.json --check\n"
            "  python3 scripts/build_mindmap.py nodes.json -o mindmap.html\n"
            "  python3 scripts/build_mindmap.py nodes.json --theme dark\n"
            "  python3 scripts/build_mindmap.py nodes.json --script transcript.txt\n"
        ),
    )
    parser.add_argument("graph", type=Path, help="path to the node-graph JSON file")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="output HTML path (default: <graph>.html)")
    parser.add_argument("-t", "--template", type=Path, default=DEFAULT_TEMPLATE,
                        help="board template (default: assets/mindmap-board.template.html)")
    parser.add_argument("--theme", choices=("light", "dark"), default=None,
                        help="override the board theme")
    parser.add_argument("-s", "--script", type=Path, default=None,
                        help="transcript the graph was built from; checks that every abstract "
                             "node's anchor actually comes from it")
    parser.add_argument("--context", type=Path, default=None,
                        help="path to the Phase 0 context card (previz/context.md): checks every "
                             "figure on the board against the figures ledger")
    parser.add_argument("--check", action="store_true", help="validate only, write nothing")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="only print errors")
    parser.add_argument("--pretty", action="store_true",
                        help="pretty-print the embedded JSON (larger file, easier to diff)")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    try:
        data = load_graph(args.graph)
        errors, warnings = validate(data)

        if args.script:
            try:
                script_text = args.script.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                raise ValidationError(f"cannot read script {args.script}: {exc}") from exc
            if not script_text.strip():
                raise ValidationError(f"script {args.script} is empty")
            warnings.extend(check_anchors(data["nodes"], script_text))
            warnings.extend(check_numbers(data["nodes"], script_text))

        if args.context:
            try:
                context_text = args.context.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                raise ValidationError(f"cannot read context {args.context}: {exc}") from exc
            if not context_text.strip():
                raise ValidationError(f"context {args.context} is empty")
            warnings.extend(check_context(data["nodes"], context_text))

        if errors:
            print("Invalid node graph:", file=sys.stderr)
            for error in errors:
                print(f"  ✗ {error}", file=sys.stderr)
            return 2

        if warnings and not args.quiet:
            print("Warnings:", file=sys.stderr)
            for warning in warnings:
                print(f"  ! {warning}", file=sys.stderr)

        if warnings and args.strict:
            print("Strict mode: warnings are errors.", file=sys.stderr)
            return 2

        if args.check:
            if not args.quiet:
                print("OK — node graph is valid.")
                print(summarize(data))
            return 0

        html = build(data, args.template, args.theme, args.pretty)
        output = args.output or args.graph.with_suffix(".html")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html, encoding="utf-8")

        if not args.quiet:
            print(f"Board written: {output}  ({output.stat().st_size / 1024:.1f} KB)")
            print(summarize(data))
        return 0

    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

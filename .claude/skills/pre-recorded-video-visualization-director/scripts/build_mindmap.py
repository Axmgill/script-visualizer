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
      "stat": null,
      "x": 0, "y": 0
    }
  ],
  "edges": [
    {"from": "core", "to": "hook", "rel": "flows", "label": "opens with"}
  ]
}

Node types: core, hook, claim, proof, stat, example, emotion, visual,
objection, cta, risk, note.
Relation types: supports, proves, expands, contrasts, callback, blocks,
flows, inspires.
Stat display kinds: dotgrid, bars, proportion, fraction, compare, steps,
counter.
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
    "emotion", "visual", "objection", "cta", "risk", "note",
}

REL_TYPES = {
    "supports", "proves", "expands", "contrasts",
    "callback", "blocks", "flows", "inspires",
}

STAT_KINDS = {
    "dotgrid", "dots", "bars", "chart", "proportion", "progress",
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
                            "use bars or a proportion instead"
                        )
                    if not isinstance(filled, int):
                        warnings.append(f"node '{node_id}': dotgrid 'filled' should be an integer")
                    elif isinstance(total, int) and 0 <= filled <= total and total >= 20:
                        ratio = filled / total
                        if 0 < ratio < 0.03:
                            warnings.append(
                                f"node '{node_id}': only {filled}/{total} dots are highlighted — "
                                "at card size that reads as empty; consider a counter instead"
                            )

        for key in ("visual", "summary", "emotion", "function"):
            if key in node and node[key] is not None and not isinstance(node[key], str):
                errors.append(f"node '{node_id}': '{key}' must be a string")

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
    stats = sum(1 for node in nodes if isinstance(node, dict) and node.get("stat"))
    return (
        f"{len(nodes)} nodes ({by_type})\n"
        f"{len(edges)} connections\n"
        f"{timed} nodes with timecodes · {stats} data points with metaphor graphics"
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an interactive mind-map board from a JSON node graph.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python3 scripts/build_mindmap.py nodes.json --check\n"
            "  python3 scripts/build_mindmap.py nodes.json -o mindmap.html\n"
            "  python3 scripts/build_mindmap.py nodes.json --theme dark\n"
        ),
    )
    parser.add_argument("graph", type=Path, help="path to the node-graph JSON file")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="output HTML path (default: <graph>.html)")
    parser.add_argument("-t", "--template", type=Path, default=DEFAULT_TEMPLATE,
                        help="board template (default: assets/mindmap-board.template.html)")
    parser.add_argument("--theme", choices=("light", "dark"), default=None,
                        help="override the board theme")
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

# Change plan — review copy

**Status:** implemented (2026-11-08), with the exceptions listed under "Not done" at the end of each workstream.

Two independent workstreams are waiting:

- **A — Board UX and responsive rebuild** (the large one)
- **B — Charts and data visualisation as first-class visuals** (the correction you asked for)

They are planned separately so each can be approved, built and verified on its own.

---

## A. Board UX and responsive

**Primary file:** `assets/mindmap-board.template.html` (1,566 lines — the single source for every board)
**Regenerated after each phase:** `examples/mindmap/napkin-proof.html`, `examples/mindmap/abstract-to-anchor.html`
**Unchanged:** `scripts/build_mindmap.py` data schema, the board's JSON contract, the skill's phases.

### A1. CSS changes

| # | Change | Detail | Why |
|---|---|---|---|
| A1.1 | `100vh` → `100dvh` | with a `100vh` fallback declaration first | mobile URL bar clipped the board |
| A1.2 | Safe-area insets | `env(safe-area-inset-*)` padding on `#topbar`, mobile `#actionbar`, `#sheet` | notched phones |
| A1.3 | Layout tokens | new `:root` vars: `--rail-w`, `--insp-w`, `--card-w`, `--ring-base`, `--fs-*`, each in `clamp()` | one stylesheet, every size |
| A1.4 | Six breakpoints | replaces the single `@media (max-width:1080px)` block; keyed on `body[data-layout]` | 320 → 2560 support |
| A1.5 | Step-mode styles | `.step` card, `.peek` neighbours, `#sheet`, `#actionbar` | phones cannot show a map legibly |
| A1.6 | New component styles | `#coach`, `#breadcrumb`, `#minimap`, `#attn`, `#kbdhint` | navigation and orientation |
| A1.7 | Legend reduced | 11 per-type colour classes → 4 family classes (`core`, `claim`, `evidence`, `risk`) | two taxonomies at once was the main visual noise |
| A1.8 | Inspector rail state | `.rail` width 48px with icon controls, expands on selection | 312px of empty panel on first load |
| A1.9 | `prefers-reduced-motion` | disables camera animation and auto-play | accessibility |
| A1.10 | `prefers-color-scheme` | dark theme on first load unless the user chose otherwise | accessibility, and it looks better |
| A1.11 | Print sheet | poster layout: all cards, numbered connections, no chrome | shareable on paper/PDF |

### A2. Markup changes (`<div id="app">`)

**Added:**

- `#coach` — first-run card: *"Click a card · drag to pan · F to fit"*, dismissed on first interaction
- `#breadcrumb` — `core → hook → claim`, each step clickable
- `#minimap` — canvas thumbnail with viewport rectangle, click to fly
- `#attn` — "Needs attention" panel: unresolved anchors, numbers without a body, missing timecodes, with a count badge
- `#kbdhint` — persistent hint bar: `F fit · / search · ? help`
- `#actionbar` + `#sheet` — phone-only controls and detail sheet
- `#stepview` — step-mode container (same cards, different layout class)
- `aria-live="polite"` region for selection announcements
- `role="application"` on the stage plus a visually hidden beat list as a text alternative

**Changed:**

- `#panel-left` — three collapsible sections (Search, Key, Stats) instead of four stacked blocks; Key starts collapsed
- `#inspector` — gains a `.rail` collapsed state
- `#timeline` — becomes a draggable range scrubber, not only clickable ticks
- Legend markup — 4 rows, with the specific node type kept as a text chip on each card

**Preserved (JS depends on these ids — no renames):** `#app #topbar #board-title #board-sub #board-meta #btn-panels #btn-theme #btn-fit #btn-export #btn-help #panel-left #search #legend #relkey #stats #stage #world #edges #nodes #zoom-hud #btn-out #zoom-level #btn-in #btn-fit2 #inspector #inspector-empty #inspector-body #timeline #track #tl-estimate #help #btn-help-close #toast #board-data`

### A3. JavaScript changes

**Replace**

| # | Change | Detail |
|---|---|---|
| A3.1 | `window.resize` → **`ResizeObserver` on `#stage`** | debounced 80ms; this is the fix for both reproduced defects (16% boot scale, skipped overlap pass) |
| A3.2 | Layout detection | `matchMedia` per breakpoint → `body[data-layout]`, then re-fit; fires on rotation |
| A3.3 | `fit()` | per-class minimum scale (0.5 tablet/phone instead of 0.16); no-op if the user has manually zoomed; guards zero size |
| A3.4 | `resolveOverlaps()` | re-run after fonts settle and after any layout-class change; retry if cards measured at 0 |
| A3.5 | `renderLegend()` | 4 families instead of 11 types |
| A3.6 | `applyFilters()` | adds a results list; `Enter` jumps, `←/→` cycles, camera animates to the match |
| A3.7 | `renderTimeline()` | range scrub → filters visible beats |
| A3.8 | `bindControls()` | new buttons, gesture wiring, expanded keyboard map |

**Add**

| # | Function | Purpose |
|---|---|---|
| A3.9 | `enterStepMode()` / `renderStep()` | phone default: one card, neighbour peeks, swipe to move |
| A3.10 | `nextBeat()` / `prevBeat()` | reading order, used by keys, swipes and the sheet button |
| A3.11 | `setReadingOrder(on)` | dims everything except the current beat and its connections |
| A3.12 | `renderMinimap()` / `minimapJump()` | orientation |
| A3.13 | `updateBreadcrumb()` | path to the current selection |
| A3.14 | `renderAttention()` / `nextIssue()` | walk the queue of cards that need a decision |
| A3.15 | `persist()` / `restore()` | `localStorage`: pan, zoom, dragged positions, theme, layout mode (versioned key, safe when storage is blocked) |
| A3.16 | `exportPNG()` | 2× PNG of the current view, alongside the existing JSON |
| A3.17 | Pinch zoom + long-press drag | two-pointer scaling; 350ms long-press to move a card on touch |

### A4. Tests and rebuilds

| # | Change | Detail |
|---|---|---|
| A4.1 | Rebuild both example boards from the template | byte-for-byte reproducible |
| A4.2 | Headless check at every breakpoint | 320–2560, asserts: no JS errors, no NaN positions, no overlapping cards once measured, every node reachable |
| A4.3 | Hidden-boot test | stage 0×0 at first paint → reveal → board must fit legibly |
| A4.4 | Optional: commit the jsdom harness | as `tests/board/` with a README saying it is developer-only and not shipped in the skill — **needs your approval, it adds a `package.json`** |

### A5. Phases

| Phase | Ships | Risk |
|---|---|---|
| **P0** Foundations | dvh, safe areas, ResizeObserver, both defect fixes, 4-family legend, coach card, keyboard hint | low — mostly behaviour, no layout redesign |
| **P1** Navigation | reading order, search-jump, minimap, breadcrumb, attention queue | medium — new interaction model |
| **P2** Responsive | six classes, step mode, sheet, action bar, touch gestures | high — layout rewrite; do it after P1 so navigation exists to test |
| **P3** Document | persistence, PNG export, print layout | low |
| **P4** Hardening | reduced motion, aria-live, contrast audit, 60-node performance | low |

Each phase ends with both example boards rebuilt and the headless suite green.

---

## B. Charts and data visualisation

The correction: **a chart is a legitimate visual.** The failure is a shape chosen because a number appeared, not a chart existing.

### B1. Files

| File | Change |
|---|---|
| `scripts/build_mindmap.py` | `form` stops being a hard error when a chart is justified; new optional `dataviz` block; new warnings |
| `references/mindmap-previz.md` | §4 rewritten: three valid carriers — object, chart, type — chosen by what the sentence is about |
| `references/design-craft.md` | new chart-craft subsection; anti-pattern table corrected |
| `SKILL.md` | Phase 4 line now says numbers may be carried by an object **or a chart**, with the reason stated |
| `examples/` | napkin example unchanged (no numbers); abstract example unchanged; add one chart-carrying stat to demonstrate |

### B2. Builder rule change

| Today | Proposed |
|---|---|
| `stat` without `form` → **build error**: *"A chart alone is not a body"* | `stat` needs **either** `form` (an object) **or** `dataviz` with a stated reason. Missing both → error |
| `dataviz` does not exist | `dataviz: { kind, of, because }` — `kind` from a fixed list (`bars`, `line`, `proportion`, `fraction`, `compare`, `steps`, `counter`, `dotgrid`), `of` = what is being compared, `because` = the clause of the sentence that makes it a comparison |
| Board warns *"every number is a schematic — charts are a fallback"* | Warning only when a chart has no `because`, or when a chart is used for something that is not a comparison |
| `stat` field = "OPTIONAL schematic preview" | renamed in copy to **preview** of the chart or object, clearly labelled *"Schematic — not the finished look"* |

### B3. Craft rules to add (from the design-craft work)

- Choose the chart by the **relationship in the sentence**, not by taste: rise over time → line; share of a whole → proportion, not decoration; ranking → sorted bars; before/after → two bars, not a pie.
- **Direct labels beat legends** whenever one series exists.
- **Honest axes**: a truncated axis must be declared on screen, or the chart is a lie.
- **Animate the change, not the furniture** — no bar-by-bar build-in unless the build carries meaning.
- **One annotation is worth ten gridlines**: mark the moment the narration names.
- **No 3D, no pies for three-way comparisons, no gauges with needles, no growth arrows the script never claimed.**
- If the sentence is a single figure with no comparison, type beats a chart, and a chart there is still decoration.

### B4. Tests

- A chart without `because` → warning; object-only → passes; neither → error.
- Every figure still checked against the transcript (unchanged).

---

## C. Documentation

| File | Change |
|---|---|
| `README.md` | board section: responsive + navigation; number section: charts allowed with a reason |
| `docs/board-ux-plan.md` | already written — keep as the UX spec |
| `docs/change-plan.md` | this file |

No CHANGELOG exists; I would not add one unless you want it.

---

## D. Explicitly NOT changing

- The 17-phase workflow and its reference files (apart from the Phase 4 number rule).
- The node-graph JSON schema, beyond the optional `dataviz` block.
- `estimate_timecodes.py`, `scan_ambiguity.py`, the Unclarity Scan.
- The install flow, the zip, the single-file/no-dependency promise.
- Any wording of your scripts.

---

## E. Order of execution

1. **B** (charts) — small, self-contained, testable, and it fixes a rule that is currently wrong.
2. **A-P0** — the two defects plus foundations.
3. **A-P1** — navigation.
4. **A-P2** — responsive classes and step mode.
5. **A-P3 / A-P4** — persistence, export, hardening.

Rebuild examples and run the headless suite at the end of each step.

---

## F. Decisions I need before starting

1. **Charts field** — is `dataviz: { kind, of, because }` the shape you want, or should a chart simply be a `form` like *"a rising line, 12 → 40"* with no new field?
2. **Tests in the repo** — commit the jsdom harness (`tests/board/` + `package.json`), or keep verification out of the repo as it is now?
3. **Legend** — 4 families, or all 11 types behind a collapsed Key?
4. **Reading order** — default on boot, or free canvas first?
5. **Persistence** — remember dragged positions, or always open canonical?
6. **Scope of the first merge** — P0 only, P0+P1, or everything through P3?

---

## What shipped

**B — charts:** `stat` nodes record one of three carriers — `form` (an object), `chart` with `what` + `why`, or `"carrier": "type"`. A chart is no longer an error; a chart with no written reason is. The board warning no longer says "charts are a fallback". `mindmap-previz.md` §4 is rewritten as questions rather than mappings, and `design-craft.md` gained a data-visualisation craft section. New example: `examples/mindmap/numbers-by-context.json` — four numbers, four different carriers, each decided by its sentence.

**A — board:** every P0, P1 and P2 item, plus persistence and PNG export from P3. See `board-ux-plan.md` → "What shipped".

**Not done:** committed jsdom test suite (`tests/board/` + `package.json`) — still an open decision; large-board virtualisation.

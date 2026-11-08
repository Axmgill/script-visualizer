# Mind-map board — UX and responsive plan

**Status:** implemented (2026-11-08). The board was rebuilt against this spec — see "What shipped" at the end.

**Applies to:** `assets/mindmap-board.template.html` (the single source) and every board built from it by `scripts/build_mindmap.py`.

**Constraint that does not change:** one self-contained HTML file, no dependencies, no network requests, no build step beyond the Python builder. Everything below is hand-rolled CSS and vanilla JS.

---

## 1. What is wrong today

Measured on the current example boards (11 cards, 16 connections):

| Problem | Evidence |
|---|---|
| Chrome eats the canvas | 236px left panel + 312px right panel = **548px** of a 1440px screen, and the right panel is **empty until you click** |
| No entry point | Board opens as a cloud; nothing marks the core as "start here" |
| Two taxonomies at once | 11 node-type colours **and** 8 relation styles, before a single card is read |
| Search doesn't navigate | Typing fades unrelated cards but the camera never moves; no result list |
| No sense of place | No minimap, no breadcrumb; pan away and you are lost |
| Hidden affordances | `F`, `/`, `?` work but nothing on screen says so |
| State is disposable | Pan, zoom, dragged positions, theme all reset on reload |
| Export is developer-shaped | JSON only; nothing a user can send to a client |
| Responsive is binary | One breakpoint at 1080px that hides both panels; below it, search becomes unreachable on some widths |
| Mobile is untested | `height:100vh` breaks under mobile browser chrome; no pinch zoom; no touch targets |

Two reproduced defects fold into this work:

1. **16% boot scale.** The stage measures 0×0 at boot in a hidden tab or collapsed pane; `fit()` clamps to `scale(0.16)` and the board opens as a postage stamp.
2. **Anti-overlap pass silently skipped.** `resolveOverlaps()` reads `offsetWidth/offsetHeight`; measured while hidden, both are 0, so the pass does nothing and cards can end up stacked.

Both have the same root cause — **layout is computed once from a window event instead of from the element's actual size** — and the same fix: `ResizeObserver` on `#stage`.

---

## 2. Design principles

1. **A route, not a cloud.** The board exists to be read in order. Reading order is the default; free canvas is a mode.
2. **One primary action per screen size.** Desktop: read and annotate. Tablet: read. Phone: step.
3. **Chrome serves the card.** Panels earn their pixels or collapse.
4. **Nothing is learned twice.** Any shortcut also exists as a visible control.
5. **The same board everywhere.** No "mobile version". One document that re-lays itself out.

---

## 3. Navigation model (shared across all breakpoints)

Three ways to move, always available:

- **Reading order** — beats in timecode sequence (`←` / `→`, `Space` plays through). Current card bright, its connections lit, everything else at 20% opacity. Auto-advances the camera, never scroll-jacks.
- **Free canvas** — pan, zoom, drag. The current behaviour, kept.
- **Needs attention** — a queue of cards that need a decision: unresolved anchors, numbers with no body, beats missing timecodes. `J` / `K` to walk it; a counter in the header `2 open`.

Plus: **search that navigates** (results list, `Enter` to jump, `←/→` to cycle), **minimap** with viewport rectangle, and a **breadcrumb** (`core → hook → claim`) where each step is clickable.

---

## 4. Responsive plan

### 4.1 Viewport classes

| Class | Range | Layout | Default mode |
|---|---|---|---|
| **Wide** | ≥ 1440px | 3 columns: rail (220) · canvas · inspector (340) | Reading order |
| **Desktop** | 1200–1439px | 3 columns, narrower; legend collapsed by default | Reading order |
| **Laptop** | 1024–1199px | 2 columns: canvas · inspector; search in the header | Reading order |
| **Tablet portrait** | 768–1023px | Canvas full width; panels become overlays (left slide-in, right bottom sheet at 45% height) | Reading order |
| **Phone landscape** | 568–767px, landscape | Canvas full; single bottom bar with prev/next/insight | Step |
| **Phone** | < 568px | Canvas full; top search bar, bottom action bar, sheet for detail | **Step** |

Breakpoints are driven by CSS `@media` **and** a `matchMedia` listener that re-fits the board when the class changes (so a rotation or window drag never leaves the board off-centre).

### 4.2 "Step" mode — what the board becomes on a phone

A node map at 375px wide is unreadable: at `fit()` scale the labels land around 5px. So below 568px the default is **Step**:

- One card fills the width (max 92vw), sized to its content, at a readable 15px label.
- The beats before and after appear as compact peeks (48px tall) above and below, so sequence is still visible.
- Swipe left/right or tap the peeks to move; the map is one tap away (`Map` toggle) and opens zoomed to the current node with the rest of the board dimmed.
- Detail (visual idea, form, anchor, connections) lives in a bottom sheet that can be dragged to 92% height, with a sticky "next beat" button.

Step mode uses the same DOM and the same data — it is a layout class, not a second document.

### 4.3 Layout mechanics

- `100vh` → **`100dvh`** everywhere, with a `100vh` fallback for older browsers. Mobile URL bars no longer clip the timeline.
- CSS `env(safe-area-inset-*)` padding on the top bar, bottom bar and any fixed control, for notched phones.
- `#app` grid becomes `grid-template-areas` per class; panels toggle with `data-layout` on `<body>`, not by display:none + JS width math.
- **`ResizeObserver` on `#stage`** replaces the window `resize` listener: fires when the element itself changes size (panel open, pane revealed, rotation), debounced 80ms, calls `fit()` only if the user has not manually zoomed. This also fixes the 16% boot bug and the skipped overlap pass, because measurement happens when the element actually has size.
- Overlap resolution re-runs after fonts settle **and** after any class change, guarded by a size check (`if (!n.w || !n.h) retry`).

### 4.4 Canvas scaling per class

The radial layout currently uses fixed radii (250 + 215 per ring) and fixed card widths (224 / 262). On small screens that produces a board that must be zoomed to ~0.16 to fit.

- **Card widths** become `clamp(168px, 22vw, 262px)`; the core stays 1.15× the body width.
- **Ring radii** scale with the viewport: `radius = base * clamp(0.62, viewportWidth / 1200, 1)`.
- **Minimum fit scale** rises from 0.16 to 0.5 on tablet and phone — if the board cannot fit legibly, the board re-flows into **step** rather than shrinking further. A map you cannot read is not a map.
- Node label type: `clamp(12.5px, 0.95vw + 8px, 15px)`; body copy never below 12.5px.

### 4.5 Touch and pointer input

| Gesture | Desktop | Touch |
|---|---|---|
| Pan | drag empty canvas | one finger drag |
| Zoom | wheel at cursor | pinch (two-pointer), plus `+` / `−` buttons |
| Select | click | tap |
| Move node | drag node | long-press (350ms) then drag; a plain drag pans |
| Fit | `F` / button | double-tap empty canvas, plus a Fit button in the action bar |
| Step beats | `← / →` | swipe left / right in step mode |

- `pointerdown/pointermove/pointerup` throughout (already used) with `setPointerCapture`, so a drag survives leaving the element.
- Hit targets ≥ 44×44 CSS px on touch; icon buttons grow to 44px below 1024px.
- No hover-only information: anything revealed on hover is also reachable by tap.
- `touch-action: none` on the stage only — never on the page — so vertical page scroll still works where the board is embedded.

### 4.6 Type, spacing and density

- A single `clamp()`-based type scale on `:root` — no separate mobile typography to maintain.
- Panel widths in `clamp()`: rail `clamp(0px, 16vw, 220px)`, inspector `clamp(0px, 24vw, 340px)`.
- Spacing scale in `rem`, root font size 16px, no `px` fixed gutters below 1024px.
- Cards collapse their secondary rows (emotion, form, anchor) behind a `+` on phone; the header chip and label always show.

### 4.7 Accessibility and motion

- `prefers-reduced-motion: reduce` → no camera animation, no auto-play; steps change instantly.
- `prefers-color-scheme: dark` → dark theme by default on first load; the manual toggle still wins and persists.
- Focus visible on every control; the board is operable by keyboard alone (`Tab` order: header → search → canvas → inspector → timeline).
- Announce selection changes with `aria-live="polite"` so screen readers hear "Beat 4 of 11, Proof: the napkin".
- Contrast: node chips and edge labels checked to 4.5:1 in both themes.
- The canvas gets `role="application"` with a text alternative list of beats, so an agent or screen reader can still read the board content.

### 4.8 Performance

- `will-change: transform` only during gesture; removed on `pointerup`.
- Edges re-rendered on a `requestAnimationFrame` throttle, not per-move.
- Above 60 nodes, labels hide below 0.55 scale and re-appear when zoomed — reads as a cleaner map rather than a smudge.
- Target: 60fps drag on a 2019 Android mid-range device with 40 nodes.

### 4.9 Print and export

- Print CSS keeps a poster layout (already partially present): all cards, connections numbered, no chrome.
- **Export PNG** (2× device pixel ratio) alongside the existing JSON, plus **Copy as image** where the clipboard allows.
- Export honours the current theme.

---

## 5. Work phases

| Phase | Scope | Outcome |
|---|---|---|
| **P0 — Foundations** | `dvh`, safe areas, `ResizeObserver` + re-fit, overlap re-run, 4 colour families, coach card, "start at the core", keyboard hint bar | Board opens correctly on any device and explains itself |
| **P1 — Navigation** | Reading-order mode, search-with-jump, minimap, breadcrumb, `←/→` stepping | The board can be *read*, not just panned |
| **P2 — Responsive layout** | Six viewport classes, step mode, bottom sheet, action bar, touch gestures, `clamp()` type and widths | Genuinely usable from 320px to 2560px |
| **P3 — Working document** | Needs-attention queue, `localStorage` persistence, PNG export, print layout | The board becomes something you work in and share |
| **P4 — Hardening** | Reduced motion, `aria-live`, contrast audit, 60-node performance pass, empty/loading states | Shippable to a client |

Each phase ends with the boards rebuilt from the template (`napkin-proof`, `abstract-to-anchor`) and re-verified.

---

## 6. Acceptance criteria

A phase is not done until all of these hold:

- **No horizontal scrolling** at 320, 375, 393, 568, 768, 834, 1024, 1280, 1440, 1920, 2560 px wide.
- **Boot in a hidden container** (0×0 at first paint) then reveal → board fits at a readable scale, cards do not overlap.
- **Rotation** on phone and tablet → board re-fits, no card outside the viewport, selection preserved.
- **Every action reachable by touch** at 44px, and by keyboard alone.
- **No text below 12.5px** at any width.
- **No JS errors** in a headless DOM run at each breakpoint (extend the jsdom harness already used for boards).
- **Single file**, no network requests, opens from `file://`.
- Rebuild is byte-for-byte reproducible from the template + JSON.

## 7. Test matrix

| Device class | Sizes to check | What matters |
|---|---|---|
| Phone small | 320×568, 375×667 | Step mode, no clipping, 44px targets |
| Phone large | 393×852, 430×932 | Bottom sheet drag, safe areas |
| Phone landscape | 667×375, 932×430 | Action bar doesn't cover the card |
| Tablet | 768×1024, 834×1112 | Overlay panels, rotation |
| Laptop | 1280×800, 1440×900 | 3 columns, inspector not crowding |
| Desktop | 1920×1080, 2560×1440 | Board centred, not stretched |

## 8. Open decisions

1. **Lifecycle of reading order** — always on at boot (recommended), or remembered per user?
2. **Legend content** — do you want the reduced 4-family legend, or is node type important enough to keep all 11 visible behind a toggle?
3. **Step mode on tablet portrait too**, or map only above 568px?
4. **Persistence** — is saving drag positions to `localStorage` desirable, or does every open want a clean canonical layout?

---

## What shipped

| Spec | Status |
|---|---|
| `100dvh`, safe-area insets | done |
| `ResizeObserver` on the stage, replacing the window resize listener | done — fixes the 16% boot scale and the skipped overlap pass |
| Six viewport classes (`wide`, `desktop`, `laptop`, `tablet`, `phone-land`, `phone`) | done |
| Reading order (`←` / `→`, `J` / `K`) | done |
| Search with a jump list | done |
| Minimap, breadcrumb | done |
| Needs-attention queue | done |
| Legend cut to 4 families, full type still on every card | done |
| Step mode below 568px, map one tap away | done |
| Timeline range scrub | done |
| Persistence of pan / zoom / positions / theme | done |
| PNG export alongside JSON | done |
| Coach card, keyboard hint bar | done |
| `clamp()` type and card widths, per-class minimum fit scale | done |
| Pinch zoom, long-press drag, 44px touch targets | done |
| Reduced motion, `prefers-color-scheme`, aria-live announcements | done |
| Print sheet | carried over from the previous template |

**Not done (deliberately):** virtualised rendering above 60 nodes (no board in the skill is that large yet), and a committed jsdom test suite — the checks were run during development but the repo still has no `package.json`.

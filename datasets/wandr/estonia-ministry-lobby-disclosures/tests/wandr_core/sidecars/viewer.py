"""Single-file HTML viewer for one WANDR run.

Usage:
    uv --quiet --no-config run --locked python -m sidecars.viewer <wandr_metrics.json> [-o viewer.html]

Two sections:
  1. Configuration — collapsible per-task tree showing task templates, judge schema,
     and per-key canon/dedup section templates (with section/full × raw/bound/rendered toggles).
  2. Rollup — recursive composed/standalone/raw tree with subtasks attached at their
     shared key, records as clickable url leaves opening a record modal.  Rollup head
     (title + toolbar) sticks to the viewport while the tree scrolls underneath.

Connector geometry (├─/└─ bars between rows) is drawn via CSS pseudo-elements on
`.rt-row::before` / `.rt-node::after`, colored by `currentColor` inherited from the
parent's `.rt-children` wrapper (so each level inherits its parent's key/subtask color).
"""

import argparse
from pathlib import Path
from typing import Any

import orjson

from sidecars.report import report_from_metrics_file

HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<style>
:root {
  --fg: #1a1a1a; --muted: #666; --bg: #fafafa; --card: #fff;
  --border: #e0e0e0; --accent: #2961d6; --accent-soft: #eaf0fa;
  --green: #1f7a35; --red: #b53030; --yellow: #b8860b; --pair-bg: #f4f7fc;
  --tree-line: #c5c5d5;
}
* { box-sizing: border-box; }
body { font-family: ui-sans-serif, -apple-system, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 13px; color: var(--fg); background: var(--bg); margin: 0; }
main { padding: 14px 18px; max-width: 1500px; margin: 0 auto; }
section { margin-bottom: 24px; }
/* Rollup section's heading + toolbar stick to the viewport top while the tree scrolls
   underneath them.  Background painted opaque so the underlying tree rows don't bleed
   through.  Negative side margins extend the band to the section's edges so the
   sticky strip lines up flush with the surrounding 18px padding. */
.rollup-sticky-head { position: sticky; top: 0; z-index: 20; background: var(--bg); padding-top: 4px; padding-bottom: 8px; border-bottom: 1px solid var(--border); margin-bottom: 8px; }
.rollup-sticky-head h2 { margin-top: 0; margin-bottom: 4px; }
/* Standing nav-hint box under the rollup toolbar. */
.rollup-nav-hint { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 4px; padding: 6px 10px 6px 10px; margin: 8px 0 0 0; font-size: 11.5px; color: #1e3a8a; line-height: 1.5; }
.rollup-nav-hint ul { margin: 0; padding-left: 18px; }
.rollup-nav-hint li { margin-bottom: 2px; }
.rollup-nav-hint code { background: rgba(30, 58, 138, 0.08); color: #1e3a8a; padding: 0 4px; border-radius: 2px; font-family: ui-monospace, monospace; font-size: 10.5px; }
section > h2 { margin: 0 0 10px 0; font-size: 15px; font-weight: 600; border-bottom: 2px solid var(--accent); padding-bottom: 3px; display: inline-block; }

/* generic toggle */
.tg-row { cursor: pointer; user-select: none; display: flex; align-items: center; gap: 6px; padding: 4px 0; }
.tg-caret { display: inline-block; width: 10px; color: var(--muted); transition: transform 0.1s; font-size: 11px; }
.tg-caret.open { transform: rotate(90deg); }
.tg-body { display: none; }
.tg-body.open { display: block; padding: 6px 0 10px 0; }
/* Section header with inline toolbar (Expand all / Collapse all buttons next to h2).
   Used by the Configuration section. */
.section-head { display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }
.section-head h2 { margin: 0; }
.section-head .toolbar { margin: 0; }

/* Task Overview section — static guide explaining the rollup semantics and how
   to review the task. */
.ov-task-desc { margin: 0 0 4px 0; font-size: 13.5px; line-height: 1.45; }
.ov-task-desc b { color: var(--fg); }
.ov-task-meta { color: var(--muted); font-size: 11.5px; font-weight: normal; }
.ov-task-layout { margin: 0 0 14px 0; font-size: 12px; }
.ov-task-layout code { font-family: ui-monospace, monospace; background: var(--accent-soft); padding: 1px 5px; border-radius: 3px; font-size: 11.5px; }
.ov-guide { font-size: 13px; line-height: 1.5; max-width: 980px; }
.ov-guide h3 { font-size: 14px; margin: 18px 0 6px 0; color: var(--fg); }
.ov-guide ul { padding-left: 20px; margin: 0 0 8px 0; }
.ov-guide li { margin-bottom: 5px; }
.ov-guide li ul { margin-top: 4px; padding-left: 22px; }
.ov-guide li ul li { margin-bottom: 2px; }
.ov-guide code { font-family: ui-monospace, monospace; background: var(--accent-soft); padding: 0 4px; border-radius: 2px; font-size: 11.5px; }
.ov-guide p.ov-hint { color: var(--muted); font-size: 11.5px; margin: 0 0 8px 0; font-style: italic; }
/* Blue-tinted box around the guide toggle so it stays discoverable while
   collapsed. Same palette as `.rollup-nav-hint`. */
.ov-guide-box { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 4px; padding: 6px 12px; margin: 8px 0 12px 0; }
.ov-guide-box .ov-section-label { color: #1e3a8a; font-weight: 600; }
.ov-guide-box .ov-guide { color: #1e3a8a; }
.ov-guide-box .ov-guide h3 { color: #1e3a8a; }
.ov-guide-box .ov-guide code { background: rgba(30, 58, 138, 0.08); color: #1e3a8a; }

/* overview node */
.ov-node { background: var(--card); border: 1px solid var(--border); border-radius: 5px; margin-bottom: 8px; padding: 8px 10px; }
.ov-header { cursor: pointer; user-select: none; display: flex; align-items: baseline; gap: 8px; }
.ov-header .tg-caret { font-size: 12px; }
.ov-name { font-weight: 600; font-size: 14px; }
.ov-name.subtask { color: var(--accent); }
.ov-keys { color: var(--muted); font-size: 12px; font-family: ui-monospace, "SF Mono", Menlo, monospace; }
.ov-content { margin-top: 10px; padding: 4px 0 6px 18px; border-left: 2px dashed var(--tree-line); }
.ov-content > * + * { margin-top: 14px; }
.ov-children { margin-top: 12px; padding-left: 18px; border-left: 2px solid var(--tree-line); }
.ov-section { margin-bottom: 6px; }
.ov-section-label { font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
/* "Other templates" body breathing room — section labels and panes get clear vertical
   gaps so consecutive (per-key judge / dedup / canon) sections don't squash together. */
.ov-other > .ov-section-label { margin-top: 18px; margin-bottom: 6px; }
.ov-other > .ov-section-label:first-child { margin-top: 4px; }
.ov-other > .ov-pane + .ov-pane { margin-top: 8px; }
/* Judge column inside the 2-col Judge|Schema grid: multiple panes stack vertically with a small gap. */
.ov-judge-col { display: flex; flex-direction: column; gap: 8px; }
.ov-judge-col > .ov-pane + .ov-pane { margin-top: 0; }
/* Inside .ov-other, each component's own container also stacks its panes. */
.ov-other > div > .ov-pane + .ov-pane { margin-top: 8px; }
.ov-twocol { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 6px; }
/* Lock both columns of the judge/schema grid to the same fixed height regardless of
   view (section/full); each scrolls internally instead of changing the box size. */
.ov-twocol > .ov-judge-col, .ov-twocol > .ov-pane { height: 70vh; overflow: auto; max-height: none; }
.ov-twocol > .ov-judge-col > .ov-pane { max-height: none; overflow: visible; flex-shrink: 0; }
.ov-pane { border: 1px solid var(--border); border-radius: 4px; padding: 8px 10px; background: #fcfcfc; max-height: 70vh; overflow: auto; }
.ov-pane h5 { margin: 0 0 6px 0; font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }
.ov-pane pre { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 11.5px; line-height: 1.5; white-space: pre-wrap; margin: 0; }
/* Segmented toggle for raw/bound/rendered + section/full controls. */
.seg-row { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-bottom: 8px; }
.seg { display: inline-flex; border: 1px solid var(--border); border-radius: 4px; overflow: hidden; font-size: 11px; }
.seg-opt { padding: 3px 8px; cursor: pointer; background: var(--card); color: var(--muted); user-select: none; border-right: 1px solid var(--border); }
.seg-opt:last-child { border-right: none; }
.seg-opt:hover { background: var(--accent-soft); }
.seg-opt.active { background: var(--accent); color: white; }
.seg-opt.disabled { opacity: 0.45; cursor: not-allowed; }
.seg-opt.disabled:hover { background: var(--card); }

/* schema fields */
.sch-group { margin-top: 6px; }
.sch-group-label { font-size: 10.5px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
.sch-field { margin-bottom: 4px; padding: 4px 7px; border-left: 3px solid var(--accent); background: var(--accent-soft); border-radius: 0 3px 3px 0; }
.sch-field .name { font-family: ui-monospace, monospace; font-weight: 600; font-size: 11.5px; }
.sch-field .type { color: var(--muted); font-size: 10.5px; font-family: ui-monospace, monospace; margin-left: 4px; }
.sch-field .desc { font-size: 11.5px; line-height: 1.4; margin-top: 2px; color: #333; }
.sch-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px; padding: 6px; background: var(--pair-bg); border-radius: 4px; }
.sch-pair-stem { grid-column: 1 / -1; font-size: 10.5px; font-weight: 600; color: var(--accent); margin-bottom: 2px; }

/* full renders */
.tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 8px; flex-wrap: wrap; }
.tab { padding: 5px 11px; cursor: pointer; border: 1px solid transparent; border-bottom: none; border-radius: 3px 3px 0 0; font-size: 12px; }
.tab.active { background: var(--card); border-color: var(--border); position: relative; top: 1px; font-weight: 600; }
.tab-panel { display: none; background: var(--card); border: 1px solid var(--border); border-top: none; padding: 10px; }
.tab-panel.active { display: block; }
.tab-panel { position: relative; }
.render-toggle { position: absolute; top: 8px; right: 12px; z-index: 1; padding: 3px 8px; background: var(--accent-soft); border: 1px solid var(--border); border-radius: 4px; }
pre.rendered { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 11.5px; line-height: 1.5; white-space: pre-wrap; max-height: 70vh; overflow: auto; margin: 0; padding: 6px; background: #f6f6f6; border-radius: 4px; }

/* rollup tree — flat-shared-right-edge so pills align in a tabulated column */
.rt-node { /* nesting only for collapse logic; visual indent handled per-row */ }
.rt-row, .rt-leaf {
  display: flex; align-items: center; gap: 8px;
  padding: 3px 8px;
  border-radius: 3px; cursor: pointer; min-height: 22px;
}
.rt-row:hover { background: var(--accent-soft); }
.rt-leaf {
  /* Border-only by default so the leaf plays nice with the merged_group bg behind it
     (sky tint shows through).  Hover fills the bg to reinforce clickability. */
  background: transparent; border: 1px solid #7dd3fc;
  margin: 2px 0; padding: 5px 10px; transition: background 0.1s;
}
.rt-leaf:hover { background: #e0f2fe; border-color: #38bdf8; }
.rt-row .score-pill, .rt-leaf .score-pill { flex-shrink: 0; }
.rt-children { padding-left: 18px; border-left: 1px dotted var(--tree-line); }
.rollup-grid { padding: 4px 0; }
.rollup-grid.hide-hints .rt-hint { display: none; }
.hints-toggle { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; cursor: pointer; user-select: none; padding: 3px 8px; border: 1px solid var(--border); border-radius: 4px; background: var(--card); }
.toolbar button.ctrl-tree-only { font-size: 12px; padding: 3px 10px; border: 1px solid var(--border); border-radius: 4px; background: var(--card); cursor: pointer; }
.toolbar button.ctrl-tree-only:hover { background: var(--accent-soft); }
.rt-key { font-family: ui-monospace, monospace; color: var(--muted); font-size: 12px; font-weight: 600; }
.rt-task { font-family: ui-monospace, monospace; color: var(--fg); font-weight: 600; font-size: 12px; }
.rt-subtask { font-family: ui-monospace, monospace; color: var(--accent); font-weight: 600; font-size: 12px; }
.rt-value { font-family: ui-monospace, monospace; font-size: 12px; word-break: break-all; }
.rt-leaf-url {
  font-family: ui-monospace, monospace; font-size: 11.5px; color: var(--accent);
  /* Take available space, truncate with ellipsis past a generous width.  Full URL
     remains accessible via the `title=` tooltip on hover. */
  flex: 1; min-width: 0; max-width: 100ch;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.rt-meta { color: var(--muted); font-size: 11px; }
/* Deficit / surplus markers and pads.  Markers are a dashed-connector separator row;
   pads are zero-score placeholders for missing slots up to `required`.
   Both share `.rt-leaf` geometry so the parent's connector CSS positions them the
   same way as real leaves; the `border: 1px solid transparent` matches the visible
   leaf's 1px border so text/pill X-position aligns flush with sibling leaves. */
.rt-leaf.rt-marker, .rt-leaf.rt-pad {
  background: transparent; cursor: default;
  border: 1px solid transparent;
  margin: 1px 0; min-height: 18px;
}
.rt-leaf.rt-marker:hover, .rt-leaf.rt-pad:hover { background: transparent; border-color: transparent; }
/* Marker text inherits the parent's currentColor (key/subtask tint, same as the
   connector tick) — no per-class color override. */
.rt-marker-label { font-size: 11px; font-style: italic; }
.rt-marker-trail {
  flex: 1; height: 1.5px; align-self: center;
  border-bottom: 1.5px dashed currentColor;
  opacity: 0.6;
}
/* Warning block in the rollup sticky head: surfaces key_levels where the entity
   extract returned empty for one or more records (records excluded from the
   rollup, surfaced here as a diagnostic instead of cluttering the tree).
   Orange tint — warning-not-error semantics (the rollup is still meaningful,
   just under-coverage at the flagged key). */
.rollup-warnings { background: #fff7ed; border: 1px solid #fed7aa; border-radius: 4px; padding: 6px 10px; margin-bottom: 6px; font-size: 11.5px; }
.rollup-warnings-title { color: #9a3412; font-weight: 600; margin-bottom: 3px; }
.rollup-warnings-list { margin: 0; padding-left: 18px; color: #7c2d12; }
.rollup-warnings-list li { line-height: 1.5; }
.rollup-warnings-list code { background: rgba(124, 45, 18, 0.08); padding: 0 4px; border-radius: 2px; font-size: 10.5px; font-family: ui-monospace, monospace; }
.rollup-warnings-list code.rollup-warnings-task { color: #7c2d12; }
/* merged-cluster group: each cluster's variants share a yellow band so the take-worst
   collapse is visually grouped (canonical first, merged-away siblings beneath).
   Dotted brown top-border separates adjacent merged groups so they don't visually fuse
   when listed as siblings under one key_level. */
.merged-group { background: #fff8e8; border-left: 3px solid var(--yellow); border-top: 1px dotted #b88a2a; border-radius: 0 3px 3px 0; padding: 3px 0; margin: 4px 0; }
.merged-group + .merged-group { margin-top: 6px; }
.rt-value.merged-away { font-style: italic; }
/* Whole merged-away SUBTREE (entity row + all descendants) is italicized + dimmed —
   not just the entity row. Pills inside also get a stronger fade. */
.merged-away-subtree, .merged-away-subtree * { font-style: italic; }
.merged-away-subtree { opacity: 0.78; }
.merged-away-subtree .score-pill { opacity: 0.55; }
/* Show Duplicates toggle: when off, hide every merged-away subtree. The merged-group
   wrapper still exists but is reduced to neutral (no band) when it carries only the
   canonical (its merged-away siblings are hidden). */
.rollup-grid.hide-dups .merged-away-subtree { display: none; }
/* Inline style on `.merged-group` sets key-tinted bg/border; use `!important`
   here so hidden duplicate groups collapse to an unframed canonical row. */
.rollup-grid.hide-dups .merged-group { background: transparent !important; border-left: none !important; border-top: none !important; padding: 0 !important; margin: 0 !important; }
.score-pill { display: inline-block; padding: 0 6px; border-radius: 8px; font-size: 10.5px; font-weight: 600; min-width: 34px; text-align: center; }
.s-pass { background: #d6f0d6; color: var(--green); }
.s-fail { background: #f5d6d6; color: var(--red); }
.s-mid { background: #f8e6c0; color: var(--yellow); }
.s-na { background: #ececec; color: #888; }
/* "empty" — no records under this node (skeleton subtask attachment, empty key_level).
   Muted red-grey to read as "missing, not failed". */
.s-empty { background: #f3e0e0; color: #a04444; font-style: italic; }

/* raw view */
.raw-scroll { max-height: 560px; overflow: auto; border: 1px solid var(--border); border-radius: 4px; }
.raw-table { border-collapse: collapse; width: 100%; font-size: 11.5px; }
.raw-table th, .raw-table td { border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); padding: 4px 6px; vertical-align: top; }
.raw-table th { background: #f0f0f0; text-align: left; font-weight: 600; font-family: ui-monospace, monospace; position: sticky; top: 0; z-index: 1; }
.raw-table td { word-break: break-word; max-width: 280px; }
.raw-table tbody tr { cursor: pointer; }
.raw-table tbody tr:hover { background: var(--accent-soft); }
.raw-table .raw-cell { font-family: ui-monospace, monospace; font-size: 11px; white-space: pre-wrap; margin: 0; max-height: 6em; overflow: auto; }
/* Modal JSON blocks use raw-cell typography but need their own wrapping box. */
.modal pre.raw-cell { font-family: ui-monospace, monospace; font-size: 11px; white-space: pre-wrap; word-break: break-all; margin: 0; max-height: 14em; overflow: auto; background: #f6f6f6; padding: 6px; border-radius: 4px; }
.raw-table .raw-url { color: var(--accent); font-family: ui-monospace, monospace; font-size: 11px; word-break: break-all; }
.field-decompositions { margin: 6px 0 10px 0; }
.field-decompositions .raw-scroll { max-height: 260px; }
.field-decompositions .raw-table tbody tr { cursor: default; }
.field-decompositions .raw-table tbody tr:hover { background: transparent; }
.field-decompositions .num { text-align: right; font-family: ui-monospace, monospace; white-space: nowrap; }

/* Duplicates Detected (raw view) — one colored block per key, matching the per-key palette
   used in tree views' merged-group bands. */
.dup-block-title { margin: 0 0 8px 0; font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }
.dup-key-block { padding: 8px 12px; margin-bottom: 8px; border-left: 3px solid var(--border); border-radius: 0 4px 4px 0; }
.dup-node { font-weight: 600; font-family: ui-monospace, monospace; font-size: 12px; margin-bottom: 4px; }
.dup-list { margin: 2px 0 0 0; padding-left: 22px; font-size: 12px; }
.dup-list li { font-family: ui-monospace, monospace; line-height: 1.5; margin-bottom: 6px; }
.dup-canon { font-weight: 600; }
/* Indent alias lines so the `⇄` glyph sits visually under the canonical's leading text;
   keeps the run-of-aliases distinct from the bullet without losing the bullet's grouping. */
.dup-others { color: var(--muted); padding-left: 0; }
/* Toolbar tree-only controls fade in raw view */
.toolbar.raw-mode .ctrl-tree-only { opacity: 0.4; pointer-events: none; }

/* toolbar */
.toolbar { display: flex; gap: 8px; align-items: center; margin-bottom: 10px; flex-wrap: wrap; }
.toolbar select, .toolbar button { font-size: 12px; padding: 3px 8px; border: 1px solid var(--border); border-radius: 4px; background: var(--card); cursor: pointer; }

/* modal */
.modal-backdrop { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.55); z-index: 100; align-items: flex-start; justify-content: center; padding: 30px; overflow: auto; }
.modal-backdrop.active { display: flex; }
.modal { background: var(--card); border-radius: 6px; padding: 18px 20px; max-width: 1100px; width: 100%; max-height: 90vh; overflow: auto; }
.modal-close { float: right; cursor: pointer; font-size: 22px; color: var(--muted); border: none; background: none; }
.modal h3 { margin-top: 0; font-size: 15px; }
.modal h4 { margin: 12px 0 4px 0; font-size: 12.5px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
.modal a.url-link { font-family: ui-monospace, monospace; font-size: 12px; color: var(--accent); word-break: break-all; }

.kv-grid { display: grid; grid-template-columns: max-content 1fr; gap: 3px 12px; font-size: 12px; }
.kv-grid dt { font-family: ui-monospace, monospace; font-weight: 600; color: var(--muted); }
.kv-grid dd { margin: 0; word-break: break-word; }

.judge-row { padding: 3px 6px; margin-bottom: 2px; border-left: 3px solid #ccc; background: #fafafa; border-radius: 0 3px 3px 0; }
.judge-row.bool-true { border-left-color: var(--green); }
.judge-row.bool-false { border-left-color: var(--red); }
.judge-row .name { font-family: ui-monospace, monospace; font-size: 11.5px; font-weight: 600; }
.judge-row .val { font-family: ui-monospace, monospace; font-size: 11.5px; margin-left: 8px; }
.judge-row.bool-true .val { color: var(--green); }
.judge-row.bool-false .val { color: var(--red); }
.judge-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 4px; padding: 4px; background: var(--pair-bg); border-radius: 4px; }
.judge-section-label { font-size: 10.5px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin: 8px 0 3px 0; }

/* ===== Rollup-tree connector geometry =====
   Each direct child of `.rt-children` (rt-node, rt-leaf, merged_group) is responsible
   for drawing its own segment of the parent's bar:
     `.rt-row::before`  = horizontal stub at row-middle ("├" / "└" tick).
                          For the LAST sibling we ALSO add a top-half vertical
                          (the `└─` bottom-corner shape) since there's no `::after`.
     `.rt-node::after`  = full vertical bar through the WHOLE node (row + its
                          expanded children container).  Drawn ONLY on non-last
                          siblings, so the parent's bar passes through the entire
                          subtree and stops cleanly at the last sibling's row middle.
   Putting `::after` on `.rt-node` (not `.rt-row`) is the key to bridging gaps when
   a non-last sibling is expanded — without it the bar dies at row bottom and leaves
   a hole over the expanded children's area.
   Merged_group: connector tick lands on the FIRST item only.  The whole group's
   vertical bar (when non-last) is drawn on `.merged-group::after`. */

.rollup-grid .rt-children {
  padding-left: 18px;
  margin-left: 12px;
  border-left: none !important;
}
.rollup-grid .rt-children > .merged-group {
  border-left: none !important; padding-left: 0 !important;
}
.rollup-grid .rt-row, .rollup-grid .rt-leaf,
.rollup-grid .rt-node, .rollup-grid .merged-group { position: relative; }

/* `.rt-node` as a block formatting context: contains its descendants' margins so
   its box height accurately includes the bottom margin of its last child.  Without
   this, a leaf's 2px (or merged_group's 4px) bottom margin would escape through
   `.rt-children` (no padding-bottom) and `.rt-node` (no padding-bottom), shrinking
   `.rt-node`'s effective box and leaving the bar too short to bridge to the next
   sibling. */
.rollup-grid .rt-node { display: flow-root; }

/* === Regular direct children of .rt-children (NOT inside merged_group) ===
   `position: absolute` anchors to the *padding-edge* of the nearest positioned
   ancestor, not the border-edge.  `.rt-leaf` has `border: 1px solid` so its
   padding-edge is 1px to the right of its border-edge; without compensation a
   leaf's bars would end up 1px to the right of any sibling `.rt-node` /
   `.merged-group` bars (which have no border-left in this view).  Leaves use
   `left: -19px; width: 19px` to compensate. */

.rollup-grid .rt-children > .rt-node > .rt-row::before {
  content: ""; position: absolute; pointer-events: none;
  left: -18px; top: 50%; width: 18px; height: 0;
  border-bottom: 1.5px solid currentColor;
}
.rollup-grid .rt-children > .rt-leaf::before {
  content: ""; position: absolute; pointer-events: none;
  left: -19px; top: 50%; width: 19px; height: 0;
  border-bottom: 1.5px solid currentColor;
}

/* Last sibling: also add top-half vertical to form `└─` shape. */
.rollup-grid .rt-children > .rt-node:last-child > .rt-row::before,
.rollup-grid .rt-children > .rt-leaf:last-child::before {
  top: 0; height: 50%;
  border-left: 1.5px solid currentColor;
}

/* Non-last sibling: full vertical bar through the whole node (row + children).
   `bottom: -5px` extends the bar past the element's box to bridge sibling margins
   (rt-leaf 2px own margin / 4px gap to next merged_group / etc). */
.rollup-grid .rt-children > .rt-node:not(:last-child)::after {
  content: ""; position: absolute; pointer-events: none;
  left: -18px; top: 0; bottom: -5px; width: 18px;
  border-left: 1.5px solid currentColor;
}
.rollup-grid .rt-children > .rt-leaf:not(:last-child)::after {
  content: ""; position: absolute; pointer-events: none;
  left: -19px; top: 0; bottom: -5px; width: 18px;
  border-left: 1.5px solid currentColor;
}

/* === Inside merged_group: tick on FIRST item only === */

.rollup-grid .rt-children > .merged-group > .rt-node:first-child > .rt-row::before {
  content: ""; position: absolute; pointer-events: none;
  left: -18px; top: 50%; width: 18px; height: 0;
  border-bottom: 1.5px solid currentColor;
}
.rollup-grid .rt-children > .merged-group > .rt-leaf:first-child::before {
  content: ""; position: absolute; pointer-events: none;
  left: -19px; top: 50%; width: 19px; height: 0;
  border-bottom: 1.5px solid currentColor;
}

/* Last merged_group's first item: top-half vertical (└─ termination). */
.rollup-grid .rt-children > .merged-group:last-child > .rt-node:first-child > .rt-row::before,
.rollup-grid .rt-children > .merged-group:last-child > .rt-leaf:first-child::before {
  top: -6px; height: calc(50% + 6px);
  border-left: 1.5px solid currentColor;
}
.rollup-grid.hide-dups .rt-children > .merged-group:last-child > .rt-node:first-child > .rt-row::before,
.rollup-grid.hide-dups .rt-children > .merged-group:last-child > .rt-leaf:first-child::before {
  top: 0; height: 50%;
}

/* Non-last merged_group: full vertical bar through whole group.  `bottom: -7px`
   bridges `.merged-group`'s `margin: 4px 0` (or 6px between adjacent groups). */
.rollup-grid .rt-children > .merged-group:not(:last-child)::after {
  content: ""; position: absolute; pointer-events: none;
  left: -18px; top: 0; bottom: -7px; width: 18px;
  border-left: 1.5px solid currentColor;
}

/* === Deficit / surplus markers: dashed horizontal tick === */
/* The horizontal connector pointing into a marker row goes dashed to flag the row as
   a synthetic separator (not a real entity).  The vertical bar continuing through
   the marker to the next sibling stays solid — it's the parent's structural bar. */
.rollup-grid .rt-children > .rt-leaf.rt-marker::before {
  border-bottom-style: dashed;
}
.rollup-grid .rt-children.bold > .rt-leaf.rt-marker::before {
  border-bottom-style: dashed;
}

/* === Bold variants (parent rendered bold → thicker connector) === */

.rollup-grid .rt-children.bold > .rt-node > .rt-row::before,
.rollup-grid .rt-children.bold > .rt-leaf::before,
.rollup-grid .rt-children.bold > .merged-group > .rt-node:first-child > .rt-row::before,
.rollup-grid .rt-children.bold > .merged-group > .rt-leaf:first-child::before {
  border-bottom-width: 2.5px;
}
.rollup-grid .rt-children.bold > .rt-node:last-child > .rt-row::before,
.rollup-grid .rt-children.bold > .rt-leaf:last-child::before,
.rollup-grid .rt-children.bold > .merged-group:last-child > .rt-node:first-child > .rt-row::before,
.rollup-grid .rt-children.bold > .merged-group:last-child > .rt-leaf:first-child::before {
  border-left-width: 2.5px;
}
.rollup-grid .rt-children.bold > .rt-node:not(:last-child)::after,
.rollup-grid .rt-children.bold > .rt-leaf:not(:last-child)::after,
.rollup-grid .rt-children.bold > .merged-group:not(:last-child)::after {
  border-left-width: 2.5px;
}

/* No toggle glyph in the rollup tree (whole row is clickable instead).  Scoped to
   `.rollup-grid` so carets elsewhere — the Configuration section —
   keep showing as expandability hints. */
.rollup-grid .rt-row, .rollup-grid .rt-leaf { padding-left: 6px !important; }
.rollup-grid .rt-toggle, .rollup-grid .tg-caret { display: none; }
.rollup-grid .rt-row.expandable { cursor: pointer; }
.rollup-grid .rt-row:not(.expandable) { cursor: default; }
.rollup-grid .rt-leaf { margin: 0; }
</style>
</head>
<body>
<main>
  <section>
    <div id="task-overview-body"></div>
  </section>
  <section>
    <div class="section-head">
      <h2>Configuration</h2>
      <span class="toolbar">
        <button class="ctrl-tree-only" onclick="setOverviewOpen(true)">Expand all</button>
        <button class="ctrl-tree-only" onclick="setOverviewOpen(false)">Collapse all</button>
      </span>
    </div>
    <div id="overview-body"></div>
  </section>
  <section>
    <div class="rollup-sticky-head" id="rollup-sticky"><h2>Rollup</h2></div>
    <div id="rollup-body"></div>
  </section>
</main>
<div class="modal-backdrop" id="modal-backdrop"><div class="modal" id="modal"><button class="modal-close" onclick="closeModal()">&times;</button><div id="modal-body"></div></div></div>

<script>
const DATA = __VIEWER_DATA__;

function el(tag, attrs={}, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k === "onclick") e.onclick = v;
    else if (k === "style") e.style.cssText = v;
    else e.setAttribute(k, v);
  }
  for (const child of children) {
    if (child == null || child === false) continue;
    e.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return e;
}

function makeToggle(label, body, opts={}) {
  const open = opts.open ?? false;
  const wrap = el("div");
  const caret = el("span", {class: "tg-caret" + (open ? " open" : "")}, "▶");
  const row = el("div", {class: "tg-row"}, caret, label);
  const bodyWrap = el("div", {class: "tg-body" + (open ? " open" : "")});
  bodyWrap.append(body);
  row.onclick = () => {
    caret.classList.toggle("open");
    bodyWrap.classList.toggle("open");
  };
  wrap.append(row, bodyWrap);
  return wrap;
}

// === Overview ===

function renderSchemaGroups(groups) {
  const wrap = el("div");
  for (const group of groups) {
    const groupBox = el("div", {class: "sch-group"});
    groupBox.append(el("div", {class: "sch-group-label"}, group.label));
    if (group.kind === "fields") {
      for (const field of group.fields) groupBox.append(renderSchemaField(field));
    } else if (group.kind === "pairs") {
      for (const pair of group.pairs) {
        const pairBox = el("div", {class: "sch-pair"});
        pairBox.append(el("div", {class: "sch-pair-stem"}, pair.stem));
        pairBox.append(renderSchemaField(pair.satisfied), renderSchemaField(pair.supported));
        groupBox.append(pairBox);
      }
    }
    wrap.append(groupBox);
  }
  return wrap;
}

function renderSchemaField(f) {
  const box = el("div", {class: "sch-field"});
  box.append(
    el("div", {}, el("span", {class: "name"}, f.name), el("span", {class: "type"}, f.type)),
    el("div", {class: "desc"}, f.description || ""),
  );
  return box;
}

/* Segmented control: returns an element with one .seg-opt per option.  Clicking an
   option calls onChange(value) and updates the active class.  If a value's content
   is empty (e.g., no example data → rendered is ""), the option is greyed out but
   still selectable so the user sees an empty preview rather than nothing happening. */
function makeSegmented(options, initial, onChange, disabledOf = (() => false)) {
  const seg = el("div", {class: "seg"});
  const opts = [];
  options.forEach(({value, label}) => {
    const cls = "seg-opt" + (value === initial ? " active" : "") + (disabledOf(value) ? " disabled" : "");
    const o = el("div", {class: cls}, label);
    o.dataset.value = value;
    o.onclick = () => {
      opts.forEach(x => x.classList.remove("active"));
      o.classList.add("active");
      onChange(value);
    };
    opts.push(o);
    seg.append(o);
  });
  return seg;
}

function renderOverviewNode(node, isSubtask=false) {
  const block = el("div", {class: "ov-node"});

  // Build the body (collapsible content)
  const content = el("div", {class: "ov-content"});

  // -- Task template: raw / bound toggle ---------------------------------------
  {
    const variants = node.task_template_variants || {raw: "", bound: ""};
    const pre = el("pre", {}, variants.raw || "(none)");
    let mode = "raw";
    const seg = makeSegmented(
      [{value: "raw", label: "raw"}, {value: "bound", label: "bound"}],
      mode,
      v => { mode = v; pre.textContent = (variants[mode] || "(empty)"); },
      v => !variants[v],
    );
    const pane = el("div", {class: "ov-pane"},
      el("div", {class: "seg-row"}, seg),
      pre);
    content.append(makeToggle(el("span", {class: "ov-section-label"}, "Task template"), pane, {open: true}));
  }

  /* makePromptPane: small pre+heading combo for a single prompt body. */
  function makePromptPane(heading, text) {
    return el("div", {class: "ov-pane"},
      heading ? el("h5", {}, heading) : null,
      el("pre", {}, (text === "" || text == null) ? "(empty)" : text));
  }

  /* Render the "left column" of a component into `container`, given a (view, mode).
     `runtimeShape` controls full-mode behavior:
       - "component": full mode renders ONE combined pane (judge runtime shape).
       - "per_key":   full mode renders one pane per non-url key (canon/dedup runtime shape).
     `showComponentSection` controls whether section mode includes the component-level
     section_template pane above the per-key sections (true for judge). */
  function paintComponentPanes(container, promptVariants, view, mode, kind, opts) {
    container.replaceChildren();
    if (!promptVariants) return;
    const showComponentSection = opts.showComponentSection;
    const runtimeShape = opts.runtimeShape;
    if (view === "section") {
      if (showComponentSection && promptVariants.component) {
        container.append(makePromptPane(kind, (promptVariants.component.section || {})[mode]));
      }
      for (const [key, variants] of Object.entries(promptVariants.per_key || {})) {
        container.append(makePromptPane(`${kind}.${key}`, (variants.section || {})[mode]));
      }
    } else {  // full
      if (runtimeShape === "component") {
        // One LLM call per record → one full prompt for the whole component.
        container.append(makePromptPane(kind, (promptVariants.component?.full || {})[mode]));
      } else {  // per_key
        // One LLM call per key → one full prompt per key.
        for (const [key, variants] of Object.entries(promptVariants.per_key || {})) {
          container.append(makePromptPane(`${kind}.${key}`, (variants.full || {})[mode]));
        }
      }
    }
  }

  // -- Judge | Schema: 2-column.  Left = judge content; right = schema.  Both columns
  // react to the view toggle:
  //   section → judge component section + per-key sections; schema shows ONLY the
  //             task-specific groups (`label` starts with "Custom").
  //   full    → one combined judge prompt; schema shows the full set of groups
  //             (universal gates + custom + universal requirements + universal verdict).
  {
    const judgeCol = el("div", {class: "ov-judge-col"});
    const schemaBody = el("div");
    let view = "section";
    let mode = "raw";
    const allGroups = node.schema_groups || [];
    const customGroups = allGroups.filter(group => (group.label || "").startsWith("Custom"));
    const paintSchema = () => {
      const groups = view === "section" ? customGroups : allGroups;
      schemaBody.replaceChildren(renderSchemaGroups(groups));
    };
    const repaint = () => {
      paintComponentPanes(judgeCol, node.judge_variants, view, mode, "judge", {
        showComponentSection: true,
        runtimeShape: "component",
      });
      paintSchema();
    };
    repaint();
    const viewSeg = makeSegmented(
      [{value: "section", label: "section"}, {value: "full", label: "full"}],
      view, v => { view = v; repaint(); });
    const modeSeg = makeSegmented(
      [{value: "raw", label: "raw"}, {value: "bound", label: "bound"}, {value: "rendered", label: "rendered (example)"}],
      mode, v => { mode = v; repaint(); });
    const schemaPane = el("div", {class: "ov-pane"},
      el("h5", {}, "Judge schema"), schemaBody);
    const wrap = el("div");
    wrap.append(el("div", {class: "seg-row"}, viewSeg, modeSeg),
                el("div", {class: "ov-twocol"}, judgeCol, schemaPane));
    content.append(makeToggle(el("span", {class: "ov-section-label"}, "Judge template | Schema"), wrap));
  }

  // -- Other templates: canon / dedup, one shared section/full × raw/bound/rendered pair.
  // Each component knows its runtime shape:
  //   canon  runs once per key  → "per_key"  (one full pane per key)
  //   dedup  runs once per key  → "per_key"
  {
    const subs = [
      {kind: "canon", promptVariants: node.canon_variants, showComponentSection: false, runtimeShape: "per_key"},
      {kind: "dedup", promptVariants: node.dedup_variants, showComponentSection: false, runtimeShape: "per_key"},
    ].filter(subsection => subsection.promptVariants);
    if (subs.length > 0) {
      const other = el("div", {class: "ov-other"});
      let view = "section";
      let mode = "raw";
      const containers = subs.map(subsection => ({subsection, container: el("div")}));
      const repaintAll = () => {
        for (const {subsection, container} of containers) {
          paintComponentPanes(container, subsection.promptVariants, view, mode, subsection.kind, {
            showComponentSection: subsection.showComponentSection,
            runtimeShape: subsection.runtimeShape,
          });
        }
      };
      const viewSeg = makeSegmented(
        [{value: "section", label: "section"}, {value: "full", label: "full"}],
        view, v => { view = v; repaintAll(); });
      const modeSeg = makeSegmented(
        [{value: "raw", label: "raw"}, {value: "bound", label: "bound"}, {value: "rendered", label: "rendered (example)"}],
        mode, v => { mode = v; repaintAll(); });
      other.append(el("div", {class: "seg-row"}, viewSeg, modeSeg));
      for (const {subsection, container} of containers) {
        other.append(el("div", {class: "ov-section-label"}, subsection.kind));
        other.append(container);
      }
      repaintAll();
      content.append(makeToggle(el("span", {class: "ov-section-label"}, "Other templates"), other));
    }
  }

  // Header (the name itself is the toggle).  Subtasks use their top-level key color;
  // root task stays neutral.  Names are wrapped as `#name#` per the task/key namespace
  // convention.  Key summary tints each key segment.  All tasks open by default — the
  // user-facing default reveals every task at once with each task's `Task template`
  // sub-toggle pre-opened (per `makeToggle({open: true})` on that toggle).
  const caret = el("span", {class: "tg-caret open"}, "▶");
  const subColor = isSubtask ? subtaskColor(node.name) : null;
  const nameStyle = subColor ? `color: ${subColor.text};` : "";
  const header = el("div", {class: "ov-header"},
    caret,
    el("span", {class: "ov-name" + (isSubtask ? " subtask" : ""), style: nameStyle}, `#${node.short_name}#`),
    el("span", {class: "ov-keys"}, renderKeySummary(node.key_summary)),
  );
  const bodyWrap = el("div", {class: "tg-body open"});
  bodyWrap.append(content);
  header.onclick = () => {
    caret.classList.toggle("open");
    bodyWrap.classList.toggle("open");
  };
  block.append(header, bodyWrap);

  if (node.children && node.children.length > 0) {
    const childrenWrap = el("div", {class: "ov-children"});
    for (const child of node.children) childrenWrap.append(renderOverviewNode(child, /*isSubtask*/ true));
    block.append(childrenWrap);
  }
  return block;
}

/* ── Task Overview section ──
   Render the short task description at the top
   plus a static "how to read this whole thing" guide that explains the rollup
   semantics, the review checklist, and the deeper concepts (canon/dedup,
   surplus/deficit, precision/recall/f1, full/retrieval, validity/requirements).
   Static prose is authored once and shipped verbatim; only the task-specific
   description + Layout column changes per viewer. */
const TASK_OVERVIEW_HTML = `
<h3>Quick overview</h3>
<ul>
  <li>These are tasks where the agent is asked to produce a lot of entities passing some qualification criteria.</li>
  <li>The qualification is <b>hierarchical</b>, e.g. <code>root(n) → child(m) → url(k)</code> means we need <code>n</code> root entities, each root entity qualifies if it has <code>m</code> qualifying child entities under it, and each child entity qualifies if it has <code>k</code> urls independently corroborating that key path. The agent is expected to produce <code>n × m × k</code> records, each judged independently.</li>
  <li><b>Leaf-keys are always <code>url</code></b>: each record is judged by fetching the url's content and checking whether it corroborates the qualification (1 / 0).</li>
  <li>Metrics form a <b>2×2 grid plus F1</b>: <code>{soft,hard} × {precision,recall}</code>, with <code>soft-f1</code> / <code>hard-f1</code> derived from each pair as <code>2·P·R/(P+R)</code>. One universal rollup at every level: <b>precision</b> averages every supplied child score; <b>recall</b> collapses duplicates via take-worst, ranks descending, and truncates/pads to the required count before averaging. <b>Soft</b> keeps each level's aggregate as-is; <b>hard</b> thresholds it at 1.0 everywhere below the top level, so a subtree counts only once fully qualified and the top level reads as the rate of fully-qualified entities. Soft rewards partial progress; hard demands the whole stack.</li>
  <li><b>Subtasks</b> are additional qualifications for some (non-<code>url</code>) keys, e.g. a flat <code>entity(n) → url(k)</code> subtask can ask for extra evidence attached to the <code>entity</code>. Subtasks have the same general structure as the root task. On rollup, parent values are <b>multiplied</b> by subtask values: if a root entity has root soft-recall = 0.6 and subtask soft-recall = 0.67, its total becomes 0.4. If there is a key above that entity, 0.4 propagates upward instead of 0.6. Subtasks are normally used when the evidence has a different shape (<code>m × n</code> vs <code>n</code>) or you want tighter conditions (a 0 subtask collapses the cell to 0 rather than giving partial 1/<code>m</code> credit).</li>
  <li>Subtasks <b>can have subtasks</b> — used for chain-type tasks: find FDA-approved drugs → find their active molecule → find authors of the discovery paper → find their alma maters. Missing any link in the chain gives the total entity score 0.</li>
</ul>

<h3>How to navigate the viewer</h3>
<p class="ov-hint">Concepts referenced below (canon/dedup, surplus/deficit, the metric grid, full vs retrieval) are unpacked under <b>More details</b>.</p>
<ul>
  <li><b>Configuration</b> — one card per <code>(sub)task</code>.
    <ul>
      <li><b>Task template</b> is the research brief; toggle <code>raw</code> ↔ <code>bound</code> to fill the placeholders in.</li>
      <li><b>Judge template | Schema</b> is what the judge reads and emits per record: <code>section</code> shows the task-specific fragments, <code>full</code> the complete prompt with the universal gates, and <code>rendered (example)</code> substitutes a real record. On subtasks, the first key's volume is decorative — its required count comes from the parent task.</li>
      <li><b>Other templates</b> holds the canon / dedup prompts where the task configures them.</li>
    </ul>
  </li>
  <li>The <b>Rollup</b> is the scored tree. Every row expands/collapses on click; url leaves open a record modal with the full submission (item / answer / excerpts), the judge's per-field breakdown and reasoning, and a page-text preview.
    <ul>
      <li><b>View</b>: <code>composed</code> multiplies subtasks into their parent entities — this is what the headline score reflects; <code>standalone</code> shows each (sub)task's own tree plus per-field decomposition tables; <code>raw</code> shows the flat submitted-record tables and the detected aliases.</li>
      <li><b>Criterion</b>: <code>full</code> is the complete verdict including excerpt discipline; <code>retrieval</code> asks only whether the page satisfies the requirements.</li>
      <li><b>Metric</b>: any cell of the <code>{soft,hard} × {precision,recall,f1}</code> grid. Pills follow the selection; row ordering stays put, so the tree holds still while you flip criterion/metric and watch the numbers change. <b>Sort</b> re-orders the current tree by the selection on demand.</li>
      <li><b>Show duplicates</b> reveals merged-away alias variants inside their take-worst bands; <b>Show hints</b> toggles the per-level annotations.</li>
    </ul>
  </li>
  <li><b>Reading a level hint</b> like <code>20 req: 12.5/20 s-rec, 8/20 h-rec; 25 ans, 2 dup: 18.2/25 prec</code>: twenty required slots holding 12.5 soft-recall / 8 hard-recall mass; 25 records supplied, two collapsed as duplicates, carrying 18.2 precision mass.</li>
  <li><b>Markers and pills</b>: <code>pad</code> rows are zero-filled missing slots and <code>deficit</code> marks how many are lacking; <code>surplus</code> separates over-delivery that only counts where it beats weaker entries; an <code>empty</code> pill means no records exist under a junction where they're expected — typically a subtask with no corresponding entry, failing the composition.</li>
</ul>

<h3>More details</h3>
<ul>
  <li><b>Canon / dedup</b> — two mechanisms for normalizing the key values the agent supplies.
    <ul>
      <li><b>Canon</b> is for closed / predictable sets: it maps surface variants to a canonical name (e.g. "United States" → "USA"). When the canon set is finite, you can require <i>exact recall</i>: set required-n = canon-list-size and let the canon stage disqualify anything outside the list.</li>
      <li><b>Dedup</b> is for unbounded sets: it clusters surface variants by similarity at runtime so different wordings of the same entity collapse via take-worst — a mechanism for penalizing duplicates (submitting two surface variants of the same entity gets collapsed into one slot at the worse of the two scores, instead of counting as two separate qualifying entries).</li>
    </ul>
  </li>
  <li><b>Surplus / deficit</b> — agents could over/under-deliver relative to volume requirements. The recall aggregation sorts entities by score, keeps only the top <i>required</i> (rewarding surplus in expectation) and pads short with zeros (penalizing deficit). Precision has no volume axis: it averages everything supplied, duplicates included.</li>
  <li><b>Reading the grid</b>:
    <ul>
      <li><b>soft-precision</b> ≈ precision (mean of all supplied marks, no dedup/slice/pad). Not affected by alias collapses or volume requirements.</li>
      <li><b>soft-recall relative to soft-precision</b> ≈ recall (low recall + high precision = well-formed records, just too few).</li>
      <li><b>hard relative to soft</b> ≈ comprehensiveness / gappiness / reliability (4/5 evidence each time = soft-recall 80%, hard-recall 0%).</li>
      <li><b>f1</b> per flavor — one number balancing supplied-record quality against required-volume coverage.</li>
    </ul>
  </li>
  <li><b>Excerpt discipline.</b> Beyond the URL itself, each record must include citation text from the page. Excerpts must be <i>faithful</i> to the page (verbatim or near-verbatim, semantics preserved) and the <i>requirements for qualification must be inferable directly from the excerpts alone</i> — i.e. a careful reader given the excerpts but not the page should still arrive at the same yes/no. This splits the judge's evaluation into two sub-criteria: <code>requirements_all_satisfied</code> (via full page content) + <code>requirements_all_supported</code> (via the faithful excerpts alone).</li>
  <li><b>Full vs retrieval</b> — the two lineages, both rolled up identically through the key hierarchy but differing in what counts as a passing leaf signal.
    <ul>
      <li><b>Full</b>: passes only if the page satisfies the requirements AND the agent's excerpts are faithful AND the requirements are excerpt-supported AND the page-content / answer-intent gates pass. Strict; reflects "fully-correct, fully-disciplined record".</li>
      <li><b>Retrieval</b>: passes if <code>requirements_all_satisfied</code> alone — diagnostic on retrieval quality in isolation, independent of excerpt-faithfulness / support. A large retrieval-vs-full gap on the same data means retrieval is fine but the excerpt / record-forming discipline is lacking (or perhaps the discipline requirements are overly harsh / poorly communicated).</li>
    </ul>
  </li>
  <li><b>Validity vs requirements</b> in the judge schema.
    <ul>
      <li><b>Requirements</b> are "the main thing": the page supports the claim, and asking for an exact excerpt proving it makes sense.</li>
      <li><b>Validity</b> is everything else — page-agnostic submission eligibility, shape conditions (e.g. excerpts must be substantive enough), and sanity checks that are sensible for the judge to verify but unsuitable for excerpt-only evidence (e.g. "author is a real person" under a quote ↔ author attribution task: a reasonable bar for the judge, but the attribution page itself isn't where you'd cite evidence of the author's existence).</li>
      <li>When canon is configured, it's automatically promoted into a validity check.</li>
    </ul>
  </li>
</ul>
`;

function renderTaskOverview() {
  const root = document.getElementById("task-overview-body");
  if (!root) return;
  const guide = el("div", {class: "ov-guide"});
  guide.innerHTML = TASK_OVERVIEW_HTML;
  const guideBox = el("div", {class: "ov-guide-box"},
    makeToggle(el("span", {class: "ov-section-label"}, "Guide"), guide));
  root.append(guideBox);
}

function renderOverview() {
  document.getElementById("overview-body").append(renderOverviewNode(DATA.overview));
}

/* Bulk toggle helper for the Configuration section's Expand/Collapse all buttons.
   Opens or collapses every task header + every inner sub-toggle (Task template,
   Judge template | Schema, Other templates) in one sweep. */
function setOverviewOpen(open) {
  const root = document.getElementById("overview-body");
  if (!root) return;
  root.querySelectorAll(".tg-caret").forEach(c => c.classList.toggle("open", open));
  root.querySelectorAll(".tg-body").forEach(b => b.classList.toggle("open", open));
}

// === Rollup tree ===

let currentCriterion = "full";   // "full" | "retrieval"
let currentMetric = "soft_recall";  // "{soft,hard}_{precision,recall,f1}"
let currentView = "composed";    // "composed" | "standalone" | "raw"
let currentSortKey = null;       // {criterion, metric} — set by the Sort button

const METRICS = [
  "soft_precision", "soft_recall", "soft_f1",
  "hard_precision", "hard_recall", "hard_f1",
];

function nodeScore(node) {
  return node?.scores?.[currentCriterion]?.[currentMetric];
}

// === On-demand sibling sort ===
// Row order is baked into the report (full soft-recall) so the tree holds
// still while criterion/metric flip. The Sort button re-orders each key
// level's entity/leaf/merged_group rows by the selected criterion + metric.
// The surplus marker keeps separating the same number of counted slots, and
// deficit/pad rows stay trailing.

function sortValue(node) {
  const value = node?.scores?.[currentSortKey.criterion]?.[currentSortKey.metric];
  return value == null ? -1 : value;
}

function sortLabel(node) {
  return String(node?.value || node?.url || node?.name || "").toLowerCase();
}

function sortedSiblings(children) {
  if (!currentSortKey) return children;
  const sortable = [];
  const trailing = [];
  let surplusMarker = null;
  let countedSlots = 0;
  for (const child of children) {
    const type = child?.type;
    if (type === "entity" || type === "leaf" || type === "merged_group") {
      sortable.push(child);
    } else if (type === "surplus_marker") {
      surplusMarker = child;
      countedSlots = sortable.length;
    } else {
      trailing.push(child);  // deficit_marker, pad
    }
  }
  if (!sortable.length) return children;
  const sorted = [...sortable].sort(
    (a, b) => (sortValue(b) - sortValue(a)) || sortLabel(a).localeCompare(sortLabel(b))
  );
  const rows = surplusMarker
    ? [...sorted.slice(0, countedSlots), surplusMarker, ...sorted.slice(countedSlots)]
    : sorted;
  return [...rows, ...trailing];
}

function keyColor(keyName) { return DATA.key_colors?.[keyName] || null; }
function subtaskColor(taskName) {
  const top = DATA.subtask_top_keys?.[taskName];
  return top ? keyColor(top) : null;
}
function keyText(keyName) {
  const color = keyColor(keyName);
  return color ? `color: ${color.text};` : "";
}
function keyBg(keyName) {
  const color = keyColor(keyName);
  return color ? `background: ${color.bg}; border-left-color: ${color.border};` : "";
}

/* Detect "empty" nodes — those with zero records below them.  Used to render the
   pill as "empty" instead of "0%", which is more honest about missingness
   (skeleton subtask attachments where the subtask has no records for this entity,
   key_levels where no entities were supplied, etc.). */
function nodeIsEmpty(node) {
  if (!node || node.type === "leaf") return false;
  const rollupMeta = node.rollup_meta && node.rollup_meta[currentCriterion];
  if (rollupMeta) return (rollupMeta.provided ?? 0) === 0;
  // Entity / merged_group: no rollup_meta — peek at the first key_level child.
  for (const child of node.children || []) {
    if (child && child.type === "key_level") {
      return ((child.rollup_meta && child.rollup_meta[currentCriterion]) || {}).provided === 0;
    }
  }
  return false;
}

function scorePill(v, isEmpty) {
  if (isEmpty) return el("span", {class: "score-pill s-empty"}, "empty");
  if (v == null) return el("span", {class: "score-pill s-na"}, "—");
  const cls = v >= 0.999 ? "s-pass" : (v <= 0.001 ? "s-fail" : "s-mid");
  return el("span", {class: "score-pill " + cls}, (v * 100).toFixed(0) + "%");
}

// === Rollup-tree rendering ===
// Whole row is clickable to collapse/expand (no caret glyph in the rollup tree itself —
// the Configuration section still uses carets via `.tg-caret`).
// Bars are drawn per-child via CSS pseudo-elements on `.rt-row::before` / `.rt-node::after`
// so `├─` / `└─` shapes can be expressed structurally and colored by the parent's
// `currentColor` (set on `.rt-children`).  See the connector-CSS block for geometry.

function _isBoldType(node) {
  // Tasks / subtasks / key_levels render bold text; their children's connectors thicken
  // to 2.5px to match (via the `.rt-children.bold` modifier on the children wrapper).
  return node && (node.type === "task" || node.type === "subtask" || node.type === "key_level");
}

function _parentColor(node) {
  // The "color" for a parent's children's connector bar = parent's own color.
  // Tasks/subtasks use subtaskColor; key_levels/entities use the key color;
  // merged_groups defer to their first inner child (they all share `key`).
  if (!node) return null;
  if (node.type === "task" || node.type === "subtask") {
    const color = subtaskColor(node.name);
    return color ? color.text : null;
  }
  if (node.type === "key_level" || node.type === "entity") {
    const color = keyColor(node.key);
    return color ? color.text : null;
  }
  if (node.type === "merged_group") {
    const inner = (node.children || [])[0];
    return inner ? _parentColor(inner) : null;
  }
  return null;
}

function makeCollapsibleRow(labelChildren, pillEl, bodyChildren, openByDefault, postPillChildren, parentNode, pathKey) {
  const wrap = el("div", {class: "rt-node"});
  const row = el("div", {class: "rt-row" + (bodyChildren && bodyChildren.length ? " expandable" : "")});
  for (const labelChild of labelChildren) row.append(labelChild);
  if (pillEl) row.append(pillEl);
  if (postPillChildren) for (const postPillChild of postPillChildren) row.append(postPillChild);
  const parentColor = _parentColor(parentNode);
  const childrenStyle = (openByDefault ? "" : "display:none;") + (parentColor ? `color: ${parentColor};` : "");
  const childrenWrap = el("div", {
    class: "rt-children" + (_isBoldType(parentNode) ? " bold" : ""),
    style: childrenStyle,
  });
  if (pathKey) childrenWrap.dataset.k = pathKey;
  for (const bodyChild of bodyChildren) if (bodyChild) childrenWrap.append(bodyChild);
  if (bodyChildren && bodyChildren.length) {
    row.onclick = () => {
      const isOpen = childrenWrap.style.display !== "none";
      childrenWrap.style.display = isOpen ? "none" : "block";
      row.classList.toggle("open", !isOpen);
    };
    if (openByDefault) row.classList.add("open");
  }
  wrap.append(row, childrenWrap);
  return wrap;
}

// Each collapsible container is tagged with an identity path (data-k) built
// from the node chain, so expansion state survives redraws that re-order
// siblings (criterion/metric flips and Sort alike).
function renderRollupNode(node, path = "") {
  const pill = scorePill(nodeScore(node), nodeIsEmpty(node));

  if (node.type === "task") {
    // Root task → no color.  When this renderer is reused for a STANDALONE-view
    // subtask tree, `node.name` is the subtask FQN and `subtaskColor` returns its
    // top-key color, so the standalone subtask header gets colored to match.
    const nodePath = `${path}|t:${node.name || ""}`;
    const color = subtaskColor(node.name);
    const cls = color ? "rt-subtask" : "rt-task";
    const style = color ? `color: ${color.text};` : "";
    const labelChildren = [
      el("span", {class: cls, style}, `#${node.short_name}#`),
      el("span", {class: "rt-meta rt-hint"}, renderKeySummary(node.key_summary)),
    ];
    const childRender = (node.children || []).filter(child => child).map(child => renderRollupNode(child, nodePath));
    return makeCollapsibleRow(labelChildren, pill, childRender, /*open*/ true, null, node, nodePath);
  }
  if (node.type === "subtask") {
    const nodePath = `${path}|s:${node.name || ""}:${node.entity_id || ""}`;
    const color = subtaskColor(node.name);
    const labelChildren = [
      el("span", {class: "rt-subtask", style: color ? `color: ${color.text};` : ""}, `#${node.short_name}#`),
      el("span", {class: "rt-meta rt-hint"}, renderKeySummary(node.key_summary)),
    ];
    const childRender = (node.children || []).map(child => renderRollupNode(child, nodePath));
    return makeCollapsibleRow(labelChildren, pill, childRender, false, null, node, nodePath);
  }
  if (node.type === "key_level") {
    const rollupMeta = node.rollup_meta?.[currentCriterion] || {};
    const softSum = rollupMeta.soft_recall_sum, hardSum = rollupMeta.hard_recall_sum;
    const supplied = rollupMeta.provided ?? node.supplied_count;
    const dupes = rollupMeta.duplicates ?? 0;
    const precSum = rollupMeta.soft_precision_sum;
    const n = node.required;
    const trim = v => (v ?? 0).toFixed(2).replace(/\.?0+$/, "") || "0";
    // Ans block: "m ans, p dup: k/m prec" — always include `dup` (count of supplied
    // entries the LLM-dedup pass collapsed via take-worst at this level).  Three-letter
    // tags (req / ans / dup) stay visually aligned.
    const ansBase = `${supplied} ans, ${dupes} dup`;
    const ans = (supplied > 0 && precSum != null)
      ? `${ansBase}: ${trim(precSum)}/${supplied} prec` : ansBase;
    let summary;
    if (n != null && (softSum != null || hardSum != null)) {
      summary = `${n} req: ${trim(softSum)}/${n} s-rec, ${trim(hardSum)}/${n} h-rec; ${ans}`;
    } else {
      summary = ans;
    }
    const nodePath = `${path}|k:${node.key || ""}`;
    const labelChildren = [
      el("span", {class: "rt-key", style: keyText(node.key)}, node.label),
      el("span", {class: "rt-meta rt-hint"}, summary),
    ];
    const childRender = sortedSiblings(node.children || []).map(child => renderRollupNode(child, nodePath));
    return makeCollapsibleRow(labelChildren, pill, childRender, false, null, node, nodePath);
  }
  if (node.type === "merged_group") {
    // Pass-through wrapper.  Children render directly under the merged_group's own
    // .rt-children container; the band tint comes from the outer .merged-group div
    // which doesn't itself draw a connector bar (its parent already did).
    const nodePath = `${path}|g:${node.entity_id || ""}`;
    const inner = node.children?.[0];
    const groupKey = inner?.key;
    const wrap = el("div", {class: "merged-group", style: keyBg(groupKey)});
    for (const child of node.children) wrap.append(renderRollupNode(child, nodePath));
    return wrap;
  }
  if (node.type === "entity") {
    const nodePath = `${path}|e:${node.value || ""}:${node.entity_id || ""}`;
    const isMerged = node.is_canonical === false;
    const valStyle = keyText(node.key);
    const labelChildren = [
      el("span", {class: "rt-value" + (isMerged ? " merged-away" : ""), style: valStyle},
         node.value || "(empty)"),
    ];
    const postPill = isMerged ? [el("span", {class: "rt-meta"}, "(merged-away)")] : null;
    const childRender = (node.children || []).map(child => renderRollupNode(child, nodePath));
    const row = makeCollapsibleRow(labelChildren, pill, childRender, false, postPill, node, nodePath);
    if (isMerged) row.classList.add("merged-away-subtree");
    return row;
  }
  if (node.type === "leaf") {
    const row = el("div", {class: "rt-leaf"});
    const isMerged = node.is_canonical === false;
    if (isMerged) row.classList.add("merged-away-subtree");
    const urlSpan = el("span", {class: "rt-leaf-url", title: node.url}, node.url);
    row.append(urlSpan, pill);
    if (isMerged) row.append(el("span", {class: "rt-meta"}, "(merged-away)"));
    row.onclick = () => showRecordModal(DATA.records[node.record_idx]);
    return row;
  }
  if (node.type === "deficit_marker" || node.type === "surplus_marker") {
    // Visualizes the rollup's slice/pad math: dashed horizontal connector +
    // short label + dashed trail extending right.  Text color inherits from
    // the parent's `.rt-children` (key/subtask color).
    const isDeficit = node.type === "deficit_marker";
    const cls = "rt-leaf rt-marker " + (isDeficit ? "deficit" : "surplus");
    const text = isDeficit
      ? `deficit (${node.missing} lacking)`
      : `surplus (${node.extra} extra)`;
    const row = el("div", {class: cls});
    row.append(el("span", {class: "rt-marker-label"}, text));
    row.append(el("span", {class: "rt-marker-trail"}));
    return row;
  }
  if (node.type === "pad") {
    // A padded zero slot — solid connector + red "pad" pill (no label).
    // Reflects the `_pad(xs, n)` step that pads short lists with 0.0 up to
    // `required` before averaging.  The pads are REAL contributions to the
    // mean (each one 0%), so they render at full opacity.
    const row = el("div", {class: "rt-leaf rt-pad"});
    row.append(el("span", {class: "score-pill s-fail"}, "pad"));
    return row;
  }
  return el("div", {}, "(unknown node type)");
}

function _collectInvalids(node, invalids) {
  // Walk the tree; collect every key_level that has `invalid` info into a flat
  // list.  Used by the rollup warning block to surface ill-formed records that
  // were excluded from the rollup math (so the user can investigate without
  // having those rows clutter the tree itself).
  if (!node) return;
  if (node.type === "key_level" && node.invalid) {
    invalids.push({
      task_name: node.task_name,
      key: node.key,
      count: node.invalid.count,
      sample_urls: node.invalid.sample_urls,
    });
  }
  for (const child of node.children || []) _collectInvalids(child, invalids);
}

function renderRollupWarnings() {
  // Aggregate invalid-record diagnostics across all composed key-level instances.
  const tally = new Map();
  const occurrences = [];
  _collectInvalids(DATA.composed_tree, occurrences);
  for (const invalid of occurrences) {
    const key = invalid.task_name + "::" + invalid.key;
    const previous = tally.get(key);
    if (previous) {
      previous.count += invalid.count;
      // Keep a few unique sample URLs across occurrences.
      for (const url of (invalid.sample_urls || [])) {
        if (previous.sample_urls.length >= 8) break;
        if (!previous.sample_urls.includes(url)) previous.sample_urls.push(url);
      }
    } else {
      tally.set(key, {
        task_name: invalid.task_name, key: invalid.key, count: invalid.count,
        sample_urls: [...(invalid.sample_urls || [])].slice(0, 8),
      });
    }
  }
  if (tally.size === 0) return null;
  const wrap = el("div", {class: "rollup-warnings"});
  wrap.append(el("div", {class: "rollup-warnings-title"},
    `⚠️ ${tally.size} ill-formed key${tally.size === 1 ? "" : "s"} — records excluded from rollup`));
  const ul = el("ul", {class: "rollup-warnings-list"});
  for (const invalid of tally.values()) {
    const li = el("li", {});
    li.append(el("code", {class: "rollup-warnings-task"}, invalid.task_name));
    li.append(document.createTextNode("  ·  "));
    li.append(document.createTextNode(`${invalid.count} record${invalid.count === 1 ? "" : "s"} with empty `));
    const tip = (invalid.sample_urls || []).join("\n");
    li.append(el("code", {title: tip}, invalid.key));
    li.append(document.createTextNode(" key  (hover key for sample URLs)"));
    ul.append(li);
  }
  wrap.append(ul);
  return wrap;
}

function renderKeySummary(summary) {
  /* Color each key segment in `[gpu(20) → game(10) → url(1)]` according to its key.
     Returns a DocumentFragment-like Node sequence. */
  if (!summary) return document.createTextNode("");
  const span = el("span", {});
  // Tokenize: split on " → " preserving leading "[" and trailing "]"
  const stripped = summary.replace(/^\[|\]$/g, "");
  const parts = stripped.split(" → ");
  span.append(document.createTextNode("["));
  parts.forEach((part, index) => {
    if (index > 0) span.append(document.createTextNode(" → "));
    // Extract key name (alphanum_), e.g. `gpu(20)`, `trade_deal{a,b}(25)`, `url(1)`
    const match = part.match(/^([A-Za-z_][\w]*)/);
    const keyName = match ? match[1] : null;
    const color = keyName ? keyColor(keyName) : null;
    span.append(el("span", {style: color ? `color: ${color.text};` : ""}, part));
  });
  span.append(document.createTextNode("]"));
  return span;
}

function overviewNodeByName(name, node=DATA.overview) {
  if (!node) return null;
  if (node.name === name) return node;
  for (const child of node.children || []) {
    const found = overviewNodeByName(name, child);
    if (found) return found;
  }
  return null;
}

function pctText(v) {
  return v == null ? "—" : `${(v * 100).toFixed(1)}%`;
}

function fieldDecomposition(taskName) {
  return (DATA.field_decompositions || []).find(section => section.name === taskName) || null;
}

function renderFieldDecompositions(taskName) {
  const fields = fieldDecomposition(taskName)?.fields || [];
  if (!fields.length) return null;

  const wrap = el("div", {class: "field-decompositions"});
  const table = el("table", {class: "raw-table"});
  const thead = el("thead");
  const head = el("tr");
  ["field", "true", "false", "prec", "rec", "f1"].forEach((label, i) => {
    head.append(el("th", {class: i === 0 ? "" : "num"}, label));
  });
  thead.append(head);
  table.append(thead);

  const tbody = el("tbody");
  for (const row of fields) {
    const tr = el("tr");
    tr.append(el("td", {}, row.field));
    tr.append(el("td", {class: "num"}, String(row.true ?? "—")));
    tr.append(el("td", {class: "num"}, String(row.false ?? "—")));
    tr.append(el("td", {class: "num"}, pctText(row.soft_precision)));
    tr.append(el("td", {class: "num"}, pctText(row.soft_recall)));
    tr.append(el("td", {class: "num"}, pctText(row.soft_f1)));
    tbody.append(tr);
  }
  table.append(tbody);

  const scroll = el("div", {class: "raw-scroll"});
  scroll.append(table);
  wrap.append(scroll);
  return wrap;
}

function renderRawTable(taskName, rows) {
  /* Per-task raw record table.  Headers: [...item keys, answer, excerpts, url, score].
     Score pill picks node.scores[currentCriterion][currentMetric] (leaf signal — same
     under any view, since there's no further rollup at the leaf level). */
  const wrap = el("div", {style: "margin-bottom: 18px;"});
  // Section title — root task uses neutral; subtasks use their top-level key color.
  const tColor = subtaskColor(taskName);
  const titleClass = tColor ? "rt-subtask" : "rt-task";
  const titleStyle = tColor ? `color: ${tColor.text};` : "";
  const header = el("div", {class: "rt-row", style: "padding-left:0;"},
    el("span", {class: titleClass, style: titleStyle}, `#${taskName}#`),
    el("span", {class: "rt-meta"}, `${rows.length} records`));
  wrap.append(header);

  if (rows.length === 0) {
    wrap.append(el("div", {class: "rt-meta", style: "padding:6px 12px;"}, "(no records)"));
    return wrap;
  }
  const itemKeys = [];
  const seen = new Set();
  for (const r of rows) for (const k of Object.keys(r.item || {})) {
    if (!seen.has(k)) { itemKeys.push(k); seen.add(k); }
  }
  // Drop noisy *_canon keys; sort the rest by natural key_order so columns line up across
  // task/subtask tables in the consistent gpu → game → url orientation.
  const visibleItemKeys = itemKeys
    .filter(k => !k.endsWith("_canon"))
    .sort((a, b) => (DATA.key_order?.[a] ?? 999) - (DATA.key_order?.[b] ?? 999));

  const table = el("table", {class: "raw-table"});
  const thead = el("thead");
  const headRow = el("tr");
  for (const k of visibleItemKeys) {
    headRow.append(el("th", {style: keyText(k)}, k));
  }
  headRow.append(el("th", {}, "answer"));
  headRow.append(el("th", {}, "excerpts"));
  headRow.append(el("th", {style: keyText("url")}, "url"));
  headRow.append(el("th", {}, "score"));
  thead.append(headRow);
  table.append(thead);

  const tbody = el("tbody");
  for (const r of rows) {
    const tr = el("tr");
    tr.onclick = () => showRecordModal(DATA.records[r.record_idx]);
    for (const k of visibleItemKeys) {
      tr.append(el("td", {style: keyText(k)}, String(r.item?.[k] ?? "")));
    }
    tr.append(el("td", {}, el("pre", {class: "raw-cell"}, JSON.stringify(r.answer || {}, null, 0))));
    const ex = (r.excerpts || []).map(e => `• ${e}`).join("\n");
    tr.append(el("td", {}, el("pre", {class: "raw-cell"}, ex || "—")));
    tr.append(el("td", {}, el("a", {href: r.url, target: "_blank", class: "raw-url"}, r.url)));
    const score = (r.scores || {})[currentCriterion]?.[currentMetric];
    tr.append(el("td", {}, scorePill(score)));
    tbody.append(tr);
  }
  table.append(tbody);
  // Wrap in scrollable container — fixed viewport, rows beyond ~20 scroll.
  const scrollWrap = el("div", {class: "raw-scroll"});
  scrollWrap.append(table);
  wrap.append(scrollWrap);
  return wrap;
}

function renderDuplicatesBlock(globalDups) {
  /* Global per-key duplicate groups — one colored block per key, matching the merged-group
     band styling in the rollup tree. Keys ordered per `DATA.key_order` (the natural
     hierarchy/subtask traversal order). */
  if (!globalDups || Object.keys(globalDups).length === 0) return null;
  const wrap = el("div");
  wrap.append(el("h4", {class: "dup-block-title"}, "Aliases detected"));
  const keys = Object.keys(globalDups).sort(
    (a, b) => (DATA.key_order?.[a] ?? 999) - (DATA.key_order?.[b] ?? 999)
  );
  for (const key of keys) {
    const groups = globalDups[key];
    const block = el("div", {class: "dup-key-block", style: keyBg(key)});
    block.append(el("div", {class: "dup-node", style: keyText(key)}, `[${key}]`));
    const ul = el("ul", {class: "dup-list"});
    for (const group of groups) {
      const others = group.variants.filter(variant => variant !== group.canonical);
      // One row per variant — canonical on top (kept as the list's bullet),
      // each alias on its own `⇄` line below.  Easier to read for long quote-like
      // values than a comma-joined run-on.
      const li = el("li");
      li.append(el("div", {class: "dup-canon"}, group.canonical));
      for (const alias of others) {
        li.append(el("div", {class: "dup-others"}, "⇄ " + alias));
      }
      ul.append(li);
    }
    block.append(ul);
    wrap.append(block);
  }
  return wrap;
}

function renderRollup() {
  // Toolbar lives in the sticky head (with the "Rollup" h2) so it stays pinned at
  // the viewport top while the tree scrolls underneath.  Tree content goes in
  // `rollup-body`, which scrolls normally.
  const stickyHead = document.getElementById("rollup-sticky");
  const body = document.getElementById("rollup-body");
  const warnings = renderRollupWarnings();
  if (warnings) stickyHead.append(warnings);
  const toolbar = el("div", {class: "toolbar"});

  // Order: View | Criterion | Metric | Sort | Show Duplicates | Show Hints.
  // Everything after Criterion is tree-only — faded in raw view.
  const viewSel = el("select");
  for (const view of ["composed", "standalone", "raw"]) viewSel.append(el("option", {value: view}, view));
  const critSel = el("select");
  for (const criterion of ["full", "retrieval"]) critSel.append(el("option", {value: criterion}, criterion));
  const metSel = el("select");
  for (const metric of METRICS) metSel.append(el("option", {value: metric}, metric));
  metSel.value = currentMetric;
  viewSel.value = currentView;
  critSel.value = currentCriterion;

  const dupsLabel = el("label", {class: "hints-toggle ctrl-tree-only"});
  const dupsCb = el("input", {type: "checkbox"}); dupsCb.checked = false;
  dupsLabel.append(dupsCb, document.createTextNode(" Show duplicates"));

  const hintsLabel = el("label", {class: "hints-toggle ctrl-tree-only"});
  const hintsCb = el("input", {type: "checkbox"}); hintsCb.checked = true;
  hintsLabel.append(hintsCb, document.createTextNode(" Show hints"));

  // "Sort" re-orders each key level by the selected criterion + metric; the
  // ordering then sticks until the next click, so criterion/metric flips keep
  // the tree still.  Expansion state is preserved via identity-keyed capture.
  const sortBtn = el("button", {
    class: "ctrl-tree-only",
    title: "Re-order rows by the selected criterion + metric",
  }, "Sort");

  // "Expand all" / "Collapse all" — opens or closes every collapsible row in the
  // current tree.  Tree-view-only (faded out in raw view via .ctrl-tree-only).
  const expandBtn = el("button", {class: "ctrl-tree-only"}, "Expand all");
  const collapseBtn = el("button", {class: "ctrl-tree-only"}, "Collapse all");

  toolbar.append(
    el("span", {}, "View:"), viewSel,
    el("span", {}, "Criterion:"), critSel,
    el("span", {class: "ctrl-tree-only"}, "Metric:"), metSel,
    sortBtn,
    dupsLabel,
    hintsLabel,
    expandBtn,
    collapseBtn,
  );
  metSel.classList.add("ctrl-tree-only");
  stickyHead.append(toolbar);

  const navHint = el("div", {class: "rollup-nav-hint"});
  navHint.innerHTML = `<ul>
    <li>click any node to expand the tree view, click again to collapse</li>
    <li>click any url-carrying row to show the full submission pop-up view</li>
    <li>change <b>view</b> from <code>composed</code> to <code>raw</code> to see the flat record submissions; when subtasks are present, switch to <code>standalone</code> to see each (sub)task's rollup tree independently</li>
    <li>change <b>criterion</b> from <code>full</code> to <code>retrieval</code> to see url-only scores without the citation-text (excerpts) grading gates</li>
    <li>change <b>metric</b> across the <code>{soft,hard} × {precision,recall,f1}</code> grid</li>
    <li>rows hold still until <b>Sort</b> re-orders them by the current criterion + metric selection</li>
  </ul>`;
  stickyHead.append(navHint);

  // Match the dupsCb default (off) — `.hide-dups` collapses merged-away rows.
  const treeBox = el("div", {class: "rollup-grid" + (dupsCb.checked ? "" : " hide-dups")});
  const standaloneTreesByName = Object.fromEntries(
    (DATA.standalone_trees || []).map(t => [t.name, t])
  );

  const draw = () => {
    toolbar.classList.toggle("raw-mode", currentView === "raw");
    if (currentView === "composed") {
      treeBox.replaceChildren(renderRollupNode(DATA.composed_tree));
    } else if (currentView === "standalone") {
      // One tree per task in natural task_order. The tree's top row already
      // shows the fully-qualified `#name#`, so standalone view does not need
      // an outer header.
      const wrap = el("div");
      const order = DATA.task_order || Object.keys(standaloneTreesByName);
      order.forEach((name, i) => {
        const t = standaloneTreesByName[name];
        if (!t) return;
        const sec = el("div", {style: i > 0 ? "margin-top:18px;" : ""});
        sec.append(renderRollupNode(t.tree));
        wrap.append(sec);
      });
      const fieldWrap = el("div", {style: "margin-top:22px; padding-top:12px; border-top:1px solid var(--border);"});
      let nFieldTables = 0;
      order.forEach((name, i) => {
        const fields = renderFieldDecompositions(name);
        if (!fields) return;
        const tColor = subtaskColor(name);
        const titleClass = tColor ? "rt-subtask" : "rt-task";
        const titleStyle = tColor ? `color: ${tColor.text};` : "";
        const sec = el("div", {style: nFieldTables > 0 ? "margin-top:18px;" : ""});
        sec.append(el("div", {class: titleClass, style: titleStyle}, `#${name}#`));
        sec.append(fields);
        fieldWrap.append(sec);
        nFieldTables += 1;
      });
      if (nFieldTables > 0) wrap.append(fieldWrap);
      treeBox.replaceChildren(wrap);
    } else {  // raw
      const wrap = el("div");
      const dups = renderDuplicatesBlock(DATA.duplicates_global);
      if (dups) wrap.append(dups);
      const order = DATA.task_order || Object.keys(DATA.records_by_task);
      for (const taskName of order) {
        const rows = DATA.records_by_task[taskName];
        if (rows) wrap.append(renderRawTable(taskName, rows));
      }
      treeBox.replaceChildren(wrap);
    }
  };
  // Capture/restore expansion state across redraws, keyed by each container's
  // identity path (data-k) so it survives sibling re-ordering (Sort) as well
  // as criterion/metric flips.
  const captureExpansion = () => {
    const state = {};
    treeBox.querySelectorAll(".rt-children[data-k]").forEach(container => {
      state[container.dataset.k] = container.style.display !== "none";
    });
    return state;
  };
  const restoreExpansion = (state) => {
    treeBox.querySelectorAll(".rt-children[data-k]").forEach(container => {
      const open = state[container.dataset.k];
      if (open === undefined) return;
      container.style.display = open ? "block" : "none";
      const row = container.previousElementSibling;
      if (!row || !row.classList) return;
      row.classList.toggle("open", open);
      const caret = row.querySelector(".tg-caret");
      if (caret) caret.classList.toggle("open", open);
    });
  };
  const drawPreserving = () => {
    const s = captureExpansion();
    draw();
    restoreExpansion(s);
  };

  viewSel.onchange = () => { currentView = viewSel.value; draw(); };
  critSel.onchange = () => { currentCriterion = critSel.value; drawPreserving(); };
  metSel.onchange  = () => { currentMetric = metSel.value; drawPreserving(); };
  sortBtn.onclick  = () => {
    currentSortKey = {criterion: currentCriterion, metric: currentMetric};
    drawPreserving();
  };
  dupsCb.onchange  = () => { treeBox.classList.toggle("hide-dups", !dupsCb.checked); };
  hintsCb.onchange = () => {
    treeBox.classList.toggle("hide-hints", !hintsCb.checked);
    navHint.style.display = hintsCb.checked ? "" : "none";
  };
  const _setTreeOpen = (open) => {
    // Open/close every collapsible row in the current tree: caret class, .rt-children
    // display, .tg-body (if any) class, and .rt-row.open marker for whole-row clicks.
    treeBox.querySelectorAll(".tg-caret").forEach(c => c.classList.toggle("open", open));
    treeBox.querySelectorAll(".rt-children").forEach(c => { c.style.display = open ? "block" : "none"; });
    treeBox.querySelectorAll(".tg-body").forEach(b => b.classList.toggle("open", open));
    treeBox.querySelectorAll(".rt-row").forEach(r => r.classList.toggle("open", open));
  };
  expandBtn.onclick = () => _setTreeOpen(true);
  collapseBtn.onclick = () => _setTreeOpen(false);
  body.append(treeBox);
  draw();
}

// === Record modal ===

function renderJudgeGroups(judge, schemaGroups) {
  /* Render judge values in canonical order, paired display for *_satisfied/*_supported. */
  const wrap = el("div");
  for (const group of schemaGroups || []) {
    wrap.append(el("div", {class: "judge-section-label"}, group.label));
    if (group.kind === "fields") {
      for (const field of group.fields) wrap.append(renderJudgeField(field.name, judge[field.name]));
    } else if (group.kind === "pairs") {
      for (const pair of group.pairs) {
        const pairBox = el("div", {class: "judge-pair"});
        pairBox.append(renderJudgeField(pair.satisfied.name, judge[pair.satisfied.name]));
        pairBox.append(renderJudgeField(pair.supported.name, judge[pair.supported.name]));
        wrap.append(pairBox);
      }
    }
  }
  return wrap;
}

function renderJudgeField(name, value) {
  const box = el("div", {class: "judge-row"});
  if (typeof value === "boolean") box.classList.add(value ? "bool-true" : "bool-false");
  let display;
  if (typeof value === "boolean") display = String(value);
  else if (name === "reasoning") {
    box.append(el("div", {class: "name"}, name));
    box.append(el("pre", {class: "rendered", style: "margin-top:3px"}, String(value ?? "")));
    return box;
  }
  else if (typeof value === "string" || typeof value === "number") display = String(value);
  else if (value == null) display = "—";
  else display = JSON.stringify(value);
  box.append(el("span", {class: "name"}, name), el("span", {class: "val"}, display));
  return box;
}

function findOverviewNode(name, root=DATA.overview) {
  if (root.name === name) return root;
  for (const child of root.children || []) {
    const found = findOverviewNode(name, child);
    if (found) return found;
  }
  return null;
}

function safeExternalUrl(value) {
  try {
    const parsed = new URL(String(value));
    return (parsed.protocol === "http:" || parsed.protocol === "https:") ? parsed.href : null;
  } catch (_) {
    return null;
  }
}

function showRecordModal(record) {
  const body = document.getElementById("modal-body");
  body.replaceChildren();
  const ovNode = findOverviewNode(record.task_name) || DATA.overview;

  body.append(el("h3", {}, `${record.task_name}`));
  body.append(el("div", {class: "rt-meta", style: "margin-bottom:10px"}, ovNode.key_summary));

  // SUBMISSION block: URL + ITEM + ANSWER + EXCERPTS
  body.append(el("h4", {}, "Submission"));
  const sub = el("div", {style: "padding-left:6px; border-left: 2px solid var(--accent-soft);"});
  // URL
  sub.append(el("div", {class: "judge-section-label"}, "url"));
  const safeUrl = safeExternalUrl(record.url);
  if (safeUrl) {
    sub.append(el("a", {class: "url-link", href: safeUrl, target: "_blank", rel: "noopener noreferrer"}, record.url));
  } else {
    sub.append(el("span", {class: "url-link"}, String(record.url || "")));
  }
  // Item
  sub.append(el("div", {class: "judge-section-label", style: "margin-top:8px"}, "item"));
  const itemDl = el("dl", {class: "kv-grid"});
  for (const [k, v] of Object.entries(record.item || {})) {
    itemDl.append(el("dt", {}, k), el("dd", {}, String(v)));
  }
  sub.append(itemDl);
  // Answer — render as a literal JSON dict (matches the raw-table column format
  // and treats an empty answer naturally as `{}`).
  sub.append(el("div", {class: "judge-section-label", style: "margin-top:8px"}, "answer"));
  sub.append(el("pre", {class: "raw-cell"}, JSON.stringify(record.answer || {}, null, 0)));
  if (record.__comment) {
    sub.append(el("div", {class: "judge-section-label", style: "margin-top:8px"}, "record comment"));
    sub.append(el("pre", {class: "rendered"}, String(record.__comment)));
  }
  // Excerpts
  sub.append(el("div", {class: "judge-section-label", style: "margin-top:8px"}, `excerpts (${(record.excerpts || []).length})`));
  if (record.excerpts && record.excerpts.length) {
    sub.append(el("pre", {class: "rendered"}, record.excerpts.map(e => `• ${e}`).join("\n\n")));
  } else {
    sub.append(el("div", {class: "rt-meta"}, "(none)"));
  }
  body.append(sub);

  // Judge in canonical order
  body.append(el("h4", {}, "Judge"));
  body.append(renderJudgeGroups(record.judge || {}, ovNode.schema_groups || []));

  // Page text preview
  if (record.page_text_preview) {
    body.append(el("h4", {}, `Page text (preview, ${record.page_text_preview.length} chars)`));
    body.append(el("pre", {class: "rendered"}, record.page_text_preview));
  }

  document.getElementById("modal-backdrop").classList.add("active");
}

function closeModal() { document.getElementById("modal-backdrop").classList.remove("active"); }
document.getElementById("modal-backdrop").onclick = (e) => { if (e.target.id === "modal-backdrop") closeModal(); };
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });

// init
renderTaskOverview();
renderOverview();
renderRollup();
</script>
</body>
</html>
"""


def render_report_html(report: dict[str, Any]) -> str:
    viewer_data = {
        key: value for key, value in report.items() if key not in {"scoremap", "full_instruction"}
    }
    encoded = orjson.dumps(viewer_data).decode("utf-8")
    # HTML parses script end tags case-insensitively. Escaping every markup
    # delimiter keeps serialized, untrusted report strings inside the JS value.
    encoded = (
        encoded.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
    html = HTML_TEMPLATE.replace("__TITLE__", f"viewer · {report['task_name']}")
    return html.replace("__VIEWER_DATA__", encoded)


def emit_html(report: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_report_html(report))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("metrics_json", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    report = report_from_metrics_file(args.metrics_json)
    out_path = args.output or args.metrics_json.with_name("report.html")
    emit_html(report, out_path)
    print(f"{report['task_name']} → {out_path}")
    print(f"  records: {len(report['records'])}  tasks: {report['task_order']}")


if __name__ == "__main__":
    main()

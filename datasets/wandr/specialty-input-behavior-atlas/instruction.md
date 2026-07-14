Solve the following task and write the results to the specified JSONL file.

## Universal rules

The following rules apply to every task below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets.

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `specialty_input_behavior_atlas`

Build a factual public evidence atlas of documented user-visible behavior for
specialty input/control components. For 55+ systems or
libraries, identify 3+ specialty input/control
components per system or library; for each system/control pair and each of the
3 behavior facets listed below, supply 2+
meaningfully distinct documented behavior findings, each backed by a public
behavior-evidence source (i.e. 1+ URL).

This is an evidence atlas, not a recommendation list, implementation-code
inventory, product-help spreadsheet, live-demo catalog, version-change tracker,
or source-status audit. The evidence of interest is public page text that says
how a reusable input/control behaves for users.

Behavior facets:

- `entry_parsing_or_formatting`: how user-entered values are parsed, masked,
  segmented, formatted, normalized, constrained while typing, or represented in
  the visible field.
- `keyboard_focus_or_commit`: keyboard operation, focus movement, selection,
  opening/closing, accepting, cancelling, committing, clearing, tabbing, or
  related interaction semantics.
- `validation_error_or_boundary`: validation states, invalid values, min/max or
  boundary behavior, required/optional behavior, error messaging,
  disabled/read-only constraints, rejected input, or equivalent user-visible
  boundary behavior.

The system/library ought to be a public reusable UI source family, such as a
design system, component library, enterprise UI framework, UI kit, government or
public-sector component system, Web Component library, accessibility pattern
library, formatter, or masking library. The component/control ought to be a
genuine user-facing specialty input/control. Examples include date pickers, date
fields, time pickers, number fields, currency or formatted-number inputs, file
inputs, uploads, comboboxes, autocomplete controls, selects, token or
multi-value inputs, masked inputs, sliders, steppers, rating controls, and
segmented inputs. A generic text input is in scope only when the page documents a
concrete typed, constrained, masked, formatted, or otherwise specialty behavior
mode. The URL should be public, non-login, non-paywalled, and usable as text
evidence; broken pages, search-results pages, gated Storybooks,
screenshot/video-only pages, and JavaScript-empty demo shells with no readable
behavior text are outside the task.

Requirements:

- The page must identify the claimed system/library and the claimed
  component/control, either directly in page text or through clear project,
  title, URL, repository-path, or documentation context.
- The page should make its reusable-control evidence role visible. Official or
  maintainer/project-linked component docs, pattern/accessibility docs, docs
  source markdown, product help pages, release or changelog notes, and public
  project-linked issue/discussion pages can qualify when their text anchors them
  to the claimed system/control and concrete user-visible behavior. Generic
  marketing, random forum/listing pages, unrelated tutorials, package mirrors,
  search-result pages, implementation-only code with no user-visible behavior,
  and generic workflow help with no reusable-control behavior usually will not
  contain enough source-role evidence.
- The page must state the claimed behavior finding as concrete user-visible
  behavior for the claimed component/control and selected behavior facet. Generic
  claims such as "accessible", "customizable", "supports validation", broad
  best-practice advice, property names alone, or API/code snippets alone do not
  count unless the page ties them to an observable behavior of the control. Two
  findings are distinct only when they state different observable behavior, not
  paraphrases of the same sentence or broad component capability.

Write one JSON object per line to `results_specialty_input_behavior_atlas.jsonl`:
{"item": { "system_or_library": "<system_or_library>", "component_or_control": "<component_or_control>", "behavior_facet": "<behavior_facet>", "behavior_finding": "<behavior_finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

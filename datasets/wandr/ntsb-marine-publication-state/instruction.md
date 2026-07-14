You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `ntsb_marine_publication_state`
  - `ntsb_marine_publication_state.docket_state`
  - `ntsb_marine_publication_state.report_release`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `ntsb_marine_publication_state`

For 40+ NTSB marine investigations with accident dates from January 1, 2021 through December 31, 2025, supply 1+ official NTSB investigation detail URL per investigation that states the investigation identity and current public lifecycle status.

Use `investigation` as the NTSB investigation number plus a concise event title, such as `DCA25FM012 — Collision between Towing Vessel Patrick J Studdert and Bulk Carrier Clara B`. In the answer, name the source-stated status, event date, location or waterway, and any report/docket links shown on the page that help explain the public-record state.

This task is about the NTSB public record lifecycle, not a vessel casualty table. CAROL search/API/export pages are fine for discovery, but they do not satisfy this root record by themselves; the scored URL must be the official per-investigation NTSB page. Do not add causal analysis, legal fault, blame, safety advice, casualty-field inference, or report/docket absence inferred from search failure.

Requirements:
- The page must identify the claimed NTSB investigation as a marine investigation, including the investigation number and enough event title, vessel, location, or waterway context to anchor the item.
- The page must state an event/accident date within January 1, 2021 through December 31, 2025.
- The page must state the current source-stated public lifecycle status for the investigation, such as `Ongoing`, `Completed`, probable-cause text already posted, report links already posted, or page-present language that the investigation remains underway.

Write one JSON object per line to `results_ntsb_marine_publication_state.jsonl`:
{"item": { "ntsb_number": "<ntsb_number>", "event_title": "<event_title>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `ntsb_marine_publication_state.docket_state`

Cross-tasknode identifier discipline: this task is for the same {= investigation =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= investigation =}+ NTSB marine investigations with accident dates from January 1, 2021 through December 31, 2025, supply 1+ official NTSB Docket Management System URL per investigation that states the public docket state.

Use the `data.ntsb.gov/Docket/?NTSBNumber=<id>` route, or a printable table-of-contents page reached from that docket, so the docket state is tied to the NTSB investigation number. In the answer, name the docket state (`released` or `not released`), public release date/time when shown, and docket item count when shown.

The docket state must be page-present official state. A released docket must show project summary/release metadata or docket items. An unreleased docket must cite the official Docket page that says the docket has not been released. Do not substitute CAROL exports, broad search results, or an inferred absence of docket items.

Requirements:
- The page or URL must tie the docket state to the claimed NTSB investigation number.
- The page must state the public docket state: either a public-release date/time with docket item summary, or explicit language that the docket for the investigation has not been released.

Write one JSON object per line to `results_ntsb_marine_publication_state.docket_state.jsonl`:
{"item": { "ntsb_number": "<ntsb_number>", "event_title": "<event_title>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `ntsb_marine_publication_state.report_release`

Cross-tasknode identifier discipline: this task is for the same {= investigation =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= investigation =}+ NTSB marine investigations with accident dates from January 1, 2021 through December 31, 2025, supply 1+ official NTSB URL per investigation that states the report-product release or no-final-yet state.

Eligible evidence includes an NTSB report/brief PDF, a per-investigation NTSB page with a `Reports` section or explicit ongoing/no-final language, or an NTSB docket page/item listing that identifies a close-out memorandum or other official report product. In the answer, name the report-release state, report/brief/memo number or title when present, release/adoption/reissue date when present, and any source-stated probable-cause or casualty detail you choose to include.

No-final, no-brief, or no-report states must be positively stated by an official page, such as an ongoing-investigation passage, an NTSB statement that another agency will produce the final report, or an official close-out memorandum listing. Do not infer missing reports from search absence, and do not use CAROL exports or aggregate report indexes as scored evidence by themselves. Probable cause, casualty fields, and report type must stay source-stated; do not add causal/legal analysis or blame beyond NTSB wording.

Requirements:
- The source must tie the report-product state to the claimed NTSB investigation number or unmistakable event title.
- The source must state the report-product release state claimed in the answer, such as a released MIR/MAB/final report, a close-out memorandum, a corrected/reissued report, or an ongoing/no-final-yet state.
- Any report type, report number, report date, probable-cause text, casualty field, reissue/correction note, or no-final explanation included in the answer must be directly source-stated.

Write one JSON object per line to `results_ntsb_marine_publication_state.report_release.jsonl`:
{"item": { "ntsb_number": "<ntsb_number>", "event_title": "<event_title>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

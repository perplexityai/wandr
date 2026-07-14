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

## `npdes_cwa_records`

For at least 5+ CWA/NPDES `record_class` buckets, find at least 20+ Clean Water Act / NPDES permits in each bucket, name at least 1+ source-stated CWA/NPDES public record for each permit-class pair, and supply at least 1+ official EPA/ECHO URL for each permit-record row.

Use one of these `record_class` values for every row: `permit_status_period`, `violation_noncompliance`, `inspection_evaluation`, `enforcement_action`, or `dmr_limit_value`. The `record_kind` must be a specific source-stated record inside that class, not just a restatement of the class label. Use the NPDES permit or official permit-tracking ID as the identity spine. Facility name, FRS/Registry ID, address, operator, and geography are useful answer context, but they do not replace the permit ID. Make each `cwa_record` specific enough to disambiguate the record class, record kind, date or reporting period, and source-stated status/action/value; for DMR or limit rows, include the pollutant/parameter, outfall, monitoring period, or comparable source row anchors when they are needed to identify the row.

Use official EPA/ECHO or EPA CWA/NPDES human-readable pages or reports as row evidence. The cited URL's visible page/report text must expose the permit-specific row fact and its date, period, or as-of/vintage context. Do not use raw ECHO REST/API responses, JSON blobs, raw CSV/ZIP download rows, Swagger/spec payloads, or script-parsed structured data as row evidence. A data dictionary, download summary, search form, or top-level Detailed Facility Report summary can support context, but it is not enough by itself for a permit-record row if the claimed row facts live somewhere else.

This is intended as current/as-of public-record provenance, not a historical annual-report transcription task. Historical permit periods or old actions can be valid when they are displayed on a current official EPA/ECHO page or report with a current page/report vintage. Legacy annual compliance/noncompliance appendices, archived annual reports, or old dense list PDFs whose own publication/reporting vintage is before 2020 do not satisfy row evidence by themselves. Do not submit rows whose only permit-specific fact is membership in an old annual appendix/list with one repeated status/action/value.

The record fact should be specific to the permit and class rather than a generic source-page fact. Repeated identical triples of `record_kind`, `date_or_period`, and `source_stated_status_action_or_value` with only the permit ID changed are weak unless the cited page visibly supports each permit-specific row fact.

Requirements:
- The page must be an official EPA/ECHO or EPA CWA/NPDES human-readable page/report surface for the claimed row.
- The page must identify the claimed NPDES permit ID and tie the record to CWA/NPDES context.
- The claimed row must fit the submitted `record_class`.
- The page must support the claimed record kind and source-stated status, action, violation, limit, DMR value, noncompliance status, inspection/evaluation fact, or comparable row fact.
- The page must support the claimed date, monitoring period, reporting quarter, permit period, action date, inspection date, or explicit data vintage/as-of period for the row.
- The cited source must not be a pre-2020 annual appendix/report-only row.

Write one JSON object per line to `results_npdes_cwa_records.jsonl`:
{"item": { "record_class": "<record_class>", "npdes_permit": "<npdes_permit>", "record_kind": "<record_kind>", "date_or_period": "<date_or_period>", "source_stated_status_action_or_value": "<source_stated_status_action_or_value>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

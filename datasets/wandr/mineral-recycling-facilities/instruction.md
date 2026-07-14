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

## `mineral_recycling_facilities`

For 90+ companies, public agencies, joint ventures, subsidiaries, or comparable operators with 1+ well-identified critical-mineral or metal recycling facility, asset, hub, campus, plant, project, or site-level operation each, supply 1+ public source URLs per facility asset that substantiate source-stated recycling or recovery capability.

This is a public provenance task, not a ranking, sourcing, investment, procurement, supplier-recommendation, market-scoring, outreach, lead-generation, contact-enrichment, price-forecast, or capacity-comparison task. Use May 1, 2026 as the reference date for interpreting facility status, ownership, and public capability claims: planned, under-construction, operating, paused, acquired, and unclear status can all count when the source states them, but announced or designed capacity should stay announced or designed.

Eligible source classes include official facility pages, sustainability or annual reports with site-level detail, public filings, regulator permits, environmental assessments, technical brochures or PDFs, investor presentations, trade-association pages with substantive site claims, and reputable industry articles. Contact-only directories, company-wide recycling blurbs, generic "top recycler" lists, procurement pages, investment writeups, and pages whose only value is contact information do not count unless the page itself gives substantive facility-level capability evidence.

Capacity, throughput, volume, parent/acquirer, and facility-status details are optional. Preserve them only when the page states them; preserve the source's units and qualifiers instead of normalizing, comparing, or scoring them. For downstream provenance use, also note the public source class, visible source date, page checked date, confidence, and missing or conflict states such as no parent source, no capacity source, no current page, no mineral source, no facility source, or name conflict.

Requirements:
- The page must be a public provenance source with substantive content about the submitted facility asset, not merely a contact directory, broad ranking, procurement page, investment thesis, or generic company overview.
- The page must tie the submitted operator to the submitted facility, asset, hub, campus, plant, project, or site-level operation.
- The page must explicitly connect that facility asset to recycling, recovery, refining, reprocessing, or resource recovery of critical-mineral, battery-material, rare-earth, e-waste, industrial/base-metal, precious-metal, or PGM-bearing streams or outputs.
- Any submitted details about materials, feedstock or output, process or service, status, parent or acquirer, capacity, throughput, volume, units, source date, source class, and missing/conflict states must be source-stated or clearly marked as absent; capacity, throughput, and volume claims must preserve source wording, units, and qualifiers.

Write one JSON object per line to `results_mineral_recycling_facilities.jsonl`:
{"item": { "operator": "<operator>", "facility_asset": "<facility_asset>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

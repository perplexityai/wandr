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

## `opto_stage_variant_provenance`

For 30+ suppliers of opto-mechanical positioning stages, with 2+ product families per supplier and 2+ part-numbered or model-coded variants per product family, supply an official source URL for each variant that documents why the variant belongs in the 100-150 mm provenance set (at least 1 URL per variant).

The useful output is a public product/spec provenance census, not a purchase comparison. For each record, report the source-stated qualifying dimension type and value, stage type or axes when stated, useful native-unit specs, source class, source date or observed date when present, checked date, confidence, and source-stated missing/partial/name-conflict states. Public price, quote-required state, and origin/manufacturing claims should be recorded only when the cited public source states them.

A variant counts when an official source states a 100-150 mm inclusive platform/table/top-plate side length, stage/table diameter, or primary travel/stroke for the submitted part number/model code. The source can be an official product page, manufacturer family/specification table, manufacturer-hosted datasheet or catalog PDF, or equivalent manufacturer-controlled technical page. Distributor pages and optics directories can help discovery or alternate-SKU corroboration, but they do not replace official spec evidence for this task.

Manual and motorized linear/translation stages, XY stages, goniometers, rotation/tilt stages, vertical/labjack stages, and comparable opto-mechanical positioning stages can all fit when the source binds the in-band dimension to the specific variant. Do not normalize specs into rankings, calculate cost/precision value, infer origin, infer dimensions from images, contact vendors, recommend products, or treat a family-level range as variant-level evidence unless the source table or page binds the in-band value to the submitted variant.

Requirements:
- The page should visibly be a manufacturer-controlled product page, family specification table, datasheet/catalog PDF, or equivalent official technical source for the claimed supplier.
- The page must bind the claimed supplier, product family, and submitted part-numbered/model-coded variant together.
- The page must source-state the qualifying 100-150 mm dimension type and value for the submitted variant or an explicitly bound variant row.
- The page should expose at least two additional source-stated technical specifications for the variant or explicitly bound family row, preserving native units and source wording.
- Reported specs and optional provenance states should remain source-stated: source dates, public price, quote-required state, origin claims, conflicts, and missing/partial states should not be invented, normalized into scores, or converted into purchase advice.

Write one JSON object per line to `results_opto_stage_variant_provenance.jsonl`:
{"item": { "supplier": "<supplier>", "product_family": "<product_family>", "qualifying_variant": "<qualifying_variant>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

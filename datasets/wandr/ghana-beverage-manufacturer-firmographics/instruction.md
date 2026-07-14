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

## `ghana_beverage_manufacturer_firmographics`

Identify 75+ companies as Ghana beverage manufacturers; for each manufacturer, cover each of the 3 firmographic facets below by supplying a public source (i.e. 1+ URL under each facet) that states a manufacturer-specific firmographic fact. Use source-family separation: do not rely on one URL, one PDF, one multi-company registry/list, or one source family for all facets for a manufacturer. Suitable sources include company-controlled pages, parent-company disclosures, annual reports or prospectuses, manufacturer-specific Ghana public authority profiles, reputable Ghana business profiles, and official public records when they visibly support the specific manufacturer fact; lead/contact databases, rankings/listicles, supplier recommendations, market outlooks, sales-targeting pages, and safety/quality/compliance verdicts do not count.

Firmographic facets:
- `product_line`: beverage products, product categories, named brands, or product lines tied to the manufacturer, from a manufacturer-specific product/brand/company page, parent disclosure, annual report/prospectus, reputable company profile, or public authority profile centered on that manufacturer. Multi-company product registers, certification lists, standards/FDA/GSA-style tables, and appendices listing many producers do not count as sole `product_line` evidence.
- `ghana_location_or_facility`: source-stated Ghana headquarters, factory, plant, production facility, bottling/manufacturing site, or operational facility tied to the manufacturer. Company pages, manufacturer-specific profiles, and public registry/list rows can count here when the cited content visibly names the manufacturer and a Ghana site.
- `corporate_history_or_control`: source-stated founding, incorporation, start-production, parent/subsidiary relation, ownership, listing status, nationality, corporate-group relation, revenue/financial-period, workforce, capacity, production-size, annual-report/prospectus fact, or comparable corporate history/control/scale fact tied to the manufacturer. A mere product registration, license number, certification status, source period, or inclusion on a multi-company product/standards/FDA/GSA-style list does not count for this facet, even when the same row names the product and location.

Bottlers, breweries, distillers, water producers, and other beverage producers count when the source ties them to Ghana manufacturing, production, bottling, factory, plant, or facility evidence. Product brands do not count as manufacturers unless the source treats the brand itself as the operating or manufacturing entity; importer-, distributor-, retailer-, or seller-only evidence does not establish a manufacturer.

Requirements:
- The page must identify the submitted manufacturer or operating company.
- The page must tie that manufacturer to beverage manufacturing, production, bottling, brewing, distilling, water production, or a beverage facility in Ghana.
- The page must state a firmographic fact matching the selected `firmographic_facet`, with any visible source date, period, status, or currentness context preserved when it is load-bearing for the fact.

Write one JSON object per line to `results_ghana_beverage_manufacturer_firmographics.jsonl`:
{"item": { "manufacturer": "<manufacturer>", "firmographic_facet": "<firmographic_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `wa_grocery_distributor_capability_provenance`

For 210+ wholesale grocery, foodservice, convenience, specialty/import, produce/fresh, cash-and-carry, or institutional food distributors serving Washington or a clearly Washington-linked regional market, supply public evidence for each of the 3 capability facets below (i.e. 1+ URL for each distributor/facet pair).

The goal is public provenance for a regional food-distribution capability picture, not a supplier recommendation, contact list, procurement guide, ranking, lead-scoring sheet, or outreach plan.

Capability facets:
- `service_scope`: source-stated products, services, or customer channels served, such as grocery, independent grocery, convenience, foodservice, restaurant, specialty/import, produce/fresh, cash-and-carry, institutional/public food, or similar.
- `geographic_footprint`: source-stated service area, distribution area, route region, Washington city/subregion, Inland Northwest, Pacific Northwest, West Coast, official Washington facility/location/store presence, or comparable regional service basis.
- `facility_or_operations`: source-stated warehouse, distribution center, cash-and-carry or wholesale location, fleet, route/delivery network, logistics operation, distribution-center count, or comparable operational footprint.

Sources should be public and substantive. Official distributor pages, service-area pages, facility/location pages, product/service pages, trade articles, press releases, company history pages, public directories, association pages, government/public resources, annual reports, filings, and reputable grocery or foodservice articles can all work when the page carries distributor-specific evidence. Discovery directories are useful only when they provide enough distributor-specific substance for the claimed row. Contact-enrichment profiles, buyer-contact databases, email/phone harvesting pages, quote forms, Yelp-style rankings, generic national pages with no Washington or regional tie, and thin listicles should not be used as the only evidence for a row.

Requirements:
- The page must clearly identify the named distributor.
- The page must credibly tie that distributor to Washington, a named Washington place or subregion, the Inland Northwest, the Pacific Northwest, the West Coast, Oregon/Washington service, an official Washington facility/location/store, or another source-stated regional market that makes the Washington link visible. Generic national service language alone is not enough.
- The page should make its facet-appropriate source role visible. For `service_scope`, it should read as service/product/channel evidence. For `geographic_footprint`, it should read as service-area, distribution-area, route, regional, or location evidence. For `facility_or_operations`, it should read as operational evidence rather than a bare contact address.
- The page should expose a focused public finding clearly scoped to the named distributor and capability facet. For `service_scope`, the finding should name source-stated products, services, or customer channels. For `geographic_footprint`, it should name the source-stated geography or regional basis. For `facility_or_operations`, it should name the warehouse, distribution center, wholesale location, route/fleet, delivery/logistics, or similar operational signal.

Write one JSON object per line to `results_wa_grocery_distributor_capability_provenance.jsonl`:
{"item": { "distributor": "<distributor>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

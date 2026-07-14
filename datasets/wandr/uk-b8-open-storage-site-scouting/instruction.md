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

## `uk_b8_open_storage_site_scouting`

You are scouting UK town and local-authority markets for a B8, container self-storage, or open-storage operator starting from AL8 7NW. As of May 13, 2026, treat the geography as the broad southern and eastern England road market around AL8 7NW, used as a screening boundary rather than an exact drive-time assertion. For 35+ towns, cities, urban areas, or local-authority markets, cover each of the 5 evidence labels below with 1+ concise source-bounded finding per (area, axis) cell, supplying a source (1+ URL per finding).

Use the task as a public-source screening panel, not a parcel acquisition mandate. Industrial estates, trade-counter districts, logistics parks, and business parks can provide evidence only under the town or local authority they sit in; they should not be submitted as separate outer areas. The demand row must make the 25,000+ population or comparable employment/logistics demand base visible from the source.

Evidence labels:
- `demand_population` -- **Demand and population base**: 25,000+ resident population, or explicit comparable employment, household-growth, logistics, or customer-base evidence that makes the area large enough for self-storage or open-storage screening
- `storage_supply_context` -- **Storage supply and operator context**: container self-storage, open storage, vehicle storage, warehouse/pallet storage, operator locations, facility coverage, or a careful source-bounded supply observation
- `planning_use_context` -- **Planning or use-class context**: B8 storage/distribution, B2 general industrial, industrial/logistics allocation, employment land, planning-policy wording, or a listing that explicitly states the industrial/storage use context
- `land_site_availability` -- **Land or site availability**: available yard, open-storage plot, vacant hardstanding, industrial unit, logistics park, employment land, brownfield site, or other publicly evidenced candidate space
- `road_logistics_access` -- **Road and logistics access**: motorway, A-road, ring-road, port/airport/logistics corridor, HGV, trade-counter, or local-distribution access evidence relevant to B8 or open-storage operations

Each sourced finding should use exactly one of those labels. The same page may support more than one label, but split the facts into separate findings when it does.

Use public, item-level sources that a practitioner could revisit: ONS or council population pages, local plans, planning applications, property listings, estate or developer pages, operator/facility pages, trade/economic sources, or transport/logistics pages. Avoid final evidence that is only a search result, map pin, social post, generic directory, paywalled/private source, or broad marketing page with no area-specific fact.

Keep claims source-bounded. Do not assert exact drive time from AL8 7NW, absence or undersupply of storage, live availability, planning permission, lawful container-storage use, or suitability for a specific operator unless the source directly supports that stronger claim.

Requirements:
- The page must focus on, or directly locate the evidence in, the submitted town, city, urban area, or local-authority market.
- The page must support the submitted finding under the applicable evidence label above: 25,000+ population or equivalent demand base, storage supply, planning/use context, land/site availability, or road/logistics access.
- The page must be an appropriate public source for that evidence label, such as an official statistics/planning source, operator or facility page, commercial property listing, landowner/developer page, transport/logistics source, or credible local economic/business source.
- The submitted finding must stay within what the source supports, without overclaiming exact drive time, storage absence or undersupply, live availability, planning permission, lawful use, population threshold, or container-storage suitability.

Write one JSON object per line to `results_uk_b8_open_storage_site_scouting.jsonl`:
{"item": { "town": "<town>", "local_authority": "<local_authority>", "evidence_axis": "<evidence_axis>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

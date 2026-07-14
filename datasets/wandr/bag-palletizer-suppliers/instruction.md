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

## `bag_palletizer_suppliers`

For 60+ suppliers, manufacturers, official distributors, integrators, or represented brands of bag palletizing or end-of-line pallet-handling systems, cover the 4 capability facets listed below for each one with public evidence (i.e. 1+ URL under each facet). The `regional_presence` facet is the required UAE/GCC/MENA market-tie evidence; the other facets establish product, application, and technical/service provenance for that same supplier or represented brand.

The point is public capability provenance for industrial packaging equipment, not procurement selection. Contact details, quote requests, supplier ranking, best-option recommendations, compatibility guarantees, buying advice, outreach, and lead scoring are out of scope.

Capability facets:
- `regional_presence`: substantive UAE/GCC/MENA market presence or reach, such as a local office, official distributor or representative, service/support territory, event/exhibitor presence, regional installation, official regional page, or named country responsibility
- `palletizing_offering`: actual palletizer, palletiser, robotic palletizing, bag palletizing, or end-of-line pallet-handling equipment, not only pallet wrapping, pallet products, pallet trucks/racks, or logistics palletization services
- `application_fit`: source-stated animal feed, pet food, feed bags/sacks, or a named comparable bagged-bulk material such as powder, granules, pellets, grains, seeds, flour, sugar, fertilizer, cement, minerals, chemicals, or cat litter. Generic words such as food, bags, packaging, logistics, or broad industry lists are not enough by themselves
- `technical_or_service_detail`: a concrete public technical or service datum, such as model name, package type, bag weight, throughput, bags/hour, packs/minute, cycles/hour, pallet/load dimensions, layer/pallet capacity, production rate, installation reference, service region, support territory, or comparable deployment scope. Thin event boilerplate, generic automation claims, and broad product blurbs do not count without at least one concrete detail

Evidence may come from official supplier or manufacturer pages, product pages, catalogs/PDFs, distributor or represented-brand pages, event/exhibitor pages, marketplace listings, public directories, source hubs, or similar public sources when the page itself proves the selected facet. Event, directory, marketplace, and source-hub pages can support `regional_presence` when they provide a real UAE/GCC/MENA tie. For `palletizing_offering`, `application_fit`, or `technical_or_service_detail`, those pages only work when they are supplier/OEM-controlled or are dedicated product/catalog sources with concrete product text for the selected facet. A distributor page plus an OEM/product page can support the same entity only when the represented-brand relationship is visible; otherwise treat the distributor and OEM/brand as separate entities.

Requirements:
- The page must clearly identify the named supplier or brand, or an officially represented OEM/product brand tied to it.
- The page must make its facet-appropriate source role visible for the selected `capability_facet`.
- The page must expose substantive evidence for the selected `capability_facet`.

Write one JSON object per line to `results_bag_palletizer_suppliers.jsonl`:
{"item": { "supplier_or_brand": "<supplier_or_brand>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

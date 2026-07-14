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

## `canada_copacker_capabilities`

Build a public provenance bundle for at least 20+ Canadian food, ingredient, packaging, co-packing, or contract-manufacturing operators/facilities relevant to broth, stock, soup-base, dry-mix, or single-serve powder manufacturing. For each submitted operator/facility, cover each of the 7 evidence axes listed below with 1+ URL per axis. Each row should be a public provenance citation for one source-stated axis, not a vendor recommendation.

Evidence axes:
- `facility_identity_location`: official, registry, government/directory, or manufacturer-specific evidence for the operator/facility identity plus a Canadian city/province, facility, or address; generic Canada-wide marketing context alone is not enough
- `copack_or_private_label_service`: source-stated food/ingredient co-packing, contract packing, co-manufacturing, contract manufacturing, or private-label production service for the submitted operator/facility; broad private-brand or retail-customer wording alone is not enough
- `powder_or_single_serve_format`: dry/powder blending, powder handling, dry-mix manufacturing, powder filling or packing, spray drying, stick-pack, sachet, packet, pouch, or comparable single-serve dry format; liquid, frozen, meat-cutting, or bulk food context without dry/powder/single-serve wording is not enough
- `retail_finished_goods_packaging`: source-stated finished-goods packaging operation or format, such as consumer-ready, shelf-ready, case-packed, boxed, pouched, bottled, tinned, labeled, coded, carton, stick-pack, sachet, or retail-ready units; merely selling to retailers or doing private label is not enough
- `broth_stock_soup_base_relevance`: positive broth, stock, bouillon, soup mix, soup base, gravy/base, meat/poultry/seafood base, or comparable savory base category relevance for the submitted operator/facility; generic meat products, meat alternatives, sauces, or frozen prepared foods without broth/stock/soup-base/dry-mix/base wording are not enough
- `registration_or_food_safety_credential`: source-stated official food/NHP registration, licence, establishment status, inspection status, or food-safety / quality credential such as CFIA SFC, SQF, HACCP, BRCGS, cGMP/GMP, organic, kosher, or halal; generic quality claims without a named credential or official status are not enough
- `independent_bundle_crosscheck`: a non-operator-controlled, entity-specific government, certification, regulatory, or substantive industry source that cross-checks the submitted operator/facility and at least two bundle anchors among Canadian location, co-pack/private-label service, dry/powder/single-serve format, broth/stock/soup-base relevance, or credential status; generic listicles, search pages, and member-supplied supplier catalogs are not enough

Each operator/facility should be named as a company plus a Canadian facility city/province, province, facility, or address. Prefer facility/province/address evidence. Do not use generic Canada-wide marketing context as the location leg unless the selected source is an official registration, inspection, certification, or government source that identifies the Canadian establishment context.

Submit an operator/facility only when public evidence can support a real bundle across the axes. Do not fill one axis with unrelated operators that lack the rest of the bundle. Do not infer buyer suitability, bone-broth-powder readiness, legal compliance, or practical fit from separately sourced partial claims. Keep observations source-stated and restrained: no rankings, fit scoring, lead scoring, buyer suitability claims, contact collection, outreach, negotiation, MOQ/capacity advice, food-safety advice, or legal/compliance conclusions.

Requirements:
- The page must clearly identify the submitted operator or facility.
- The page must tie that operator/facility to a Canadian city/province, province, facility, address, official establishment context, or equivalent specific Canadian operating context.
- The page must make its public source role visible for the selected evidence axis. Axis-specific source roles matter: capability axes need operator/manufacturer pages or substantive entity-specific independent sources, not broad supplier-directory category tags alone; credential axes need official, certification, registry, or named-credential pages; `independent_bundle_crosscheck` must be non-operator-controlled and entity-specific.
- The page must visibly state the selected evidence axis for the submitted operator/facility.
- For `broth_stock_soup_base_relevance`, do not count generic meat products, meat alternatives, sauces, or prepared foods unless the page states broth, stock, bouillon, soup mix, soup base, gravy/base, or a comparable savory base/dry-mix category.

Write one JSON object per line to `results_canada_copacker_capabilities.jsonl`:
{"item": { "company": "<company>", "facility_location_or_province": "<facility_location_or_province>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

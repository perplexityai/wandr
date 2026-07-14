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

## `precast_decking_capability_provenance`

For 60+ Northeast or nearby Mid-Atlantic precast/prestressed concrete producers, collect public capability-provenance evidence for each of the 3 capability facets below; for each (`producer`, `capability_facet`) pair, supply a source (i.e. 1+ URL) that supports that specific facet.

The work is public capability provenance, not supplier selection. The useful distinction is whether a public source ties the producer to structural deck, floor, roof, or bridge-deck systems, rather than merely saying "precast."

Regional scope: Northeast and nearby Mid-Atlantic producer evidence, centered on ME, NH, VT, MA, RI, CT, NY, NJ, PA, DE, MD, DC, VA, and WV. An adjacent state or province can count only when a regional association, certification, project, or producer source places the producer in this Northeast/Mid-Atlantic producer context.

Capability facets:
- `plant_identity`: producer-owned evidence or a producer-/plant-specific off-producer record that the producer operates a named precast/prestressed plant, production facility, manufacturing facility, certified plant, or equivalent producer site at a stated location in scope; broad multi-producer list/search/hub pages and address-only member rows are insufficient.
- `structural_decking_capability`: producer-owned product or capability page, catalog, PDF, or project evidence that the producer makes a qualifying structural deck, floor, roof, or bridge-deck product family.
- `independent_qualification`: off-producer, producer-specific product/project/plant evidence corroborating certification, qualification, agency approval, project use, or comparable independent validation tied to qualifying structural decking capability; broad multi-producer member lists, search pages, and directory hubs are insufficient.

Qualifying product families include hollow-core plank or slabs; structural floor or roof deck systems; precast/prestressed deck slabs or panels; full-depth or stay-in-place bridge deck slabs or panels; double tees or single tees when the source ties them to floor, roof, deck, or structural framing use; and NEXT or deck-beam bridge products when the source explicitly frames them as deck or deck-system products.

The following do not count by themselves: generic precast, ready-mix, septic tanks, drainage products, retaining walls, barriers, steps, utility structures, decorative or architectural panels, generic custom precast, generic bridge girders/I-beams/bulb tees without a deck-system tie, sales offices, erectors, distributors, general contractors, and trade-directory pages with no product-specific evidence.

Requirements:
- The page must clearly identify the submitted producer, plant, or corporate producer identity.
- The page must fit the declared `capability_facet`. `plant_identity` needs a producer-owned source or producer-/plant-specific off-producer record that explicitly identifies a named plant, production facility, manufacturing facility, certified plant, or equivalent producer site at a scoped location. `structural_decking_capability` needs a producer-owned product or capability page, catalog, brochure/PDF, or producer-owned project/case-study source. `independent_qualification` needs an off-producer source whose page or record is specific to the submitted producer, plant, approved product, or project, such as a certified-plant record, agency approved product/plant list entry with a producer-specific URL or record page, public project document, bid/spec/award record, project profile, or reputable trade/project article.
- The page must provide substantive facet evidence: operation of a scoped precast/prestressed plant for `plant_identity`; making, producing, fabricating, or offering a qualifying structural product family for `structural_decking_capability`; and off-producer corroboration of certification, qualification, agency approval, project use, or comparable independent validation tied to qualifying capability for `independent_qualification`.
- Source roles are intentionally separated. Association, PCI/chapter, directory, agency approval, and other off-producer profile/list/hub pages do not satisfy `structural_decking_capability`, even when they list deck, floor, roof, bridge-deck, hollowcore, double-tee, or slab products.
- Broad multi-producer member lists, searchable plant/member directories, regional producer-list pages, and hub pages do not satisfy `plant_identity` or `independent_qualification`, even when the visible row names the submitted producer, a plant address, certification codes, or qualifying product categories. Use off-producer evidence for those facets only when the cited page or record is producer-, plant-, approved-product-, or project-specific rather than one reusable page containing many producer rows.
- Generic state precast approvals, generic NPCA or trade memberships, generic PCI membership/certification, generic "commercial precast," and generic bridge-beam/girder pages do not prove structural decking capability or independent qualification unless the page is producer-specific and ties the producer to a qualifying deck/floor/roof/bridge-deck product family.
- Price, quote, contact, minimum-order, lead-time, freight, delivery-radius, landed-cost, ranking, recommendation, or outreach details are not evidence targets for this task.

Write one JSON object per line to `results_precast_decking_capability_provenance.jsonl`:
{"item": { "producer": "<producer>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

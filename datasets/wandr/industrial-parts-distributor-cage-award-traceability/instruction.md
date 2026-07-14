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

## `industrial_parts_distributor_cage_award_traceability`

For each of the 4 industrial part categories below, for 40+ U.S.-serving industrial parts distributors per category, supply 1+ public URL for each submitted distributor and each of the 5 evidence axes listed below.

The task is a neutral public-evidence table. It is not a supplier recommendation, federal-bid strategy, quote/RFQ workflow, pricing request, contact-enrichment task, ranking, or prediction about whether an entity will bid on future federal work. Absence or zero-award evidence is only a dated source state from the checked public source.

Part categories:
- `fasteners_hardware`: threaded fasteners, nuts, bolts, screws, rivets, washers, clamps, inserts, aerospace or mil-spec hardware, and closely related stocked hardware.
- `seals_gaskets_orings`: o-rings, seals, gaskets, packing, sealing kits, elastomeric sealing products, and related gasket/seal distribution.
- `aerospace_mro_consumables`: aviation or aerospace MRO consumables, expendable hardware, aircraft supply-chain parts, aviation shop consumables, and defense/aerospace maintenance supplies.
- `hand_tools_tooling`: cutting tools, aircraft tools, machine-shop tooling, tooling components, shop tools, and industrial hand tools.

Evidence axes:
- `product_scope`: a distributor-owned or distributor-scoped product, catalog, line-card, or capability source showing the distributor serves the submitted part category.
- `line_card_or_authorization`: source evidence for a named manufacturer, brand, product line, authorized/franchised/factory distributor relationship, official distributor listing, or category-relevant line card.
- `traceability_quality`: source evidence for traceability, certificate of conformance, material certs, lot/batch/heat/cure records, AS9120/AS9100/ISO quality systems, DFARS/ITAR/JCP/NIST-style quality/compliance, or comparable distributor quality capability.
- `entity_identifier_state`: source evidence for a public entity identifier such as CAGE, UEI, SAM registration, DUNS, or a facility/legal-entity identifier state tied to the distributor.
- `federal_award_record_state`: source evidence for a dated federal-award public-record state for the distributor/legal entity/facility, preferably from USAspending GET recipient API/profile data or another fetchable official FPDS/USAspending-derived source.

Briefly state the axis-specific finding for each submitted URL. For `line_card_or_authorization`, include a `source_strength` label from the source-strength states below. For `entity_identifier_state` and `federal_award_record_state`, include `checked_date`, `identifier_or_search_basis`, `source_state`, and any `ambiguity_note` needed to preserve facility, DBA, parent/child, owner-CAGE, acquired-brand, or legal-entity uncertainty.

Line-card or authorization source-strength states:
- `manufacturer_owned_authorization`: manufacturer or brand page, distributor locator, announcement, or official partner/distributor document naming the distributor.
- `manufacturer_owned_distributor_directory`: manufacturer or brand directory/listing naming the distributor, even if thinner than a relationship announcement.
- `distributor_owned_authorized_claim`: distributor page names a manufacturer/brand/product line and claims authorized, franchised, factory-authorized, or official distribution.
- `distributor_owned_line_card_named_brand`: distributor page or line card names a manufacturer/brand/product line relevant to the submitted category without proving authorization.
- `official_qualification_or_qsl`: official qualification list or government-controlled supplier qualification source; this supports qualification standing, not private manufacturer authorization.
- `generic_brand_list_or_logo_wall`: weak or invalid unless the submitted named brand/product line is textually visible and the claimed relationship is narrow enough for the record.

Entity identifier states:
- `official_cage_or_sam_record`: fetchable official CAGE/SAM-style record evidence for the submitted legal entity or facility.
- `usaspending_recipient_identifier`: USAspending recipient data exposing the entity name, UEI, DUNS, recipient id, address, parent, or comparable identifier fields.
- `self_published_identifier`: distributor-published CAGE/UEI/DUNS/SAM-style identifier evidence.
- `official_derived_fallback`: official-derived commercial page such as HigherGov, CAGE.report, AeroBase, or comparable source, explicitly labeled as fallback.
- `identifier_ambiguous`: source evidence shows multiple facilities, DBAs, parent/child entities, owner CAGEs, acquired brands, or other legal-entity ambiguity that must be preserved.

Federal-award record states:
- `profile_records_found`: fetchable public record shows award transactions, obligations, counts, amounts, or specific awards for the matched recipient/legal entity/facility.
- `profile_zero_transactions`: fetchable USAspending GET recipient API/profile-style record exists and shows zero transactions or equivalent zero-award state.
- `ambiguous_multiple_matches`: fetchable evidence shows multiple plausible recipient/legal-entity matches or parent/child ambiguity that prevents a clean found/zero state.
- `official_derived_fallback_used`: a labeled official-derived commercial page is used because the official page is inaccessible or does not expose fetchable text.
- `official_source_inaccessible`: the record is specifically about official-source access/fetch state, not a no-award claim. Do not use this as a silent substitute for award absence.

Requirements:
- The page must identify the submitted distributor, legal entity, facility, DBA, or recipient entity closely enough for the submitted evidence. Do not silently treat parent companies, sister companies, acquired brands, owner CAGEs, or similarly named recipients as the same distributor.
- The page must fit the submitted `evidence_axis`. A product-category page is not automatically evidence of traceability; a homepage is not automatically line-card evidence; a CAGE page is not automatically award-history evidence.
- For `product_scope`, the page must show that the distributor sells, stocks, sources, or catalogs products in the submitted `part_category`.
- For `line_card_or_authorization`, the page must name a manufacturer, brand, product line, official distributor relationship, or category-relevant line-card entry. Generic logo walls and broad "authorized for thousands of manufacturers" claims are not enough unless the submitted named brand/product line is textually visible and the claim is specific enough.
- For `traceability_quality`, the page must show distributor traceability, certificate-of-conformance, material-cert, lot/batch/heat/cure traceability, AS9120/AS9100/ISO, DFARS/ITAR/JCP/NIST, or comparable quality/compliance capability. Buyer-side quality clauses and generic industry articles do not count.
- For `entity_identifier_state`, prefer official CAGE/SAM/UEI evidence when fetchable. Distributor-published identifiers and official-derived commercial pages can count only when the submitted finding labels the source state and preserves ambiguity.
- For `federal_award_record_state`, prefer fetchable official USAspending GET recipient API URLs or other official FPDS/USAspending-derived GET pages that expose entity and award-state text. USAspending human pages that fetch only as JavaScript shells, human search-result pages, and POST-only search/count/autocomplete results do not count as ordinary evidence URLs. Official-derived commercial pages can count only as labeled fallback or ambiguity evidence.

Write one JSON object per line to `results_industrial_parts_distributor_cage_award_traceability.jsonl`:
{"item": { "part_category": "<part_category>", "distributor": "<distributor>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `agricultural_supplier_sources`
  - `agricultural_supplier_sources.country_commodity_context`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `agricultural_supplier_sources`

For 24+ agricultural country/commodity contexts, name 6+ public supplier entities per context, each as a named agricultural supplier organization or source-linked agricultural facility at the exact public granularity shown by the source; cover each of the 2 entity evidence facets listed below with a source (i.e. 1+ URL per context/entity/facet) that establishes public supplier-source provenance.

The task studies public evidence about source standing and provenance under uneven agricultural disclosure. It is not a supplier ranking, procurement recommendation, sourcing strategy, compliance or safety adequacy conclusion, investment view, contact-enrichment exercise, outreach list, lead score, dashboard, alert, RFQ, price, availability, or private supplier-intelligence table.

Entity evidence facets:
- `role_and_crop_anchor`: the exact named entity or facility is publicly tied to the country/commodity context and an agricultural supply-chain role; this facet does not require a certification, approval, program listing, or buyer relationship.
- `public_system_or_relationship_state`: the exact same entity or facility has a source-stated public certification, registration, approval, agricultural membership, named program or competition listing/result, buyer/program relationship, traceability or supplier-list inclusion, expired/suspended/de-certified state, no-current-disclosure state, or comparable public source-standing state beyond bare existence in the country/commodity context.

In-scope entities are named agricultural supplier organizations and source-linked agricultural facilities: producer cooperatives, farmer organizations, producer groups, packers, exporters, aggregators, estates, plantations, farms, mills, warehouses, packhouses, buying stations, and processing facilities. Facilities count as facilities, not as growers or cooperatives by default. When a source distinguishes a farm, facility, parent company, buyer, program, certification scheme, and farmer/representative/contact person, those are distinct public units; the relevant entity is the named unit whose role or state the page actually states. Individual people, contact persons, generic product categories, buying programs, certification schemes, RFQ pages, and private leads are out of scope as supplier entities.

Certification, registry, and finder ecosystems count only through stable entity-level profiles, visible listing rows, readable reports/PDFs, table rows, or entity-owned pages where the cited page itself names the supplier entity and the country/commodity/facet evidence. Generic finder pages, search forms, directory shells, and unlinked interactive result states are not supplier evidence when the entity details are not visible on the cited page.

Requirements:
- The page must clearly identify the exact named supplier organization or facility, not only a generic portal, broad parent brand, buyer/program page, certification scheme page, or person/representative/contact name.
- The page must tie that exact entity or facility to the claimed country, commodity, and agricultural supply-chain context.
- The page should make its facet-appropriate source role visible at the cited URL. For `role_and_crop_anchor`, this means a stable entity-specific profile, visible directory/list row, registry entry, cooperative/trade listing, report/PDF/table row, entity-owned page, or comparable source that can anchor country, commodity, and role. For `public_system_or_relationship_state`, this means a stable visible entity-specific profile, listing row, section, report/PDF/table row, or page stating a public certification, registration, approval, membership, named program or competition listing/result, relationship, list inclusion, or source-backed stale/suspended/expired/de-certified/no-current-disclosure state.
- The page must expose a substantive public fact scoped to `entity_facet`. For `role_and_crop_anchor`, the fact should establish a crop or commodity role such as grower group, cooperative, exporter, packer, mill, warehouse, buying station, estate, farm, aggregator, processor, or comparable agricultural supply-chain role. For `public_system_or_relationship_state`, the fact should be a source-stated public certification, registration, approval, membership, program/competition listing or result, relationship, list inclusion, or status/state for that same entity; generic scheme mentions, directory membership inferred from a domain, search failure, or hidden finder state are not enough.

Write one JSON object per line to `results_agricultural_supplier_sources.jsonl`:
{"item": { "country": "<country>", "commodity": "<commodity>", "entity": "<entity>", "entity_type": "<entity_type>", "entity_facet": "<entity_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `agricultural_supplier_sources.country_commodity_context`

Cross-tasknode identifier discipline: this task is for the same {= country_commodity =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= country_commodity =}+ agricultural country/commodity contexts, cover each of the 3 context facets listed below with a country/commodity context source (i.e. 1+ URL per context/facet). These sources may discuss the broader sector, market, calendar, or policy context and do not need to name any individual supplier entity.

The context evidence is public sector/market provenance for interpreting the country/commodity setting, not procurement advice, concentration scoring, supplier ranking, legal/safety adequacy, investment advice, dashboarding, or alerting.

Context facets:
- `seasonality_or_marketing_calendar`: harvest, export, buying, marketing, crop-cycle, season-opening, or comparable timing for the country/commodity pair.
- `market_structure_or_fragmentation`: smallholder share, cooperative share, concentration or fragmentation, traceability coverage, production/export share, value-chain structure, or comparable public market structure.
- `production_export_or_policy_context`: production/export scale, market flow, destination or channel context, export-control, phytosanitary, public policy, or comparable source-relevant context.

Context sources should be authority-bearing or report-like: official agriculture/export agencies, USDA FAS or comparable public reports, FAO or statistical sources, national crop boards, trade associations, market reviews, sector packs, crop calendars, methods papers, reputable agriculture-sector analysis, or similar public sources.

Requirements:
- The page must clearly tie its context evidence to the submitted country and commodity.
- The page should make its authority-bearing or report-like source role visible for the submitted `context_facet`.
- The page must expose a substantive public context fact scoped to `context_facet`. For `seasonality_or_marketing_calendar`, this is timing evidence. For `market_structure_or_fragmentation`, this is structure, concentration, fragmentation, smallholder/cooperative share, traceability, or similar market-organization evidence. For `production_export_or_policy_context`, this is production/export scale, market flow, destination/channel, export-control, phytosanitary, public policy, or comparable source-relevant context.

Write one JSON object per line to `results_agricultural_supplier_sources.country_commodity_context.jsonl`:
{"item": { "country": "<country>", "commodity": "<commodity>", "context_facet": "<context_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `nulogy_adjacent_capability_evidence`

In each of the 2 Nulogy-adjacency clusters, for 70+ public software companies or branded product lines, supply public provenance for 2+ capability families per company/product, with 1+ URL under each family. Use 2026-06-29 as the reference date and keep the record public-source only: no private database extraction, competitor ranking, buyer guide, procurement recommendation, investment advice, sales targeting, outreach, or contact enrichment. Nulogy is the reference anchor, not a target row subject.

Adjacency clusters:
- `near_core_packaging_manufacturing_operations`
- `broader_adjacent_operations_software`

Capability families:
- `contract_packaging_or_co_manufacturing_operations`
- `production_scheduling_shop_floor_mes_or_oee`
- `inventory_wms_lot_traceability_or_warehouse_operations`
- `quality_compliance_audit_batch_or_regulatory_workflow`
- `supplier_or_external_manufacturing_collaboration`
- `food_cpg_traceability_or_supply_chain_transparency`
- `packaging_artwork_labeling_or_specification_management`
- `erp_process_manufacturing_or_industry_operations_suite`
- `integration_edi_api_marketplace_or_partner_connectivity`
- `other_adjacent_operations_software`

Each record should state a concise capability finding plus source class, support state, source date or observed-date status, checked date, and confidence. Useful support states include `official_supported`, `secondary_only`, `capability_supported_category_missing`, `conflicting_labels`, `name_or_product_conflict`, and `no_visible_date`. These provenance labels must match the cited page's ownership, source posture, dating, and capability evidence.

Source roles can include official company, product, feature, industry, integration, customer-story, partner-marketplace, public filing, press release, reputable software directory, analyst/review source, or trade article pages. Secondary, directory, analyst, and trade pages are useful as labeled context, but clean capability records should mostly cite official or product-specific pages. Ranking-only alternatives pages, private databases, generic vendor homepages, login-only pages, contact pages, and pages that merely mention a product name without capability evidence do not count.

Requirements:
- The page must clearly identify the named company and, when a product or suite is named, the specific product, suite, module, or branded product line.
- The page must support the declared adjacency cluster: `near_core_packaging_manufacturing_operations` for contract packaging, co-packing, contract manufacturing, private-label, external manufacturing, manufacturer supplier-collaboration, or shop-floor operations context; `broader_adjacent_operations_software` for concrete adjacent manufacturing, supply-chain, quality, traceability, packaging, process-ERP, integration, or operations-workflow context.
- The page must substantively support the claimed capability family through concrete software, module, workflow, feature, integration, or use-case content for the named company/product. Large suite vendors need product/module-specific evidence, not a generic corporate homepage.

Write one JSON object per line to `results_nulogy_adjacent_capability_evidence.jsonl`:
{"item": { "adjacency_cluster": "<adjacency_cluster>", "company": "<company>", "product_or_suite": "<product_or_suite>", "capability_family": "<capability_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

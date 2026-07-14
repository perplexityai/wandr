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

## `bar_restaurant_ops_software_catalog_source_table`

For each of the 6 ecosystem bands listed below, cover 35+ distinct vendors, products, public portals, marketplaces, catalogs, APIs, data providers, or source systems relevant to bar, restaurant, hospitality, beverage, alcohol, inventory, supplier catalog, menu, label/OCR, UPC/product-data, or on-prem operations. For each vendor/source, supply one URL for each of the 2 evidence surfaces listed below.

The task is a public source-provenance atlas: it rewards locating official public surfaces that state what the source can do and how it can be accessed or bought. It is not asking for rankings, procurement advice, unit economics, scraping plans, product build specs, OCR pipeline design, database schemas, implementation roadmaps, outreach, or lead scoring.

Ecosystem bands:
- `pos_menu_on_prem_operations_software`: POS, menu, order, table, floor, on-prem restaurant/bar operations, or hospitality operations software.
- `inventory_purchasing_invoice_bar_cost_software`: inventory, purchasing, invoice capture, vendor order, recipe costing, food cost, liquor cost, or bar-cost software.
- `supplier_distributor_marketplace_or_catalog`: supplier/distributor portals, wholesale marketplaces, product catalogs, beverage catalogs, price-list/order portals, or buyer catalogs for bars/restaurants/hospitality.
- `public_regulatory_alcohol_label_or_product_database`: public regulatory, government, or official database/search portal for alcohol labels, beverage products, product approvals, or related public records.
- `upc_product_beverage_data_api_or_provider`: UPC/GTIN/barcode lookup, product data APIs, beverage product-data providers, or comparable structured product-data sources.
- `ocr_label_recognition_data_extraction_provider`: OCR, label recognition, invoice data extraction, alcohol/wine/beverage label recognition, or comparable visual/document data extraction providers.

Evidence surfaces:
- `capability_or_data_source`: an official or controlled page states a concrete capability, data function, catalog/portal function, docs/API function, OCR/recognition function, or product-data coverage.
- `commercial_or_access_source`: an official or controlled page states a commercial or access posture, such as public pricing/tier, free or no-fee access, trial, quote/demo/contact-sales, login/account/customer-only access, registration or API-key access, no-login public portal access, marketplace access, territory-limited distributor access, or similar.

Use a vendor/source name that is precise enough to identify the controlled entity or product/source: include product or portal identity when a parent company owns multiple relevant systems, and disambiguate aliases, legacy brands, country portals, or name conflicts where useful.

Source guidance:
- Capability/data claims should come from the subject entity's official or controlled surface: product/feature pages, docs/API pages, integration pages, help pages, public portals, official catalogs, official marketplace pages, developer portals, or comparable controlled pages.
- Commercial/access claims should also be source-stated by an official or controlled surface. A page can count when it publicly says the useful access fact is login-required, API-key-required, account-required, customer-only, quote/demo-required, free/no-fee, or no-login public portal access.
- Third-party directories, comparison blogs, review sites, and listicles can help discovery, but they do not prove the main capability/data or commercial/access evidence for the compared vendor/source in this task.
- Do not turn absence states into required proof. A row should not claim `no pricing`, `no API`, `no current page`, or similar unless the page itself source-states the relevant access posture.
- Generic OCR, UPC, data, or software providers count only when the page's stated function is concretely relevant to product, label, alcohol, beverage, hospitality operations, inventory, supplier, catalog, menu, POS, or restaurant/bar operations data.

Requirements:
- The page must clearly identify the named vendor/source or its named product, portal, catalog, API, marketplace, or data service.
- The page must tie that vendor/source to the claimed ecosystem band's substance, not just to vague software, data, restaurant, or beverage keywords.
- The page must make its official or controlled source role visible and be appropriate for the row's evidence surface.
- The page must state the specific evidence-surface finding: a capability/data function for `capability_or_data_source`, or a commercial/access state for `commercial_or_access_source`.

Write one JSON object per line to `results_bar_restaurant_ops_software_catalog_source_table.jsonl`:
{"item": { "ecosystem_band": "<ecosystem_band>", "vendor_or_source": "<vendor_or_source>", "evidence_surface": "<evidence_surface>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

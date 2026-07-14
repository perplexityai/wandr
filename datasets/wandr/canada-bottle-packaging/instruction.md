You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `canada_bottle_packaging`
  - `canada_bottle_packaging.canada_service`

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

## `canada_bottle_packaging`

For 60+ suppliers/channels, cover 3+ concrete beverage-bottle, wine/spirits glass, closure, cap, cork, capsule, or directly related bottle-packaging products or product lines per supplier; for each supplier-product pair, cover each of the 3 product evidence areas below with corroborating public sources (i.e. 2+ URLs per supplier-product-area).

The purpose is public capability provenance, not supplier selection. Commercial, shipping, standards, finish, and compatibility language counts only as page-stated public posture; it is not a product-suitability, safety, compliance, supplier-quality, delivered-cost, or recommendation conclusion.

Product evidence areas, referred to as `product_axis`, are:
- `format_or_spec`: source-stated product format, capacity, style, material, finish, neck/closure type, dimensions, source-stated compatibility, or comparable product specification
- `pack_or_order_quantity`: source-stated case pack, bottles per case, pallet quantity, MOQ, order unit, quantity tier, bulk threshold, or comparable order-pack fact
- `commercial_or_shipping_state`: source-stated public price, quote-required or call-for-availability state, pickup/local-delivery restriction, shipping/freight locator, shipping exclusion, flat-rate exclusion, or comparable public commercial/order posture

Supplier/channel entities should be real public sellers, distributors, retailers, manufacturers, marketplace sellers, or brand channels in the bottle, closure, wine/spirits glass, brewing/winemaking, or related bottle-packaging supply space. Product identities should be meaningful source-framed products, product lines, product families, or product categories; color, stock status, price tier, pack-size, or SKU changes are not enough by themselves when the supplier presents them as variants of the same underlying product. The URLs under a supplier-product-area are corroboration: each cited page must independently identify the supplier-product relationship and state the selected product-area fact, rather than splitting those obligations across pages. Alternate URLs for the same page that only add tracking, source, view, variant, fragment, sort, or filter decorations are not independent corroboration.

Requirements:
- The page must identify the named supplier/channel and tie the named product or product line to that supplier as an in-scope bottle, closure, or related bottle-packaging offering.
- The page must state a concrete public fact for the selected `product_axis`.

Write one JSON object per line to `results_canada_bottle_packaging.jsonl`:
{"item": { "supplier": "<supplier>", "product": "<product>", "product_axis": "<product_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `canada_bottle_packaging.canada_service`

Cross-tasknode identifier discipline: this task is for the same {= supplier =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= supplier =}+ suppliers/channels, cover each of the 3 Canadian-service proof areas below with corroborating public sources (i.e. 2+ URLs per supplier/proof-area pair).

Canadian-service proof areas, referred to as `canada_service_proof`, are:
- `canadian_operating_presence`: source-stated Canadian physical or operating footprint for the supplier/channel, such as a Canadian store, warehouse, head office, pickup or local-delivery base, Canadian wholesale/supplier identity, or comparable Canada-specific operating statement
- `canada_order_service`: explicit Canada-specific ordering, shipping, pickup, delivery, freight, storefront, marketplace-seller, or customer-service posture for the supplier/channel on a supplier-scope service/order source
- `canada_packaging_supply_scope`: Canadian-facing or Canada-serving bottle, closure, cap, cork, capsule, brewing/winemaking, or related bottle-packaging supply scope for the supplier/channel

The supplier/channel should be a real public seller, distributor, retailer, manufacturer, marketplace seller, or brand channel in beverage bottle, wine/spirits glass, closure, cap, cork, capsule, brewing/winemaking, or directly related bottle-packaging supply. Contact or location pages can count for `canadian_operating_presence` only when they identify a concrete Canadian operating footprint, not merely contact methods. Shipping, terms, storefront, marketplace, freight, pickup/delivery, and customer-service pages can count for `canada_order_service` only when they state a Canada-specific service or orderability signal; a generic product page, add-to-cart button, shipping-calculated-at-checkout line, pickup label, quote form, or contact form is not enough by itself. Product, catalog, category, manufacturer, distributor, or marketplace-seller pages can count for `canada_packaging_supply_scope` only when they tie the supplier/channel to in-scope bottle, closure, cap, cork, capsule, brewing/winemaking, or related bottle-packaging supply in a Canadian-facing or Canada-serving context. The URLs under a supplier/proof-area pair are corroboration: each cited page must independently identify the supplier/channel, visibly fit the selected proof area, and state the selected proof fact. Alternate URLs for the same page that only add tracking, source, view, variant, fragment, sort, or filter decorations are not independent corroboration.

Requirements:
- The page must identify the named supplier/channel.
- The page must make its selected `canada_service_proof` source role visible: for `canadian_operating_presence`, a company, about, contact, location, warehouse, store, pickup/local-delivery, or comparable supplier-scope page with Canadian footprint context; for `canada_order_service`, a shipping, order, terms, storefront, marketplace-seller, freight, delivery, pickup, customer-service, or comparable supplier-scope page with Canada-specific service context; for `canada_packaging_supply_scope`, a product, catalog, category, manufacturer, distributor, supplier-owned capability, or marketplace-seller page with Canada-facing or Canada-serving bottle/closure/packaging context.
- The page must state the selected Canada-service proof: for `canadian_operating_presence`, a Canadian address, store, warehouse, head office, local pickup/delivery base, Canadian supplier/wholesale identity, or comparable operating-presence statement; for `canada_order_service`, Canada-specific shipping, delivery, pickup, ordering, freight, marketplace availability, storefront availability, customer-service availability, or comparable service/order posture; for `canada_packaging_supply_scope`, Canadian-facing or Canada-serving bottle, closure, cap, cork, capsule, brewing/winemaking, wine/spirits glass, or related packaging supply scope for the supplier/channel.

Write one JSON object per line to `results_canada_bottle_packaging.canada_service.jsonl`:
{"item": { "supplier": "<supplier>", "canada_service_proof": "<canada_service_proof>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

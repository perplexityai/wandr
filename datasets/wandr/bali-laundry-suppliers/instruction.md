You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `bali_laundry_suppliers`
  - `bali_laundry_suppliers.supplier_product_range`
  - `bali_laundry_suppliers.supplier_price_signal`

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

## `bali_laundry_suppliers`

For at least 30+ Bali-relevant commercial laundry-chemical suppliers, distributors, wholesalers, manufacturers, or marketplace storefronts, supply 1+ public URL per supplier. This root URL is the supplier-eligibility gate: it must itself prove both source-stated Bali relevance and commercial laundry-chemical supplier identity.

For the same supplier universe, companion subtasks ask for public product-range/capability evidence and public price or quote-state evidence. Do not substitute those sidecar URLs for this root gate. A supplier belongs in the task only when the root URL states Bali, Denpasar, a Bali branch/reseller/distributor/service area, a Bali-facing listing, marketplace availability for Bali, or an equivalent public Bali-relevant availability signal.

This is public product/source provenance only. Do not collect phone numbers, WhatsApp handles, email addresses, personal contacts, street-address details, outreach steps, purchase recommendations, supplier rankings, lead scores, negotiation or procurement advice, or chemical handling/safety advice. Product-specific quote-state cues can be noted without reporting contact details.

Supplier names should be business or storefront identities, not product names, individual contacts, phone/address strings, laundry-service operators, hotels, or equipment-only sellers. Eligible public evidence can come from official branch/reseller/service-area pages, supplier/product pages, catalogs or PDFs, B2B directory/storefront pages, marketplace storefront pages, and readable public social/business pages when the page itself supports the Bali supplier claim. Generic search results, contact-only or directions-only pages, laundry-service pages, equipment-only pages, household-only product pages with no commercial laundry context, cost-of-living price pages, safety/handling articles, procurement/ranking/recommendation pages, and review/map locator pages without supplier/product evidence do not count.

Visible source dates, last-updated dates, or page-publication dates can be used as provenance context when present. Undated pages should not be represented as current availability beyond the public page evidence.

Requirements:
- The page must identify the named supplier/business/storefront.
- The page must tie that supplier to commercial laundry-chemical supply, such as detergent/deterjen, bleach/pemutih, softener/pelembut, stain remover/penghilang noda, sanitizer/disinfectant, laundry perfume/pewangi, neutralizer/sour/alkaline, hotel or institutional laundry chemicals, or comparable laundry inputs.
- The page must state Bali/Denpasar relevance for the supplier through a Bali location, branch, distributor, reseller, service area, Bali-facing listing, marketplace availability, or equivalent source-stated Bali-relevant availability. A generic Indonesia-wide supplier homepage does not by itself satisfy this root gate.

Write one JSON object per line to `results_bali_laundry_suppliers.jsonl`:
{"item": { "supplier": "<supplier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `bali_laundry_suppliers.supplier_product_range`

Cross-tasknode identifier discipline: this task is for the same {= supplier =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= supplier =}+ commercial laundry-chemical suppliers in the Bali-eligible supplier universe, supply 1+ public product-range or capability URL per supplier. The supplier identity must match the root supplier. This product/capability URL does not need to repeat the Bali marker when the root supplier-gate URL proves Bali relevance.

This is public product/source provenance only. Do not collect phone numbers, WhatsApp handles, email addresses, personal contacts, street-address details, outreach steps, purchase recommendations, supplier rankings, lead scores, negotiation or procurement advice, or chemical handling/safety advice.

Eligible evidence can come from official supplier product pages, catalogs or PDFs, B2B directory/storefront pages, marketplace storefront or product pages, and readable public social/business pages when the page itself ties the supplier to commercial laundry-chemical products. Generic search results, contact-only or directions-only pages, broad marketplace/category searches, laundry-service pages, equipment-only pages, household-only product pages with no commercial laundry context, cost-of-living price pages, safety/handling articles, procurement/ranking/recommendation pages, and review/map locator pages without product evidence do not count.

Requirements:
- The page must identify or unambiguously tie the page to the named supplier/business/storefront.
- The page must show product-range or commercial laundry-chemical capability for that supplier, such as multiple relevant products, a laundry-chemical category/catalog, product line, product-family page, PDF/catalog section, storefront section, or source-stated capability involving detergent/deterjen, bleach/pemutih, softener/pelembut, stain remover/penghilang noda, sanitizer/disinfectant, laundry perfume/pewangi, neutralizer/sour/alkaline, hotel or institutional laundry chemicals, or comparable laundry inputs.

Write one JSON object per line to `results_bali_laundry_suppliers.supplier_product_range.jsonl`:
{"item": { "supplier": "<supplier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `bali_laundry_suppliers.supplier_price_signal`

Cross-tasknode identifier discipline: this task is for the same {= supplier =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= supplier =}+ commercial laundry-chemical suppliers in the Bali-eligible supplier universe, supply 1+ public price or quote-state URL per supplier. The supplier identity must match the root supplier. This price/quote URL does not need to repeat the Bali marker when the root supplier-gate URL proves Bali relevance.

This is public product/source provenance only. Do not collect phone numbers, WhatsApp handles, email addresses, personal contacts, street-address details, outreach steps, purchase recommendations, supplier rankings, lead scores, negotiation or procurement advice, or chemical handling/safety advice. Product-specific quote-state cues can be noted without reporting contact details.

Eligible evidence can come from official supplier product pages, catalogs or PDFs, public price-list documents, B2B directory/storefront pages, marketplace storefront or product pages, and readable public social/business pages when the price or quote-required state attaches to a product, catalog entry, storefront product family, or price-list context. Generic contact pages, footer buttons, account bios, generic search results, contact-only or directions-only pages, broad marketplace/category searches, laundry-service pages, equipment-only pages, household-only product pages with no commercial laundry context, cost-of-living price pages, safety/handling articles, procurement/ranking/recommendation pages, and review/map locator pages without product price context do not count.

Requirements:
- The page must identify or unambiguously tie the page to the named supplier/business/storefront.
- The page must place the price or quote-required state in a commercial laundry-chemical product, product-category, catalog, storefront, marketplace, or price-list context.
- The page must show a public price, price-list entry, marketplace price, CALL/tanya harga/Hubungi Kami-style quote state, or comparable product-specific price/quote cue for detergent/deterjen, bleach/pemutih, softener/pelembut, stain remover/penghilang noda, sanitizer/disinfectant, laundry perfume/pewangi, neutralizer/sour/alkaline, hotel or institutional laundry chemicals, or comparable laundry inputs.

Write one JSON object per line to `results_bali_laundry_suppliers.supplier_price_signal.jsonl`:
{"item": { "supplier": "<supplier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

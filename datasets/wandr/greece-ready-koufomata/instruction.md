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

## `greece_ready_koufomata`

Identify 120+ suppliers/channels as Greek-market-facing public supply channels for windows, doors, frames, balcony doors, exterior/security doors, PVC systems, aluminum systems, laminate/internal doors, or comparable koufomata products; for each supplier, identify 1+ supplier-scoped product offer, and for each such (`supplier`, `product`) pair cover each of the 3 evidence axes listed below with a source (i.e. 1+ URL).

The task is public product provenance, not a supplier ranking, purchase table, installation guide, building-code task, lead-enrichment workflow, or contact list.

The evidence axes, which we refer to as `evidence_axis`, are:
- `channel_role`: evidence that the supplier/channel is Greek-market-facing and connected to window, door, frame, or comparable koufomata supply.
- `product_material_dimension`: evidence that the same supplier-scoped product offer has a stated material and a concrete public dimension, size, standardized dimension, or size range.
- `ready_standard_posture`: evidence that the same supplier-scoped product offer has a source-stated ready-made, standard-size, stock-size, fixed-size, pre-sized, express, fast-delivery, or similar availability posture.

The supplier ought to be a real Greek-market-facing supplier, retailer, manufacturer-channel, fabricator, showroom, marketplace operator/product channel, seller storefront, or comparable public supply channel. A seller name that appears only as one option inside a price-comparison table, marketplace offer widget, directory listing, or broad catalog page is not by itself a separate supplier/channel identity. The product ought to be a real supplier-scoped product offer, line, SKU, family, product page, or page-stated size range tied to the supplier through a supplier-controlled page, retailer-controlled page, seller storefront/product page, or dedicated marketplace product-offer page that visibly binds the named channel to the offer. One-off classifieds or resale ads, bare systems-brand catalogs without a retail/supply offer, supplier-ranking articles, generic search/category/list pages without product-specific evidence, and configurator-only pages where dimensions are merely user inputs are outside the scope.

Requirements:
- The page must identify or strongly anchor the named `supplier`; for `product_material_dimension` and `ready_standard_posture`, it must also identify the named `product` as a product or offer under the same supplier/channel rather than merely placing the supplier name beside a shared marketplace or directory product description.
- The page must make its evidence-axis source role visible: for `channel_role`, a Greek-market supplier/channel role in window, door, frame, or koufomata supply; for `product_material_dimension`, a supplier-controlled, retailer-controlled, seller-storefront, or dedicated product-offer surface for the named supplier-scoped offer rather than a generic category, price-comparison, directory, broad listing, or shared catalog surface; for `ready_standard_posture`, a product-specific availability or standardization surface for that same supplier-scoped offer rather than merely an ecommerce page with a price or a marketplace seller list.
- The page must contribute the evidence required by `evidence_axis`: for `channel_role`, a Greek-market tie plus an in-scope supply role; for `product_material_dimension`, both material and a concrete public dimension/size/size range for the named offer; for `ready_standard_posture`, source-stated ready-made, standard-size, stock-size, fixed-size, pre-sized, express, fast-delivery, or similar posture for the named offer rather than posture inferred from ecommerce context, price, or general purchasability.

Write one JSON object per line to `results_greece_ready_koufomata.jsonl`:
{"item": { "supplier": "<supplier>", "product": "<product>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

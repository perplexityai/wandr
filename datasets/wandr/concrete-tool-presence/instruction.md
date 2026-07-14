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

## `concrete_tool_presence`

Identify 8+ manufacturers as current makers or brand owners of public concrete finishing tools or close accessories; for each manufacturer identify 8+ product SKU/model examples, and for each product cover each of the 3 public-presence facets below with 1+ URL. Use a broad open set across brands, product families, and source domains; do not fill the grid from one brand family, one retailer, or one repeated page pattern.

The task is about public product/source provenance for concrete finishing work: floats, bull floats, groovers, edgers, trowels, brackets/adapters, handles, float hooks, tote/carrier kits, finishing brushes, and similar close accessories. It is not a price-comparison, seller-ranking, distributor-recommendation, quote-solicitation, customer-targeting, demand-inference, or safety/compatibility task.

Presence facets:
- `official_identity`: a manufacturer-controlled product detail page, category/product card, datasheet, or official catalog section showing the claimed manufacturer and SKU/model/product identity.
- `public_seller_price_state`: a non-manufacturer retailer, distributor, marketplace, or specialist-store listing for the claimed product that shows a page-local listing or price state.
- `unit_or_pack_signal`: a configuration-rich secondary source showing source-stated product configuration. Use a non-manufacturer seller/distributor/marketplace listing, or a manufacturer catalog, PDF, datasheet, spec table, or kit-content section. A basic manufacturer product landing page that could also serve as the `official_identity` citation is not enough.

Manufacturers ought to be real makers or brand owners in this product space. Product examples must be product-level concrete finishing tools or close accessories, not food Kraft products, kraft-paper packaging/dunnage, unrelated generic hardware, seller category pages, or private procurement records.

Requirements:
- The page must identify the claimed manufacturer and claimed product/SKU/model, or a clearly equivalent product identifier.
- The page should make the source role for the selected `presence_facet` visible. `official_identity` needs manufacturer-controlled product or catalog evidence; `public_seller_price_state` needs a non-manufacturer seller, distributor, marketplace, or store listing; `unit_or_pack_signal` needs a configuration-rich secondary source rather than simple reuse of the basic official product page.
- The page must expose the selected public signal. For `official_identity`, it must show official product identity. For `public_seller_price_state`, it must show a page-local state such as visible price, price-in-cart, account/login price, request quote/RFQ, available-by-request, sold out/out of stock, or a visible unpriced listing. For `unit_or_pack_signal`, it must show at least two source-stated configuration details tied to the product, such as UOM/each/pack/carton/kit quantity plus dimension, size, material, handle length, component contents, or compatible bracket/handle facts. A single "includes 1" or generic size mention by itself is not enough.
- Prefer a distinct URL for each facet of the same product. Same-URL reuse across `official_identity` and `unit_or_pack_signal` is usually invalid unless the unit/pack URL is a separate catalog/PDF/datasheet/spec-table or kit-content section, not the same basic official product landing page.

Write one JSON object per line to `results_concrete_tool_presence.jsonl`:
{"item": { "manufacturer": "<manufacturer>", "sku": "<sku>", "product": "<product>", "presence_facet": "<presence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `lentropiste_retail_provenance`
  - `lentropiste_retail_provenance.retailer_context`

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

## `lentropiste_retail_provenance`

Identify 50+ retailer/storefront surfaces as public commercial surfaces carrying L'Entropiste, and for each surface cover each of the 2 product roles listed below with a product-specific source (i.e. 1+ URL).

The evidence is public retail provenance for L'Entropiste, with Dorian's Spleen as the anchor product. It is not a price ranking, purchase guide, authenticity verdict, review summary, delivery-reliability claim, customs guide, inventory alert, or source for contact/outreach collection.

Product roles:
- `dorians_spleen`: a public product page for L'Entropiste Dorian's Spleen.
- `other_lentropiste_product`: a public product page for a different named L'Entropiste product, not a Dorian's Spleen size, sample, or travel-format variant.

Retailer/storefront surfaces can include brand-owned shop pages, perfume retailers, marketplace seller pages, sample/decant storefronts, or other public commercial storefronts when the cited page visibly binds the product to the claimed storefront. The retailer and storefront/domain names should identify the commercial surface rather than a broad fragrance database, review site, or editorial page.

Requirements:
- The page must clearly identify the claimed retailer/storefront surface.
- The page must identify the L'Entropiste product at the bar for `product_role`: Dorian's Spleen for `dorians_spleen`; a clearly different named L'Entropiste product for `other_lentropiste_product`.
- The page must show public retail-offer detail for that product, including at least one size/format and a price with currency.

Write one JSON object per line to `results_lentropiste_retail_provenance.jsonl`:
{"item": { "retailer": "<retailer>", "storefront_or_domain": "<storefront_or_domain>", "product_role": "<product_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `lentropiste_retail_provenance.retailer_context`

Cross-tasknode identifier discipline: this task is for the same {= retailer_surface =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= retailer_surface =}+ retailer/storefront surfaces carrying L'Entropiste, cover each of the 2 retailer-context roles listed below with a public context source (i.e. 1+ URL).

Context roles:
- `brand_relationship`: a page that visibly ties the retailer/storefront surface to L'Entropiste as a carried brand, collection, stockist, seller, direct shop, or source-stated authorized retailer.
- `market_or_delivery_scope`: a page that visibly states the storefront's market, store geography, shipping country/region, delivery condition, shipping threshold, or comparable public delivery/market scope.

Source-stated authorization is provenance evidence only, not an authenticity, reliability, customs, or purchase-suitability conclusion. The evidence is not a source for recommendations, rankings, lead scoring, outreach collection, or procurement advice.

Requirements:
- The page must clearly identify the claimed retailer/storefront surface.
- The page must contribute context at the bar for `context_role`: a L'Entropiste retail relationship for `brand_relationship`; a public market, store, shipping, delivery, threshold, or geography signal for `market_or_delivery_scope`.
- The page must provide the context in a page-visible way through headings, breadcrumbs, store/location text, brand-collection framing, policy text, shipping banners, source-stated stockist/authorization wording, or comparable content anchors.

Write one JSON object per line to `results_lentropiste_retail_provenance.retailer_context.jsonl`:
{"item": { "retailer": "<retailer>", "storefront_or_domain": "<storefront_or_domain>", "context_role": "<context_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

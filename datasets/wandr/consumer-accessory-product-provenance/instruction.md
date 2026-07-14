You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `consumer_accessory_product_provenance`
  - `consumer_accessory_product_provenance.retail_prices`
  - `consumer_accessory_product_provenance.dated_signals`

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

## `consumer_accessory_product_provenance`

For all the 8 consumer electronics accessory categories listed below, name 10+ distinct brand/product pairs per category and supply 1+ official product or manufacturer-store URL for each category/product pair. The work is public product provenance: source-stated facts only, with no target-company anchor, rankings, buying recommendations, strengths/weaknesses, or strategy.

Target categories:
- **earbuds and headphones**
- **smartwatches and fitness wearables**
- **portable power banks**
- **wireless chargers**
- **phone cases and protection**
- **charging cables and adapters**
- **item trackers and finders**
- **tablet keyboard cases**

Official pages must be controlled by the manufacturer, brand, or official store and must identify a specific currently or recently marketed accessory product. Broad brand homepages, category hubs, retailer listings, reviews, press/news pages, "best" listicles, and ranking surfaces do not count for this official identity/spec source role.

Requirements:
- The page must clearly identify the claimed brand and product.
- The page must show that the product fits the claimed accessory category.
- The page must state at least one concrete product spec or feature for that product.

Write one JSON object per line to `results_consumer_accessory_product_provenance.jsonl`:
{"item": { "category": "<category>", "brand": "<brand>", "product": "<product>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `consumer_accessory_product_provenance.retail_prices`

Cross-tasknode identifier discipline: this task is for the same {= brand_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= brand_product =}+ consumer electronics accessory category/brand/product pairs, supply current source-stated retail prices from commerce product pages, at least 2 different pages per product.

Each page must be a product-dedicated retailer, marketplace, or commerce listing for the specific product and show a current purchasable price. Manufacturer marketing/spec pages, price-comparison aggregators, search or category pages, reviews, "best deals" roundups, and pages with only MSRP or historical price mentions do not count.

Requirements:
- The page must clearly identify the claimed brand and product.
- The page must show a concrete current price or price range for that specific product listing.

Write one JSON object per line to `results_consumer_accessory_product_provenance.retail_prices.jsonl`:
{"item": { "category": "<category>", "brand": "<brand>", "product": "<product>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `consumer_accessory_product_provenance.dated_signals`

Cross-tasknode identifier discipline: this task is for the same {= brand_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= brand_product =}+ consumer electronics accessory category/brand/product pairs, supply dated public product/news signals, 1+ URL per product.

Each page must be a dated newsroom item, press release, PR wire item, or reputable industry/news article whose central subject includes the claimed product or product line. Retailer listings, undated official product pages, generic category pages, "best" listicles, buyer's guides, and recommendation/ranking surfaces do not count as dated-signal evidence.

Requirements:
- The page must clearly identify the claimed brand and product.
- The page must show an on-page date for the product signal.
- The page must describe a launch, announcement, availability, material update, or comparable public product/news signal for the claimed product.

Write one JSON object per line to `results_consumer_accessory_product_provenance.dated_signals.jsonl`:
{"item": { "category": "<category>", "brand": "<brand>", "product": "<product>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

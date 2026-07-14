You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `au_letterbox_product_presence`
  - `au_letterbox_product_presence.brand_public_trace`

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

## `au_letterbox_product_presence`

For 15+ Australia-facing residential letterbox or mailbox brands, sellers, or manufacturers, name 2+ residential letterbox/mailbox models per brand; for each brand/model pair and each of the 2 model evidence facets listed below, supply a public source (i.e. 1+ URL under each facet) showing official or commerce-visible product evidence.

The point is public product provenance: specifications, price, availability, and retailer-observed details count only as page-shown observations, not as buyer advice, value ranking, suitability claims, or product-quality truth.

Model evidence facets:
- `official_spec`: brand-controlled product or product-range evidence for source-stated specifications, features, materials, dimensions, capacity, construction, finish, lock/slot/weatherproofing, or model-family details.
- `retail_commerce`: Australian public retail, marketplace, deal, or purchasable-listing evidence for price, availability, retailer-observed product state, or commerce framing.

A brand should have public AU-facing presence in residential letterboxes/mailboxes. A model should be a named residential letterbox/mailbox product; colour, finish, SKU, package-size, ratio-like, dimension-only, or minor variant labels of the same product are not separate models unless the source itself frames them as distinct model families. Sources should be public, accessible, and usable normal pages.

Requirements:
- The page must identify the named brand and model, or an unambiguous model/range alias for the claimed product.
- The page must tie the product to the Australian public market, retailer ecosystem, brand presence, or AU-facing consumer context.
- The page should make its facet-appropriate source role visible. For `official_spec`, this means brand/maker control or official product-range framing. For `retail_commerce`, it should read as an Australian retail, marketplace, deal, or purchasable listing.
- The page should expose a concrete observation scoped to the named product and evidence facet. For `official_spec`, this means a source-stated specification, feature, material, dimension, capacity, construction, finish, lock/slot/weatherproofing, or model-family detail. For `retail_commerce`, it means price, availability, retailer product state, purchasability, or marketplace/deal context.

Write one JSON object per line to `results_au_letterbox_product_presence.jsonl`:
{"item": { "brand": "<brand>", "model": "<model>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `au_letterbox_product_presence.brand_public_trace`

Cross-tasknode identifier discipline: this task is for the same {= brand =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= brand =}+ Australia-facing residential letterbox or mailbox brands, sellers, or manufacturers, cover each of the 2 brand-level public trace facets listed below with distinct public sources (i.e. 2+ URLs) per facet. Each source should expose public reception or third-party market context for the brand's letterbox/mailbox products, product range, or residential-mailbox channel, without requiring a specific model-level match.

The point is brand-level public product provenance: reviews, complaints, guide mentions, deal discussions, installed-use context, and comparable traces count only as page-shown observations, not as buyer advice, value ranking, suitability claims, or sentiment truth.

Brand-level trace facets:
- `public_reception`: public rating, review count, review text, Q&A, forum/social owner comment, complaint, or customer-review evidence about the brand's residential letterbox/mailbox products or a clearly scoped product range.
- `independent_market_trace`: non-maker public context, such as an editorial guide, hardware/garden article, product directory, installed-use/context page, marketplace/deal discussion, or comparable third-party trace that identifies the brand or range and gives a concrete public-context observation.

A brand should have public AU-facing presence in residential letterboxes/mailboxes. Brand-level traces may refer to a named model, a clearly scoped product range, or the brand's residential-mailbox channel; traces about unrelated garden, pottery, homeware, gate, fencing, or general delivery products do not establish this brand trace. Sources should be public, accessible, and usable normal pages.

Requirements:
- The page must clearly identify the named brand or an unambiguous brand/channel alias.
- The page must tie the brand trace to the Australian public market, retailer ecosystem, brand presence, or AU-facing consumer context.
- The page must connect the trace to the brand's residential letterbox/mailbox products, a clearly scoped product range, or residential-mailbox channel.
- The page should make its facet-appropriate source role visible. For `public_reception`, it should be recognizable as rating, review, Q&A, forum/social owner-comment, complaint, or customer-review evidence. For `independent_market_trace`, it should be a non-maker public-context source and not merely the same official product page or simple checkout listing doing official specifications or retail-commerce work.
- The page should expose a concrete observation scoped to the named brand and trace facet. For `public_reception`, this means a visible rating/review-count signal, review/Q&A text, owner comment, complaint, or customer observation. For `independent_market_trace`, it means a third-party public-context observation such as guide/editorial positioning, installed-use context, directory placement, deal-thread context, or comparable market trace.

Write one JSON object per line to `results_au_letterbox_product_presence.brand_public_trace.jsonl`:
{"item": { "brand": "<brand>", "trace_facet": "<trace_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

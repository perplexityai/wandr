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

## `bachir_doha_brand_competitors`

Identify 100+ brands as Doha/Qatar-operating ice-cream, gelato, frozen-dessert, sweets, bakery-dessert, or dessert-cafe brands; cover the 4 analysis facets listed below for each brand by supplying a source (i.e. 1+ URL under each axis) which exposes a focused, substantive, tangible finding clearly scoped to the facet in question.

The purpose is to build a competitor landscape for the Bachir Ice Cream brand (the reported brands set could cover it as well).

Analysis facets:
- `owned_social_identity`: the brand's public identity, self-presentation, and owned/operated presence in the Qatar/Doha market
- `customer_sentiment`: public customer reaction to the brand's Qatar/Doha product, service, or outlet experience
- `delivery_commerce`: the brand's public menu, ordering, delivery, price, or purchasability presence in Qatar
- `market_positioning`: how the brand is situated in the local dessert / ice-cream / cafe competitive landscape

The sources should be fully public, accessible, and usable (e.g. not paywall-guarded, bare app pages, or login screens).

Requirements:
- The page must clearly identify the named brand.
- The page must credibly tie the brand to Doha, Lusail, Qatar, a Qatar delivery market, or a specific Qatar outlet.
- The page should make its facet-appropriate source role visible. For `owned_social_identity`, this might come from page/account identity text tying the brand to an official, operator, outlet, franchise, or social presence (e.g. "Shop" / "Stores" / "Our shops" wording plus brand's ownership signals, an official social account title/handle, a mall/operator tenant header, a Qatar/Doha outlet title, etc). For `customer_sentiment`, it should be recognizable as a review or user-reaction surface, e.g. through anchors like "Review score", "reviews", "From Google", reviewer names / review dates / star counts, platform wording unambiguously suggesting the user-generated-review nature of the page, and so on. For `delivery_commerce`, it should read as a menu, order, or delivery surface, e.g. through wording like "delivery service in Qatar", "restaurant menu", "delivers to you", branch / area selectors, city or delivery-market labels, order buttons, cart controls, or other page-role cues making the menu / order / delivery availability clear. For `market_positioning`, it should read as article, guide, venue-directory, or local-list context, with signals such as publisher / title / date context, dining-directory labels, article or guide framing, list / table headings, category lines, nearby / similar-brand sections, or comparable page framing that gives the brand editorial / guide / venue-directory treatment; a "Local Guide" user label, user-review award, or similar UGC badges on a `customer_sentiment`-eligible source wouldn't justify a market-positioning source fit.
- The page should expose a focused finding clearly scoped to the named brand and analysis facet. For `owned_social_identity`, this means a concrete self-presentation or public-presence signal, such as a Qatar-specific account identity, brand story, heritage claim, outlet/operator identity, visual/social tone, or a distinct public-facing persona cue. For `customer_sentiment`, it means a specific rating pattern, review-volume signal, praise, complaint, or customer observation. For `delivery_commerce`, it means a concrete menu item, category breadth evidence, best-seller anchor and corresponding product information, prices, delivery condition, or Qatar-market orderability detail. For `market_positioning`, it means a tangible positioning frame carried by editorial / guide / venue-directory / curated local-list voice, such as "premium" / "mainstream" / "artisanal" / "family" / "tourist" / "vegan-friendly", salient (rationale-backed) distinction from competitor brands.

Write one JSON object per line to `results_bachir_doha_brand_competitors.jsonl`:
{"item": { "brand": "<brand>", "analysis_facet": "<analysis_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

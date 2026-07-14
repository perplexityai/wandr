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

## `online_houseplant_retailer_catalog`

Identify 50+ online houseplant or home-garden plant retailers; cover the 4 evidence facets listed below for each retailer by supplying a source (i.e. 1+ URL per facet) which exposes a focused, substantive, source-bounded capability finding clearly scoped to the facet in question. Each retailer should sell live houseplants, rare or tropical collector plants, succulents or cacti, outdoor garden plants, seeds, shrubs, perennials, or comparable home-garden plant goods through an online catalog, shop, or order flow.

Evidence facets:
- `catalog_specialty` -- catalog scope or specialty: houseplants, rare / variegated plants, aroids, tropicals, succulents, cacti, outdoor perennials, shrubs, seeds, or related home-garden plant categories
- `commerce_terms` -- online commerce terms: retail / wholesale posture, price ranges, order minimums, contact email, guarantees, checkout behavior, bulk gifting, or customer-support process
- `shipping_region` -- shipping reach and constraints: regions served, carriers, shipping days, weather holds, heat packs, agricultural bans, quarantine, export paperwork, or live-plant restrictions
- `trust_signal` -- public trust and demand signals: customer reviews, BBB / Trustpilot-style pages, Reddit or collector-forum corroboration, testimonials, social proof, or press mentions

Sources should be meaningfully usable and substantive (e.g. login-only checkout shells, scraped record-dump mirrors, or generic "best plant shops" listicles are not enough by themselves). Marketplace category pages, search-result pages, and thin tracking or coupon pages can help discovery, but they do not count as evidence sources on their own.

Requirements:
- The page must identify or credibly profile the named retailer as an online source for live houseplants, rare plants, tropicals, succulents, perennials, shrubs, seeds, or comparable home-garden plant goods.
- The page must communicate a source class appropriate to the named evidence facet: for `catalog_specialty`, an official retailer catalog, collection, homepage, or product page that visibly carries the catalog scope; for `commerce_terms`, an official retailer ordering, FAQ, policy, wholesale, contact, or support page; for `shipping_region`, an official retailer shipping, delivery, returns, FAQ, or policy page; for `trust_signal`, a public review, community, social, press, BBB / Trustpilot-style page, or a retailer-hosted testimonial section that visibly carries a retailer-specific signal.
- The page should expose a finding with substantive depth one rung beyond the page title or homepage tagline, scoped to the named retailer and appropriate to the facet: for `catalog_specialty`, a source-visible category mix, named plant class, or stated catalog scale (not a bare homepage tagline or product-title restatement); for `commerce_terms`, a source-visible price, threshold, support channel, guarantee, wholesale posture, or order-handling term (not a generic "they take orders online"); for `shipping_region`, a source-visible region, carrier, timing, weather-hold, agricultural restriction, or live-plant packaging detail (not a generic "they ship plants"); for `trust_signal`, a source-visible rating, review count, review-text excerpt, BBB / Trustpilot grade, press mention, or testimonial body (not a generic "they have reviews").
- The submitted finding must stay within what the cited page visibly states or reasonably communicates, including the numeric, temporal, geographic, and source-class boundary of any prices, thresholds, regions, ratings, review counts, restrictions, or guarantees claimed.

Write one JSON object per line to `results_online_houseplant_retailer_catalog.jsonl`:
{"item": { "retailer": "<retailer>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

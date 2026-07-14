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

## `dubai_fitness_brand_competitors`

For 90+ brands, cover the 4 analysis facets listed below for each brand by supplying a source (i.e. 1+ URL under each facet) that exposes a focused, substantive, tangible finding clearly scoped to the facet in question. The brands should operate in the Dubai / UAE fitness, boutique gym, yoga / pilates, sports recovery, activewear, wellness-membership, or sports-nutrition retail market, and each source ought to be a fully public, accessible, usable page rather than a paywall-guarded page, bare app screen, empty social shell, or login-only listing.

The purpose is to build a competitive public-presence landscape for premium fitness and wellness brands in Dubai, where owned channels, booking commerce, customer reaction, and local positioning often live on different surfaces.

Analysis facets:
- `owned_social_identity`: how the brand defines and projects itself through channels it controls or operates in the Dubai / UAE market
- `customer_sentiment`: public customer reaction to the brand's classes, facilities, product, service, or outlet experience in Dubai / UAE
- `booking_commerce`: how a prospective customer in Dubai / UAE can actually transact with or buy from the brand
- `market_positioning`: how the brand is situated in the local fitness / wellness / active-lifestyle competitive landscape

Requirements:
- The page must clearly identify the named brand.
- The page must credibly tie the brand to Dubai, Abu Dhabi, the UAE, a UAE delivery / booking / retail market, or a specific UAE outlet.
- The page should make its facet-appropriate source role visible. For `owned_social_identity`, this means official account, site, operator, outlet, franchise, tenant, or self-presentation signals. For `customer_sentiment`, it should be recognizable as a review, rating, testimonial, user-reaction, or customer-feedback surface. For `booking_commerce`, it should read as a class schedule, booking, membership, price, shop, cart, delivery, retail, or orderability surface. For `market_positioning`, it should read as article, guide, curated local list, venue directory, awards, or editorial / directory voice that positions the brand rather than merely collecting user reviews.
- The page should expose a focused finding clearly scoped to the named brand and analysis facet. For `owned_social_identity`, this means a concrete self-presentation or public-presence signal. For `customer_sentiment`, it means a specific rating pattern, review-volume signal, praise, complaint, or customer observation. For `booking_commerce`, it means a concrete class, product, membership, schedule, price, package, booking, or availability detail. For `market_positioning`, it means a tangible positioning frame carried by editorial / guide / directory voice, such as premium, budget, women-focused, family-oriented, rehabilitation-focused, high-intensity, boutique, luxury, community, or similar.

Write one JSON object per line to `results_dubai_fitness_brand_competitors.jsonl`:
{"item": { "brand": "<brand>", "analysis_facet": "<analysis_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

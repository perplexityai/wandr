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

## `focal_brand_local_competitor_panels`

For each of the 6 focal consumer brands below, cover 10+ consumer brands in that focal brand's local-market competitor set — the focal brand itself or any other brand a brand-strategy analyst would reasonably include in its same-vertical, same-local-market competitor panel — with 3+ distinct public evidence areas per covered brand, 1+ concise source-bounded audit finding per cell, and a source (1+ URL per finding). The focal subjects are:

- **Bachir Ice Cream** in Doha (local market: Doha, Lusail, Qatar, a Qatar delivery market, or a specific Qatar outlet)
- **Pierre Marcolini** in Brussels (local market: Brussels, a Belgian retail location, a Brussels boutique, or a Belgian delivery market)
- **Magnolia Bakery** in New York (local market: New York City, Manhattan, Brooklyn, a New York retail location, or an NYC delivery market)
- **Pinkberry** in Los Angeles (local market: Los Angeles, the LA metro, a Los Angeles County retail location, West Hollywood, or an LA delivery market)
- **Tim Hortons** in Toronto (local market: Toronto, the GTA, an Ontario retail location, or a Toronto delivery market)
- **Nusr-Et** in Doha (local market: Doha, the Sheraton Grand Doha, a Qatar restaurant location, or a Qatar delivery market)

Count brand-owned pages, public social profiles or posts, map/review pages, delivery or menu pages, local guide/editorial pages, venue/mall/tourism listings, and similarly visible public sources. App-only or login-only shells are not enough by themselves. The finding may use audit labels such as positioning class, engagement or social-quality signal, sentiment summary, common complaint, heritage framing, tourist/family appeal, or competitor context only when the cited page supports that wording.

Evidence areas:

- **owned_social_identity**: brand-owned, official, or public social evidence for identity, visual tone, content quality, storytelling, heritage, or public-facing social presence
- **customer_sentiment**: review, rating, praise, complaint, service-quality, product-quality, or review-volume evidence from public customer-review or guide/listing pages
- **delivery_commerce**: public delivery, menu, ordering, best-seller, price, category, rating, availability, or delivery-platform evidence
- **market_positioning**: local editorial, venue, tourism, official-brand-story, or guide evidence for positioning such as premium, mainstream, trendy, authentic, family, tourist, heritage, or competitor context

Requirements:

- The page must clearly identify or credibly profile the submitted brand and tie it to the local market of the row's focal subject.
- The submitted brand must belong to a credible competitor panel for the row's focal brand by sharing the same consumer vertical: the focal brand itself or any brand a brand-strategy analyst would reasonably include in the focal brand's vertical-aligned competitor set.
- The page must support the submitted finding for the row's evidence area.
- The cited surface must fit the evidence area and expose brand-specific public evidence rather than generic directory, search-result, or category filler.
- The submitted finding must stay within what the cited source publicly states, including any ratings/review counts, menu items, prices, currentness, sentiment, complaint, positioning, or competitor-comparison boundary.

Write one JSON object per line to `results_focal_brand_local_competitor_panels.jsonl`:
{"item": { "focal_brand": "<focal_brand>", "brand": "<brand>", "evidence_axis": "<evidence_axis>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

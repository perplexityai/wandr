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

## `alaska_food_producers`

For each of the 3 source families listed below, cover 225+ named Alaska food producers or Alaska food product businesses; for every (`source_family`, `producer`) pair, supply 1+ public URL whose page independently supports that producer/source-family provenance claim.

The target is provenance evidence, not a consumer directory or lead list. Useful evidence names a business or producer and shows that it grows, raises, harvests, catches, makes, processes, or otherwise produces food in Alaska.

Source family labels:
- `official_or_program_directory`: government, Alaska Grown, Made in Alaska, university/program, or comparable official directory or program page that names the producer and food-product evidence.
- `producer_owned_or_brand_page`: the producer's or brand's own public site, storefront, product page, about page, blog, or other controlled channel.
- `regional_market_foodhub_or_sector_source`: regional local-food directories, food hubs, Local Food Marketplace pages, farmers market or co-op pages, mariculture/seafood/sector sources, and comparable public regional or sector pages.

Report the community/city, region when source-stated or defensibly inferred, food product category, provenance type, currentness state, and a concise evidence note. If the cited source supports an Alaska tie but no specific community or reliable region, say so instead of inventing one; use `no_region` when the region is not source-stated or defensibly inferable. Provenance type should use one or more of: grown, raised, harvested, caught, made, processed, mariculture, local_food_marketplace.

Currentness is source-local: label what the cited source itself shows, not whether no other current proof exists elsewhere.
- `current`: the cited source itself gives a current or recent signal, such as active producer profile language, products for sale, availability timing, or otherwise live producer/product wording.
- `stale`: the cited source is explicitly old, archived, closed, sunset, or tied to a past season/year, so it supports historical provenance but not current status.
- `conflict`: the cited source or submitted excerpts contain materially conflicting signals about current activity, location, product category, or production provenance.
- `no_current_proof`: the cited source supports producer provenance but gives no source-local current, stale, or conflict signal; this is not a global claim about other sources.

Producers ought to be actual Alaska food producers or Alaska food product businesses. Restaurants, grocers, distributors, gift shops, chambers, caterers, and resellers do not count unless the cited page supports their own Alaska-made food product. Non-food farms/products, flowers, fiber, nursery starts, hay/feed, crafts, farm tourism, and services do not count unless separate food-product evidence is present.

Sources should be public pages with producer/product/provenance content. Do not use review sites, "best of" listicles, affiliate pages, lead-generation company databases, social-only surfaces, food-safety or nutrition pages, contact-only seafood supplier lists, buyer notes, price lists, wholesale-capacity pages, shipping terms, outreach notes, or procurement guidance as primary evidence.

Requirements:
- The page must visibly fit the claimed `source_family`.
- The page must clearly name the claimed producer or food product business.
- The page must support a food product or food-product category for that producer.
- The page must support both an Alaska location or operating tie and the claimed production provenance type for that food product.

Write one JSON object per line to `results_alaska_food_producers.jsonl`:
{"item": { "source_family": "<source_family>", "producer": "<producer>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `artisan_brand_visibility`

Identify 60+ brands as small, artisan, independent, maker-led, farm, craft, beauty, food, home, or lifestyle consumer-product brands; for each brand and each of the 4 visibility facets listed below, supply a native consumer- or trade-facing public placement source for that facet (i.e. 1+ URL).

The point is public placement provenance, not PR planning, merchant enablement, ecommerce case-study collection, broad retailer shelf mapping, or generic beauty/lifestyle brand discovery: the evidence should come from the outlet, program, award, retailer, marketplace, stockist, collaborator, or other native surface where an audience actually encounters a brand-specific placement. Brand-owned press roundups, commerce-service/vendor pages, bare award indexes, ordinary shop shelves, and generic brand/profile pages are not native visibility sources when they only aggregate, list, tease, summarize, or discuss placements from the outside.

Visibility facets:
- `editorial_profile`: an independent editorial, trade, local, lifestyle, or product-category article, interview, profile, feature, or similar publisher-controlled story centered on the brand, founder, or branded product line
- `award_or_curated_list`: an award-program entry, finalist/winner page, honoree page, consumer buyer-guide entry, editorial list, trade/style gift guide, or curated-market page that publicly recognizes the brand or one of its products with brand- or product-specific treatment
- `produced_appearance`: a native podcast episode page, TV segment page, video feature, conference/session page, broadcast page, or comparable produced program page where the brand, founder, maker, or principal operator appears as a guest, speaker, subject, or featured participant
- `retail_or_collaboration`: a consumer-facing retailer/platform feature, marketplace story, public stockist/vendor spotlight, co-branded collection, product collaboration, product-drop story, new-to-platform feature, or collaborator-controlled announcement involving the brand

Brands ought to be real consumer product brands with a discernible small, independent, maker, founder-led-and-still-brand-led, farm, craft, artisan, or closely held lifestyle identity. Beauty, food, home, or lifestyle category membership alone is not enough. Mass retailers, marketplaces, PR agencies, media outlets, award programs, podcasts, TV shows, conglomerate labels, celebrity/personality labels without an independent product-brand identity, large mass-market product lines, and generic product categories do not count as brands for this task.

Requirements:
- The page must clearly identify the named brand.
- The page should make its native source role visible for the claimed `visibility_facet`: independent publisher/editorial control for `editorial_profile`, excluding native episode/program pages unless they also carry a standalone written profile; award, honoree, buyer-guide, gift-guide, curated-market, or brand-specific list-entry framing for `award_or_curated_list`; native program, episode, segment, video, broadcast, or event/session framing for `produced_appearance`; consumer-facing retailer, platform, stockist, marketplace-story, spotlight, collection, drop, feature, or collaborator framing for `retail_or_collaboration`.
- The page must describe the actual public visibility event, recognition, appearance, feature, drop, spotlight, or collaboration for the named brand on that native surface. The load-bearing proof must be brand/product-specific: a bare row in a master award index, an ordinary retailer brand shelf or product grid, a generic brand profile, a secondary mention inside a commerce-service case study, merchant-education article, generic business/marketing example, contact page, media inquiry page, vendor directory, search result, tag archive, or brand-owned press roundup does not count.
- The page should carry usable public context for the native visibility, such as an article date, award cycle, list edition plus brand-specific entry context, episode or segment title/date, event/session date, collection season, product-drop context, spotlight framing, or retailer/platform/collaborator feature context.

Write one JSON object per line to `results_artisan_brand_visibility.jsonl`:
{"item": { "brand": "<brand>", "visibility_facet": "<visibility_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

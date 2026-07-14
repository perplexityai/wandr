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

## `uconn_basketball_trading_cards`

For at least 150+ (player, card_issue) tuples drawn from notable UConn men's or women's basketball alumni who reached the NBA or WNBA, supply at least 1 URL each on a card-level marketplace surface substantiating the card's identity and one of two collector-value routes: graded-tier value at or above $25, or raw / ungraded value at or above $50. Each tuple ought to be well formed: the player ought to be a real UConn basketball alum who reached the NBA or WNBA, and the card_issue ought to identify one specific plausible card.

Requirements:
- The source must be a card-level marketplace surface focused on one specific (player, card_issue) — either a single-card page with the card's identifying attributes and price or sales evidence in dedicated layout, or an identifiable card-level marketplace row carrying its own card identity and grade / value columns. Bare transactional item-listing pages are excluded, even if they show one offered or sold card with identifying attributes and a realized price; the page must have card-level valuation / sales-history structure, an identifiable card-level value row, or an admitted auction-lot style record rather than just a standalone listing.
- The source must identify the card with sufficient specificity to anchor the row's claim — at minimum the issue year, brand and set, and card number — and any parallel / insert variant claimed in the row must also appear on the source rather than being implied by extrapolation.
- The source's named card subject must be the same player the row claims, not a same-named or similarly-named player from the same draft class or set.
- The source must evidence the card's collector value through one of two routes — a graded-tier (PSA 9, BGS 9, SGC 9, or higher) figure at or above $25, or a raw / ungraded figure at or above $50. The figure must be a marketplace-tracked or realized-sale price; values displayed with an explicit estimate-disclaimer do not satisfy this for the disclaimed tier.

Write one JSON object per line to `results_uconn_basketball_trading_cards.jsonl`:
{"item": { "player": "<player>", "card_issue": "<card_issue>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

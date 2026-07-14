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

## `prize_contingency_insurance`

Build a public-source provenance map for 100+ entities tied to promotional-prize, prize-indemnity, contingency, over-redemption, weather-triggered promotion, prediction-contest, conditional-rebate, loyalty/reward-protection, contractual-bonus, or comparable incentive-risk insurance activity in the United States, Canada, or the United Kingdom. For each entity, cover at least 2 of the source roles below with 1+ URL per role; more source roles are useful when public evidence exists.

The point is to show what public sources actually establish about each entity's place in the promotional-risk chain, not to rank providers or infer private diligence facts. Insurance and carrier relationships should stay source-stated. Unknown or conflicting capacity, role, geography, parent, or date information should be marked as missing or conflicted rather than filled in from inference.

Source roles:
- `product_mechanics`: a source tying the entity to promotional-risk products and describing the covered mechanic, such as prize indemnity, over-redemption, weather promotion, conditional rebate, prediction contest, contractual bonus, or comparable incentive-risk coverage.
- `market_role`: a source clarifying the entity's public role in the insurance or promotion-risk chain, such as carrier, underwriter, broker, MGA/MGU, Lloyd's coverholder, reinsurer, program administrator, wholesaler, promotion agency/procurer, or comparable role.
- `capacity_authority`: a source-stated carrier, capacity, Lloyd's, reinsurance, licensing, public filing, regulator, or enforcement signal; absence of public capacity is a missing state rather than a reason to invent a partner.
- `event_case`: a public promotion, payout, denial, dispute, fraud, enforcement, or comparable case example tied to the entity's promotional-risk activity.

Sources can include official provider/product/program pages, regulator or enforcement records, public filings, carrier/partner pages, official market-role pages, reputable insurance trade coverage, and reputable event/case coverage. Directories, marketplace listings, market reports, Wikipedia-style pages, consumer explainers, law-firm blog explainers, and generic compliance summaries may help discovery but do not count by themselves as primary evidence for a row.

Promotion agencies, administrators, and procurers can count when the source ties them to arranging, administering, procuring, or supporting promotional-risk insurance; they should not be mislabeled as insurers unless the source says so. Event examples can corroborate activity when public, but they do not need to identify a carrier unless the source itself does.

Requirements:
- The page must clearly identify the submitted entity.
- The page must tie the entity to the United States, Canada, or the United Kingdom, either directly or through an explicitly global / worldwide promotional-risk offering that reaches those markets.
- The page must connect the entity to promotional-risk insurance activity or a closely related incentive-risk product mechanic.
- The page must make the declared `source_role` visible through source-class and content signals appropriate to that role.
- The submitted provenance must stay within what the page states or directly communicates, including honest missing or conflict states for role, capacity, carrier, geography, parent, event identity, or date when the source does not settle them.

Write one JSON object per line to `results_prize_contingency_insurance.jsonl`:
{"item": { "entity": "<entity>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

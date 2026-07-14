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

## `hkex_ai_disclosures`

For 13+ HKEX-listed AI-value-chain issuers, pair listing-document claims with officially filed or posted issuer documents available through 2026-06-28. For each issuer, cover the 4 disclosure facets below. For each issuer/facet, name 1+ concrete listing-document claim, then supply 1+ URL for each of the 2 source roles.

Each issuer must be tied by its listing materials to AI, large models, AI software or applications, AI compute or infrastructure, robotics, autonomy, or a similar AI-value-chain business. News branding alone does not count.

Disclosure facets:
- `business_or_product_capability`: business model, AI product, platform, model, robotics/autonomy, or AI-enabled capability
- `commercial_or_operating_metric`: revenue, customer, user, deployment, order, contract, gross-profit, or operating-volume metric
- `rd_technology_or_compute_investment`: R&D expense, technology roadmap, compute infrastructure, model-training, chip, data, or platform investment
- `capital_structure_proceeds_or_corporate_action`: global-offering proceeds, share capital, over-allotment, use of proceeds, dividend, name change, A-share plan, repurchase mandate, monthly return, or other official corporate action

Source roles:
- `listing_baseline`: official HKEX prospectus, PHIP, global-offering document, or clearly official issuer-hosted mirror of listing materials
- `post_listing_followup`: official post-listing HKEX or issuer disclosure dated no later than the checked date, with after-listing timing supported when the cited record exposes the listing date

Keep the comparison factual. `claim_summary` must identify a specific listing-document metric, statement, product or model capability, R&D or compute investment, proceeds/listing/share-capital action, or similarly concrete claim. Broad source-role or facet summaries do not count. Report the filing/publication date, a page/section/table or announcement locator visible in the cited source, the source-role statement, and a factual relationship status when the source role is `post_listing_followup`. When the cited record exposes the issuer's listing date, report it and keep the timing comparison factual. Do not provide investment advice, legal opinion, valuation, stock-performance interpretation, market-performance judgment, or claims about company quality.

Requirements:
- The page must identify the same issuer as the submitted stock code and issuer name.
- The page must fit the submitted source role as an official HKEX or issuer document, not news, market data, analyst commentary, or stock-price material.
- The page must provide a document filing, publication, prospectus, announcement, or reporting date. For `post_listing_followup`, that date must be on or before 2026-06-28; when the cited page also exposes the issuer's listing date, the document date must be after that listing date.
- The page must belong to the submitted disclosure facet.
- The cited source and excerpts must visibly localize the claim to a reasonably specific page, section, table, note, heading, announcement title, or equivalent document passage.
- The page must supply the source-role side of a concrete `claim_summary`: for `listing_baseline`, the listing document must state the specific baseline metric, statement, product/model capability, R&D/compute investment, proceeds/listing/share-capital action, or similar claim; for `post_listing_followup`, the later official document must state a metric, statement, corporate action, or explicit non-comparable field/status in the same factual lineage. A generic facet or source-role template is not enough.
- The factual relationship status must be supported at the source-role bar. A global no-follow-up claim does not count unless the cited official document itself supports no comparable field or a comparable non-disclosure status.

Write one JSON object per line to `results_hkex_ai_disclosures.jsonl`:
{"item": { "stock_code": "<stock_code>", "issuer_name": "<issuer_name>", "disclosure_facet": "<disclosure_facet>", "claim_summary": "<claim_summary>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

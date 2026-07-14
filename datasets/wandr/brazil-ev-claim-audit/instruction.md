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

## `brazil_ev_claim_audit`

For at least 5+ claim families about Brazil fuel prices, Brazil electrified-vehicle context, BYD Dolphin Mini sales / rankings, BYD Dolphin Mini product-economy inputs, or BYD / We "Custa Pouco Rodar Muito" campaign artifacts in the February 22, 2026 through April 30, 2026 window, name 275+ canonical public factual claims per family; for each canonical claim and each of the 2 evidence roles described below, supply 1+ source URL.

This is a factual source-verification audit. Public claims are the starting point: repeated articles using the same agency, company, or brand language should be grouped under one canonical claim and treated as propagators, not as independent corroboration. Routine official data tables, price bulletins, model catalogs, rankings, and source hubs are normally verification or definition-context sources, not factories for hundreds of standalone public claims. They can count as `public_claim` only when the submitted canonical claim is genuinely the page's own public assertion, release, headline, methodology statement, campaign artifact, or explicitly highlighted data point being audited, not an ordinary row or cell harvested from a bulk table.

Claim families in scope:
- `fuel_price_context`: Retail or wholesale fuel-price claims, price-formation context, or energy-input claims tied to Brazil.
- `vehicle_sales_ranking`: BYD Dolphin Mini or related Brazil vehicle sales, retail ranking, emplacamento, Q1, monthly, or YTD claims.
- `ev_market_context`: Brazil electrified, BEV, PHEV, HEV, share, geography, or market-definition claims used as context.
- `product_economy_inputs`: BYD Dolphin Mini product, autonomy, battery, consumption, electricity-cost, or cost-equivalence inputs.
- `campaign_artifact`: Money, Milionarios, R$0.80/liter activation, cupom fiscal, agency credit, timing, location, or campaign-artifact claims.
- `commercial_offer`: Adjacent BYD offer or promotion claims that are publicly tied to the same date window or claim family.
- `fragile_signal`: Optional fragile public-signal claims such as Google Trends, social posts, award/case status, or no-durable-source findings.

Evidence roles:
- `public_claim`: A public source or artifact that makes, republishes, or visibly propagates the canonical factual claim as a public claim surface, not routine table/catalog mining.
- `verification_source`: The strongest available source found for checking, qualifying, contradicting, or status-labeling that same claim with a meaningfully distinct basis.

Strong verification sources often include official government or industry data, company-owned pages for company/product claims, dated technical PDFs, campaign trade press, general press, agency or brand-owned surfaces, and fragile public surfaces when their checked date and limitations are clear. Press can prove that a public claim was made or propagated; it should not be treated as independent primary evidence for a numeric fact when it is only repeating company or agency language.

Definitions matter: preserve distinctions such as gasoline C retail vs gasoline A wholesale, retail vs total emplacamentos, BEV vs broader electrified vehicles, PBEV or other autonomy bases, national vs city/state geography, electricity tariff class/date, dynamic offer pages, and indexed rather than raw search-volume data.

Requirements:
- The page must anchor the submitted canonical claim for the submitted `evidence_role`: `public_claim` pages publicly state or propagate the claim as a claim surface, not merely expose a reusable table row or catalog cell; `verification_source` pages check, qualify, contradict, or status-label the same underlying factual claim rather than merely mention the topic.
- The page must fit the submitted evidence role and support a defensible source-strength judgment, including whether it is official data, a company or agency claim, trade press, general press, social or dynamic evidence, repeated copy, estimate-only evidence, a no-primary-source finding, a conflict, or a stronger primary verification source. If the same URL or same source family is used across both evidence roles for a canonical claim, the `verification_source` role must add a meaningfully distinct check, qualification, contradiction, explicit status label, source-lineage label, or definition/methodology limitation; it must not simply mirror the public-claim basis.
- The page must localize the claim with the relevant value, unit, date or window, geography or scope, and definition or methodology when those are available; when they are absent, dynamic, stale, or methodologically unclear, the source must support that limitation rather than silently converting it into an exact fact.
- The submission must stay within factual audit evidence: no campaign-causality conclusion, ROI / AVE endorsement, investment advice, vehicle-buying advice, policy advice, creative-strategy recommendation, or unsupported campaign-effect claim.

Write one JSON object per line to `results_brazil_ev_claim_audit.jsonl`:
{"item": { "claim_family": "<claim_family>", "canonical_claim": "<canonical_claim>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

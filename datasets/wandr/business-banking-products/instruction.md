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

## `business_banking_products`

For at least 30+ providers of U.S.-oriented business-banking or fintech banking products, name 1+ public product / plan per provider and cover at least 6 evidence facets for each product or plan, with 1+ source URL per facet.

The work is a public provenance atlas, not a recommendation list. Found is a useful calibration example, but the provider set should range across business checking, startup banking, freelancer / self-employed banking, SMB operating accounts, and similar products from fintechs or banks. Consumer-only fintechs, lending-only products, payroll/accounting tools without a banking product, and generic software integrations do not count.

Evidence facets:
- `product_feature`: provider-owned product, help, legal, or app-platform pages that state a concrete capability, packaging claim, feature availability, or feature caveat.
- `pricing_fee`: provider-owned pricing, fee-schedule, account-agreement, terms, or legal pages. Third-party reviews can mention prices only under `independent_review`, not as pricing truth.
- `rate_or_yield`: provider-owned rate/APY/yield/legal pages. Third-party restatements and customer comments do not carry the rate truth.
- `eligibility_limit`: provider-owned product/help/terms/legal pages carrying eligibility, geography, business-type, plan-availability, or transaction-limit evidence.
- `bank_disclosure`: provider-owned legal or disclosure pages carrying partner-bank, FDIC, sweep/program-bank, card-issuer, not-a-bank, or pass-through-insurance language. Regulatory/bank pages can support bank identity, but a bank identity page alone does not prove the provider-product relationship.
- `app_platform`: Apple App Store, Google Play, or comparable platform pages for app packaging, developer identity, platform feature descriptions, ratings, review counts, version history, or platform-visible disclosures.
- `independent_review`: independent review, press, trade, or editorial pages for reviewer framing, public interpretation, noted strengths/limits, or source-visible tensions.
- `customer_sentiment`: app reviews, Trustpilot-like surfaces, marketplace reviews, or other customer-review pages for customer-observable sentiment only.

Each finding should preserve the source-stated claim or datum, the broad source role, a visible source date / effective date / version date when one exists or a checked / undated state when it does not. Checked dates are observation metadata, not page-effective dates. Missing, conflict, superseded, own-source-only, or aggregator-discovery caveats should be used only when the source actually supports them. Public roundups, competitor comparison pages, vendor guides, directories, and sponsor-bank maps may help discover providers, but they should not carry core product, pricing, fee, APY, legal, or bank-relationship facts unless the row is explicitly about their independent-review or discovery-source framing.

Requirements:
- The page must clearly identify the submitted provider.
- The page must tie the submitted product / plan to a business-banking, business-account, or fintech banking product from that provider.
- The page must make its facet-appropriate source role visible.
- The page must state a concrete product fact, datum, disclosure, caveat, platform signal, review framing, or customer-observable theme scoped to the submitted facet.
- The finding must stay factual and source-stated, with any date, source-state, missing/conflict/superseded caveat, or support limitation grounded in the cited source rather than inferred from private documents, recommendations, rankings, SWOT, investment analysis, risk scores, outreach/contact data, lead scoring, or competitive advice.

Write one JSON object per line to `results_business_banking_products.jsonl`:
{"item": { "provider": "<provider>", "product_plan": "<product_plan>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

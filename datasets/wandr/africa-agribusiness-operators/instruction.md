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

## `africa_agribusiness_operators`

For 50+ commercially significant African agribusiness operators or operating systems, supply public-source provenance for each of the 3 evidence axes below, with 1+ source per operator-axis pair. The result is public evidence provenance for agribusiness operating systems, not investment advice, deal recommendation, operator ranking, valuation, lead scoring, procurement recommendation, credit decision, policy advice, causal GDP or technology-impact claim, market forecast, outreach, or contact enrichment.

Include Francophone West/Central Africa, Morocco, and other French-language source surfaces where public sources support them.

Evidence axes:
- `operating_control`: the source shows what agribusiness bottleneck the operator controls, such as finance, insurance, input distribution, farmer services, storage, warehouse receipts, logistics, cold chain, quality/compliance, traceability, mechanization, market access, production/processing, or exchange/market infrastructure.
- `independent_scale_or_footprint`: the source states a concrete scale or footprint signal, such as farmers served, hectares or acres, tonnes processed/traded/stored, warehouse capacity, transaction volume, countries served, facilities, borrowers, insured farmers, or another source-stated operating scale.
- `capital_or_economics_provenance`: the source states capital, funding, audited revenue/profit/margin, DFI investment amount, loan size, repayment/default metric, transaction value, warehouse-receipt finance value, or a similar source-stated economics/capital signal. Market size, valuation, growth narrative, and inferred estimates do not count.

Use source-class labels from this closed set when characterizing a source: `audited_or_regulated_filing`, `dfi_or_institutional_disclosure`, `exchange_wrs_or_public_dataset`, `annual_or_integrated_report`, `investor_or_accelerator_disclosure`, `reputable_press`, `official_operator_page`.

Use control-point labels from this closed set: `finance_credit_insurance`, `input_distribution_or_farmer_services`, `storage_or_warehouse_receipts`, `exchange_or_market_infrastructure`, `logistics_or_cold_chain`, `quality_traceability_or_compliance`, `mechanization_services`, `integrated_production_processing_or_market_access`.

When a submission makes a scale, capital, or economics claim, use metric-kind labels from this closed set: `farmer_or_user_count`, `hectares_or_acres`, `tonnes_or_volume`, `warehouse_or_facility_capacity`, `transaction_or_trade_value`, `funding_or_investment_amount`, `audited_revenue_or_profit`, `loan_repayment_default_or_payout`, `country_or_facility_footprint`, `other_source_stated_scale`.

The source should also make clear the countries, source date or year, and the specific claim being supported. A pre-2023 source can support historical existence or historical capital, but current scale or economics claims need a current or clearly dated source. Conflicting evidence should be surfaced as conflict or insufficiency rather than resolved by invention.

Source bars are strict. Audited financial statements, regulator filings, listed-company reports, annual or integrated reports, DFI and institutional disclosures, commodity exchange or warehouse-receipt records, public datasets, named investor disclosures, and reputable press can support the appropriate axes when they state the claim directly. Official operator pages can support `operating_control` and sometimes direct company-stated footprint, but they do not validate revenue, profitability, margin, repayment/default, or independent scale by themselves unless they are audited or regulated annual-report-equivalent pages.

Aggregator and business-intelligence profiles, startup databases, generic startup listicles, social posts, lead-generation pages, broad market reports, market-size forecasts, and policy narratives are discovery leads only. They do not validate record-level financial metrics, revenue, profitability, margin, loan performance, current scale, or operator economics unless the cited page itself quotes and links a qualifying source.

Requirements:
- The page must identify the named operator or system and tie it to Africa-specific agribusiness operations, countries, or facilities.
- The page must show that the operator controls a real agribusiness bottleneck matching the submitted control point.
- The page must directly support the submitted evidence axis with a focused, source-stated claim for that operator; generic page existence, generic company descriptions, repeated boilerplate excerpts, or one URL reused for several unsupported axes do not count.

Write one JSON object per line to `results_africa_agribusiness_operators.jsonl`:
{"item": { "operator": "<operator>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

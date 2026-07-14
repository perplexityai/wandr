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

## `sales_tax_economic_nexus`

For each of the 45+ US states with a statewide sales tax, supply 4 concrete current-rule findings on the state's economic-nexus or remote-seller collection rule: one with `rule_facet=dollar_threshold`, one with `rule_facet=transaction_threshold_logic`, one with `rule_facet=measurement_period`, one with `rule_facet=threshold_sales_basis`. `rule_facet` must be exactly one of `dollar_threshold`, `transaction_threshold_logic`, `measurement_period`, `threshold_sales_basis`, with the following meanings:

- `dollar_threshold`: the current dollar threshold amount that triggers a remote-seller or marketplace-facilitator economic-nexus obligation under the state's statewide sales/use tax.
- `transaction_threshold_logic`: whether the current rule has a separate transaction-count threshold, has no transaction-count threshold at all (including cases where one was removed post-Wayfair), or uses a dual threshold; if dual, the finding must distinguish OR-style and AND-style stringency rather than merely reciting two numbers.
- `measurement_period`: the lookback period used to measure the threshold, such as previous and/or current calendar year, preceding twelve calendar months, immediately preceding four sales-tax quarters, or previous calendar year only.
- `threshold_sales_basis`: the sales base used for threshold measurement, such as retail sales, taxable remote sales, gross receipts, gross revenue, gross sales, tangible personal property and services, or gross proceeds — distinctions that produce materially different rules.

The reported finding under each facet should be a concise current-rule proposition — for instance a specific dollar amount, the absence-or-presence of a transaction-count threshold along with its OR / AND stringency if dual, the lookback wording ("previous calendar year", "preceding twelve calendar months", "immediately preceding four sales-tax quarters", etc.), or the sales-basis wording ("retail sales", "taxable remote sales", "gross receipts", "gross revenue", "gross sales", and so on).

Source evidence comes from the state's own tax authority — its Department of Revenue, Tax Department, Comptroller, Board of Equalization or equivalent — from its statute / regulation / administrative-code text, or from state-specific Streamlined Sales Tax Governing Board remote-seller materials. Aggregator matrices and tax-service-provider summaries, such as Avalara, Sovos, TaxJar, Sales Tax Institute, CPA / law-firm alerts, and similar, do not authoritatively source the rule.

Each row supplies a source URL (1+ per finding) on a page authoritatively substantiating the state's economic-nexus or remote-seller collection rule.

States in scope:

- **Alabama** (also written as: AL)
- **Arizona** (also written as: AZ)
- **Arkansas** (also written as: AR)
- **California** (also written as: CA)
- **Colorado** (also written as: CO)
- **Connecticut** (also written as: CT)
- **Florida** (also written as: FL)
- **Georgia** (also written as: GA)
- **Hawaii** (also written as: HI)
- **Idaho** (also written as: ID)
- **Illinois** (also written as: IL)
- **Indiana** (also written as: IN)
- **Iowa** (also written as: IA)
- **Kansas** (also written as: KS)
- **Kentucky** (also written as: KY)
- **Louisiana** (also written as: LA)
- **Maine** (also written as: ME)
- **Maryland** (also written as: MD)
- **Massachusetts** (also written as: MA)
- **Michigan** (also written as: MI)
- **Minnesota** (also written as: MN)
- **Mississippi** (also written as: MS)
- **Missouri** (also written as: MO)
- **Nebraska** (also written as: NE)
- **Nevada** (also written as: NV)
- **New Jersey** (also written as: NJ)
- **New Mexico** (also written as: NM)
- **New York** (also written as: NY, N.Y.)
- **North Carolina** (also written as: NC, N.C.)
- **North Dakota** (also written as: ND, N.D.)
- **Ohio** (also written as: OH)
- **Oklahoma** (also written as: OK)
- **Pennsylvania** (also written as: PA)
- **Rhode Island** (also written as: RI, R.I.)
- **South Carolina** (also written as: SC, S.C.)
- **South Dakota** (also written as: SD, S.D.)
- **Tennessee** (also written as: TN)
- **Texas** (also written as: TX)
- **Utah** (also written as: UT)
- **Vermont** (also written as: VT)
- **Virginia** (also written as: VA)
- **Washington** (also written as: WA, Washington State)
- **West Virginia** (also written as: WV, W.Va.)
- **Wisconsin** (also written as: WI)
- **Wyoming** (also written as: WY)

Requirements:
- The page concerns the state's statewide sales/use tax economic nexus, remote-seller collection rule, or marketplace-facilitator economic-nexus rule — not adjacent classes such as physical-presence-only nexus, income / franchise tax nexus, sales-tax-rate pages, or local-only sales-tax content.
- The page is on the state's own tax authority, in the state's statute / regulation / administrative-code text, or on state-specific Streamlined Sales Tax Governing Board remote-seller material.
- The page substantively supports the concrete current-rule finding under the claimed facet. Similar-looking facets are not interchangeable: gross receipts are not retail sales, previous / current calendar year is not the immediately preceding four sales-tax quarters, and a marketplace-provider rule is not automatically the remote-seller rule.
- The page presents the finding as the current rule as of May 7, 2026. Pre-Wayfair-era thresholds and superseded transaction-count thresholds presented as currently operative do not count.

Write one JSON object per line to `results_sales_tax_economic_nexus.jsonl`:
{"item": { "state": "<state>", "rule_facet": "<rule_facet>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

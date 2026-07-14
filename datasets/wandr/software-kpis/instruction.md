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

## `software_kpis`

For 10+ companies from the closed company list below, cover all 8 fiscal periods and at least 2+ operational KPI axes per fiscal period, with 1+ issuer-published or SEC-hosted source URL for each company-period-axis combination.

The metric evidence is useful only when it can be traced to the issuer's own period language. Canonical `fyYYYY_qN` labels may represent the issuer's source-stated period label, including forms such as `Second Quarter 2024`, `Q2 2024`, or `second quarter ended June 30, 2025`, but a publication date alone is not enough. Calendar-quarter inference does not establish a fiscal label.

Closed software-company list:
- `elastic`: Elastic, Elastic N.V., ESTC
- `sprout_social`: Sprout Social, Sprout Social Inc., SPT
- `commerce_com_bigcommerce`: Commerce.com, BigCommerce, BigCommerce Holdings, BigCommerce Holdings Inc., BIGC, Commerce.com BigCommerce
- `weave`: Weave, Weave Communications, Weave Communications Inc., WEAV
- `blend_labs`: Blend, Blend Labs, Blend Labs Inc., BLND
- `bill_holdings`: BILL, BILL Holdings, BILL Holdings Inc., Bill.com, Bill.com Holdings
- `gitlab`: GitLab, GitLab Inc., GTLB
- `appian`: Appian, Appian Corporation, APPN
- `blackline`: BlackLine, BlackLine Inc., BL
- `workiva`: Workiva, Workiva Inc., WK
- `commvault`: Commvault, Commvault Systems, Commvault Systems Inc., CVLT
- `certara`: Certara, Certara Inc., CERT
- `schrodinger`: Schrodinger, Schrodinger Inc., SDGR

Fiscal-period labels:
- `fy2024_q1`: examples include FY2024 Q1, Fiscal 2024 Q1, Q1 FY2024
- `fy2024_q2`: examples include FY2024 Q2, Fiscal 2024 Q2, Q2 FY2024
- `fy2024_q3`: examples include FY2024 Q3, Fiscal 2024 Q3, Q3 FY2024
- `fy2024_q4`: examples include FY2024 Q4, Fiscal 2024 Q4, Q4 FY2024
- `fy2025_q1`: examples include FY2025 Q1, Fiscal 2025 Q1, Q1 FY2025
- `fy2025_q2`: examples include FY2025 Q2, Fiscal 2025 Q2, Q2 FY2025
- `fy2025_q3`: examples include FY2025 Q3, Fiscal 2025 Q3, Q3 FY2025
- `fy2025_q4`: examples include FY2025 Q4, Fiscal 2025 Q4, Q4 FY2025

Metric axes:
- `revenue_or_revenue_growth`: Quarterly or fiscal-period revenue, or a source-stated revenue growth rate.
- `retention_or_expansion_rate`: Net revenue retention, dollar-based net retention, expansion, renewal, or comparable retention rate.
- `customer_cohort_or_arr_threshold`: Customer counts or cohorts defined by ARR, ACV, subscription value, spend, seats, or comparable issuer thresholds.
- `committed_revenue_or_backlog`: Remaining performance obligations, current RPO, committed ARR, backlog, subscription backlog, or comparable committed revenue.
- `headcount_or_employee_count`: Employee count or headcount, including fiscal-year-end headcount used for the issuer's fourth fiscal quarter.

Requirements:
- The source must be issuer-published or SEC-hosted primary material: shareholder letter, earnings release, annual or quarterly report, 10-K, 10-Q, 8-K exhibit, investor presentation, or issuer-hosted/SEC-hosted transcript. Market-data aggregators, analyst notes, trade press, third-party transcript sites, press-wire republications away from the issuer or SEC, and current careers pages do not count.
- The page must identify the claimed issuer. BigCommerce, BIGC, and Commerce.com references can count for `commerce_com_bigcommerce` when the source itself establishes that issuer identity.
- The page must state the claimed fiscal period label, quarter/year, or year-end fiscal label for a fourth-quarter employee/headcount record. A publication date or calendar quarter is not enough by itself.
- The page must state a metric that belongs to the claimed axis and must state the exact KPI value, rate, threshold, count, backlog/RPO amount, or comparable figure being used. Calculated growth rates, retention rates, ARR thresholds, backlog, headcount, or normalized metrics do not count unless the source states that figure.

Write one JSON object per line to `results_software_kpis.jsonl`:
{"item": { "software_company": "<software_company>", "fiscal_period": "<fiscal_period>", "metric_axis": "<metric_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

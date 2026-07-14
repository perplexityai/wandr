You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `semiconductor_financial_deep_dive`
  - `semiconductor_financial_deep_dive.analysis_angles`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `semiconductor_financial_deep_dive`

For each of the 6 companies below, supply fiscal-quarter financial claims for 8+ quarters per company, limited to period ends from 2024-05-01 through 2026-05-12, supplying a source (1+ URL per company-quarter claim). A qualifying source visibly anchors the quarter and the claimed values on the page itself; floating quote widgets, annual-only summaries, and forward-looking guidance do not by themselves qualify as quarterly historical financial evidence.

Companies in scope:
- **Amkor Technology** (also known as: AMKR, Amkor, Amkor Technology, Inc.)
- **Photronics** (also known as: PLAB, Photronics, Inc.)
- **Celestica** (also known as: CLS, Celestica Inc., Celestica International LP)
- **ASE Technology** (also known as: ASX, ASEH, ASE Technology Holding, ASE Technology Holding Co., Ltd.)
- **Fabrinet** (also known as: FN, Fabrinet Ordinary Shares)
- **Onto Innovation** (also known as: ONTO, Onto, Onto Innovation Inc.)

The claim names the fiscal-quarter label, period-end date, and quarterly financial values.

Requirements:
- The page must identify the claimed company and the claimed fiscal quarter or period-end date.
- The page must state the claimed quarterly financial values for that same period: revenue or net sales, supplied profitability values such as operating income or net income, and supplied free-cash-flow or cash-flow/capex values.

Write one JSON object per line to `results_semiconductor_financial_deep_dive.jsonl`:
{"item": { "company": "<company>", "fiscal_quarter": "<fiscal_quarter>", "period_end": "<period_end>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `semiconductor_financial_deep_dive.analysis_angles`

Cross-tasknode identifier discipline: this task is for the same {= company =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For each of the {= company =} companies below, supply a dated investor-analysis finding for every analysis angle below: 1+ finding for each company-angle combination, supplying a source (1+ URL per finding). A qualifying source visibly ties the finding to source dates or source-stated periods from 2024-01-01 through 2026-05-12 by source publication / call / filing / transaction / snapshot date, or by another source-stated reporting-period anchor, and carries the claimed investor-analysis evidence itself. Forward guidance can qualify when that source-side anchor is in-window even if the guided quarter extends beyond the window.

Companies in scope:
- **Amkor Technology** (also known as: AMKR, Amkor, Amkor Technology, Inc.)
- **Photronics** (also known as: PLAB, Photronics, Inc.)
- **Celestica** (also known as: CLS, Celestica Inc., Celestica International LP)
- **ASE Technology** (also known as: ASX, ASEH, ASE Technology Holding, ASE Technology Holding Co., Ltd.)
- **Fabrinet** (also known as: FN, Fabrinet Ordinary Shares)
- **Onto Innovation** (also known as: ONTO, Onto, Onto Innovation Inc.)

Analysis angles:
- **margin_trend**: gross, operating, net, EBITDA, or adjusted-margin movement over a dated period
- **liquidity_leverage**: cash, debt, current ratio, debt-to-equity, interest coverage, credit facility, or balance-sheet capacity
- **ownership_flow**: institutional ownership, holder concentration, shareholder percentage, inflow / outflow, or 13F-style change
- **insider_activity**: director, executive, major-holder, or congressional transaction activity with transaction date and buy/sell signal
- **earnings_call_guidance**: management outlook, guidance range, KPI, beat / miss versus guide, or transcript language from a dated call
- **analyst_valuation**: valuation multiple, consensus rating, price target, forecast, or peer/history comparison from a dated market-data page
- **segment_economics**: segment, end-market, application, product-family, or customer-category revenue / margin economics
- **supply_chain_customer_exposure**: customer concentration, material supply, utilization, capacity, geographic footprint, bottleneck, or ramp exposure

The claim names a concise finding label, a source date or source-stated period, and the investor-analysis finding.

Requirements:
- The page must tie the finding to the named company and to the claimed dated period, transaction date, ownership snapshot, filing date, call date, or publication date.
- The page must substantively support the claimed analysis angle for that company.

Write one JSON object per line to `results_semiconductor_financial_deep_dive.analysis_angles.jsonl`:
{"item": { "company": "<company>", "analysis_axis": "<analysis_axis>", "finding_label": "<finding_label>", "source_date": "<source_date>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `neo_compensation`

For 60+ companies, and for each of the 2 fiscal years FY2024 and FY2025, extract official Summary Compensation Table evidence for 5+ named executive officers per company fiscal year, with 1+ official proxy source per executive-fiscal-year table row.

This is factual filing extraction only: companies should be public issuers with official DEF 14A/proxy filings, and the executive should be a named individual NEO for that company and fiscal year. SEC EDGAR filings are preferred; issuer-hosted proxies count only when visibly the same filed proxy. Secondary mirrors, finance summaries, filing-news pages, MarketScreener/Yahoo/PublicNow/StockTitan/Quartr-style pages, 10-Ks, director compensation tables, pay-versus-performance tables, and proxy narrative without the Summary Compensation Table row do not count.

Compensation advice, governance judgment, pay-fairness commentary, investment analysis, causal performance explanation, and executive profiling are out of scope.

Requirements:
- The page must communicate that the cited source is an official DEF 14A or proxy statement for the claimed company.
- The page must bind the Summary Compensation Table evidence to the claimed fiscal year, not merely to the proxy filing year.
- The page must show the Summary Compensation Table context and a usable table location.
- The page must identify the submitted executive as the named executive officer table row, including role or principal position when the table provides it.
- The page must show the exact compensation values in the submitted executive's Summary Compensation Table row: salary, bonus if present, stock awards, option awards, non-equity incentive plan compensation, all other compensation, total compensation, and any intermediate SCT columns the issuer includes.
- The page must preserve row/component footnote markers and explicit no-value states (0, dash, N/A, blank, not applicable, or excluded/comparability notes) needed to read that executive's row.

Write one JSON object per line to `results_neo_compensation.jsonl`:
{"item": { "company": "<company>", "fiscal_year": "<fiscal_year>", "executive_name": "<executive_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

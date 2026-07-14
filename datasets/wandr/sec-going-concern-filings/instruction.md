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

## `sec_going_concern_filings`

For 60+ SEC 10-K annual report filings covering fiscal years 2024 or 2025 whose financial statements or auditor's report raise substantial doubt about the registrant's ability to continue as a going concern, cover the 2 disclosure facets listed below for each filing by supplying a source (i.e. 1+ URL under each facet) which exposes a focused, substantive finding clearly scoped to the facet in question for that registrant.

The aim is to assemble a benchmarking corpus for auditors and financial analysts: a record, per filing, of the specific conditions that triggered the going-concern doubt and the specific plans management put forward to alleviate it, so that recurring conditions and mitigation strategies can be compared across registrants.

Disclosure facets:
- `going_concern_condition`: the specific financial conditions or events the filing identifies as raising substantial doubt — e.g. recurring operating losses, net losses, an accumulated deficit, negative working capital, negative operating cash flow, debt maturities or covenant breaches, or insufficient liquidity to fund operations for the next twelve months. The bar is descriptive: the page must attribute a concrete, named condition to this registrant as a basis for the doubt.
- `mitigation_plan`: management's specific stated plans to alleviate the substantial doubt — e.g. raising new equity or debt financing, refinancing or restructuring existing obligations, a contract or revenue pipeline, cost-reduction or restructuring measures, asset sales, or sponsor / parent support. The bar is strict: the page must state an action management intends to take, not merely a generic hope of "obtaining additional funding"; a bare assertion that the company will seek capital with no further specifics does NOT count.

The source must be a fully public, accessible page — the filing on the SEC's public archive, the registrant's own filed document, or another public surface that reproduces the relevant disclosure text — not a paywalled summary, a login-gated terminal, or a bare aggregator stub.

Requirements:
- The page must identify the registrant by a name or ticker that matches the filing and make clear it concerns a 10-K annual report (or its amendment). At least one quoted excerpt must itself name the registrant — a cover, title, or header line carrying the entity name (or its ticker / former name); a numeric or CIK-only document URL does not supply the registrant name, so quote the name line that sits alongside the finding.
- The page must show that this filing raises substantial doubt about the registrant's ability to continue as a going concern — through going-concern wording, an auditor's going-concern paragraph, or an explicit management going-concern note — not merely general risk-factor language about needing capital.
- The page must expose a finding scoped to the row's `disclosure_facet`, met at the bar appropriate to that facet per the definitions above. For `going_concern_condition`, a concrete named condition tied to this registrant as a basis for the doubt; for `mitigation_plan`, a specific action management states it intends to take to alleviate the doubt, not a generic capital-raising platitude.

Write one JSON object per line to `results_sec_going_concern_filings.jsonl`:
{"item": { "filing": "<filing>", "disclosure_facet": "<disclosure_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

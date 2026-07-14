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

## `clm_offering_evidence`

For 70+ public CLM, contract-management, agreement-management, legal-operations, e-signature/CLM-suite, or adjacent document-workflow software offerings, cover each of the 4 evidence axes below by supplying a public source (i.e. 1+ URL per offering and axis).

Name the vendor and the specific product or platform line the source supports. Company-wide pages can support `trust`, and sometimes `integrations`, when the page clearly applies to the offering's company or agreement-management platform; `pricing` and `capabilities` need to apply to the claimed offering or platform, not an unrelated sibling product.

Evidence axes:
- `pricing`
- `capabilities`
- `integrations`
- `trust`

The work is public software-evidence provenance. It is not a vendor ranking, procurement recommendation, buyer guide, legal advice, contract-drafting advice, roadmap analysis, gap analysis, review-sentiment score, lead list, or outreach task.

For each source, state a concise finding and include the source class, pricing state when the axis is `pricing`, any source-stated target segment, source date when visible, checked date, confidence, and notes for aliases, rebrands, acquisition context, or source-limited uncertainty.

Requirements:
- The page must clearly identify the submitted vendor and product or platform line in a contract, agreement, legal-operations, e-signature, or document-workflow context.
- The page must have the source role required by `evidence_axis`: official pricing/plan/quote/demo/commercial pages for `pricing`; official product, docs, help, case-study, changelog, or substantive official-release pages for `capabilities`; official integrations, API, partner, marketplace, docs, or help pages for `integrations`; and official security, trust, privacy, compliance, certification, status, or substantive security/compliance sections for `trust`.
- The page must contribute concrete source-stated evidence for the declared axis: public price or quote/contact-sales pricing language; CLM/contract/document-workflow capabilities; named integrations, API, partner, or ecosystem support; or security, privacy, compliance, certification, uptime/status, or comparable trust evidence.
- The submitted finding should stay source-stated and source-scoped: no vendor rankings, recommendations, review sentiment, legal/procurement advice, roadmap/gap claims, competitor weakness claims, or global absence claims from a single page.

Write one JSON object per line to `results_clm_offering_evidence.jsonl`:
{"item": { "vendor": "<vendor>", "product_or_platform": "<product_or_platform>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

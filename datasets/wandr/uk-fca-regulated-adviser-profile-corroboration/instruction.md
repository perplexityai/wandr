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

## `uk_fca_regulated_adviser_profile_corroboration`

For 48+ firms, name 2+ current advisers per firm; for each adviser-firm pair and each of the 2 evidence checks below, supply an evidence source (i.e. 1+ URL).

The evidence checks of interest, which we refer to as `evidence_axis`, are:
- `fca_current_status`: a direct FCA Register individual page for the adviser, using the canonical `https://register.fca.org.uk/s/individual?id=...` form or an equivalent official FCA individual record page that visibly renders the same person record.
- `firm_profile_role`: a firm-owned or officially controlled person profile, adviser page, planner page, team page, or comparable firm surface for the same adviser.

Firms should be UK financial advice, wealth planning, financial planning, or comparable advice practices. Current appointed-representative and principal-firm relationships count when the FCA source and the firm-owned source together bind the same adviser to the current advice role at the claimed firm or trading style. Use the stable direct FCA individual URL or a visible public FCA reference to disambiguate the adviser; person names alone are not enough. Current means current at the time the source is checked: history-only FCA records, no-current-role records, no-longer-authorised relationships, and stale firm profiles do not count unless current role evidence is separately visible. Search results, snippets, raw FCA shell pages, pages containing only `Loading` / `CSS Error` / `Refresh` shell text, commercial directories, review or matching marketplaces, LinkedIn, contact-only pages, and lead-generation pages are discovery leads only.

Firm-owned pages may contain email, phone, review, rating, booking, awards, or marketing material, but the evidence of interest is only professional identity, firm relationship, and adviser/planner role. Contact details, contact forms, review scores, ratings, matching prompts, rankings, recommendation or suitability claims, and outreach hooks do not count as evidence.

Requirements:
- The page must identify the claimed adviser as the same person, with enough page context to distinguish same-name people.
- The page must tie that adviser to the claimed firm, trading style, appointed representative, or principal-firm relationship.
- The page must provide the evidence required by `evidence_axis`: current FCA Register/Directory status, role, approval, certification, assessment, or current roles-and-activities language for `fca_current_status`; current adviser, financial adviser, planner, financial planner, wealth planner, or comparable advice-role language for `firm_profile_role`.

Write one JSON object per line to `results_uk_fca_regulated_adviser_profile_corroboration.jsonl`:
{"item": { "firm": "<firm>", "adviser_name": "<adviser_name>", "fca_person_url_or_reference": "<fca_person_url_or_reference>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

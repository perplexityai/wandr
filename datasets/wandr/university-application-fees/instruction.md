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

## `university_application_fees`

For 20+ degree-granting higher education institutions in each of the 6 destination markets below, supply current or upcoming application fee facts for international applicants or for all-applicant routes visibly open to international applicants (1+ per institution), with 1+ official URLs per fee scope.

Universities, colleges, institutes, and comparable tertiary institutions count when they award degrees and are admissions targets in the submitted market.

Destination markets in scope:
- **Canada**: degree-granting higher education institutions in Canada, including official provincial application service routes when tied to a submitted institution and scope
- **United States**: degree-granting universities and colleges in the United States, including official institution pages that route through Common App, Coalition, or campus systems
- **United Kingdom**: degree-granting higher education institutions in England, Scotland, Wales, or Northern Ireland, including institution-owned pages that route through UCAS or graduate systems
- **Continental Europe**: degree-granting higher education institutions in Europe outside the United Kingdom, including official national or institutional application service routes tied to the submitted institution and scope
- **Australia and New Zealand**: degree-granting higher education institutions in Australia or New Zealand, including official institutional pages for international or all-applicant application routes
- **East and Southeast Asia**: degree-granting higher education institutions in East Asia or Southeast Asia, including Hong Kong, Singapore, Japan, South Korea, Taiwan, and similar destination markets

Each fee fact must name the institution, the applicant category, and the degree, program, or application route. Applicant categories can be explicitly international/non-domestic, or an all-applicant route that is visibly open to international applicants; domestic-only, resident-only, in-state, or citizen-only scopes do not count. The fee state must be current or upcoming on the live official page, not an obsolete historical schedule.

Eligible URLs are official institution-controlled admissions, graduate, bursar, fee, or application pages; official institutional PDFs or fee schedules; or official application service pages that tie the fee state to the submitted institution and scope. Generic portal fee pages count only when they make that institution/scope tie, and each URL must carry the institution, scope, and fee evidence by itself. Unofficial aggregators, agency advice pages, visa-fee pages, tuition-only pages, deposit pages, housing-charge pages, and general affordability advice are out of scope.

Fee facts may be charged fees, explicit no-fee statements, or scoped waiver/exemption facts. Absence of a fee on an application page is not evidence of a free or waived application.

Requirements:
- The page must identify the submitted institution and the claimed applicant category plus degree, program, or application route; the scope must be explicitly international/non-domestic or an all-applicant route that includes international applicants.
- The page must state the claimed current or upcoming application fee state for that scope: amount and currency for a charged fee, or explicit no-fee, waiver, or exemption language, plus any visible application cycle, term, or effective period attached to the fee statement.
- The page must frame the claimed fee state, whether a charged fee, no-fee state, waiver, or exemption, as an application, admissions processing, or application service fee for applying to the submitted institution/scope, not as tuition, enrollment deposit, visa charge, housing charge, standardized-test fee, or general affordability advice.

Write one JSON object per line to `results_university_application_fees.jsonl`:
{"item": { "destination_market": "<destination_market>", "university": "<university>", "applicant_category": "<applicant_category>", "degree_or_program_scope": "<degree_or_program_scope>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

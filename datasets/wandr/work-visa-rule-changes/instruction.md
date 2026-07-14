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

## `work_visa_rule_changes`

Build a table covering 12+ immigration-rulemaking jurisdictions, with 5+ dated rule-change events per jurisdiction for employer, sponsored, skilled, temporary, or other work-authorisation routes. Each event needs an official announcement, publication, update, or effective-date signal inside 1 January 2024 through 17 June 2026 inclusive. For each event, assign a change-category label (1+ per event) from the list below and supply both 2 official source roles, with 1+ URL for each role.

This is an operations audit of official dated changes, not legal advice and not a table of current work-visa rules. For each row, report a concise before/after or current/new effect summary and `checked_date`, the official date signal inside the target period. `effective_date` is the operative, commencement, implementation, or future effective date for the rule change when the official source states or clearly implies one; if no operative date is stated or clearly implied, use `not stated` rather than reusing a publication or update date.

Change-category labels:
- `application_document_or_process`: application documents, filing channel, evidence timing, form, certificate, or process requirements
- `eligibility_or_occupation`: worker eligibility, occupation-list coverage, skill level, qualification, experience, language, or route access
- `fee_or_processing`: official fee, processing service standard, processing priority, or comparable official case-handling parameter
- `route_launch_or_closure`: launch, replacement, suspension, closure, renamed route, or major route-status transition
- `salary_or_wage_threshold`: salary, wage, income, going-rate, maintenance, or financial threshold
- `sponsor_or_employer_duty`: sponsor, employer, accreditation, job-check, compliance, reporting, or labour-market-test duty
- `visa_duration_or_stay_limit`: maximum stay, visa validity, extension, renewal, cooling-off, dependent access, or transition-period duration

Official source roles:
- `change_instrument`: official legal instrument, gazette, Federal Register-like rule, statement of changes, formal notice, department announcement, or change log that states the rule movement and date
- `implementation_guidance`: official route page, implementation guidance, policy manual, fee table, occupation list, application guide, or comparable operational page showing the resulting rule or transitional effect

Official sources only: government immigration, labour, home-affairs, foreign-affairs, ministry, official gazette, parliamentary, or regulator-controlled pages count. Third-party immigration firms, law firms, relocation vendors, news outlets, Wikipedia, uncontrolled social posts, and scraped aggregator pages do not count even when they accurately summarize an official change.

Future-effective changes count when `checked_date` is inside 1 January 2024 through 17 June 2026 inclusive and the page states the future `effective_date`. A page that only states a current rule without a dated change, implementation date, update history, or transition framing does not count.

Requirements:
- The page must tie the record to the named jurisdiction, work program, and affected rule topic for an employer/work-authorisation route.
- The page must fit the submitted `source_role`: `change_instrument` sources state the official change event itself; `implementation_guidance` sources show the resulting operative rule or transitional effect for applicants, workers, employers, or sponsors.
- The page must expose an official announcement, publication, update, or effective-date signal usable as `checked_date` inside the target period and support the submitted `effective_date` as the rule's operative, commencement, implementation, or future effective date when the source states or clearly implies one.
- The page must substantively support the submitted `change_category` and claimed rule effect, with enough detail to distinguish the rule movement from generic route background.

Write one JSON object per line to `results_work_visa_rule_changes.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "work_program": "<work_program>", "change_event": "<change_event>", "effective_date": "<effective_date>", "change_category": "<change_category>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

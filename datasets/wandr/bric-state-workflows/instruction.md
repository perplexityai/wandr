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

## `bric_state_workflows`

For 35+ U.S. state, territory, or DC jurisdictions with official public guidance for the FY 2024/2025 FEMA Building Resilient Infrastructure and Communities (BRIC) funding round, cover each of the 3 marker kinds listed below. For every jurisdiction and marker kind, name one concrete state-specific `workflow_marker` and supply 2+ official jurisdiction URLs that each independently support that same marker.

This task is about the state and territory implementation layer below FEMA: local letters of interest, notices of intent, preapplications, state FEMA GO submission dates, state-to-FEMA submission timing, state review or ranking steps, local portal steps, technical-issue notice timing presented in a local application timeline, FY 2024 pending-subapplication migration/revision/withdrawal instructions, and local funding-methodology or eligibility/process rules.

The marker kinds, reported exactly as `marker_kind`, are:
- `intake_path`: local applicant intake or subapplicant action before state review, such as an LOI, NOI, preapplication, invited materials deadline, local FEMA GO packet due date, or required intake portal step.
- `state_review_path`: state review, ranking, selection, revision, or state-to-FEMA submission handling after local intake, including review deadlines and state submission timing.
- `rules_or_transition`: a BRIC-specific process rule, funding methodology, eligibility condition, procurement/applicant rule, technical-issue notice rule, or FY 2024 pending-subapplication migration, revision, resubmission, or withdrawal instruction.

Keep the key roles distinct: `jurisdiction` is the state, territory, or DC name; `marker_kind` is one of the category labels above; `workflow_marker` is the concrete marker text; and each supporting source remains the row URL with excerpts. Do not rename the marker text as `marker_label`, `label`, or `title`.

The `workflow_marker` wording should be concrete and should fit the submitted `marker_kind`. Date-bearing markers should make clear what kind of date is being named. A bare federal close date, a state page that only repeats the federal close date, or a date label with no local workflow context is not enough. Non-date markers should make clear what local process, transition, funding, eligibility, applicant-scope, or procurement rule is being named.

The two URLs under the same `workflow_marker` are corroboration, not split evidence: each URL must by itself support the jurisdiction, FY 2024/2025 BRIC cycle, marker kind, marker detail, and local workflow function. Use distinct official pages or documents rather than duplicate anchors, print views, mirrors, or a generic homepage paired with a detail source. Across a jurisdiction, avoid letting one BRIC homepage, timeline table, NOFO, or webinar deck carry all three marker kinds unless separate cited pages or self-contained document sections genuinely provide independent marker evidence.

Official state, territory, or DC emergency-management, homeland-security, grant-office, governor, administrative-register, webinar deck, state NOFO, fact sheet, funding announcement, and comparable public-agency sources can count. Federal FEMA, Simpler.Grants.gov, Grants.gov, federal NOFO, and generic FEMA GO pages can orient the cycle, but they do not satisfy a state-specific marker by themselves. Private summaries, consultant pages, grant-writing portals, social posts, municipal mirrors, pages that only repeat the federal July 23, 2026 close date, generic application advice, and portal login/status pages do not count.

The cited page or section should naturally fit the submitted marker kind. Intake rows need applicant-facing intake, NOI/LOI, preapplication, invited-materials, or portal-entry evidence. State-review rows need review, ranking, revision, selection, state FEMA GO handling, or state-to-FEMA submission evidence. Rules-or-transition rows need a real BRIC process rule, funding method, eligibility/applicant/procurement condition, technical-issue notice rule, or FY 2024 pending-subapplication transition instruction, not just another date from a timeline.

Requirements:
- The page must place the cited guidance in the FY 2024/2025 FEMA BRIC round. BRIC/FMA or HMA blended pages count only when the submitted marker is clearly BRIC-applicable.
- The page must support the submitted `marker_kind` category for the named marker.
- The page must support the specific deadline, portal/review step, transition instruction, funding methodology, or eligibility/process rule named in `workflow_marker`.
- The page must give enough local process context to explain how the marker functions in the jurisdiction's BRIC process, such as the responsible state office, applicant class, workflow stage, review/submission path, funding method, eligibility condition, or transition handling.
- The page must make the marker state-specific rather than only restating the federal close date or generic FEMA GO guidance.

Write one JSON object per line to `results_bric_state_workflows.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "marker_kind": "<marker_kind>", "workflow_marker": "<workflow_marker>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

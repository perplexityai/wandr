You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `nj_hib_school_contacts`
  - `nj_hib_school_contacts.district_hib_sources`

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

## `nj_hib_school_contacts`

For 60+ New Jersey public school districts or charter/local education agencies, supply current school/building HIB specialist or contact evidence for 3+ public schools per district (i.e. 1+ URL per district-school pair).

Acceptable sources are official district, school, board-of-education, or district-controlled vendor pages/documents for local HIB contacts, such as district HIB pages, school contact rosters, staff contact pages, BoardDocs packets, policy manuals, or district HIB resource pages. The source must be presented as a current or operative contact surface at page time; undated active district HIB/contact pages can count when they are not marked archived, superseded, or limited to a past school year. Generic statewide NJDOE HIB pages, stale official pages, districtwide reporting instructions without a school-specific HIB contact, news articles, encyclopedic summaries, scraped directories, and third-party explainers do not count.

Requirements:
- The page must identify the claimed district and a matching school/building.
- The page must communicate local HIB authority through district, school, or board branding; a policy-manual identity; a district-specific reporting form or system; HIB specialist or coordinator labels; or comparable local authority signals.
- The page must expose a named Anti-Bullying Specialist, Anti-Bullying Coordinator, or comparable HIB contact with a role or contact channel for the claimed school/building.

Write one JSON object per line to `results_nj_hib_school_contacts.jsonl`:
{"item": { "district": "<district>", "school": "<school>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `nj_hib_school_contacts.district_hib_sources`

Cross-tasknode identifier discipline: this task is for the same {= district =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= district =}+ New Jersey public school districts or charter/local education agencies, supply 1+ URL for each of the 2 district-level HIB evidence sides. Annual grade/self-assessment evidence must be for 2023-2024 or 2024-2025; reporting-process evidence can be undated when the district-specific reporting or investigation route is visible.

District-level HIB evidence sides:

- `reporting_process`: official district instructions, forms, policy, or procedure for reporting or investigating alleged HIB incidents in the claimed district.
- `annual_grade_report`: official district annual HIB grade or Anti-Bullying Bill of Rights self-assessment source.

Acceptable sources are official district, school, board-of-education, public board-packet, district-controlled document-host, or report-file sources. Generic statewide NJDOE HIB guidance, news articles, encyclopedic summaries, scraped directories, and third-party explainers do not count. For `annual_grade_report`, a HIB resource page must expose a visible annual report year in 2023-2024 or 2024-2025; pages with only general undated HIB resources do not count for that side.

Requirements:
- The page must identify the claimed district.
- The page must communicate local HIB authority through district, school, or board branding; a policy-manual identity; a district-specific reporting form or system; HIB specialist or coordinator labels; annual HIB grade or self-assessment framing; or comparable local authority signals.
- The page must expose district-side-specific HIB content: for `reporting_process`, instructions, a form, policy, or procedure for reporting or investigating alleged HIB incidents; for `annual_grade_report`, a dated annual HIB grade report, self-assessment report, score table, or official report-file link for the claimed district, with the report year visible.

Write one JSON object per line to `results_nj_hib_school_contacts.district_hib_sources.jsonl`:
{"item": { "district": "<district>", "district_evidence_side": "<district_evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

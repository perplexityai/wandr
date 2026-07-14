You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `grid_deployment_award_provenance`
  - `grid_deployment_award_provenance.project_evidence_facets`

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

## `grid_deployment_award_provenance`

For 40+ public DOE / Grid Deployment Office / DOE Office of Electricity grid-deployment selected projects or awards, name the project and lead recipient, then supply 1+ official or source-of-award URL for each project.

GRIP should be the anchor universe, but other DOE / GDO / DOE Office of Electricity selected projects or awards count when the public source-of-award record is about deployment of electric-grid infrastructure: transmission, grid resilience, grid modernization, grid-enhancing technologies, or similar implementation work. BEAD, NEVI, EU analogs, broadband, EV charging, planning-only studies, engineering-only design, procurement-only notices, ratepayer or investment proceedings, and vendor or product marketing do not count.

Useful official anchors include DOE / GDO / DOE Office of Electricity project pages, DOE program or award announcements with project-level entries, NETL GRIP FOIA or source-file pages, USAspending award records that identify the eligible DOE award, FOA award files, or other official federal source-of-award records for the same eligible project. Recipient, partner, state, utility, tribal, local, and trade sources are useful corroboration elsewhere, but this official-anchor task needs a federal source-of-award page.

The official page should make visible the program, cohort, round, FOA, or award-record context. When the page states status or amount language, source wording such as selected, selected for award negotiations, awarded, executed, obligated, amended, terminated, withdrawn, official federal amount, and "up to" qualifiers is material evidence; a selection source does not establish an executed or obligated award unless the same source supports that step.

Requirements:
- The page must identify the claimed project or award and tie it to the claimed lead recipient, applicant, awardee, or prime recipient.
- The page must place the project in an eligible DOE / GDO / DOE Office of Electricity grid-deployment source-of-award context such as a program, selection round, announcement cohort, FOA, or award record.
- The page must state any official status and amount limits with enough specificity to make material distinctions clear: federal share is not the same as cost-share or total project value, "up to" language matters, and selected / selected-for-negotiations is not the same as executed or obligated.

Out of scope: grid-planning advice, resilience scoring, vendor ranking, procurement guidance, investment analysis, ratepayer forecasting, engineering design, implementation recommendations, legal entitlement conclusions, and general product marketing.

Write one JSON object per line to `results_grid_deployment_award_provenance.jsonl`:
{"item": { "project_name": "<project_name>", "lead_recipient": "<lead_recipient>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `grid_deployment_award_provenance.project_evidence_facets`

Cross-tasknode identifier discipline: this task is for the same {= grid_deployment_project =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= grid_deployment_project =}+ public DOE / Grid Deployment Office / DOE Office of Electricity grid-deployment selected projects or awards, name the project and lead recipient; for each project, cover each of the 4 evidence axes below with 1+ URL under each axis.

Evidence axes:
- `funding_facet_support`
- `participant_role_support`
- `lifecycle_status_support`
- `independent_corroboration`

Use project-specific public evidence rather than repeated reuse of one broad program index. Recipient, partner, state, tribal, utility, local, trade, NETL, USAspending, DOE status-change, and other public sources can support an axis when they actually carry the claimed project facet. Broad all-project tables, CSV rows, program indexes, and blog/list pages can help identify the award universe, but by themselves they are too thin for the facet layer unless the cited page or visible section adds project-specific context beyond a row copied from an award list. GRIP should remain the anchor universe, but other DOE / GDO / DOE Office of Electricity grid-deployment selections or awards count when they satisfy the same public provenance bar. BEAD, NEVI, EU analogs, broadband, EV charging, planning-only studies, engineering-only design, procurement-only notices, ratepayer or investment proceedings, and vendor/product marketing do not count.

Facet meanings:
- `funding_facet_support`: federal amount, cost-share, recipient investment, total project value, obligation amount, assistance identifier, or an explicit conflict / qualifier among these public amounts.
- `participant_role_support`: lead recipient, awardee, consortium lead, named partner, utility, vendor, tribal / state / local participant, or project-specific role distinction.
- `lifecycle_status_support`: source-stated status such as selected, selected for award negotiations, executed, obligated, amended, terminated, withdrawn, or an explicit page-stated conflict / uncertainty about the project's lifecycle status.
- `independent_corroboration`: a non-federal public source that adds concrete project-specific provenance context, such as participant role, geography, funding, source-stated status, project scope, utility / state / local participation, recipient reporting, trade reporting, or program/cohort context. A non-federal page that merely reproduces an award row or broad all-project table does not count.

Requirements:
- The page must clearly tie the finding to the claimed project and lead recipient, not merely to a broad program, company, technology, or geographic theme.
- The page should make its project-specific source context visible at the bar appropriate to the claimed evidence axis: for `funding_facet_support`, a dedicated project fact sheet, award/spending record, recipient / partner / utility / state / local page, trade article, or project-specific section that carries the funding context; for `participant_role_support`, a project page, release, report, participant page, utility / state / local page, or trade article that names a role in the project; for `lifecycle_status_support`, an award record, status-change/update page, execution / obligation source, termination / amendment notice, recipient update, or comparable project-status source; for `independent_corroboration`, a non-federal recipient, partner, state, tribal, local, utility, trade, or project-reporting page with project-specific context rather than a broad list or reposted award table.
- The page must expose a project-specific finding appropriate to the claimed evidence axis.
- The page must state material qualifiers and distinctions for the finding: federal amount vs cost-share vs total value, lead recipient vs partner / vendor, selected vs executed / obligated, and explicit page-stated conflict or uncertainty when present.

Out of scope: grid-planning advice, resilience scoring, vendor ranking, procurement guidance, investment analysis, ratepayer forecasting, engineering design, implementation recommendations, legal entitlement conclusions, and general product marketing.

Write one JSON object per line to `results_grid_deployment_award_provenance.project_evidence_facets.jsonl`:
{"item": { "project_name": "<project_name>", "lead_recipient": "<lead_recipient>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

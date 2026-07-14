You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `housing_funding_awards`
  - `housing_funding_awards.solicitation_terms`

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

## `housing_funding_awards`

For 32+ distinct official housing or homelessness funding cycles dated within 2024-2026, name funded award projects or recipient award rows (8+ per program cycle) and supply official public award-source URLs (1+ URL per award project). The 32-cycle parent count is binding: a complete root answer needs at least 32 separate administered program cycles, each with its own 8+ award-project rows, not many rows or source artifacts from a smaller cycle set. A program_cycle is the administered funding competition, NOFA, opportunity, round, fiscal year, window, notice, or allocation cycle. Use one stable program_cycle label for the same agency/program/year/round cycle across all award rows and, when the same administered cycle appears in solicitation_terms, use the same identity there; award lists, press releases, dashboards, spreadsheets, PDF filenames, geography or CoC slices, recipient rows, project rows, amendment notices, and source-page titles are aliases, not separate cycles. Federal HUD program cycles should use California award rows; California HCD and closely related California public housing/homelessness authority awards are in scope through official public award evidence.

Official award sources include HUD award reports, HCD award dashboards, HCD award PDFs/XLS files, official state or federal award lists, and official award pages that name recipients or projects with award amounts or comparable project-level details. One official artifact may support multiple award rows when it contains row-specific evidence, but the artifact, file name, table section, geography slice, or award-row label never creates an additional program_cycle by itself. Sponsor press releases alone, news coverage alone, consultant/nonprofit/grant-writing/law-firm/advocacy summaries, generic program pages without project-level award evidence, and gated portals without stable public award artifacts do not count.

In the answer, briefly report the awarded amount or equivalent project-level detail, geography if the page states it, and source date or award date if available.

Requirements:
- The page must tie the award evidence to the claimed program cycle.
- The page must name the claimed funded project, recipient, jurisdiction award, or award-row identity.
- The page must state at least two concrete award-outcome details beyond the project name.

Write one JSON object per line to `results_housing_funding_awards.jsonl`:
{"item": { "program_cycle": "<program_cycle>", "award_project": "<award_project>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `housing_funding_awards.solicitation_terms`

Cross-tasknode identifier discipline: this task is for the same {= program_cycle =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For 32+ distinct official housing or homelessness funding cycles dated within 2024-2026, supply official solicitation or program-term sources for each of the 4 public terms facets per program cycle (1+ URL per facet). The 32-cycle parent count is binding for this subtask too: a complete solicitation_terms answer needs at least 32 separate administered program cycles, each with all 4 public terms facets, not repeated facets or source artifacts from a smaller cycle set. A program_cycle is the administered funding competition, NOFA, opportunity, round, fiscal year, window, notice, or allocation cycle. Use one stable program_cycle label for the same agency/program/year/round cycle across all term facets and, when the same administered cycle appears in the root award task, use the same identity there; NOFA PDFs, guidelines filenames, grant-listing titles, amendment notices, award-list titles, geography or CoC slices, recipient rows, project rows, and source-page titles are aliases, not separate cycles.

The terms_facet value must be one of:
- **solicitation_identity** - official NOFO, opportunity, round, fiscal year, release, amendment, or comparable cycle identity
- **funding_or_award_range** - available funding, allocation amount, award range, per-project cap, per-unit limit, or comparable award-scale term
- **eligible_use_or_project_type** - eligible use, project component, activity, applicant/project type, or comparable program-use term
- **geography_or_set_aside** - geographic scope, California row/scope, jurisdiction allocation, CoC/region, rural/tribal/DV/youth set-aside, or comparable geography term

Official solicitation-term sources include HUD NOFO PDFs, Grants.gov or Simpler Grants official listings, HCD NOFAs, HCD program pages, official guidelines, timelines, amended NOFAs, and comparable public program documents. One official artifact may support multiple term facets when it states each claimed term, but the artifact, file name, grant-listing title, amendment notice, geography slice, or award-list heading never creates an additional program_cycle by itself. Third-party NOFO analyses, consultant/nonprofit/grant-writing/law-firm/advocacy summaries, generic program directories without the claimed term, sponsor press releases, news coverage, and gated portals without stable public term artifacts do not count.

In the answer, briefly report the term or source phrase that supports the submitted facet.

Requirements:
- The page must tie the solicitation or program-term evidence to the claimed program cycle.
- The page must state the specific public term claimed for the submitted terms_facet.

Write one JSON object per line to `results_housing_funding_awards.solicitation_terms.jsonl`:
{"item": { "program_cycle": "<program_cycle>", "terms_facet": "<terms_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

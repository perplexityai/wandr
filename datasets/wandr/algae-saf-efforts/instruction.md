You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `algae_saf_efforts`
  - `algae_saf_efforts.external_confirmation`

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

## `algae_saf_efforts`

Identify 150+ public efforts as named algal aviation-fuel projects, grant agreements, award lines, company or developer programs, facilities, fuel products or product programs, demonstrations, certification programs, technology pathway programs, or consortium projects. For each effort, cover each of the 2 evidence roles listed below with a public source (1+ URL per role). This is public provenance as of 2026-06-30, not a ranking, investment recommendation, funding recommendation, procurement recommendation, capacity forecast, outreach list, lead scoring, contact enrichment, customer targeting, or competitive attack.

Evidence roles:
- `root_identity`: a page establishing the named public effort as one real root and tying it to algae, microalgae, macroalgae, seaweed, kelp, wet algal feedstock, or cyanobacteria framed as algae/cyanobacteria, plus aviation fuel, SAF, biojet, jet fuel, or a source-stated intermediate explicitly upgradable to SAF or aviation fuel.
- `dated_public_signal`: a page tying the same named public effort to a source-stated date, project period, award or selection date, reporting period, certification, demonstration, facility milestone, public funding or financing event, legal/status event, partner use, or scale/deployment signal.

A valid effort is the project, award, program, facility, product, demonstration, certification effort, technology pathway, or consortium/collaborative project as a whole. A CORDIS grant ID, DOE/NEDO award line, SBIR/ARPA-E award, public project page, or multi-award listing can count once when it gives its own title/recipient/performer identity and its own algal aviation-fuel relevance.

Participants, beneficiaries, coordinators, subcontractors, work packages, workstreams, objectives, subcomponents, technical phrases, contribution amounts, funding amounts, capacity figures, geographies, status labels, and source dates are not separate efforts merely because they appear on a project page. Academic paper titles, DOI pages, PubMed pages, Semantic Scholar pages, conference abstracts, bibliographic records, market reports, player lists, generic algae companies with no aviation-fuel tie, and generic SAF producers with only non-algae feedstocks are also out of scope as efforts.

Capacity, funding amount, airline or offtake partnership, production target, geography, source date, checked date, status, and participant names are optional source-stated notes only. Use 2026-06-30 as the checked date unless the source was checked later.

Requirements:
- The page must clearly identify the same named public effort: a project title, grant agreement, award ID, award-line title/recipient/performer, company program, facility, fuel product/program, demonstration, certification program, technology pathway, consortium name, or clear alias.
- The page must fulfill the claimed `evidence_role`: `root_identity` evidence must establish both the algal material/pathway and the aviation-fuel/SAF/biojet/jet-fuel relevance for the same effort; `dated_public_signal` evidence must provide a dated public signal tied to the same effort.

Write one JSON object per line to `results_algae_saf_efforts.jsonl`:
{"item": { "project_owned_algal_aviation_effort": "<project_owned_algal_aviation_effort>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `algae_saf_efforts.external_confirmation`

Cross-tasknode identifier discipline: this task is for the same {= project_owned_algal_aviation_effort =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= project_owned_algal_aviation_effort =}+ project-owned algal aviation-fuel efforts, provide an external confirmation source (1+ URL per effort) from a different meaningful public surface confirming the same root or a material public signal for that root.

Good confirmation surfaces include project websites, operator/company pages, participant-owned press releases that name the root, public deliverables, NEPA/status/legal pages, lab pages, airline, airport, regulator, technology-partner, or investor announcements, public filings, and reputable trade articles. A broad CORDIS, DOE, NEDO, funder, or national-program fact sheet, participant roster, multi-award listing, generic program page, market report, player list, or bibliographic page is not external confirmation. A separate root-specific status, deliverable, NEPA, legal, or reporting page can count when it independently confirms the root beyond the original listing.

Requirements:
- The page must confirm the same named public effort or a material public signal for that effort.

Write one JSON object per line to `results_algae_saf_efforts.external_confirmation.jsonl`:
{"item": { "project_owned_algal_aviation_effort": "<project_owned_algal_aviation_effort>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

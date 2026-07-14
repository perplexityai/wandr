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

## `resilient_power_projects`

For 230+ publicly funded or publicly recorded resilient-power deployment projects, supply evidence for each of the 2 evidence types, with at least 1+ source URL per type. The project identity should be pinned by program or funder, recipient or host, location, and a project label or scope. Planned, funded, in-design, under-construction, and built projects can all count when the sources state the status honestly. This is public project provenance as of 2026-06-30, not procurement advice, vendor ranking, partner recommendation, contact discovery, contact enrichment, outreach, lead scoring, or private relationship inference.

The evidence types are:
- `official_award_record`: an official public award, grant, procurement, commission, regulatory, funder, agency, or program record naming a specific recipient, host, community, project, location, or scope.
- `independent_project_partner_corroboration`: a separate public source tying the same project to deployment work, status, developer, EPC, integrator, utility, host, funder, recipient, partner, or another source-stated participant role.

For downstream reading, optional factual notes can include canonical project name, program or funder, recipient or host, community, project location, technology or project scope, source-stated status, source-stated participant roles, source class, source date or observed date, checked date, confidence, and conflict or missing-state notes. Use 2026-06-30 as the checked date unless the source was checked later. Roles count only when the source states or directly describes them; otherwise use `unknown` or omit the role note.

Resilient-power deployment signals include:
- `microgrid or community microgrid`
- `standalone, remote-grid, islanded, or off-grid power system`
- `solar-plus-storage, battery-backed renewable power, or hybrid resilient-power deployment`
- `critical-facility resilience power for fire stations, shelters, clinics, schools, water systems, or emergency operations`
- `tribal, rural, remote, or island community electrification or energy-resilience project`
- `backup generation integrated with distributed energy resources for resilience`
- `utility remote-grid or non-wires resilient-power deployment`

Useful official-record surfaces include:
- `agency award or selection announcement`
- `grant agreement, staff report, board item, or agenda packet`
- `public procurement award or contract record`
- `commission or regulator filing, order, or decision`
- `official funder, program, or public authority project page`
- `public utility or co-op filing when it is the formal award/regulatory record`

Useful independent corroboration surfaces include:
- `recipient, host, tribal, community, or local government project page`
- `developer, EPC, integrator, manufacturer, or utility project announcement`
- `public project report, case study, or implementation update from a participant`
- `trade, local, or public-interest article with project-specific facts`
- `public meeting material, presentation, or packet from a project participant`

Useful source-stated status values include:
- `awarded`
- `planned`
- `in design`
- `under construction`
- `deployed`
- `commissioned`
- `funded but status not stated`
- `status unclear`

Boundary classes to keep out unless the page also proves a specific submitted project at the required evidence role:
- `generic funding opportunity or NOFO with no named recipient or project`
- `broad program overview with no submitted project identity`
- `generic clean-energy grant without resilient-power deployment substance`
- `solar farm, efficiency, weatherization, or electrification grant with no resilience, microgrid, storage, backup, remote-grid, or critical-facility power signal`
- `vendor product page or market map with no named public project or host`
- `partner role inferred from company category rather than source-stated or directly described`
- `procurement advice, vendor ranking, partner recommendation, outreach, contact discovery, contact enrichment, lead scoring, or private relationship inference`

Use distinct sources for the two evidence roles. The same URL or the same source role should not be reused as both `official_award_record` and `independent_project_partner_corroboration`. Awarded or funded status and built or deployed status are different facts; do not infer deployment from an award unless a source says it.

Requirements:
- The page must tie the submitted project identity to the same specific project through a named recipient, host, community, location, project label, program, award, or project scope. Exact titles can differ when the source context clearly identifies the same deployment.
- The submitted page itself must fulfill the claimed `evidence_type`: `official_award_record` evidence should be an official public award, grant, procurement, commission, regulatory, funder, agency, or program record; `independent_project_partner_corroboration` evidence should be a separate public source with a different source role from the official record.
- The page must support resilient-power deployment substance: microgrid, standalone or remote power, off-grid or islandable service, battery-backed renewable power, critical-facility resilience, tribal or rural electrification, utility remote grid, or comparable deployment-oriented resilience power. Generic clean-energy funding without that substance is not enough.
- The page must expose project-specific detail at the claimed evidence role. For `official_award_record`, it should name a specific recipient, host, community, project, location, award, scope, or public-record relationship. For `independent_project_partner_corroboration`, it should add a deployment, status, developer/EPC/integrator, utility, host, funder, recipient, partner, or source-stated participant-role fact for the same project.

Write one JSON object per line to `results_resilient_power_projects.jsonl`:
{"item": { "program_or_funder": "<program_or_funder>", "recipient_or_host": "<recipient_or_host>", "project_location": "<project_location>", "project_label": "<project_label>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

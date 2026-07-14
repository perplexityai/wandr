You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `texas_headcounts`
  - `texas_headcounts.reconciliation_context`

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

## `texas_headcounts`

For each of 10+ Texas employer sectors, find 9+ large or probably large employers operating in Texas and build public Texas workforce grounding evidence. Supply 2+ distinct Texas workforce evidence axes per employer and 1+ source URL per axis. This is a provenance and reconciliation task, not a ranked largest-employers list.

Treat each URL as one Texas-scoped workforce claim line. Preserve the source name/class, raw workforce wording, source date or reporting period when supplied, number or range, geography scope, metric/unit, and currentness/status so the claim can be reconciled without flattening its scope.

Use only page-local evidence that visibly appears in the cited page text. Do not invent, normalize, or combine headcount snippets from memory, search summaries, infoboxes, or another page. Wikipedia, Wikidata, generic encyclopedia pages, job/advice pages, prospecting databases, and pages that merely call an entity a "major employer" without a row-specific Texas workforce number are invalid for this grounding task.

Employer sector is an exact dispatch key. Use each sector for employers whose main Texas workforce footprint fits that sector:
- `retail_logistics_and_food`: Retail, grocery, restaurant, distribution, ecommerce, logistics, and food-service employers.
- `healthcare_hospital_and_life_sciences`: Hospital systems, health-care providers, life-science employers, and major medical complexes.
- `energy_refining_chemicals_and_industrial`: Energy, oil and gas, refining, chemicals, industrial services, and heavy industrial employers.
- `technology_semiconductor_and_telecom`: Technology, semiconductor, data-center, electronics, software, and telecom employers.
- `finance_professional_services_and_hq_ops`: Finance, insurance, professional services, headquarters operations, and administrative operations employers.
- `manufacturing_aerospace_and_transport_equipment`: Manufacturing, aerospace, defense manufacturing, automotive, and transport-equipment employers.
- `higher_ed_research_and_university_systems`: Higher-education, research, and university-system employers; K-12 school districts and individual schools are excluded.
- `state_local_government_and_public_authorities`: State agencies, local governments, transit authorities, port authorities, utility authorities, and other non-K-12 public authorities.
- `military_federal_airport_and_utility_complexes`: Military installations, federal facilities, airports, public utilities, and similar bounded employer complexes.
- `other_large_private_services`: Other large private-service employers that do not fit the other sector labels.

A Texas workforce evidence axis is one of:
- `statewide_or_system_current`: A current or current-ish actual workforce claim for the employer across Texas statewide, across multiple Texas regions, for a Texas statewide public agency, or for a genuinely statewide multi-campus Texas university system. A single-locality employer, including one school district, one city/county government, one hospital, one campus, one installation, or one site, does not satisfy this axis and belongs only in local_or_site_current.
- `local_or_site_current`: A current or current-ish actual workforce claim for the employer at a named Texas metro, county, city, region, campus, installation, plant, fulfillment center, refinery, hospital, office, or other bounded Texas worksite.

Each employer can be a company, subsidiary, DBA, non-K-12 public agency, public authority, university system, local government, military installation, medical complex, campus, worksite, or bounded employer complex when the source's workforce boundary is clear and the employer fits the submitted `employer_sector`. Do not submit K-12 public school districts, individual K-12 schools, charter networks, or similar K-12 education systems as employers in any sector. Do not infer Texas workforce grounding from broader company totals, generic "major employer" list membership, broad regional prose without a row-specific number, FTE/contractor/project-impact numbers that are not labeled as such, planned/committed jobs, peak jobs, stale claims, or ranges that are not tied to an actual Texas workforce boundary.

Requirements:
- The submitted employer must fit the submitted `employer_sector`; sector labels are part of the claim, not loose source tags.
- The page must communicate an admissible public headcount source: employer-controlled page/report, public-institution report, state/local economic-development or regional employer surface, official incentive/compliance material, credible news, or reputable third-party/ranking source used only as labeled evidence. Employer-quality rankings, job-search or hiring-advice pages, investment/vendor/prospecting pages, data-broker blurbs, and policy-advice pages do not work.
- The page must name the employer or bounded employer complex and state a numeric or narrow-range workforce claim tied to it.
- The page must tie the workforce claim to a Texas statewide, Texas-local, named Texas-site, or bounded Texas public-system geography for the submitted employer; broader-company, national, global, project/impact, and third-party conflict context does not satisfy this grounding task unless the page also gives the employer-specific Texas workforce boundary being claimed.
- The page must make the claim's source date or reporting period, geography scope, metric/unit, and currentness/status determinable enough to preserve the claim without scope-flattening.
- The page's claim must fit the submitted `workforce_evidence` label.
- A single-locality public entity's total workforce claim, including a single city, county, K-12 school district, hospital, campus, installation, or site, is a local/site claim, not `statewide_or_system_current`. Only multi-region statewide employers, statewide agencies, or statewide university systems satisfy the statewide/system axis.
- Every excerpt must be a faithful quote or tight page-local paraphrase of visible source text that supports the submitted number, employer boundary, Texas geography, and evidence label.

Write one JSON object per line to `results_texas_headcounts.jsonl`:
{"item": { "employer_sector": "<employer_sector>", "employer": "<employer>", "workforce_evidence": "<workforce_evidence>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `texas_headcounts.reconciliation_context`

Cross-tasknode identifier discipline: this task is for the same {= employer =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= employer =}+ large or probably large employers operating in Texas, supply 1+ public source URL with reconciliation context for the employer's workforce claims. These records preserve broader-company, project/impact, stale, range, third-party, or conflicting workforce/job claims so they can be compared against Texas-specific grounding evidence.

Treat each URL as one context claim line. Preserve the source name/class, raw workforce or jobs wording, source date or reporting period when supplied, number or range, geography scope, metric/unit, and limitation or conflict state. Do not flatten global, U.S., parent-company, planned, indirect, peak, contractor, FTE, stale, or range claims into a current Texas employee number.

Use only page-local evidence that visibly appears in the cited page text. Do not invent, normalize, or combine headcount snippets from memory, search summaries, infoboxes, or another page. Wikipedia, Wikidata, generic encyclopedia pages, job/advice pages, and prospecting databases are invalid even as reconciliation context.

Requirements:
- Do not submit K-12 public school districts, individual K-12 schools, charter networks, or similar K-12 education systems as employers in any sector.
- The page must communicate an admissible public headcount or jobs source: employer-controlled page/report, public-institution report, official incentive/compliance material, state/local economic-development material, credible news, reputable third-party/ranking source, securities filing, annual report, or other public source with a clear publisher. Employer-quality rankings, job-search or hiring-advice pages, investment/vendor/prospecting pages, data-broker blurbs, and policy-advice pages do not work.
- The page must name the employer or bounded employer complex and state a numeric or narrow-range workforce, jobs, FTE, contractor, project/impact, or broader-company claim tied to it.
- The page must make the claim's source date or reporting period, geography scope, metric/unit, and currentness/status determinable enough to preserve the claim without scope-flattening.
- The page must provide useful reconciliation context: broader-company scale, a project or impact jobs claim, a stale/range/conflicting claim, a third-party limitation signal, or a related public-system metric that helps explain why Texas-specific workforce estimates differ.
- Every excerpt must be a faithful quote or tight page-local paraphrase of visible source text that supports the submitted number, employer boundary, geography scope, and limitation/conflict state.

Write one JSON object per line to `results_texas_headcounts.reconciliation_context.jsonl`:
{"item": { "employer": "<employer>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

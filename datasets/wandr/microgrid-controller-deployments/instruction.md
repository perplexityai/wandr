You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `microgrid_controller_deployments`
  - `microgrid_controller_deployments.control_layer`
  - `microgrid_controller_deployments.benefit_status`

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

## `microgrid_controller_deployments`

For each of the 5 public-benefit site classes below, supply project-profile evidence for 8+ implementation-stage microgrid deployments per class. Use the first applicable site class in the listed order so each deployment belongs under one class. Include at least 1+ site-specific project/profile URL per deployment. Treat a deployment's identity as the site class, owner/operator, site, facility, or community, and location.

The project/profile source should resolve the concrete deployment itself: owner/operator, site, facility, or community, location, microgrid or comparable distributed-energy system, and operating, commissioned, under-construction, contracted, or otherwise implementation-backed status. Eligible pages include owner, public-agency, utility, funder/regulator, developer/EPC, controller/platform vendor, credible reporting, and project-reference surfaces when they carry site-specific project substance such as assets, scope, counterparties, construction, commissioning, funding/regulatory status, or implementation detail. Hybrid controls, public-outcome, or vendor-framed pages can count when they carry that project/profile substance; they do not count when the deployment facts are absent or generic.

Site classes:
- `remote_community`: isolated village, rural settlement, islanded town, tribal/community utility, or comparable remote community power system; this class takes precedence when remoteness or community-scale energy access is the defining feature
- `public_safety`: fire, police, emergency operations, emergency-management shelter, National Guard readiness center, public-safety headquarters, correctional facility, or comparable emergency-services site
- `transit_fleet`: bus depot, rail facility, port, airport, fleet yard, or comparable transportation operation; this class takes precedence for transportation charging, fueling, maintenance, or operations sites
- `critical_services`: hospital, clinic, water or wastewater utility, communications node, food/cold-chain facility, utility clean-substation or community backup power system, disaster-recovery nonprofit, or comparable critical service not better classed as public safety
- `municipal_civic`: city, county, state, school, library, community center, public housing, government office, or comparable civic facility that is not better classed as remote community, public safety, transit fleet, or critical services

Broad program cohort pages, feasibility-only awards, search/listing pages, generic microgrid explainers, product marketing without a named deployment, thin grant notices, and ordinary backup-generator pages do not count by themselves. Pure planning, technical-assistance, assessment, or selected-for-study pages do not count unless the same URL also shows implementation-stage status for the submitted owner/site/location.

Requirements:
- The page must anchor the submitted deployment: owner/operator, site, facility, or community, location, a site-specific microgrid or comparable distributed-energy system, and implementation-stage status.
- The page must provide project/profile substance: concrete assets, project scope, counterparties, construction, commissioning, funding/regulatory status, or implementation detail for the submitted deployment.

Write one JSON object per line to `results_microgrid_controller_deployments.jsonl`:
{"item": { "site_class": "<site_class>", "owner": "<owner>", "site": "<site>", "location": "<location>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `microgrid_controller_deployments.control_layer`

Cross-tasknode identifier discipline: this task is for the same {= site_class =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For each of the {= site_class =} public-benefit site classes below, supply a related sample of control-layer evidence for 3+ implementation-stage microgrid deployments per class. Use the first applicable site class in the listed order so each deployment belongs under one class. Include at least 1+ site-specific URL per control-disclosed deployment. Treat a control-disclosed deployment's identity as the site class, owner/operator, site, facility, or community, and location.

The source should be site-specific and disclose the deployment's control layer. Eligible pages include controller/platform vendor pages, integrator or engineering pages, commissioning or technical reports, owner/utility technical documents, controls-focused credible reporting, public-agency project pages, and hybrid project/deployment pages when they carry control-layer evidence for the submitted deployment. Report `control_disclosure_class` as `named_controller` when the page names a controller, control platform, energy-management platform, or control software used for the submitted deployment; report it as `site_specific_control_behavior` when the page instead describes rich site-specific operating behavior. Do not infer a control layer from solar/battery assets, inverter names, a BMS, a generic SCADA label, an energy vendor, or an ordinary project blurb.

Site classes:
- `{= site_class =}`: isolated village, rural settlement, islanded town, tribal/community utility, or comparable remote community power system; this class takes precedence when remoteness or community-scale energy access is the defining feature
- `{= site_class =}`: fire, police, emergency operations, emergency-management shelter, National Guard readiness center, public-safety headquarters, correctional facility, or comparable emergency-services site
- `{= site_class =}`: bus depot, rail facility, port, airport, fleet yard, or comparable transportation operation; this class takes precedence for transportation charging, fueling, maintenance, or operations sites
- `{= site_class =}`: hospital, clinic, water or wastewater utility, communications node, food/cold-chain facility, utility clean-substation or community backup power system, disaster-recovery nonprofit, or comparable critical service not better classed as public safety
- `{= site_class =}`: city, county, state, school, library, community center, public housing, government office, or comparable civic facility that is not better classed as remote community, public safety, transit fleet, or critical services

`site_specific_control_behavior` needs enough site-specific behavior to make the operating/control layer visible: islanding or reconnection logic, resource or load dispatch, charge or energy management, local/remote activation, network-operations control, load shedding, or comparable behavior. A single generic grid-export, market-dispatch, or asset-taking-turns sentence does not count by itself.

Requirements:
- The page must anchor the submitted deployment: owner/operator, site, facility, or community, location, a site-specific microgrid or comparable distributed-energy system, and implementation-stage status.
- The page must disclose the deployment's control layer: a named controller/platform/software or rich site-specific control behavior for the submitted deployment.
- The page must support the reported `control_disclosure_class`.

Write one JSON object per line to `results_microgrid_controller_deployments.control_layer.jsonl`:
{"item": { "site_class": "<site_class>", "owner": "<owner>", "site": "<site>", "location": "<location>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `microgrid_controller_deployments.benefit_status`

Cross-tasknode identifier discipline: this task is for the same {= deployment =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= deployment =}+ public-benefit microgrid deployments, supply public-outcome evidence for the deployment (at least 1+ site-specific URL per deployment). Use the first applicable site class in the listed order so each deployment belongs under one class. Treat a deployment's identity as the site class, owner/operator, site, facility, or community, and location.

The source should be site-specific and show the deployment's public outcome or public-service role, such as resilience, reliability, affordability or cost savings, emissions reductions, energy access, service continuity, critical-load support, public-safety support, community sheltering, or grid reliability/flexibility tied to public or community service. Owner/operator, public agency, utility, funder, community-facing, credible reporting, project-specific reference, and hybrid project/deployment pages can all work when they carry that substance. Controller-vendor, integrator, developer/EPC, or asset-delivery pages can work only when they substantively tie the submitted deployment to public outcomes or public service; they do not count when the benefit language is generic or incidental to a technical or delivery pitch. Generic microgrid explainers and broad program pages do not count by themselves.

Site classes:
- `remote_community`: isolated village, rural settlement, islanded town, tribal/community utility, or comparable remote community power system; this class takes precedence when remoteness or community-scale energy access is the defining feature
- `public_safety`: fire, police, emergency operations, emergency-management shelter, National Guard readiness center, public-safety headquarters, correctional facility, or comparable emergency-services site
- `transit_fleet`: bus depot, rail facility, port, airport, fleet yard, or comparable transportation operation; this class takes precedence for transportation charging, fueling, maintenance, or operations sites
- `critical_services`: hospital, clinic, water or wastewater utility, communications node, food/cold-chain facility, utility clean-substation or community backup power system, disaster-recovery nonprofit, or comparable critical service not better classed as public safety
- `municipal_civic`: city, county, state, school, library, community center, public housing, government office, or comparable civic facility that is not better classed as remote community, public safety, transit fleet, or critical services

Requirements:
- The page must anchor the submitted deployment: owner/operator, site, facility, or community, location, a site-specific microgrid or comparable distributed-energy system, and implementation-stage status.
- The page must show a public outcome or public-service role for the submitted deployment, such as resilience, reliability, affordability or cost savings, emissions reductions, energy access, service continuity, critical-load support, public-safety support, community sheltering, or grid reliability/flexibility tied to public or community service.

Write one JSON object per line to `results_microgrid_controller_deployments.benefit_status.jsonl`:
{"item": { "site_class": "<site_class>", "owner": "<owner>", "site": "<site>", "location": "<location>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

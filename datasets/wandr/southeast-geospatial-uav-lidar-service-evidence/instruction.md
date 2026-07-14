You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `southeast_geospatial_uav_lidar_service_evidence`
  - `southeast_geospatial_uav_lidar_service_evidence.southeast_firm_presence`

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

## `southeast_geospatial_uav_lidar_service_evidence`

Identify 100+ firms as real distinct operating service providers publicly connected to geospatial, UAV, LiDAR, photogrammetry, aerial mapping, survey, inspection, or comparable aerial-data work; for each firm, cover each of the 3 evidence facets listed below with a public source (i.e. 1+ URL per facet).

The useful evidence separates technical capability, public work record, and public standing rather than repeating the same generic service page.

Evidence facets:
- `technical_capability`: evidence of concrete aerial/geospatial technical capability, such as an operated UAV/LiDAR/sensor platform, payload, workflow, accuracy method, processing method, or technical deliverable.
- `project_or_client_work`: evidence of a concrete project, client, site, facility, asset, contract, portfolio item, social update, or past-performance episode where the firm applied aerial/geospatial work.
- `profile_or_authority`: evidence of the firm's public profile, professional standing, authority, membership, license, vendor/client recognition, platform profile, or comparable public standing outside an ordinary service-description page.

Firms should be distinct operating service providers. Lead-generation farms, directory/listing pages, reseller-only product vendors, cloned city landing pages, unnamed coordination operators, product/software vendors that merely sell tools to service firms, and placeholders are outside scope.

Requirements:
- The page must clearly identify the named firm.
- The page should make its facet-appropriate source role visible. For `technical_capability`, it should read as a technical service, equipment, workflow, accuracy, data-product, methods, or deliverables surface rather than a broad service menu. For `project_or_client_work`, it should read as a project, case study, portfolio, client/vendor article, public-agency/news item, or clearly separated work-update surface centered on a specific work episode rather than an industry/application menu. For `profile_or_authority`, it should read as a profile, authority, membership, license, public-agency/vendor, client/vendor, professional-platform, or comparable public-standing surface rather than the firm's ordinary service-description page.
- The page should expose a focused finding clearly scoped to the named firm and evidence facet. For `technical_capability`, this means a concrete technical detail such as a named sensor/platform/payload, field or processing workflow, accuracy/ground-control method, file format, point cloud, LAS/LAZ, DTM/DEM, orthomosaic, contour, CAD/topographic output, volumetric deliverable, or similar aerial/geospatial technical output. For `project_or_client_work`, it means a concrete work episode, client/project/site/facility/asset/contract, or past-performance context where the firm applied aerial/geospatial work. For `profile_or_authority`, it means a public standing signal such as a profile field, headquarters/location/size/industry/specialty profile, professional membership, license/authority signal, public vendor/prequalification status, client/vendor recognition, or comparable public profile/authority detail.

Write one JSON object per line to `results_southeast_geospatial_uav_lidar_service_evidence.jsonl`:
{"item": { "firm": "<firm>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `southeast_geospatial_uav_lidar_service_evidence.southeast_firm_presence`

Cross-tasknode identifier discipline: this task is for the same {= firm =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= firm =}+ firms, supply public regional operating evidence showing each firm has a concrete operating tie to at least one of the in-scope U.S. Southeast states (i.e. 1+ URL per firm).

Southeast states in scope:
- **Alabama**
- **Florida**
- **Georgia**
- **Mississippi**
- **North Carolina**
- **South Carolina**
- **Tennessee**

Firms should be distinct operating service providers publicly connected to geospatial, UAV, LiDAR, photogrammetry, aerial mapping, survey, inspection, or comparable aerial-data work. Lead-generation farms, directory/listing pages, reseller-only product vendors, cloned city landing pages, unnamed coordination operators, product/software vendors that merely sell tools to service firms, and generic national pages with no concrete Southeast operating evidence are outside scope. National or multi-region operators can qualify when the cited page itself carries a concrete operating tie to at least one in-scope state.

Requirements:
- The page must clearly identify the named firm.
- The page must tie the firm to at least one in-scope Southeast state through a concrete operating signal such as an office, service area with firm-specific substance, licensed/local team, named project, local client/work example, state-specific association/profile entry, public-agency/vendor entry, or comparable regional evidence.

Write one JSON object per line to `results_southeast_geospatial_uav_lidar_service_evidence.southeast_firm_presence.jsonl`:
{"item": { "firm": "<firm>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

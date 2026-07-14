You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `mn_environmental_health_agencies`
  - `mn_environmental_health_agencies.agency_authority`

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

## `mn_environmental_health_agencies`

For at least 175+ Minnesota local agency/jurisdiction rows with environmental-health, public-health, food/pool/lodging, inspection, licensing, nuisance, or environmental-hazard responsibilities, name one public roleholder or concrete public role/unit (1+ per agency row) and supply an official local source (i.e. 1+ URL) that names the roleholder or unit and ties it to that agency function.

Use `agency_name` for the provider agency or department and `jurisdiction_served` for the jurisdiction row. Keep them separate when one city, county, community health board, public-health agency, or provider serves another jurisdiction, and when the same provider appears for multiple counties. Do not satisfy the set mostly from one repeated provider, one county packet, or one obvious source family; include city-operated, county-operated, and multi-jurisdiction/community-health-provider rows when available.

Report `jurisdiction_entity_type` using one of:

- `city_or_municipal`
- `county_or_county_department`
- `multi_jurisdiction_or_community_health_provider`
- `tribal_or_other_official_local_authority`

Preserve the exact local title or unit label as `title_as_stated`; report a separate `normalized_role_category` using one of:

- `environmental_health_director`
- `environmental_health_manager`
- `environmental_health_supervisor`
- `health_director`
- `public_health_director`
- `community_health_administrator`
- `health_department_executive`
- `public_health_environment_director`
- `external_provider_environmental_health_manager`
- `environmental_health_unit_no_named_lead`
- `unclear_equivalent_counterpart`

This is public role/title/source evidence only. Suppress personal phone numbers, email addresses, contact-enrichment details, salary/personnel material, private profiles, litigation framing, inferred tenure, and biography enrichment. Report source-date or checked-date context as a sighting/currentness aid, not as a tenure claim.

Expected local sources are official city, county, tribal, community-health-board, public-health-agency, department, budget, org-chart, staff report, agenda packet, minutes, annual report, advisory council, WebLink/Laserfiche, or other government-hosted public records. For provider-served or multi-jurisdiction rows, the local source must identify the submitted jurisdiction or a bounded service area that includes it; a provider page that names only the provider but not the jurisdiction/service area does not count for that row. Private profiles, snippets, salary pages, background-check pages, and generic contact-only blocks do not count.

Requirements:
- The page must tie the roleholder or unit to the submitted agency_name or to the official provider serving that agency row.
- The page must name the submitted roleholder_or_unit and support the exact title_as_stated as local source wording, not a normalized rewrite.
- The page must tie that roleholder or unit to environmental health, food/pool/lodging, inspections, licensing, nuisance, environmental hazards, or a relevant local public-health authority/function.
- The page must support the submitted jurisdiction_entity_type and, for provider-served or multi-jurisdiction rows, identify the submitted jurisdiction or a bounded service area that includes it.
- The normalized_role_category must fit the page-supported title or unit state.

Write one JSON object per line to `results_mn_environmental_health_agencies.jsonl`:
{"item": { "agency_name": "<agency_name>", "jurisdiction_served": "<jurisdiction_served>", "roleholder_or_unit": "<roleholder_or_unit>", "title_as_stated": "<title_as_stated>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `mn_environmental_health_agencies.agency_authority`

Cross-tasknode identifier discipline: this task is for the same {= agency =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For at least {= agency =}+ Minnesota agency/jurisdiction rows, supply an official MDH, MDA, or Minnesota state authority source (i.e. 1+ URL) showing the agency_name, jurisdiction_served, and environmental-health or local-health authority/function for that row.

Primary authority anchor for this task:

- Source name: `Minnesota State and Local Food, Pools, and Lodging Contacts`
- Live URL: `https://www.health.state.mn.us/communities/environment/food/docs/license/locals.pdf`
- Visible artifact date: `02/04/2026`
- Checked date: `2026-06-26`
- HTTP metadata: `Last-Modified: Wed, 04 Feb 2026 17:06:54 GMT; ETag: "1770224814"; Content-Length: 688425`
- PDF XMP metadata: `CreateDate 2026-02-04T10:46:00-06:00; ModifyDate 2026-02-04T11:01:33-06:00`

Report `jurisdiction_entity_type` using one of:

- `city_or_municipal`
- `county_or_county_department`
- `multi_jurisdiction_or_community_health_provider`
- `tribal_or_other_official_local_authority`

The live PDF URL is mutable, so cite the official state authority URL and preserve visible source-date, artifact-date, revision, or checked-date context where available. Local government pages can help understand a row, but this authority node needs an MDH/MDA/Minnesota state authority surface.

Requirements:
- The page must support the submitted agency_name and jurisdiction_served as the same local agency/provider and jurisdiction row.
- The page must tie the row to MDH/MDA/state local-health or environmental-health authority, delegation, inspection, licensing, food, pools, lodging, manufactured home parks, recreational camping areas, youth camps, or a comparable state-supervised function.
- The page must support the jurisdiction scope at the granularity claimed, including provider, exclusion, or delegation distinctions when those define the row.
- The page must support the submitted jurisdiction_entity_type and, for provider-served or multi-jurisdiction rows, identify the submitted jurisdiction or a bounded service area that includes it.

Write one JSON object per line to `results_mn_environmental_health_agencies.agency_authority.jsonl`:
{"item": { "agency_name": "<agency_name>", "jurisdiction_served": "<jurisdiction_served>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

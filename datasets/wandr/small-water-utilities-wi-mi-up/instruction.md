You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `small_water_utilities_wi_mi_up`
  - `small_water_utilities_wi_mi_up.utility_narratives`

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

## `small_water_utilities_wi_mi_up`

For 30+ small community/public water systems in each target region below, supply a source (1+ system-specific official drinking-water record/profile URL per system). The page must establish the submitted PWS/system ID, system name, served community or location, system type, population served at or below 10,000, and source-water class.

Target regions:
- **wisconsin**: Wisconsin statewide.
- **mi_up_west**: Michigan Upper Peninsula communities in the county-based western target area: all of Delta County, including Gladstone, plus Menominee, Dickinson, Iron, Gogebic, Ontonagon, Houghton, Keweenaw, Baraga, and Marquette counties.

The cited page must be specific to the submitted drinking-water system. Bulk all-systems lists, third-party tap-water mirrors, enforcement schedules, generic municipal homepages, and local utility pages do not count for this official-profile requirement.

Requirements:
- The page must communicate that it is an official federal or state drinking-water record/profile page for the submitted system.
- The page must show the claimed system ID and system name.
- The page must tie the system to the submitted served community or location and claimed target region.
- The page must show the submitted system type is a community or equivalent year-round public drinking-water system.
- The page must show the submitted population served at or below 10,000.
- The page must show the submitted source-water class.

Write one JSON object per line to `results_small_water_utilities_wi_mi_up.jsonl`:
{"item": { "region": "<region>", "system_id": "<system_id>", "system_name": "<system_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `small_water_utilities_wi_mi_up.utility_narratives`

Cross-tasknode identifier discipline: this task is for the same {= utility_system =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= utility_system =}+ named utility systems, supply a source (1+ local/operator/project URL per utility) from a page that provides narrative evidence beyond a registry or contact-list row.

Focus only on narrative evidence tied to the submitted utility identity. Bare registry rows, contact-list entries, and pages that only repeat profile attributes do not count unless the same page also provides substantive operations, treatment, service, public-works, funding, or project narrative.

The URL must tie the page to the same submitted PWS/system ID, distinctive utility name, water department, or public-works utility. Same municipality alone is not enough for school, mobile-home-park, association, district, or other distinct systems with their own PWS/system identities.

Requirements:
- The page must communicate that it is a local, utility-controlled, municipal, county, township, engineering/operator, or comparable official project source.
- The page must tie the narrative to the same submitted utility/system.
- The page must substantively describe operator, treatment, water/wastewater utility service, capital project, funding/project, or public-works evidence for that utility.

Write one JSON object per line to `results_small_water_utilities_wi_mi_up.utility_narratives.jsonl`:
{"item": { "region": "<region>", "system_id": "<system_id>", "system_name": "<system_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `construction_3d_printing_deployments`

For at least 100+ named construction-scale 3D printing projects, deployments, public pilots, built components, commercial or public facilities, infrastructure components, or research demonstrators, supply a project-specific public URL (i.e. at least 1+ URL for each one).

Each submitted item is identified by `project_or_deployment`, `locality`, and `country`. Within the submitted set, include at least 4 India-specific records; at least 3 of those India records should be named projects, deployments, demonstrators, public pilots, or built components. India is a floor, not the whole task.

Use project-specific public evidence. The cited page must itself prove the submitted project/deployment row; discovery pages or generic technology pages do not replace project-specific evidence.

Status or date basis should be source-stated, using labels such as:
- `announced`
- `under-construction`
- `completed`
- `opened/occupied`
- `prototype/demonstrator`
- `public-pilot`
- `component/infrastructure`

Alongside the URL, include the source-stated status/date basis and actor roles. Source class, checked date, confidence, missing-state flags, and optional project details are useful review context; they do not replace page evidence. Optional details include:
- machine/system or technology provider
- material or mix supplier
- material type
- build size, area, height, unit count, or component dimensions
- capability, print speed, cost, or execution-time detail

When an optional detail is not stated, leave it blank or use a missing-state note such as:
- `no-machine-source`
- `no-material-source`
- `no-cost-source`
- `no-current-status-source`
- `no-independent-corroboration`
- `name-conflict`

The source should not be any of these as row evidence:
- company catalog
- product-only printer or system page
- patent-only page
- market report or top-company list
- ranking, recommendation, or purchase-advice page
- material-formulation or engineering-design guidance page
- social/video-only page

This is not a company catalog, product-only printer/system table, patent map, country or global leadership ranking, technology recommendation, machinery purchase guide, material formulation guide, construction engineering advice, investment analysis, commercialization forecast, outreach list, lead-scoring task, market/top list, or cost-estimation exercise.

Requirements:
- The page must identify the named project/deployment and place it in the claimed locality and country.
- The page must show that construction-scale 3D printing or additive manufacturing was used, planned, or demonstrated for that named project/deployment.
- The page must state a project status or date basis; do not infer completion, occupancy, public use, machine model, material, cost, or capability from photos, reputation, or generic vendor relationships.
- The page must tie at least one real actor to the project/deployment, such as a builder, operator, technology provider, client, authority, university, contractor, machine supplier, or material supplier.
- Any machine/system, material/mix, material type, cost, build size, capability, print speed, execution time, or technology detail submitted for the row must be explicitly source-stated on the cited page; absent optional details are fine when marked missing or omitted.

Write one JSON object per line to `results_construction_3d_printing_deployments.jsonl`:
{"item": { "project_or_deployment": "<project_or_deployment>", "locality": "<locality>", "country": "<country>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

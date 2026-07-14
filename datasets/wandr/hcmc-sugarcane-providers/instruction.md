You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `hcmc_sugarcane_providers`
  - `hcmc_sugarcane_providers.provider_capability`

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

## `hcmc_sugarcane_providers`

For at least 25+ distinct business-like providers physically based in Ho Chi Minh City, Vietnam, that publicly supply, manufacture, assemble, repair, distribute, warehouse, or showcase sugarcane juice machines or closely attached sugarcane-machine equipment, supply at least 1+ public URLs per provider on pages establishing both HCMC presence and sugarcane-machine capability. The target public-source frame is 2026-04-13; current public pages are eligible unless they clearly describe only a defunct, historical, or one-off resale situation.

Providers must be businesses, workshops, showrooms, warehouses, public shops, or comparable ongoing provider entities, not private one-off resale posts, generic product categories, directories as entities, or contact/person names. Sources should be public, substance-bearing pages such as official sites, product pages, directory entries, public shop/profile pages, marketplace listings, or article-style workshop pages. Contact-only pages, private or group-harvested surfaces, rankings, purchase advice, price-negotiation pages, outreach lists, and lead-scoring surfaces do not count. Do not extract phone numbers, Zalo IDs, hotlines, private contacts, rankings, recommendations, procurement advice, outreach targets, or lead scores.

Requirements:
- The page must clearly identify the claimed provider.
- The page must state the provider's physical presence in Ho Chi Minh City / TP.HCM; shipping or delivery to HCMC alone is not enough.
- The page must state the provider's sugarcane-machine capability, such as supplying, selling, manufacturing, assembling, repairing, distributing, warehousing, or showcasing sugarcane juice machines or closely attached sugarcane-machine equipment.

Write one JSON object per line to `results_hcmc_sugarcane_providers.jsonl`:
{"item": { "provider": "<provider>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `hcmc_sugarcane_providers.provider_capability`

Cross-tasknode identifier discipline: this task is for the same {= provider =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For at least {= provider =}+ sugarcane-machine providers, supply at least 3+ public capability evidence types per provider from the list below, with at least 1+ URLs for each evidence type. Each source must identify the provider and state a source-backed capability or public-source detail that fits the declared evidence type. Use source-stated details only; do not infer role, machine type, facility, warranty, delivery, repair, parts, or public-shop status from the provider name alone.

Evidence types:
- `machine_type`: source-stated sugarcane-machine type, product line, machine model family, or closely attached equipment category
- `provider_role`: source-stated role such as manufacturer, producer, assembler, distributor, seller, repair/parts provider, showroom operator, or warehouse
- `facility_presence`: source-stated showroom, workshop, factory or production site, warehouse, branch, or comparable physical operating location
- `service_terms`: source-stated warranty, repair, parts, delivery, installation, support, or comparable public service terms for sugarcane-machine equipment
- `public_shop_profile`: public marketplace, directory, social/profile, or listing surface tying the provider to sugarcane-machine products or services without contact extraction

Sources should be public, substance-bearing pages such as official sites, product pages, directory entries, public shop/profile pages, marketplace listings, or article-style workshop pages. Contact-only pages, private or group-harvested surfaces, rankings, purchase advice, price-negotiation pages, outreach lists, and lead-scoring surfaces do not count. Do not extract phone numbers, Zalo IDs, hotlines, private contacts, rankings, recommendations, procurement advice, outreach targets, or lead scores.

Requirements:
- The page must clearly identify the claimed provider.
- The page must state a provider-specific capability or public-source detail that fits the declared `evidence_type`.

Write one JSON object per line to `results_hcmc_sugarcane_providers.provider_capability.jsonl`:
{"item": { "provider": "<provider>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

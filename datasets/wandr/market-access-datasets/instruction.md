You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `market_access_datasets`
  - `market_access_datasets.dataset_size`
  - `market_access_datasets.dataset_relevance`

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

## `market_access_datasets`

For 70+ healthcare or life-sciences data vendors relevant to market access, HEOR, reimbursement, commercialization, or related evidence generation, name the vendor and at least 1+ named qualifying datasets per vendor along with what kind of data product each is, supplying a source URL (at least 1 per dataset) whose page content supports the dataset claim.

Requirements:
- The page must clearly support the claimed vendor-dataset pairing.
- The claimed description must match what the page conveys about the dataset.
- The dataset must be a named data product rather than a vague unnamed capability or arbitrary sub-feature.
- The page must be more than a generic consulting/analytics service offering with no identifiable dataset product.

Write one JSON object per line to `results_market_access_datasets.jsonl`:
{"item": { "vendor": "<vendor>", "dataset": "<dataset>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `market_access_datasets.dataset_size`

Cross-tasknode identifier discipline: this task is for the same {= vendor_dataset =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= vendor_dataset =}+ datasets, find a source supporting the size, breadth, or scale of each — at least 1 URL per dataset.

Requirements:
- The claimed size must match what the page shows for this dataset.
- The size claim must be concrete (patients, lives, claims, prescriptions, providers, sites, etc.) — not vague marketing language.
- The size evidence must be specific to the claimed dataset, not aggregate vendor-level scale that doesn't bind to this dataset.

Write one JSON object per line to `results_market_access_datasets.dataset_size.jsonl`:
{"item": { "vendor": "<vendor>", "dataset": "<dataset>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `market_access_datasets.dataset_relevance`

Cross-tasknode identifier discipline: this task is for the same {= vendor_dataset =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= vendor_dataset =}+ datasets, find evidence that each is relevant to market access, HEOR, reimbursement, commercialization, or closely related real-world evidence workflows — at least 1 URL per dataset.

Requirements:
- The claimed relevance must match what the page articulates about the dataset.
- The page must explicitly connect the dataset to market access, HEOR, reimbursement, commercialization, or closely related evidence-generation work — not just describe it as generic healthcare data.
- The relevance evidence must be specific to the claimed dataset, not broad vendor positioning that doesn't bind to this dataset.

Write one JSON object per line to `results_market_access_datasets.dataset_relevance.jsonl`:
{"item": { "vendor": "<vendor>", "dataset": "<dataset>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

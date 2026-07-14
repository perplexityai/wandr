You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `indie_bookstore_imprints`
  - `indie_bookstore_imprints.imprint_titles`

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

## `indie_bookstore_imprints`

For 30+ (bookstore, imprint) pairs, name the bookstore, the imprint, and the city of operation, supplying corroboration (2+ URLs per pair). Each (bookstore, imprint) pair must be a real *independent* bookstore that's currently operating and runs an active publishing imprint with original titles or substantive new editions of out-of-print works (reprints / new translations under the imprint's name count).

Each URL must be a page that supports the dual identity for that pair (the bookstore-publisher's own About / Publishing / Imprint page, a trade-press article in a literary publication, an encyclopedia article on the bookstore that confirms the publishing arm, or a retailer / distributor page showing the imprint as an active publisher).

Requirements:
- The page must support that the named bookstore is currently operating (current physical or web retail presence reflected in the page's content).
- The page must support that the bookstore is independent — privately or locally owned, not a corporate retail chain or chain affiliate.
- The page must support that the named imprint is currently active — i.e. has an editorial program with a stated catalog, submissions process, or recent acquisitions, not dormant or wound-down.

Write one JSON object per line to `results_indie_bookstore_imprints.jsonl`:
{"item": { "bookstore": "<bookstore>", "imprint": "<imprint>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `indie_bookstore_imprints.imprint_titles`

Cross-tasknode identifier discipline: this task is for the same {= bookstore_imprint =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= bookstore_imprint =}+ (bookstore, imprint) pairs, supply 3+ original titles per pair, published by the imprint with publication year 2020 or later and grounded by a dedicated book page (1+ URL per title). Each title must be a real published book with the named imprint as its publisher (placeholders, announced-but-not-published titles, cancelled / withdrawn books, and pure distribution / reseller relationships don't qualify; reprints and new translations of out-of-print works count when the imprint is the named publisher of the new edition).

Each URL must be the title's own dedicated book page — a publisher catalog entry for this specific book, the imprint's own product page, an authoritative library record, or a major-retailer book detail page that lists the publisher. Do not use a listicle, a roundup blog post that mentions the title in passing, or an aggregator's catalog index that lists many titles.

Requirements:
- The page must identify the named imprint as the publisher of this specific title AND support a publication year of 2020 or later.
- The page must be the title's own dedicated book page, not an aggregate listing.

Write one JSON object per line to `results_indie_bookstore_imprints.imprint_titles.jsonl`:
{"item": { "bookstore": "<bookstore>", "imprint": "<imprint>", "title": "<title>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

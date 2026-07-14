You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `gpu_benchmarks`
  - `gpu_benchmarks.gpu_prices`
  - `gpu_benchmarks.game_reviews`

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

## `gpu_benchmarks`

For 20+ GPUs (CPUs / APUs / integrated graphics out of scope) and 10+ games per GPU, find a source-backed FPS benchmark result (1+ URL per gpu-game pair) from a benchmark or review page. Note: reported game titles must be real released video games, and the source must be first-hand benchmarking (not a second-hand mention citing someone else's numbers).

Requirements:
- The benchmark on the page must be for the claimed GPU model.
- The benchmark on the page must be for the claimed game title.
- The page must confirm a concrete FPS score claim.

Write one JSON object per line to `results_gpu_benchmarks.jsonl`:
{"item": { "gpu": "<gpu>", "game": "<game>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `gpu_benchmarks.gpu_prices`

Cross-tasknode identifier discipline: this task is for the same {= gpu =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= gpu =}+ GPUs (CPUs / APUs / etc out of scope), find current US street prices from retailer product pages — at least 3 different pages per gpu.

Each page must be an actual retailer listing dedicated a specific GPU — not a price comparison page / aggregation / review site with price mentions / "best deals" roundup / etc — and show a current purchasable price.

Requirements:
- The page must be for the claimed GPU model — same family AND same tier (RTX 4090 ≠ RTX 4080; GeForce RTX ≠ Radeon RX). SKU variants (Gigabyte, MSI, ASUS, Founders) are okay and considered a model match.
- The page must show a concrete current price for the specific GPU SKU — not "out of stock" without price or a bundled price or a price for an adjacent SKU and so on.

Write one JSON object per line to `results_gpu_benchmarks.gpu_prices.jsonl`:
{"item": { "gpu": "<gpu>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `gpu_benchmarks.game_reviews`

Cross-tasknode identifier discipline: this task is for the same {= game =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= game =}+ games, find community or critic ratings from review source pages, at least 3 distinct sources per each game. Target pages are first-hand review-offering sources with review scores as the (one of) central focus(es); these would include review aggregators, dedicated single-game reviews, storefronts for specific game titles with a visible rating score and so on, not "top games" list articles / news articles talking primarily about releases or similar while mentioning some review scores in passing / community-discussion-only threads offering personal ratings and impressions through user messages / etc. Both user aggregate and critic scores will do, same as numeric ("85/100", "9.2/10") vs categorical ("Mixed bag" / "A-tier") ratings. Note: reported games must genuinely be real video game titles not e.g. tech demos or similar.

Requirements:
- The page must clearly identify the claimed game title.
- The page must show a concrete recognizable rating for the game.

Write one JSON object per line to `results_gpu_benchmarks.game_reviews.jsonl`:
{"item": { "game": "<game>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

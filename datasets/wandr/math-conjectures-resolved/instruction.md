You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `math_conjectures_resolved`
  - `math_conjectures_resolved.pop_science_coverage`

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

## `math_conjectures_resolved`

For 30+ named mathematical conjectures or named open problems completely resolved (either proved or disproved) during 2001-2026, name the resolving paper or work, the resolver(s), and the year of resolution, supplying a source (1+ URL per conjecture) on an *official-origin* page that establishes the resolution. Pages qualifying as official-origin are pages on the surface of the resolution itself: the publishing journal's article landing page, an authoritative mathematics archive hosting the resolving paper, an institutional repository or faculty page of the resolver(s), the proceedings of a learned society announcing the result, or a comparably authoritative primary surface.

Requirements:
- The page must announce the conjecture as completely resolved.
- The page must indicate the resolution year falls within 2001-2026.
- The page must communicate (possibly via URL among other things) that it is an official-origin surface for the resolution — the publishing journal, an authoritative mathematics archive hosting the resolving paper, the resolver's institutional repository or faculty page, the proceedings of a learned society announcing the result, or a comparably authoritative primary surface.
- The page must identify both the resolving paper or work and the resolver(s).

Write one JSON object per line to `results_math_conjectures_resolved.jsonl`:
{"item": { "conjecture": "<conjecture>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `math_conjectures_resolved.pop_science_coverage`

Cross-tasknode identifier discipline: this task is for the same {= conjecture =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= conjecture =}+ named mathematical conjectures or named open problems, supplying sources (3+ URLs per conjecture) on popular-science or science-news write-ups substantively about the resolution. The bar is lay-readable journalism about the resolution — a science-journalism outlet, a learned-society popular explainer, a mathematician's lay-readable blog post, or a comparable lay-audience surface — written with editorial framing and authorial voice, not the resolving paper itself, not an encyclopedic restatement, and not a press release rephrasing the abstract.

Requirements:
- The page must communicate (possibly via URL among other things) that it is popular-science or science-news coverage written for a non-specialist audience.
- The page must substantively be about the resolution — communicate that the named conjecture was resolved and name the resolver(s).

Write one JSON object per line to `results_math_conjectures_resolved.pop_science_coverage.jsonl`:
{"item": { "conjecture": "<conjecture>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

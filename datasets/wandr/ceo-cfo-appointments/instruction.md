You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `ceo_cfo_appointments`
  - `ceo_cfo_appointments.company_listings`

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

## `ceo_cfo_appointments`

For at least 70+ US-based companies (headquartered or principally operating in the United States), name a CEO or CFO appointed at the company with the announcement landing within March 1 through April 30, 2026 (1+ appointments per company needed), and supply at least 1 URL on an authoritative-source page substantiating each of the appointments provided.

Requirements:
- The page must identify the claimed company.
- The page must name the claimed appointee in the claimed role (CEO or CFO), with name and role pinned in the same announcement context.
- The page must establish that the announcement — the company's first public disclosure of the appointment — falls within March 1 through April 30, 2026. Not the effective date; pre-announced future-effective transitions count when the announcement is in window.
- The page communicates (possibly via URL among other things) that it is on the issuer's primary distribution channel (e.g. regulatory filing, the company's controlled web property, an authored press release distributed through a recognized newswire, and so on) or a directly-attributed first-hand business-journalism page.

Write one JSON object per line to `results_ceo_cfo_appointments.jsonl`:
{"item": { "company": "<company>", "appointee": "<appointee>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `ceo_cfo_appointments.company_listings`

Cross-tasknode identifier discipline: this task is for the same {= company =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= company =}+ companies, supply at least 1 URL on a recognized listing-authority surface showing that the company has primary or secondary listing on a US national securities exchange (NYSE, NASDAQ, NYSE American, NYSE Arca) or is a US-domiciled SEC-Exchange-Act-reporting issuer.

Requirements:
- The page must identify the claimed company.
- The page must communicate (possibly via URL among other things) recognized listing-authority authorship.
- The page must show the company having primary or secondary listing on a US national securities exchange or being a US-domiciled SEC-Exchange-Act-reporting issuer.

Write one JSON object per line to `results_ceo_cfo_appointments.company_listings.jsonl`:
{"item": { "company": "<company>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

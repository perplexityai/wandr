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

## `nm_immigration_enforcement`

For at least 80+ distinct federal-immigration-enforcement actions in or affecting New Mexico — via a *well-identified* enforcement event (criminal charge or indictment, sentencing, arrest operation, deportation flight, detention-facility decision, federal court ruling, county or state government action enabling federal enforcement coordination, etc.) — within March 1-24, 2026, name the actor and the concrete action, and supply a source (i.e., 1+ URLs per action) substantiating the (actor, action) pair.

Requirements:
- The page must identify the named entity as a federal-immigration-enforcement authority or as a federal-cooperating government actor taking an enforcement-enabling action.
- The page must describe a concrete federal-immigration-enforcement action — a charging, sentencing, arrest, raid, removal, detention-facility decision, federal court ruling on an immigration matter, or formal cooperation action operationally enabling federal enforcement. Pure protest events, advocacy or analytic commentary, and government actions purely restricting or rejecting federal enforcement do not qualify.
- The page must establish the action's New Mexico nexus — the action took place in New Mexico, was charged by a New Mexico federal-district authority, materially involved New-Mexico-located parties or facilities, or was rendered by a federal court directly affecting New-Mexico-pending matters.
- The page must establish that the action's primary date — the charging or sentencing date, the operation or operation-end date, the ruling-issuance date, the flight date, the contract or vote date, or the week-ending date for periodic compilation reports — falls within March 1-24, 2026. The article's publication date may lag the action by days; what counts is the action's date itself. Republications or retrospective coverage of pre-window actions do not qualify.

Write one JSON object per line to `results_nm_immigration_enforcement.jsonl`:
{"item": { "actor": "<actor>", "action": "<action>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

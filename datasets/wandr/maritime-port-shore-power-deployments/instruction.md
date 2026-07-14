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

## `maritime_port_shore_power_deployments`

For 50+ maritime ports, supply at least 2+ named maritime shore-power deployments per port and at least 1+ official/operator/government URL for each deployment.

A port is identified by `country` and `port`. A deployment is identified by `country`, `port`, `facility_or_quay_or_terminal`, and `vessel_segment`: the page-named port location plus the commercial vessel segment served there. Use the physical label the page actually names; do not invent finer berth or quay numbers from an aggregate terminal or area claim. Dates, voltage, frequency, capacity, funding, vendors, and first-vessel details can be useful supporting facts, but they are not part of the deployment identity.

Final evidence must be on an official or operator-controlled surface: port authority, terminal operator, government/regulator, public funding/program page, official sustainability or OPS page, official tender/project page, or official report. Vendor pages, news articles, encyclopedias, directories, unaffiliated consultant summaries, and general port-technology explainers do not count. Small commercial passenger or archipelago-vessel deployments count when the location and vessel segment are named; private leisure-marina shore-power pedestals do not.

Requirements:
- The page must identify the submitted port context and named facility, quay, berth, terminal, or equivalent deployment location.
- The page must state that shore power, onshore power supply, OPS, cold ironing, or an equivalent ship-to-shore electrical connection is available, commissioned, used, funded, procured, under construction, expanded, or scheduled for that specific deployment location. Planned, funded, or otherwise not-yet-operational deployments need an active official stage with a concrete date, target year, or dated milestone that is not stale as of 2026-06-20.
- The page must tie the submitted deployment location to the submitted commercial vessel segment.

Write one JSON object per line to `results_maritime_port_shore_power_deployments.jsonl`:
{"item": { "country": "<country>", "port": "<port>", "facility_or_quay_or_terminal": "<facility_or_quay_or_terminal>", "vessel_segment": "<vessel_segment>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

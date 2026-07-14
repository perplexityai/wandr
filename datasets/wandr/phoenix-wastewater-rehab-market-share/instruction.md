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

## `phoenix_wastewater_rehab_market_share`

Phoenix-area wastewater utility procurement officers need a defensible public-contract ledger before estimating vendor share.

For at least 155+ public contract actions in January 1, 2020 through May 12, 2026, name the firm, the action, the municipal or public-utility customer/facility, the action date or active period, the firm's role and rehabilitation scope, and any public dollar value, contract ceiling, task-order amount, selected-firm list, award number, agreement number, or other win-count signal. Supply at least 1 public URL for each action.

Rows may cover engineering/design, construction, CMAR, JOC, condition assessment, sewer or manhole rehabilitation, lift-station rehabilitation, water-reclamation-plant rehabilitation, wastewater-treatment upgrades, and closely related municipal wastewater renewal work for Phoenix-area Arizona public wastewater utilities. Exact market-share percentages are not required; public values, ceilings, and win-count evidence are the basis for later estimates, and not-to-exceed ceilings should not be represented as realized revenue.

Use admissible public sources directly about the action, such as public-agency procurement or council records, utility or project pages, official firm project pages, and similar public coverage. Generic capability pages, office pages, directories, search-result pages, and market-summary pages do not count.

Requirements:
- The page must tie the named firm to the named contract action or project in a real role such as engineering, design, construction, CMAR, JOC contractor, inspection, condition assessment, public outreach, operations, rehabilitation, repair, replacement, or upgrade services.
- The action must concern Phoenix-area Arizona public wastewater infrastructure rehabilitation, renewal, repair, replacement, condition assessment, inspection, construction administration, or upgrade work.
- The page must establish an action date, project date, active-work period, award date, amendment date, or completion date in January 1, 2020 through May 12, 2026, and identify the public municipal, regional, tribal, or utility customer or facility.
- The page must provide a market-share weighting signal such as a dollar value, fee, bid amount, contract ceiling, GMP, change order, amendment amount, project cost, selected-firm list, award/agreement number, JOC ceiling, or comparable public win-count signal.

Write one JSON object per line to `results_phoenix_wastewater_rehab_market_share.jsonl`:
{"item": { "firm": "<firm>", "contract_action": "<contract_action>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

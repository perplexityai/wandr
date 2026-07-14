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

## `cee_heat_operator_regulation`

For each of the 6 countries listed below, supply official regulatory evidence for 9+ current district-heat operators in that country on each of the 2 evidence sides (1+ URL per operator-side pair).

The focus is public district-heat regulation in Central and Eastern Europe: active operating authority paired with a currently operative regulated-service footprint, tariff, asset, or equivalent official signal.

Countries in scope:
- **Slovakia**
- **Czechia**
- **Poland**
- **Lithuania**
- **Latvia**
- **Croatia**

Evidence sides:
- `authorization`: current formal authority to operate in the heat sector
- `regulated_service`: current or operative regulated heat-service scope, pricing, asset, system, or customer evidence rather than bare operating authority

Use official regulator, government, official-gazette, municipal-government, or regulator-published records, decisions, registers, datasets, or PDFs. Company websites, news, procurement portals, map services, private data mirrors, scraped directories, and generic sector summaries do not count.

Requirements:
- The page must clearly identify the named operator and tie it to the claimed country's regulated heat sector.
- The page must fit the evidence side: `authorization` needs a licensing, permission, registration, concession, permit, or regulator-recognition source; `regulated_service` needs a tariff / price, service-scope, territory, asset, system, customer, or comparable official regulated-service source.
- The page must show the authority or regulated-service evidence is current, active, valid, or operative for the cited side. Revoked, cancelled, expired, superseded-only, or purely historical permissions and service records do not count.
- The page must expose an official native reference for the cited side, such as a license / permit / concession number, register entry, decision number or date, dataset snapshot, official table entry, or comparable regulator-native anchor.
- The page must expose a tangible heat-service detail beyond the operator name: an activity type, named territory, permit status, tariff / price value or period, heat-production or distribution asset, customer / system footprint, or similar service-specific detail.

Write one JSON object per line to `results_cee_heat_operator_regulation.jsonl`:
{"item": { "country": "<country>", "operator": "<operator>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `resolved_prediction_markets`

For at least 100+ resolved prediction markets — `(platform, market_question)` tuples on Polymarket or Kalshi that resolved within January 2025 through April 2026 — gather 2 evidence rows per market (at least 1 per row): one establishing the platform's resolution outcome (with date and criterion reference) and one establishing the actual real-world outcome the market was tracking (with the date the event occurred or was officially confirmed).

For each market, provide one row with `evidence_type = "platform_resolution"` and one with `evidence_type = "real_world_outcome"`.

- For `platform_resolution` rows: the URL must be the specific market's event page on the platform (polymarket.com or kalshi.com); the page must show the market as resolved with a clear outcome (Yes / No / specific bracket value), and surface either the resolution date or the criterion-text indicating the resolution. Help-center / FAQ / docs / dashboard / third-party-analytics-mirror pages do not qualify.
- For `real_world_outcome` rows: the URL must be an external authoritative source describing the actual real-world event the market was tracking — major news outlets (e.g. NYT, Reuters, Bloomberg, AP, NPR, BBC, Politico, WaPo), specialist news (e.g. ESPN / NBA.com for sports, federalreserve.gov for Fed decisions, supremecourt.gov for SCOTUS rulings, official sports federations), Wikipedia / Britannica / official government records. For markets resolving on quantitative data sources (e.g. crypto closing prices), specialist financial-data-aggregator pages also qualify. Polymarket / Kalshi pages themselves do not qualify for this arm — the platform is the platform-side authority, not an independent verification of reality.

Each `(platform, market_question)` tuple must reference a recognizable platform name (Polymarket or Kalshi) and a real, distinct market that actually resolved on that platform within January 2025 through April 2026. Each row's `evidence_type` must be either `platform_resolution` or `real_world_outcome`.

The temporal scope is bound: only markets whose resolution falls within January 2025 through April 2026 are in scope. Markets that are still active, were cancelled / voided / refunded, or resolved outside that window do not qualify.

For each row, include in `answer`:
- `outcome` (str) — for `platform_resolution`: the platform's resolution value (e.g. "Yes", "No", "$125,000+"). For `real_world_outcome`: a brief description of what actually happened (e.g. "Trump won the 2024 election", "no rate change at January 2025 FOMC").
- `date` (str, YYYY-MM-DD where possible) — for `platform_resolution`: the resolution date. For `real_world_outcome`: the date the event occurred or was officially confirmed.
- `brief_description` (str) — a one-sentence summary of what the page says, to anchor the evidence for downstream consumption.

Requirements:
- The page's source class must match the row's `evidence_type` — the platform's specific market page for `platform_resolution`, or an external authoritative source for `real_world_outcome`.
- The page must document the outcome appropriate for the row's `evidence_type` — the platform's resolution value and closed status for `platform_resolution`, or the real-world event description for `real_world_outcome`.
- The page must anchor a date appropriate for the row's `evidence_type` — the resolution date for `platform_resolution`, or the event-occurrence date for `real_world_outcome`. Year minimum, month strongly preferred.

Write one JSON object per line to `results_resolved_prediction_markets.jsonl`:
{"item": { "platform": "<platform>", "market_question": "<market_question>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

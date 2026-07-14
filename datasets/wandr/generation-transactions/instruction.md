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

## `generation_transactions`

For at least 225+ U.S. electric-generation ownership-change events with a source-stated milestone from 2010-01-01 through 2026-06-30, identify at least 1+ affected asset, fleet, generation portfolio, or generation operating company per event, and supply at least 1+ source URL for each of the 3 evidence roles. This is public transaction provenance for generation ownership/control, not investment advice, valuation, power-price forecasting, procurement guidance, ranking, lead scoring, contact enrichment, or legal advice.

The submitted event can involve:
- announcement of a definitive transaction or reorganization.
- regulatory approval or authorization.
- transaction close or completion.
- effective date.
- divestiture or transfer.
- merger.
- bankruptcy emergence.
- court-confirmed reorganization.

The affected asset or entity can be a:
- electric generating plant or facility.
- fleet or named group of plants.
- generation portfolio.
- generation operating company.
- project company or generation asset holding company.
- merchant, IPP, utility, or retail-integrated generation business when generation ownership/control is part of the event.

The evidence roles are:
- `event_status_record`: a public source that identifies the transaction, reorganization, transfer, merger, divestiture, bankruptcy emergence, or comparable event, names the parties or predecessor/successor entities, and states a milestone status or date.
- `authority_or_filing_record`: an official, regulatory, filing, court, market-monitor, state commission, SEC, FERC, bankruptcy, or comparable authority record addressing the event.
- `asset_lineage_detail`: a source that identifies at least one affected plant, fleet, generation portfolio, or generation operating entity and ties it to seller/predecessor/target and buyer/successor/post-event owner or control context.

Optional factual notes can include source-stated status/date, buyer/successor, seller/predecessor/target, plant or portfolio names, generation operating entity, capacity, fuel type, region, ISO/RTO, deal value, source class, source date, and checked date. Use 2026-06-30 as the checked date unless the source was checked later; include optional facts only when source-stated.

Boundary classes to keep out unless the page also proves event-specific generation transaction lineage:
- rumored, discussed, exploratory, or market-speculation items with no source-stated transaction milestone.
- retail-only customer-book or brand acquisitions with no generation asset or generation operating entity.
- generic current owner/operator, EIA, eGRID, FERC MBR, or annual-report asset entries without event lineage.
- investment advice, valuation, stock-reaction, power-price forecast, procurement, ranking, lead-scoring, contact, or outreach material.
- broad database landing pages, search pages, or source hubs that do not identify the submitted event.

Requirements:
- The page must tie the submitted event to a U.S. electric-generation ownership or control change involving a generation asset, plant, fleet, generation portfolio, generation operating company, or project/asset holding company, with source-stated parties or predecessor/successor context.
- The page must fulfill the submitted `evidence_role`: `event_status_record` must identify the parties and a source-stated status or date; `authority_or_filing_record` must be an official, regulatory, filing, court, market-monitor, state commission, SEC, FERC, bankruptcy, or comparable authority record; `asset_lineage_detail` must identify at least one affected plant, fleet, generation portfolio, or generation operating entity and tie it to seller/predecessor/target and buyer/successor/post-event owner or control context.
- The page must connect the submitted `affected_asset_or_entity` to the submitted event at the submitted granularity, or to the deal-level portfolio, target, generation operating entity, or successor/predecessor context that the submitted asset/entity names.

Write one JSON object per line to `results_generation_transactions.jsonl`:
{"item": { "generation_transaction_event": "<generation_transaction_event>", "affected_asset_or_entity": "<affected_asset_or_entity>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

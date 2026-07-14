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

## `transit_procurement_items`

For 30+ agencies, cover each of the 3 pipeline stages listed below with 3+ public procurement or project-status items per agency/stage; for each agency/stage/item, supply a source (i.e. 1+ URL) that gives source-stated evidence within January 1, 2025 through December 31, 2026 for transit electrical, rail systems, signaling, communications, low-voltage, traction power, OCS, train control, EV charging/fueling, or closely related transit infrastructure work.

The task is a public-record provenance atlas, not a contractor comparison scorecard: named contractors and values are useful only when the cited page states them.

Pipeline stages:
- `forecast`: a forecasted, upcoming, lookahead, planned, or pre-solicitation item.
- `active_or_advertised`: an active, open, advertised, recently posted, or due-soon solicitation / bid / RFP / IFB / opportunity.
- `award_or_status`: an award, board or committee action, contract action, notice-to-proceed, construction/project status update, change order, or comparable post-advertisement public status signal.

Agencies ought to be public transit, rail, commuter-rail, public transportation, or transit-infrastructure owner/operator/delivery bodies in North America. A pipeline item ought to be a specific project, contract, solicitation, procurement package, task-order/action, or source-stated status entry, not a whole agency, generic contact page, vendor directory, broad capability page, or undifferentiated capital program. The source should be public, accessible, and usable; source-stated projected or preliminary dates, TBD statuses, and revision caveats are fine when the page itself carries them. Contractor rankings, capacity comparisons, bid strategy, buyer targeting, contact discovery, outreach, supplier recommendation, price benchmarking, legal/procurement advice, engineering/compliance instructions, and safety adequacy conclusions are outside the task.

Requirements:
- The page must identify the named agency and the specific project, contract, solicitation, procurement package, or status item.
- The page should make its source role visible for the selected `pipeline_stage`: for `forecast`, agency-controlled or agency-officially-linked forecast / lookahead / procurement-plan authority; for `active_or_advertised`, official active-solicitation or advertised-opportunity posture, including publicly fetchable procurement-platform pages visibly tied to the agency and item; for `award_or_status`, official agency action/status authority or independent public status authority directly tied to the agency/project relationship.
- The page must state the lifecycle posture appropriate to `pipeline_stage`: preliminary/upcoming/planned for `forecast`, open/active/advertised/posted/due for `active_or_advertised`, or awarded/approved/authorized/under contract/changed/under construction/status-updated for `award_or_status`.
- The page must provide a source-stated date, quarter, month, deadline, action date, update date, or status-date signal that places the item within January 1, 2025 through December 31, 2026; for forecast items, a projected future 2026 advertisement or procurement period can count when it is stated by the source.
- The page must give concrete in-scope transit electrical/systems detail for the item, such as traction-power, signal, OCS, train-control, communications, low-voltage, electrical, charging/fueling, SCADA, system-integration, cable, substation, or comparable transit-infrastructure scope paired with item detail such as a contract/RFP number, route/facility, due date, status, value/range, named contractor when stated, board authorization, work description, or similar page-stated datum.

Write one JSON object per line to `results_transit_procurement_items.jsonl`:
{"item": { "agency": "<agency>", "pipeline_stage": "<pipeline_stage>", "item_name": "<item_name>", "item_reference": "<item_reference>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

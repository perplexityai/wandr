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

## `us_solar_manufacturing`

Identify 60+ facilities as U.S. solar manufacturing facilities or expansions that were publicly operating or publicly announced by April 13, 2026; for each named facility, cover each of the 4 evidence axes below by supplying a facility-specific public source (i.e. 1+ URL under each axis).

The interest is facility-specific public provenance for domestic solar supply-chain manufacturing, not a national directory, project portfolio, safety advice, procurement advice, risk rating, investment advice, or contact lookup.

Evidence axes:
- `status_or_capacity`: operating, under construction, announced, expanding, capacity, production scale, target opening, or similar facility-status evidence.
- `manufacturing_segment_or_technology`: module, cell, ingot/wafer, polysilicon, solar glass, tracker/racking, inverter, recycling, or other solar-supply-chain product or technology tied to the facility.
- `public_authority_finance_or_regulatory_signal`: DOE/LPO, state or local economic-development release, public incentive, permit, regulator, OSHA/DOL, environmental filing, bond, loan, or comparable public-authority trace tied to the facility.
- `supply_chain_customer_or_partner_signal`: named customer, supplier, partner, buyer, technology provider, equipment provider, input/output supply agreement, or customer agreement tied to the facility's manufactured output, input supply, technology, equipment, or facility-specific manufacturing program.

The named facility ought to identify an operator, facility/site/plant/expansion, locality, and state, and ought to be a manufacturing facility or expansion in the solar supply chain. Solar farms, BESS projects, developer portfolios, installer branches, warehouses, and generic corporate offices do not count. Broad national maps, dashboards, all-in-one manufacturer lists, and generic corporate-capacity or customer pages are discovery/calibration context rather than qualifying source pages, unless the URL is facility-dedicated or the page is a facility-specific document, announcement, profile, permit, filing, or comparable record that cannot reasonably collapse across many facilities and evidence axes.

Requirements:
- The page must clearly identify the submitted facility or operator and tie the evidence to the submitted U.S. locality and state.
- The page must make the relevant facility-specific fact public, true, or announced no later than April 13, 2026; a later-published page works only when it explicitly supports a fact that had already been true or publicly announced by then.
- The page should make its evidence-axis source role visible while remaining facility-specific in the sense above. For `status_or_capacity`, it should read as a facility announcement, operation, construction, expansion, or capacity source; for `manufacturing_segment_or_technology`, it should tie a specific solar supply-chain product or technology to the facility; for `public_authority_finance_or_regulatory_signal`, it should communicate a public authority, public finance, incentive, permit, inspection, regulator, or comparable official trace; for `supply_chain_customer_or_partner_signal`, it should identify a named customer, supplier, partner, buyer, technology provider, equipment provider, or customer/input/output supply agreement tied to the submitted facility's manufactured output, input supply, technology, equipment, or facility-specific manufacturing program.
- The page should expose a concrete finding for the selected evidence axis, clearly scoped to the submitted facility. For `supply_chain_customer_or_partner_signal`, operator-level relationship evidence works only when the page explicitly maps the relationship to the submitted facility, or when the operator has a single relevant U.S. manufacturing facility and the locality/state binding is still clear.

Write one JSON object per line to `results_us_solar_manufacturing.jsonl`:
{"item": { "operator": "<operator>", "facility": "<facility>", "locality": "<locality>", "state": "<state>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

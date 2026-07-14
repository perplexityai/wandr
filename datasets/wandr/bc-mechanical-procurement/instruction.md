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

## `bc_mechanical_procurement`

For 30+ BC Interior public-sector authorities that issue or own facility, construction, operations, utilities, health, education, housing, recreation, or infrastructure procurements, name an official procurement source surface for each authority and supply 3+ concrete procurement/source-state records on that surface, each with 1+ official URL.

Use an Okanagan-heavy BC Interior lens rather than a current-open tender tracker. BC Interior means the Okanagan/Similkameen core and adjacent Interior BC regions such as Thompson-Shuswap, Kootenay, and Cariboo. Local and regional Interior authorities count directly; province-wide public owners count only when the cited surface or record is tied to BC Interior facility or procurement activity. Closed, awarded, cancelled, stale, access-gated, unavailable-document, no-public-document, no-current-opportunity, no-mechanical, and undetermined records are useful when the public evidence supports the state. The work is an official public-source atlas, not contractor lead generation.

Valid evidence surfaces include official public-owner pages, BC Bid public pages, officially delegated owner procurement portals, official tender/PDF/project pages, official award or bid-result pages, and owner-controlled pages explaining procurement access or award disclosure. Discovery-only sources such as CivicInfo, BidCentral/SICA, MERX, ConstructConnect, CivicIQ, GlobalTenders, BidAssist, plan rooms, private bid-intelligence services, contractor self-promotion, and search snippets do not count unless the cited page itself is an official owner or officially delegated source.

Do not include personal contacts, planholders, bid strategy, inferred GC/CM outreach, or private lead intelligence. An awarded organization is useful only when an official public owner or official award surface lists it.

Requirements:
- The page must communicate that the cited URL is an official public-owner or officially delegated procurement/source surface for the named authority.
- The page must identify a named solicitation, tender, RFP, RFQ, ITT, award, cancellation, result, official project/tender document, no-current-opportunity row, or comparable concrete official procurement/source-state record tied to the procurement universe. A generic access map or source-surface policy page does not satisfy this record requirement by itself.
- The page must communicate a source-state fact for the record, such as status/currentness, document access, registration/payment/subscription barrier, prequalification/threshold routing, award disclosure, cancellation, stale listing, unavailable document, no-public-document, no-current-opportunities, or similar public procurement state. Current, stale, no-current, access-gated, and other time-sensitive source-state claims must be anchored by a page status date or checked date.
- The page must support the submitted mechanical-scope classification from public scope or access text: mechanical, HVAC, plumbing, controls, refrigeration, pumps, heat-recovery, no mechanical scope after review, or undetermined because public scope/documents are unavailable or gated. A title alone does not establish positive mechanical scope.

Write one JSON object per line to `results_bc_mechanical_procurement.jsonl`:
{"item": { "authority": "<authority>", "source_surface": "<source_surface>", "procurement_record": "<procurement_record>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

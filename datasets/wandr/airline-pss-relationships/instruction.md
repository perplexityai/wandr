You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `airline_pss_relationships`
  - `airline_pss_relationships.independent_confirmation`

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

## `airline_pss_relationships`

For 280+ source-stated public relationships between an airline/operator and a passenger-system platform vendor/product, supply 1+ vendor/platform-controlled public URL that proves both the airline/vendor relationship and the passenger-system or close passenger commercial-system scope.

The research unit is the public relationship/event, not a vendor ranking, procurement recommendation, or current-customer table. As checked on 2026-06-30, old public announcements count as historical relationship/event evidence; current operational use should only be treated as current when the cited page itself says so.

The `airline_platform` identity should name one airline/operator, one vendor, and one platform or product family. Airline-group announcements can support operating carriers only when the page names the covered carriers or otherwise makes the covered operator set explicit.

Vendor annual reports, vendor press releases, vendor relationship lists, vendor case studies, vendor-hosted announcements, and vendor-issued wire releases can count only once for a relationship: the page either proves the relationship-plus-scope claim as one vendor-controlled source, or it does not. Do not duplicate a single page as separate event proof and scope proof for the same airline/platform relationship.

Do not use airline/operator-controlled pages, regulator/procurement/filing pages, reputable trade articles, implementation reports by another actor, or other independent public surfaces in this root task. Those sources belong in the `independent_confirmation` subtask and cannot satisfy this vendor/platform-controlled evidence role even if they prove the same relationship.

Do not use pages whose useful claim is only GDS/distribution, revenue-management-only, loyalty-only without passenger-system linkage, MRO or operations-only software, generic digital-transformation marketing, logo-wall/customer-list presence, anonymous case-study prose, market-share/ranking analysis, procurement advice, pricing, contact discovery, or private customer inference.

Requirements:
- Every counted page must bind the named airline/operator and the named vendor/platform or product family to the same public relationship. Generic vendor product catalogs, platform index pages, feature pages, logo walls, and reusable customer-list pages do not satisfy the relationship unless they also name or otherwise explicitly bind the submitted airline/operator to that same platform relationship.
- The page must state a selection, renewal, go-live, migration, expansion, implementation, contract/operational-use relationship, or comparable public relationship/event for the named airline/operator and vendor/platform.
- The same page must tie that named relationship to passenger-system or close passenger commercial-system scope, such as PSS, reservations, inventory, ticketing, departure control, check-in/boarding, booking engine, airline retailing, Offer-Order/NDC, disruption/reaccommodation, interline/codeshare, revenue accounting, or comparable passenger commercial-system scope.

For acquired product families or rebrands, the page must tie the submitted vendor to the submitted relationship. A page that names Radixx, Navitaire, or another acquired platform family but does not identify the submitted acquiring vendor in that relationship is not enough for a submitted Sabre, Amadeus, or other acquirer relationship.

Write one JSON object per line to `results_airline_pss_relationships.jsonl`:
{"item": { "airline": "<airline>", "vendor": "<vendor>", "platform": "<platform>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `airline_pss_relationships.independent_confirmation`

Cross-tasknode identifier discipline: this task is for the same {= airline_platform =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= airline_platform =}+ airline/operator passenger-system platform relationships, supply at least 1+ public URL from an operator, regulator, filing, reputable industry, implementation, migration/go-live, procurement/contract, or operational source that independently confirms the same airline/operator, vendor/platform, and passenger-system or close passenger commercial-system scope.

As checked on 2026-06-30, old implementation or migration evidence can count as historical confirmation. Current operational use should only be treated as current when the cited page itself says so.

The confirmation page must be meaningfully independent from the submitted vendor/platform's own relationship surfaces. Do not use vendor-controlled annual reports, relationship-list sections, vendor press releases or vendor-issued wire releases, case studies, generic platform/product pages, customer/logo pages, or anonymous case studies as the confirmation source. Airline/operator-controlled pages, public filings, regulator/procurement pages, reputable trade coverage, implementation/migration reports by a different actor, or public operational evidence can qualify when they bind the same relationship and platform scope.

Do not use pages whose useful claim is only GDS/distribution, revenue-management-only, loyalty-only without passenger-system linkage, MRO or operations-only software, generic digital-transformation marketing, market-share/ranking analysis, procurement advice, pricing, contact discovery, or private customer inference.

Requirements:
- The page must independently bind the named airline/operator, the named vendor/platform or product family, and passenger-system or close passenger commercial-system scope in the same relationship. Passenger-system scope can include PSS, reservations, inventory, ticketing, departure control, check-in/boarding, booking engine, airline retailing, Offer-Order/NDC, disruption/reaccommodation, interline/codeshare, revenue accounting, or comparable passenger commercial-system scope.

Write one JSON object per line to `results_airline_pss_relationships.independent_confirmation.jsonl`:
{"item": { "airline": "<airline>", "vendor": "<vendor>", "platform": "<platform>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

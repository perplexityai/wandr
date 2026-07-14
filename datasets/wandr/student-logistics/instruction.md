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

## `student_logistics`

For 120+ student-oriented belongings logistics services, supply evidence for each of the 3 evidence axes and at least 1+ URL per axis. Services can include official provider services or official campus programs that help students ship, store, forward, or deliver personal belongings for university, move-in, move-out, study-abroad, or term-break logistics.

The evidence axes are:
- `pricing_structure`: a public price signal for the student logistics service, such as an exact amount, range, starting price with scope, student discount, per-box / per-item / per-period rate, handling fee, surcharge, free allowance with overage fee, or public fee schedule.
- `capability_policy_fact_a`: one concrete capability or policy fact for the service, such as a coverage amount, weight or size rule, prohibited-item rule, customs process, storage term, delivery model, package allowance, carrier handoff, or campus / route scope.
- `capability_policy_fact_b`: a second concrete capability or policy fact for the service, preferably from a different operational facet than the other capability row.

For downstream reading, include the canonical service name, operator or institution, service family, geography or route scope, student-service scope, price signal and price basis when relevant, capability / policy fact and facet when relevant, source type, checked date, confidence, and relationship or limitation notes. Use 2026-06-29 as the checked date unless the source was checked later.

Useful service families include:
- `college storage / ship-to-school service`
- `dorm pickup, storage, and delivery service`
- `student luggage or box forwarding service`
- `international student shipping or excess-baggage service`
- `official university-operated or university-brokered move-in package program`
- `student logistics discount or rate program with official provider terms`

Useful public price signals include:
- `exact amount or range`
- `starting-from price with route, region, item, or unit basis`
- `student discount percentage or dedicated student pricing`
- `per-box, per-item, per-week, per-month, or per-period rate`
- `registration, handling, delivery, late, oversize, overweight, or storage fee`
- `free allowance with an overage fee`
- `published rate-card component or fee schedule`

Useful capability and policy facets include:
- `liability / coverage amount or enhanceable cap`
- `weight, size, item, packaging, or allowance rule`
- `prohibited, restricted, uncovered, or non-compensation item rule`
- `customs or international documentation process`
- `storage duration, storage location, or move-in / move-out timing`
- `pickup, dropoff, dorm delivery, in-room delivery, or warehouse handoff model`
- `campus, university, route, country, or service-area scope`
- `carrier partner, tracking, label, collection, or handling process`

Primary public sources should be provider-controlled or institution-controlled: official service pages, pricing pages, public booking pages with visible terms, FAQ / help-center pages, T&C or policy pages, public PDFs, official campus program pages, and official campus vendor / move-in pages. Aggregator listicles, affiliate blogs, coupon pages, ranking pages, customer reviews, generic carrier advice, generic self-storage pages, generic moving-company pages, and quote-request funnels are out of scope unless the cited row-specific content itself supplies official pricing or policy evidence for a student belongings logistics service.

Requirements:
- The page must identify the submitted service, provider, official campus program, or operator-controlled policy surface with enough context to distinguish it from unrelated same-name businesses, generic carriers, generic movers, ordinary mailrooms, lead generators, or broad advice pages.
- The page must fit the submitted `evidence_axis`: `pricing_structure` evidence should state a public price signal, while each capability / policy row should state a concrete service term, limit, allowance, restriction, process, geography, route, delivery model, or comparable operational fact.
- The page must preserve the fact's basis and scope. Pricing evidence should keep the source's amount, range, discount, fee, allowance, unit, route, region, item class, period, or overage condition; capability evidence should keep the source's concrete term, rule, amount, allowance, restriction, process, geography, route, or delivery model.

Write one JSON object per line to `results_student_logistics.jsonl`:
{"item": { "service": "<service>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `benelux_health_retailers`

For 12+ health, beauty, drugstore, pharmacy, personal-care, or wellbeing retailers with public BENELUX retail activity, cover 2+ distinct dated retail events per retailer. For each event, cover all 3 evidence sides below, each backed by 1+ URL.

Each `retail_event` should name a concrete event or change episode: first country entry, first city/store opening, specific store opening, relocation, closure, acquisition or rebrand affecting retail presence, pop-up or temporary format, or logistics/fulfillment change tied to BENELUX retail operations. The event label should preserve the retailer, event type, date or bounded period, country/place or BENELUX service scope, and status such as announced, planned, opened, closed, temporary, operational, or completed. Do not split one launch into separate events merely because one page is an announcement and another is opening-day coverage; those are corroborating sides for the same event.

The evidence sides are:
- `direct_actor_source`: retailer, parent company, official newsroom, investor page, official event announcement, or public official social post by the actor. Official locators, individual store pages, product/category pages, and ordinary navigation pages do not count.
- `independent_editorial_source`: retail trade, local/mainstream, business, or industry editorial coverage that independently reports the event. RetailDetail/RetailTrends-style articles can count here only.
- `place_operator_or_counterparty_trace`: shopping-centre/operator, landlord/property, municipality/public record, logistics/vendor, lease/development, or another named counterparty trace that ties the same event to a place, facility, project, opening, closure, launch, or operational status.

Same-URL reuse cannot fill multiple evidence sides for the same event. Syndicated, copied, translated, or same-family republications of the same report do not become separate corroboration. Publication date, checked date, announced date, planned event date, opening/operational date, closure date, and completed-project date should stay distinct; a future announcement counts only as a future or planned event.

Official store locators, individual store pages without event-specific support, product/category/navigation pages, maps, reviews, scraped SEO pages, opening-hours directories, generic mall tenant pages, paid market-report snippets, unsupported market-size pages, health or purchase advice, rankings, and strategy-only commentary do not count. Static tenant pages count as place/operator traces only when they visibly support the same dated event or status being submitted.

Requirements:
- The page must identify the retailer, banner, source-relevant parent, predecessor, or acquired/rebranded banner involved in the submitted event.
- The page must support the submitted event fact, such as the opening, entry, relocation, closure, acquisition/rebrand, temporary format, or logistics/fulfillment change.
- The page must tie the event to the Netherlands, Belgium, Luxembourg, a BENELUX aggregate, a BENELUX place/facility, or BENELUX retail-service scope.
- The page must support the event timing and status, distinguishing publication, announcement, planned, opening/operational, closure, temporary, or completed-project dates where the source makes that distinction.
- The page must expose source-side cues matching the submitted `evidence_side`, such as actor-owned announcement context, editorial reporting context, or operator/vendor/landlord/public-record/counterparty context tied to the event.

Write one JSON object per line to `results_benelux_health_retailers.jsonl`:
{"item": { "retailer": "<retailer>", "retail_event": "<retail_event>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

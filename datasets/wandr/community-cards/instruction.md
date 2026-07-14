You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `community_cards`
  - `community_cards.merchant_presence`

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

## `community_cards`

For 67+ public local/community stored-value programs tied to a city, downtown, chamber area, Main Street district, neighborhood, county, tourism district, campus, or comparable local area, cover each of the 3 program facets listed below by supplying a facet-substantiating source (i.e. 1+ URL per facet).

The purpose is public provenance for shop-local stored-value programs and their civic or organizational use contexts.

Program facets:
- `local_sponsor_or_operator`: a local sponsor, operator, public agency, downtown / chamber / Main Street / tourism / campus group, or comparable local organizer publicly presents or runs the named program.
- `stored_value_mechanics`: the named program is a gift card, eCard, community card, downtown dollars, voucher, bonus card, or comparable stored-value instrument spendable at participating local businesses.
- `organizational_or_public_use`: the named program has a public bulk, corporate, employee reward, government aid, tourism, university, sponsorship, local-recovery, giveaway, or comparable organizational / public-use path.

A valid `program` is a real public local/community stored-value program tied to a specific local area. Generic national gift-card marketplaces, broad reward catalogs, API or bulk-rewards tools, and platform-provider catalogs without a visible local program wrapper do not count. The `program_facet` value is exactly one of the three listed values. Provider-hosted pages can count only when they visibly concern the named local program rather than a generic provider catalog.

Requirements:
- The page must clearly identify the named program and its local community or area.
- The page must establish the facet-specific finding: for `local_sponsor_or_operator`, the local sponsor/operator/public-agency/downtown/chamber/Main-Street/tourism/campus or comparable organizer role; for `stored_value_mechanics`, the stored-value instrument and spendability at participating local businesses; for `organizational_or_public_use`, the public bulk, corporate, employee reward, government aid, tourism, university, sponsorship, local-recovery, giveaway, or comparable organizational / public-use path.
- The page must visibly earn the facet-appropriate source role: for `local_sponsor_or_operator`, local organizer or official local-program presentation; for `stored_value_mechanics`, program purchase, redemption, terms, participant-network, sponsor, or program-specific platform context; for `organizational_or_public_use`, public program-feature context rather than generic reward-catalog or sales-platform copy.

Write one JSON object per line to `results_community_cards.jsonl`:
{"item": { "community_or_area": "<community_or_area>", "program_name": "<program_name>", "program_facet": "<program_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `community_cards.merchant_presence`

Cross-tasknode identifier discipline: this task is for the same {= program =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= program =}+ public local/community stored-value programs tied to a city, downtown, chamber area, Main Street district, neighborhood, county, tourism district, campus, or comparable local area, cover 8+ participating local merchants per program and each of the 2 evidence sides listed below by supplying a side-substantiating source (i.e. 1+ URL per side).

The purpose is public proof that program-listed merchants are real local consumer-facing places with independent local context.

Merchant evidence sides:
- `program_participation`: the page identifies the named program and the named merchant as participating, accepting, redeeming, or listed in that program.
- `independent_merchant_local_presence`: the page identifies the same merchant and establishes its local geography and consumer category independently of the program participant listing.

A valid `merchant` is a real consumer-facing local business or local organization in the claimed program area, not the platform provider, a merchant category, a form field, or a generic marketplace brand. The `merchant_evidence_side` value is exactly one of the two listed values. A program participant listing can support several `program_participation` records when each merchant is visibly present; that same participant-list context does not establish `independent_merchant_local_presence`.

Requirements:
- The page must clearly identify the named merchant.
- The page must establish the evidence side in scope: for `program_participation`, the named program and named merchant as participating, accepting, redeeming, or listed in that program; for `independent_merchant_local_presence`, the same merchant's local geography and consumer category independent of the program participant listing.
- The page must make the side-appropriate source context visible: for `program_participation`, a program, sponsor, or program-specific platform/listing context; for `independent_merchant_local_presence`, merchant-owned, official social, local directory, local article, venue page, or comparable context outside the program participant list.

Write one JSON object per line to `results_community_cards.merchant_presence.jsonl`:
{"item": { "community_or_area": "<community_or_area>", "program_name": "<program_name>", "merchant": "<merchant>", "merchant_evidence_side": "<merchant_evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

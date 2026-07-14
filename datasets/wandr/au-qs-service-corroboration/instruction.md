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

## `au_qs_service_corroboration`

For each of the 3 quantity-surveying service domains listed below, cover 30+ Australian firm/location service listings; for each such (`service_domain`, `firm`, `location`) listing and each of the 2 evidence sides, supply a source (i.e. 1+ URL) that supports the same public firm/location service-domain claim.

The purpose is public professional-service claim provenance for Australian quantity-surveying practices, not tax advice, firm-quality comparison, or procurement recommendation.

Service domains:
- `tax_depreciation_or_property_depreciation`: tax depreciation schedules, property depreciation reports, depreciation schedules, or comparable QS depreciation services for property owners or investors.
- `cost_estimating_or_cost_management`: construction cost estimating, cost planning, cost management, cost engineering, quantity-surveying cost advice, bank / progress cost reporting, or comparable cost-control services.
- `contract_advisory_or_project_management`: contract advisory, contract administration, project management, superintendent, commercial management, claims / dispute advisory, expert witness, or comparable project / contract services.

Evidence sides:
- `official_firm`: a firm-controlled surface for the named firm.
- `aiqs_directory`: a stable Unifyd AIQS firm-listing page for the named firm/location.

A valid firm/location service listing is a real Australian quantity-surveying practice or branch/location whose public evidence ties the selected service domain to that firm at the claimed Australian location, office, branch, or local service area. Directories, marketplaces, self-service tools, generic professional profiles, and arbitrary city labels are not firm listings. Multiple offices of the same national firm count as distinct only when the evidence gives each office, branch, address, city/state service area, or local listing its own service-domain tie; a broad national page can at most support a generic national or Australia-wide firm/location listing.

Requirements:
- The page must clearly identify the named firm and tie it to the claimed Australian location through office, branch, address, city/state service-area, or local listing evidence.
- The page should communicate the evidence-side source role: for `official_firm`, a firm-controlled site, document, page, profile, or comparable official surface for the named firm; for `aiqs_directory`, a stable firm-specific Unifyd AIQS listing page that carries the named firm/location listing, not a search page, generic directory index, service-directory index, or tag-only page.
- The page must bind the selected service-domain claim to the named firm/location service listing: `tax_depreciation_or_property_depreciation`, `cost_estimating_or_cost_management`, or `contract_advisory_or_project_management` as defined above. A page that merely mentions the firm, a location list, and a generic or differently scoped service somewhere on the page does not establish the cell.

Write one JSON object per line to `results_au_qs_service_corroboration.jsonl`:
{"item": { "service_domain": "<service_domain>", "firm": "<firm>", "location": "<location>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

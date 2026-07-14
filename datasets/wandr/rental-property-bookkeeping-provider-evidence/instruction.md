You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `rental_property_bookkeeping_provider_evidence`
  - `rental_property_bookkeeping_provider_evidence.provider_commitments`

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

## `rental_property_bookkeeping_provider_evidence`

For 810+ rental-property bookkeeping/accounting providers, supply 1+ provider-controlled URL per provider establishing that the named provider publicly serves rental-property, landlord, real-estate-investor, property-manager, rental-accounting, or equivalent property-accounting needs. Providers can be landlord SaaS products, property-management platforms, broad bookkeeping/accounting services with source-stated rental-property pages, rental-focused firms, or platform-specialist bookkeeping services.

The records are public-source provenance for provider fit and commitments. They are not a vendor ranking, recommendation table, quote request, price advice, tax/accounting advice, lead list, outreach task, or contact-enrichment task.

`provider` ought to be deduplicated by provider/product identity and official domain where appropriate; a platform-specialist service firm should stay separate from the software platform it specializes in.

Requirements:
- The page must communicate that it is a provider-controlled or otherwise official public surface for the named provider's own offering, such as an official pricing, product/service, help/docs, terms, official blog/policy article, or official profile/listing page. Third-party directories, review grids, comparison/listicle pages, vendor-authored competitor roundups, stale aggregator pricing pages, forums, and anecdotes do not count.
- The page must source-state that the provider's own offering fits rental-property, landlord, real-estate-investor, property-manager, rental-accounting, or equivalent property-accounting needs, and tie that offering to bookkeeping, accounting, financial reporting, ledger, rent/payment, owner-statement, or comparable property-finance operations. Generic bookkeeping, CPA, tax, QuickBooks, small-business, realtor-only, or broad real-estate wording does not establish this fit by itself.

Write one JSON object per line to `results_rental_property_bookkeeping_provider_evidence.jsonl`:
{"item": { "provider": "<provider>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `rental_property_bookkeeping_provider_evidence.provider_commitments`

Cross-tasknode identifier discipline: this task is for the same {= provider =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= provider =}+ rental-property bookkeeping/accounting providers, cover each of the 2 provider commitment areas below with a provider-controlled source (i.e. 1+ URL per provider/evidence_area).

The records are public-source provenance for provider commitments. They are not a vendor ranking, recommendation table, quote request, price advice, tax/accounting advice, lead list, outreach task, or contact-enrichment task. Exact public prices are not required.

Evidence areas:
- `pricing_posture`: the official public pricing posture from a pricing/plans/fees/terms surface or an equivalently explicit pricing statement, including public amounts, starts-at/ranges, free/core tiers, per-unit/minimum mechanics, setup/onboarding/transaction/add-on fees, contact-sales/custom-quote gates, mixed public-plus-gated pricing, or explicit quote-only/no-public-amount posture
- `bookkeeping_accounting_services`: concrete bookkeeping/accounting deliverables, capabilities, reports, tax-ready workflows, reconciliation, payment/accounting operations, platform-specialized service scope, or source-stated service limits and add-on/cleanup/catch-up terms when those are part of the service commitment

Requirements:
- The page must communicate that it is a provider-controlled or otherwise official public surface for the named provider's own offering, such as an official pricing, product/service, help/docs, terms, official blog/policy article, or official profile/listing page. Third-party directories, review grids, comparison/listicle pages, vendor-authored competitor roundups, stale aggregator pricing pages, forums, and anecdotes do not count.
- The page must state the commitment appropriate to `evidence_area`. Pricing posture must come from an official pricing, plans, fees, billing, terms, proposal, engagement, or equivalently explicit pricing-policy surface. It can state exact plan price, starts-at/range, free/core/free-tier, per-unit/minimum/threshold, setup/onboarding/transaction/add-on fee, contact-sales/custom quote, mixed public plus enterprise-gated posture, or explicit quote-only/no-public-amount posture. A generic homepage, product page, demo CTA, contact form, consultation CTA, or "talk to us" line does not prove pricing posture unless that same page locally makes an explicit pricing, fee, minimum, quote, proposal, or billing statement. Service evidence should be concrete bookkeeping/accounting deliverables or capabilities; source-stated constraints, add-ons, cleanup/catch-up terms, portfolio minimums, and market/geography limits can be included as details when they belong to the pricing or service commitment.

Write one JSON object per line to `results_rental_property_bookkeeping_provider_evidence.provider_commitments.jsonl`:
{"item": { "provider": "<provider>", "evidence_area": "<evidence_area>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

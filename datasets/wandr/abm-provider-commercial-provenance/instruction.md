You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `abm_provider_commercial_provenance`
  - `abm_provider_commercial_provenance.commercial_provenance`

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

## `abm_provider_commercial_provenance`

For 100+ public ABM/account-based marketing providers, cover each of the 3 evidence facets listed below for each provider; for each (`provider`, `evidence_facet`) pair, supply a facet-substantiating source (i.e. 1+ URL).

The purpose is public provider capability and provenance, not vendor recommendation, procurement ranking, contact enrichment, outreach planning, or recreation of a pricing spreadsheet.

Evidence facets:
- `abm_scope_and_provider_identity`: the provider's public ABM, ABX, account-based advertising, account intelligence, managed ABM, account-based revenue marketing, or comparable account-targeted B2B go-to-market identity.
- `activation_or_service_model`: the provider's concrete service, platform, or delivery model for account-based work.
- `customer_or_outcome_proof`: public customer, buyer, project, testimonial, review, case-study, or outcome proof tied to ABM/account-targeted work.

A valid `provider` is a real company, agency, platform, managed service provider, demand-generation firm, or comparable service firm publicly tied to ABM, account-based marketing, ABX, account-based advertising, account intelligence, account-based revenue marketing, managed ABM, or account-targeted B2B go-to-market work. Invalid providers include pure contact databases, lead-list/contact-enrichment vendors, generic CRM/project-management tools, generic SEO/PPC agencies, directories, listicle publishers, marketplace/category pages, and similar non-provider entities unless the cited page itself ties the named provider to ABM/account-based work. Broad category or listicle pages without provider-specific facet content are out of scope.

Requirements:
- The page must clearly identify the named provider.
- The page must establish ABM/account-based scope for the provider, either directly or through the facet claim itself.
- The page should make its facet-appropriate source role visible: for `abm_scope_and_provider_identity`, a provider-specific identity, service, product, profile, or public-positioning context; for `activation_or_service_model`, a service, platform, help/docs, workflow, managed-delivery, program, or comparable operating-model context; for `customer_or_outcome_proof`, a case study, testimonial, buyer review, customer story, public project, outcome, or comparable customer-proof context.
- The page should state a concrete facet-scoped finding: for `abm_scope_and_provider_identity`, a public ABM/account-based capability or identity claim; for `activation_or_service_model`, a concrete model such as 1:1/1:few/1:many ABM, account selection, intent/account intelligence, display/social/email activation, content syndication, web personalization, SDR/sales coordination, consulting/training, managed delivery, or self-serve workflow; for `customer_or_outcome_proof`, a named customer, case study, testimonial, verified buyer review, public project description, or measurable outcome tied to ABM/account-targeted work.

Write one JSON object per line to `results_abm_provider_commercial_provenance.jsonl`:
{"item": { "provider": "<provider>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `abm_provider_commercial_provenance.commercial_provenance`

Cross-tasknode identifier discipline: this task is for the same {= provider =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= provider =}+ public ABM/account-based marketing providers, cover each of the 2 commercial source sides listed below for each provider; for each (`provider`, `commercial_source_side`) pair, supply a provider-specific commercial evidence source (i.e. 1+ URL).

This task is about public commercial provenance for ABM/account-based provider offerings, not affordability scoring, procurement recommendation, lead capture, or absence reporting.

Commercial source sides:
- `seller_or_provider_controlled`: a provider-owned or seller-controlled page, official docs/help/pricing/FAQ page, official service page, official offer material, or marketplace/seller offer page visibly representing the seller's own offer.
- `independent_or_buyer_market`: a provider-specific third-party review, profile, pricing, procurement, buyer-market, customer, or trade source that independently carries the commercial anchor.

A valid `provider` is a real company, agency, platform, managed service provider, demand-generation firm, or comparable service firm publicly tied to ABM, account-based marketing, ABX, account-based advertising, account intelligence, account-based revenue marketing, managed ABM, or account-targeted B2B go-to-market work. Commercial evidence must include a concrete commercial anchor such as numeric price, package/tier, free tier, platform fee, per-user fee, data/credit model, minimum spend/project, hourly/monthly/retainer rate, no-minimum/no-contract statement, CPM/CPL/media fee model, marketplace contract price, onboarding/setup fee, or a specific custom-pricing/quote structure. A bare "contact sales", "request a demo", or generic quote CTA is not a commercial anchor. Broad category, listicle, comparison-table, and generic ABM budget pages are out of scope unless the page is provider-specific enough to identify the provider and carry the provider-specific commercial anchor.

Requirements:
- The page must clearly identify the named provider and the product, service, package, offer, or commercial scope being priced or packaged.
- The page should make the commercial source side visible: for `seller_or_provider_controlled`, provider ownership, official documentation, seller offer, official marketplace listing, or seller-controlled offer framing; for `independent_or_buyer_market`, third-party review/profile/pricing/procurement/buyer-market/customer/trade framing that is not vendor-controlled and is specific to the provider.
- The page must state a concrete commercial anchor for the provider's ABM/account-based, account-intelligence, account-based advertising, revenue-marketing, managed demand-generation, or comparable account-targeted B2B offering.

Write one JSON object per line to `results_abm_provider_commercial_provenance.commercial_provenance.jsonl`:
{"item": { "provider": "<provider>", "commercial_source_side": "<commercial_source_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

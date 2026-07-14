You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `logistics_software_use`
  - `logistics_software_use.named_adoption`

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

## `logistics_software_use`

For 55+ trucking, drayage, intermodal, fleet, freight, dispatch, transportation-management, or adjacent logistics-operations software products, cover each of the 4 public-use evidence facets listed below; for each facet, cover both required source-role postures for that facet (i.e. 2+ `source_role` values), each backed by a source (i.e. 1+ URL) that visibly supports a focused public-use or product-ecology signal in the selected facet and source role.

The point is public evidence provenance for logistics software use, not active-client estimation, vendor ranking, procurement recommendation, truck-count inference, growth forecasting, contact discovery, outreach, lead scoring, legal / compliance / safety conclusions, or product-suitability advice.

Facet/source-role pairs:
- `official_product_presence` / `owned_product_surface`: product-controlled or product-owned public presence explaining the software product and its logistics / trucking operating domain.
- `official_product_presence` / `independent_product_profile`: independent product-scoped profile, marketplace, review, app, directory, or category surface that identifies the product and its logistics / trucking operating domain.
- `public_user_feedback` / `hosted_review_entry`: formal app-store, review-platform, or product-review page with a visible individual user-authored review, rating, comment, complaint, praise, or reviewer experience for the product.
- `public_user_feedback` / `community_or_forum_feedback`: public forum, community, social, comment-thread, Q&A, or discussion surface where a user or operator describes experience with the product.
- `hiring_or_operations_signal` / `employer_or_job_surface`: employer, job, training, hiring, or public work-practice page from an organization using, teaching, expecting, or requesting the product in logistics work.
- `hiring_or_operations_signal` / `implementation_or_workflow_story`: focused implementation, customer-story, operations, training, workflow, or work-practice page describing one organization's product use in logistics operations.
- `integration_or_platform_signal` / `partner_marketplace_listing`: partner, marketplace, app-directory, connector, integration listing, or platform-catalog page tying the product to another software system or workflow.
- `integration_or_platform_signal` / `technical_setup_or_api_documentation`: help-center, setup, API, developer, support, or technical documentation page explaining configuration, data flow, API behavior, or operational workflow for the product's integration.

The sources should be fully public, accessible, and usable. A source-role posture should be supported by the cited page itself, not inferred from a generic product title, homepage feature menu, review prompt, rating shell, category listing, or integration title alone. Public product-use claims and fleet / driver / truck-size claims are only page-supported claims when the page itself states them; source pages do not establish current active-client counts, product adequacy, compliance, safety, implementation fit, or private customer lists.

Requirements:
- The page must clearly identify the named software product.
- The page must tie the product to trucking, drayage, intermodal, fleet, freight, dispatch, transportation management, logistics, or adjacent transportation operations.
- The page should make the selected `source_role` visible. For `owned_product_surface`, it should be a product-owned, vendor-controlled, official help, official app/listing, or product-controlled page rather than an external profile. For `independent_product_profile`, it should be an independent product-scoped profile, marketplace, review, app-store, directory, or category page rather than a vendor homepage or generic article. For `hosted_review_entry`, it should contain at least one visible individual user-authored review, rating, comment, complaint, praise, or reviewer experience; review-question templates, review-count summaries, star-rating shells, and product-profile pages without visible user-authored content are insufficient. For `community_or_forum_feedback`, it should show public discussion, Q&A, comment-thread, social, or forum-style user/operator experience rather than a formal vendor testimonial or hosted review index. For `employer_or_job_surface`, it should come from an employer, job, training, hiring, or work-practice context where the product is specifically used, taught, expected, requested, or implemented; official product pages, review-site use-case prompts, and generic product profiles are insufficient. For `implementation_or_workflow_story`, it should be a focused implementation, customer-story, operations, workflow, training, or work-practice page about one organization's logistics use; broad customer-story indexes, source hubs, and multi-customer testimonial directories are insufficient. For `partner_marketplace_listing`, it should be a partner, marketplace, app-directory, connector, integration-listing, or platform-catalog page. For `technical_setup_or_api_documentation`, it should be help-center, setup, API, developer, support, or technical documentation explaining configuration, data flow, API behavior, or operational workflow.
- The page should expose a focused public-use or product-ecology signal clearly scoped to the named product, evidence facet, and source role. For `official_product_presence`, this means concrete product/domain positioning, capability, module, product-line, category, or operating-domain evidence. For `public_user_feedback`, it means visible user-authored rating, review text, praise, complaint, reviewer experience, app-feedback detail, forum discussion, public comment, or comparable first-person/operator observation. For `hiring_or_operations_signal`, it means product-specific in-work use, implementation, training, workflow, or hiring expectation beyond a generic "or similar" category example. For `integration_or_platform_signal`, it means a concrete integration, data flow, partner platform, marketplace connection, API behavior, setup step, or workflow link involving the product.

Write one JSON object per line to `results_logistics_software_use.jsonl`:
{"item": { "software_product": "<software_product>", "evidence_facet": "<evidence_facet>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `logistics_software_use.named_adoption`

Cross-tasknode identifier discipline: this task is for the same {= software_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= software_product =}+ logistics software products, supply public named-adoption evidence for 3+ distinct organizations per product (i.e. 1+ URL per product/organization pair).

The organization should be a real company, public agency, school district, fleet operator, carrier, brokerage, 3PL, shipper, nonprofit fleet, or comparable operating organization. Anonymous reviewers, individual handles, app users without employer identity, generic logo text, source platforms, vendor self-references, and product features are not named organizations for this task.

This is source-stated public adoption/use provenance only. It does not ask for current active-client status, private customer inference, truck-count inference, lead lists, contacts, outreach, rankings, procurement advice, or product adequacy conclusions.

Requirements:
- The page must clearly identify the named software product.
- The page must clearly identify the named organization.
- The page should be focused enough on the product-organization relationship to serve as named-adoption evidence: a client-owned acknowledgment, employer/job/workflow page, credible trade article, official or dedicated vendor case study, relationship-specific customer story, or similarly focused source can count. Broad multi-customer vendor profiles, customer-reference hubs, case-study indexes, generic customer pages, and logo grids do not establish named adoption by themselves, even when they list the organization.
- The page must source-state or visibly support a specific relationship where the organization used, adopted, selected, deployed, implemented, worked with, was a customer of, or had a comparable adoption/use relationship with the product. Bare logo presence, anonymous reviews, app-store handles, product comparison pages, directory profiles, and loose "or similar" job-skill examples do not establish this relationship by themselves.

Write one JSON object per line to `results_logistics_software_use.named_adoption.jsonl`:
{"item": { "software_product": "<software_product>", "client_org": "<client_org>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

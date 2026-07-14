You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `ai_gtm_deployability_provenance`
  - `ai_gtm_deployability_provenance.pricing_packaging`
  - `ai_gtm_deployability_provenance.integration_provenance`
  - `ai_gtm_deployability_provenance.operational_provenance`

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

## `ai_gtm_deployability_provenance`

For 70+ AI-enabled B2B sales, marketing, revenue, or CRM-workflow software products, supply an official product-capability source (i.e. 1+ URL per tool).

A valid tool is a real public software product, product line, or vendor-named AI GTM workflow product. Consulting or services agencies, pure static contact databases without workflow or automation evidence, generic CRMs with no AI/GTM product evidence, directories/listicles, and buyer-ranking pages do not count.

This is public deployability provenance for AI GTM tools, not a buyer comparison, pricing estimate, lead list, outreach playbook, CRM setup recommendation, or procurement exercise.

Requirements:
- The page must clearly identify the named vendor and product or product line.
- The page should communicate that it is an official or vendor-controlled product, capability, launch, or product-line source for the named tool.
- The page must state a concrete AI-enabled GTM workflow capability, such as an AI agent, assistant, automation, prospecting, enrichment workflow, campaign, inbound or outbound workflow, CRM workflow, revenue-team workflow, or comparable sales/marketing/revenue operation.

Write one JSON object per line to `results_ai_gtm_deployability_provenance.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `ai_gtm_deployability_provenance.pricing_packaging`

Cross-tasknode identifier discipline: this task is for the same {= tool =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= tool =}+ AI-enabled B2B sales, marketing, revenue, or CRM-workflow software products, supply a public commercial-packaging source (i.e. 1+ URL per tool).

A valid tool is a real public software product, product line, or vendor-named AI GTM workflow product. Consulting or services agencies, pure static contact databases without workflow or automation evidence, generic CRMs with no AI/GTM product evidence, directories/listicles, and buyer-ranking pages do not count.

Pricing/package evidence is source-stated public commercial access or packaging: dollar price, plan/tier, per-seat, credit/usage/outcome model, free plan, trial, beta/GA availability, edition gating, custom quote, contact-sales, schedule-demo, annual minimum, or quote-only/package-dependent posture. Inferred absence, third-party estimates, and total-cost modeling do not count.

Requirements:
- The page must clearly identify the named vendor and product or product line.
- The page should communicate vendor-controlled commercial packaging context, or platform-marketplace packaging context for the same app/tool.
- The page must state a concrete public pricing or packaging state for the tool.

Write one JSON object per line to `results_ai_gtm_deployability_provenance.pricing_packaging.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `ai_gtm_deployability_provenance.integration_provenance`

Cross-tasknode identifier discipline: this task is for the same {= tool =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= tool =}+ AI-enabled B2B sales, marketing, revenue, or CRM-workflow software products, cover each of the 2 integration evidence sides below with a concrete integration source (i.e. 1+ URL per tool-side pair).

A valid tool is a real public software product, product line, or vendor-named AI GTM workflow product. Consulting or services agencies, pure static contact databases without workflow or automation evidence, generic CRMs with no AI/GTM product evidence, directories/listicles, and buyer-ranking pages do not count.

Integration evidence sides:
- `vendor_integration_source`: vendor-side integration evidence.
- `ecosystem_or_platform_source`: ecosystem, platform, marketplace, partner, CRM, or comparable non-vendor-platform integration evidence.

`integration_side` must be exactly one of the two listed values.

Requirements:
- The page must clearly identify the named vendor and product or product line.
- The page must communicate the source role required by `integration_side`: a vendor-controlled product, docs, help, integration, API, marketplace, pricing, or product article page for `vendor_integration_source`; or a platform/CRM marketplace listing, app/exchange listing, official partner/ecosystem page, official CRM/platform docs/help page, or comparable platform-controlled source independently naming the same tool or integration for `ecosystem_or_platform_source`.
- The page must state a concrete CRM or revenue-stack integration/workflow for the tool, such as syncing/importing records, creating/updating objects, logging activities, routing leads, using CRM data, marketplace installability, connector/API/trigger/action, sequence/workflow push, call/email/calendar integration, or comparable functionality.
- Vague logo-grid or "works with your stack" references do not count without a named platform and integration context. A vendor-controlled page cannot satisfy `ecosystem_or_platform_source`.

Write one JSON object per line to `results_ai_gtm_deployability_provenance.integration_provenance.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>", "integration_side": "<integration_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `ai_gtm_deployability_provenance.operational_provenance`

Cross-tasknode identifier discipline: this task is for the same {= tool =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= tool =}+ AI-enabled B2B sales, marketing, revenue, or CRM-workflow software products, cover each of the 2 operational provenance surfaces below with a deployability source (i.e. 1+ URL per tool-surface pair).

A valid tool is a real public software product, product line, or vendor-named AI GTM workflow product. Consulting or services agencies, pure static contact databases without workflow or automation evidence, generic CRMs with no AI/GTM product evidence, directories/listicles, and buyer-ranking pages do not count.

Operational surfaces:
- `docs_or_help`: product docs, help center, support article, API docs, setup/admin/user guide, knowledge-base page, integration guide, or comparable operational page that identifies the product/family and shows a deployable workflow/action.
- `release_or_update`: official release, update, launch, changelog, company-news, product-news, or comparable vendor update evidence.

`operational_surface` must be exactly one of the two listed values.

Requirements:
- The page must clearly identify the named vendor and product or product line or product family.
- The page must communicate the operational source context required by `operational_surface`: docs/help/setup/admin/API/knowledge-base context for `docs_or_help`; official release/update/launch/changelog/company-news/product-news context from January 1, 2024 through July 8, 2026 for `release_or_update`.
- The page must state a concrete operational finding for the tool: for `docs_or_help`, a deployable workflow/action/setup/admin/user/API step; for `release_or_update`, a product/capability release, update, launch, GA/beta, new feature, packaging/pricing update, or material product change.

Write one JSON object per line to `results_ai_gtm_deployability_provenance.operational_provenance.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>", "operational_surface": "<operational_surface>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

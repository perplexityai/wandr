You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `productivity_monitoring_product_capability_evidence`
  - `productivity_monitoring_product_capability_evidence.outside_capability_evidence`

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

## `productivity_monitoring_product_capability_evidence`

For 50+ vendors, identify 1+ named product or product family per vendor as public workplace monitoring, time-tracking, workforce analytics, work-management analytics, collaboration analytics, or office-support analytics; for each such (`vendor`, `product`) pair and each of the 4 product-controlled evidence roles listed below, supply a dedicated product source (i.e. 1+ URL) whose main subject visibly supports that role for the named product.

The purpose is a neutral public-source capability atlas for product provenance, not procurement advice, HR or legal advice, employee-performance scoring, surveillance recommendation, contact discovery, outreach, or sales lead scoring.

Product-controlled evidence roles, which we refer to as `product_source_role`, are:
- `signal_capture_documentation`: a product-controlled page mainly about work, time, activity, device, app/site, attendance, collaboration, or work-graph signals the product captures, derives, or displays.
- `reporting_workflow_documentation`: a product-controlled page mainly about dashboards, reports, exports, alerts, benchmarks, manager/admin/analyst views, or comparable reporting workflows.
- `privacy_visibility_control_documentation`: a product-controlled page mainly about workplace-data privacy, transparency, minimization, access, retention, consent, visibility, employee/admin access, screenshot/content handling, aggregation, anonymization, or governance controls.
- `deployment_setup_documentation`: a product-controlled page mainly about install, deployment, connector, app/extension, admin setup, sync, export, API, or platform-integration implementation.

`vendor` ought to name the real organization or brand behind the product. `product` ought to name a real product or product family sold, shipped, or documented by that vendor as a product; API methods, report endpoints, individual feature endpoints, documentation page titles, metric endpoint names, marketplace names, integration partner names, and category labels do not count as products. Work-management, collaboration, and office-support products count only when the page ties the named product or family to work, time, activity, workforce, collaboration analytics, reporting, metadata, or comparable work-pattern evidence. Sources should be fully public, accessible, and usable as normal pages. Broad homepages, all-in-one feature pages, category directories, generic marketing pages, standalone API/report method references, one-line marketplace/catalog shells, and pages where the selected role is only an incidental aside are not dedicated product sources for this task.

Requirements:
- The page must clearly identify the named vendor and named product or product family.
- The page should visibly be a product-controlled source dedicated to the selected `product_source_role`: for `signal_capture_documentation`, official product/help/admin documentation centered on captured or derived work signals; for `reporting_workflow_documentation`, official product/help/admin/reporting documentation centered on report or dashboard workflows; for `privacy_visibility_control_documentation`, official product/help/trust/privacy/security/admin documentation centered on product or workplace-data controls; for `deployment_setup_documentation`, official setup/admin/integration/developer documentation centered on deployment, connector, app, sync, export, API, or platform implementation.
- The page must expose concrete role evidence for `product_source_role`: named captured work/time/activity/collaboration signals for `signal_capture_documentation`; named dashboards/reports/exports/alerts/views or reporting workflows for `reporting_workflow_documentation`; concrete product/work-data safeguards or visibility controls for `privacy_visibility_control_documentation`; and named install/deployment/connector/app/admin setup/sync/export/API implementation facts for `deployment_setup_documentation`.

Write one JSON object per line to `results_productivity_monitoring_product_capability_evidence.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>", "product_source_role": "<product_source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `productivity_monitoring_product_capability_evidence.outside_capability_evidence`

Cross-tasknode identifier discipline: this task is for the same {= vendor_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= vendor_product =}+ named (`vendor`, `product`) pairs, identify each product or product family as public workplace monitoring, time-tracking, workforce analytics, work-management analytics, collaboration analytics, or office-support analytics; for each such pair and each of the 3 outside proof roles listed below, identify 1+ named outside organization or source entity and supply a product-scoped outside proof source (i.e. 1+ URL).

The purpose is outside public proof that the product exists in operational, integration, procurement, or independently assessed contexts, not procurement advice, HR or legal advice, employee-performance scoring, surveillance recommendation, contact discovery, outreach, or sales lead scoring.

Outside proof roles, which we refer to as `outside_proof_role`, are:
- `customer_or_procurement_proof`: a named customer, buyer, public agency, procurement body, case-study subject, or comparable outside organization tied to product use, purchase, deployment, certification, procurement, or operational availability.
- `integration_implementation_proof`: a named integration partner, platform operator, app marketplace operator, identity provider, work platform, implementation partner, or comparable counterparty tied to product setup, configuration, data flow, connector behavior, app installation, admin enablement, or product-specific implementation.
- `independent_expert_assessment`: a named non-vendor publisher, analyst, security/procurement/trade/research organization, or comparable expert source that gives product-specific capability assessment through authored editorial, analyst, testing, procurement, research, or comparable assessment voice.

`vendor` ought to name the real organization or brand behind the product. `product` ought to name a real product or product family sold, shipped, or documented by that vendor as a product; API methods, report endpoints, individual feature endpoints, documentation page titles, metric endpoint names, marketplace names, integration partner names, and category labels do not count as products. `outside_organization` ought to name a real organization, platform, public body, publisher, analyst, implementation partner, or comparable outside entity distinct from the vendor and appropriate to the selected outside proof role. Generic category labels, anonymous review pools, software-directory category pages, feature-comparison tables, search/list pages, broad customer-reference registries used as the named customer, and the vendor itself do not count as outside organizations. Sources should be fully public, accessible, and usable as normal pages.

Requirements:
- The page must clearly identify the named vendor, named product or product family, and named `outside_organization`.
- The page should visibly play the outside source role required by `outside_proof_role`: for `customer_or_procurement_proof`, a dedicated customer story, case study, procurement record, buyer/deployment page, certification page, or comparable outside-organization proof surface centered on the named customer, buyer, public body, or deployment organization; for `integration_implementation_proof`, a product-specific setup guide, implementation document, connector documentation, platform-admin page, partner implementation page, or marketplace/app page with substantive implementation detail tied to the named outside organization; for `independent_expert_assessment`, a non-vendor editorial, analyst, security, procurement, trade, research, or comparable expert source centered on product capability rather than a review-directory/category shell or templated review listicle.
- The page must expose concrete outside proof for `outside_proof_role`: actual use, purchase, deployment, procurement, certification, or operational facts for `customer_or_procurement_proof`; product-specific setup steps, configuration requirements, data objects, workflow behavior, permission/admin behavior, install behavior, connector behavior, or implementation facts for `integration_implementation_proof`; and authored product-specific capability assessment for `independent_expert_assessment`. Generic customer-reference registries, generic app availability, generic "connect apps" pages, trigger/action catalogs without implementation substance, category placement, star ratings, anonymous reviews, feature checkboxes, pros/cons shells, and review-directory boilerplate are not enough.

Write one JSON object per line to `results_productivity_monitoring_product_capability_evidence.outside_capability_evidence.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>", "outside_proof_role": "<outside_proof_role>", "outside_organization": "<outside_organization>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

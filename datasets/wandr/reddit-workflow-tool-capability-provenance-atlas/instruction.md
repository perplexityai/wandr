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

## `reddit_workflow_tool_capability_provenance_atlas`

For each of the 6 product categories below, identify 25+ currently available public products, tools, or software-backed services with explicit Reddit-specific workflow support. For each product, cover each of the 3 evidence roles below with a role-appropriate public source (i.e. 1+ URL under each role).

The goal is public provenance for real, currently available Reddit workflow support, not a ranking, buying guide, procurement strategy, contact/prospecting output, or missingness inventory.

Product categories in scope:
- **reddit_first_party_business_tool**: First-party Reddit-owned business, ads, pro, API, or data product surface.
- **reddit_scheduling_or_publishing**: A product whose public workflow centers on scheduling, publishing, cross-posting, or managing Reddit posts/comments.
- **reddit_monitoring_listening_or_alerting**: A product whose public workflow centers on Reddit monitoring, listening, mentions, alerts, or notifications.
- **reddit_analytics_research_or_insights**: A product whose public workflow centers on Reddit analytics, audience/community research, trend analysis, or insight extraction.
- **automation_integration_or_api_platform**: An automation, integration, workflow, API, connector, or developer platform with concrete Reddit operations.
- **social_management_or_customer_engagement_suite**: A social management, care, engagement, or marketing suite with a concrete current Reddit workflow.

Evidence roles:
- `reddit_workflow_claim`: public evidence that the product performs a Reddit-specific workflow.
- `commercial_access_surface`: public evidence of an official access path for the same Reddit-capable product or product surface.
- `integration_or_platform_evidence`: public evidence of a concrete Reddit platform, API, integration, connector, partner, or channel mechanism.

Products should be real public software products, first-party Reddit business tools, official integration/product surfaces, or agency/service offerings with a visible software/tooling surface. Generic social-media claims, broad "all platforms" wording, pending roadmap requests, closed products, recommendation listicles, third-party price estimates, pure agencies without tooling, and lead-generation/outreach-only tools do not establish a product for this task.

Requirements:
- The page must support the product's fit to the claimed product category, specific enough to distinguish first-party Reddit tools, schedulers/publishers, monitoring/alerting tools, analytics/research tools, automation/API platforms, and social/customer-engagement suites.
- The page must clearly identify the claimed product or organization-owned product surface.
- The page must fit the claimed `evidence_role` source class. Product-owned, official marketplace/integration, official announcement, help/docs, or Reddit-owned sources can fit `reddit_workflow_claim`; official pricing, plans, free-tier, free-tool, trial, signup, app access, request-demo, contact-sales, custom-quote, or managed-service access pages can fit `commercial_access_surface`; official docs, help, API, integration, marketplace, Reddit partner/directory, product-technical, or announcement pages can fit `integration_or_platform_evidence`.
- The page must support the claimed role's substance. For `reddit_workflow_claim`, it must explicitly state a product-owned Reddit workflow such as Reddit post scheduling, Reddit publishing, Reddit monitoring, Reddit alerts, Reddit listening, Reddit data/API access, Reddit engagement/inbox, subreddit/community research, Reddit analytics, or equivalent. For `commercial_access_surface`, it must expose an official access path for the same Reddit-capable product/surface, and generic company pricing fails when the page does not connect the access path to that product, connector, module, plan scope, or Reddit-branded surface. For `integration_or_platform_evidence`, it must show a concrete Reddit platform/API/channel/partner mechanism rather than only a logo or broad supported-platform list.

Write one JSON object per line to `results_reddit_workflow_tool_capability_provenance_atlas.jsonl`:
{"item": { "product_category": "<product_category>", "product": "<product>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

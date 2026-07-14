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

## `data_governance_kpi_evidence`

For 45+ vendors or platforms in data governance, data catalog, MDM/reference data, data quality, data observability, data stewardship, data operations, or closely adjacent data-management dashboarding, cover each of the 6 evidence facets below by supplying at least 1 public source URL for each platform and facet.

This is a public provenance atlas, not a vendor comparison. The useful work is finding what public sources state about each platform's governance visibility, metrics, workflows, integrations, pricing posture, and deployment or trust posture.

Evidence facets and source roles:
- `dashboard_reporting`: dashboard, reporting, monitoring, trend, KPI, or visibility surfaces for governance, MDM, data quality, observability, stewardship, lineage, usage, cost, policy, or issue status
  Source role: a public docs, product, support, release-note, demo, or equivalent source that visibly describes the dashboard or reporting surface
  Source-stated evidence: a source-stated dashboard, reporting, monitoring, trend, KPI, or visibility capability relevant to operational data-governance work
- `metric_kpi`: concrete metric or KPI categories, such as asset counts, enrichment, completion, lineage coverage, quality dimensions, freshness, volume, schema, issue counts, MTTR, DCR processing, usage, cost, or policy counts
  Source role: a public docs, product, support, metric-reference, or reporting source that lists or explains the metric categories
  Source-stated evidence: specific source-stated metric names, dimensions, KPI categories, counts, scores, or time-series measures rather than generic analytics wording
- `workflow_response`: stewardship, data-change-request, issue, incident, approval, task, remediation, request, or response mechanics
  Source role: a public docs, support, product, or workflow-specific source that describes user action, routing, approvals, incidents, tasks, or remediation
  Source-stated evidence: a source-stated workflow, DCR, issue-response, incident, approval, task, remediation, or request mechanic; do not infer it from dashboard language
- `integration_api`: connectors, APIs, marketplaces, developer surfaces, data-source integrations, SDKs, API tokens, REST/JDBC/OAuth surfaces, or cross-vendor integration mechanics
  Source role: an official developer, API, connector, integration, marketplace, support, or cross-vendor integration source; third-party connector pages must be framed as connector evidence, not native vendor API evidence
  Source-stated evidence: a source-stated connector, API, developer, marketplace, integration, SDK, token, REST/JDBC/OAuth, or cross-vendor integration capability
- `pricing_state`: published pricing, free or open-source plan evidence, quote-required or contact-sales state, marketplace/procurement pricing, or a source-bounded public pricing caveat
  Source role: an official pricing, contact-sales, plan, marketplace, procurement, cloud-marketplace, or public contract source; estimator pages and SEO listicles do not establish vendor pricing
  Source-stated evidence: source-stated numeric pricing, tiering, free/OSS state, quote-required state, contact-sales state, procurement price, or a bounded source caveat
- `deployment_trust`: SaaS, self-hosted, hybrid, agent/agentless, cloud, private-link, tenant, deployment architecture, security, trust, compliance-framework, or product-boundary provenance
  Source role: an official architecture, deployment, security, trust, docs, support, marketplace, procurement, or comparable source that states the deployment or trust posture
  Source-stated evidence: a source-stated architecture, deployment, hosting, agent, tenancy, security, trust, framework, or product-boundary fact; trust evidence is only provenance, not compliance advice

Generic BI, KPI-dashboard, marketing-analytics, or operations-dashboard products only count when the cited source specifically ties the platform to data governance, data quality, data observability, metadata, MDM/reference data, stewardship, lineage, policy, or a similar data-management use. A generic business dashboard alone is not enough.

Use public, usable sources. Official vendor docs, product pages, support docs, developer/API pages, pricing/contact-sales pages, trust/security pages, release notes, public demos, and architecture pages are the normal authority for vendor-authored capability claims. Marketplace, procurement, cloud-marketplace, or public-contract pages can support pricing, deployment, or public-availability evidence when labeled by the finding. Analyst articles, comparison pages, blogs, and listicles can help with discovery or identity conflicts, but they should not override official sources for capability, pricing, API, or deployment claims.

Treat source date and target fit as provenance context. Dated, versioned, archived, or procurement sources can speak more clearly to the April 20, 2026 target state; current undated pages should be framed as current public evidence rather than proof of that historical date.

Keep the submission as source-backed provenance only: no vendor ranking, product recommendation, procurement advice, implementation architecture, compliance assurance, ROI analysis, pricing negotiation, dashboard-building instructions, scraping or deployment instructions, outreach/contact behavior, or lead scoring.

Requirements:
- The page must clearly identify the submitted vendor, product, or platform.
- The page must make the source role appropriate to `evidence_facet` visible.
- The page must source-state the facet claim, caveat, or bounded missing/conflict state. DCR, workflow, compliance trend, real-time, pricing, deployment architecture, API availability, trust evidence, and missing/gated/quote-required/name-conflict/product-boundary states must not be inferred from generic wording or public-source silence.

Write one JSON object per line to `results_data_governance_kpi_evidence.jsonl`:
{"item": { "vendor_platform": "<vendor_platform>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

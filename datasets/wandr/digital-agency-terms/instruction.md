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

## `digital_agency_terms`

For each of the 5 digital-service categories listed below, identify 25+ agencies as publicly offering that service category; for each such agency and each of the 4 evidence facets listed below, supply a source (i.e. 1+ URL) showing public evidence for the agency-service pair.

Digital-agency commercial terms are unevenly public: some agencies publish packages, some explain quote-based scoping on official pages, and some have third-party project or review writeups that discuss concrete commercial terms or delivered work. The task is public provenance about what pages state, not a vendor ranking, recommendation, project-cost estimate, supplier-selection, contact-enrichment, outreach, or request-for-quote exercise.

Digital-service categories:
- `web_design_and_development`: website design, website development, WordPress/ecommerce sites, landing pages, and comparable public web builds.
- `custom_software_and_mobile_app_development`: bespoke software products, custom platforms, API-backed systems, web apps, and native or cross-platform mobile apps.
- `seo_and_digital_marketing`: SEO, paid search, paid social, content marketing, email marketing, digital PR, and comparable performance or growth-marketing services.
- `workflow_crm_automation`: CRM setup or customization, business-process automation, workflow automation, no-code/low-code implementation, and integrations among CRM or business tools.
- `ai_automation_and_agents`: AI automation, AI agents, chatbots, generative-AI implementation, AI workflow systems, and comparable client-facing AI implementation services.

Evidence facets:
- `official_service_scope`: the agency's own public service-offering presence for the selected service category.
- `commercial_terms_or_quote_posture`: focused public commercial-term evidence, or explicit custom/quote/confidential pricing posture, for the agency in the selected service category.
- `agency_project_or_portfolio_scope`: the agency's own project/client/engagement-scoped case-study, portfolio, testimonial, or work-scope evidence for the selected service category.
- `independent_project_or_review_scope`: client-owned or otherwise independent project, contract, proposal, review, article, or work-scope evidence for the agency in the selected service category.

A valid agency is a named services agency, consultancy, studio, or development/marketing firm selling client work in the selected category. SaaS tools, automation platforms, hosting products, course pages, generic pricing guides, individual-only freelance listings, staffing/job posts, and agency directories themselves are outside the agency identity. Sources should be public, accessible normal pages.

Requirements:
- The page must clearly identify the named agency and tie that agency to the selected service category.
- The page should make its facet-appropriate source role visible. For `official_service_scope`, it should communicate an agency-owned or officially controlled service surface. For `commercial_terms_or_quote_posture`, it should be an agency-owned or officially controlled commercial/pricing/package/quote/FAQ page, or a third-party page focused on a specific agency-client project, review, proposal, contract, or commercial writeup where commercial terms are substantive page content. Broad marketplace, review, or directory profiles do not fit this facet merely because they expose hourly-rate, minimum-project, service-line, pricing-snapshot, review-cost, or budget fields. For `agency_project_or_portfolio_scope`, it should be an agency-owned or officially controlled page focused on a specific client, project, engagement, case study, portfolio item, or testimonial; general service pages, portfolio indexes, client-logo walls, review indexes, and directory profiles are not enough. For `independent_project_or_review_scope`, it should be controlled outside the agency or written by an independent third party and focused on a specific client, project, engagement, contract, proposal, review, or trade/editorial account; agency-owned pages, broad per-agency marketplace profiles, review-summary pages, directory profiles, and list pages do not fit this facet.
- The page must contribute the evidence required by the selected `evidence_facet`: for `official_service_scope`, an offered service in the selected category; for `commercial_terms_or_quote_posture`, a source-stated price, rate, package, retainer, minimum project size, project-cost band, or explicit custom/quote/confidential/not-listed posture on a focused commercial source rather than incidental profile metadata; for `agency_project_or_portfolio_scope`, concrete service/work scope tied by the agency to a specific client, project, or engagement in the selected category; for `independent_project_or_review_scope`, concrete service/work, commercial, or outcome scope from the client or independent source tying the agency to a specific client, project, engagement, contract, proposal, review, or article in the selected category.

Write one JSON object per line to `results_digital_agency_terms.jsonl`:
{"item": { "service_category": "<service_category>", "agency": "<agency>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

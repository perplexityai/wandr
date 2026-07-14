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

## `construction_saas_public_evidence`

Identify 200+ platforms as public construction-workflow software platforms; for each platform, cover the 4 evidence facets below by supplying a public source (i.e. 1+ URL under each facet) that exposes a concrete source-stated public fact for that facet.

The purpose is a public evidence provenance atlas for construction SaaS and adjacent project-execution software, not a ranking, buying guide, product-roadmap exercise, build specification, outreach list, lead-scoring table, or contact-enrichment task.

Evidence facets:
- `official_product_scope`: a vendor-controlled page ties the platform to construction, real estate development, interior/fitout, infrastructure, EPC, project execution, procurement/BOQ/finance, client portals, document/design management, site progress, vendor management, mobile/offline field execution, AI analytics, or comparable construction-workflow software.
- `workflow_module_claim`: a platform-specific public page shows a concrete workflow, module, feature family, or app capability and what it does.
- `customer_or_case_evidence`: a public case study, customer story, testimonial, press item, article, or similar page ties the platform to a named or clearly described customer, project, implementation context, workflow, or source-stated outcome.
- `public_access_or_integration_signal`: a public pricing, demo, signup, app-store, marketplace, integration, mobile/offline, hiring/funding, startup-profile, or comparable public access/growth signal exposes a concrete source-stated fact about the platform.

The cited pages should be public, usable, and specific to the claimed platform and facet. Generic search/list pages, low-information rankings, broad multi-vendor catalogs, comparison pages, and "best software" listicles are discovery scaffolding, not substantive evidence by themselves. Commercial/access and organization-growth facts count only as public provenance; contacts, RFQ harvesting, rankings, recommendations, private traction guesses, compliance/safety claims, implementation guidance, roadmap/build advice, product-suitability conclusions, and UX critiques are out of scope.

Requirements:
- The page must clearly identify the named platform or vendor and tie it to construction-workflow software.
- The page should make its facet-appropriate source role visible: for `official_product_scope`, a vendor-controlled scope/solution surface; for `workflow_module_claim`, a platform-specific product, module, help, app, or workflow surface; for `customer_or_case_evidence`, a case/customer/testimonial/press/customer-story surface with real implementation context rather than a logo wall or bare "trusted by" banner; for `public_access_or_integration_signal`, a public pricing/demo/signup, app-store, marketplace, integration, mobile/offline, hiring/funding, startup-profile, or comparable access/growth signal surface.
- The page must contribute a concrete source-stated public fact at the selected facet's bar: construction product scope, a named workflow/module and what it does, a named or clearly described customer/project/implementation/workflow/outcome, or a public access/integration/mobile/offline/growth signal.

Write one JSON object per line to `results_construction_saas_public_evidence.jsonl`:
{"item": { "platform": "<platform>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

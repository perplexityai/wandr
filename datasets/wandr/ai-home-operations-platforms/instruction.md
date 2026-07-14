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

## `ai_home_operations_platforms`

Find 80+ consumer/prosumer AI home-operations platforms and cover each of the 8 evidence roles below. For every (`platform`, `evidence_role`) pair, provide 1 public URL that substantiates that platform's role-specific evidence.

The purpose is public product evidence for recurring home-management software, not rankings, buying advice, procurement recommendations, legal/tenant guidance, pricing absence tracking, or smart-home gadget control.

Use exactly these `evidence_role` values:

- `official_ai_mechanism`
- `official_pricing_or_plan`
- `official_privacy_or_data_handling`
- `public_access_or_lifecycle_status`
- `user_customer_reception_with_text`
- `independent_product_context`
- `independent_launch_partner_or_market_context`
- `service_handoff_or_integration_evidence`

A valid `platform` is a named software product, app, or platform visibly serving home operations for homeowners, renters, individual landlords, residential owners, small portfolio/prosumer operators, or adjacent occupant/home-service workflows. Home operations include maintenance, records, warranties/manuals/receipts, inspections/reports, photos/sensors, repair planning, service handoff, home health/risk, and comparable recurring home-management work.

Broad enterprise property-management suites, pro-only inspection software, generic smart-home voice/controller ecosystems, contractor CRMs, pure booking marketplaces, pure finance/bookkeeping tools, and landlord/legal products are outside scope unless the product itself is explicitly consumer/prosumer home-operations software with concrete AI or automation capability.

For each source:

- The page must clearly identify the named platform.
- The page must tie the platform to recurring home-operations work rather than only generic property management, smart-home control, field service, finance, booking, legal, or broad AI-assistant functionality.
- The page must make its evidence-role source context visible. For `official_ai_mechanism`, `official_pricing_or_plan`, and `official_privacy_or_data_handling`, use a platform/developer-controlled surface such as an official product site, pricing page, help/docs page, privacy/security page, official launch/news post, developer-controlled app-store listing, official demo page, or comparable own-channel surface. For `public_access_or_lifecycle_status`, use a page exposing public availability or lifecycle status through download, signup, waitlist, launch, current product, beta, renaming/acquisition, shutdown, or comparable status context. For `user_customer_reception_with_text`, use public product-user, customer, homeowner, renter, operator, service-partner, app-store review, review-platform feedback, user discussion, testimonial/case content, or comparable reception context with visible reception text. For `independent_product_context` and `independent_launch_partner_or_market_context`, use a source outside the platform's controlled surfaces; developer-controlled app-store listings, platform-owned testimonials, generic broad app listicles, SEO comparisons, vendor-published comparison pages, low-substance directories, and one-line category blurbs do not fit these roles by themselves. For `service_handoff_or_integration_evidence`, use an official, partner, integration, marketplace, help, case-study, or comparable page that shows a concrete handoff/integration workflow with service providers, contractors, insurers, utilities, sensors, property records, calendars, or comparable systems.
- The page must state a concrete role-scoped finding. For `official_ai_mechanism`, it must show a concrete AI, automation, or home-intelligence mechanism tied to home operations, such as an AI assistant over a home record, automated document/photo extraction, sensor/photo/report analysis, predictive maintenance/risk, home-health scoring, repair-cost estimation, automated task/reminder logic, or service handoff driven by home data; generic "AI-powered", "smart", "intelligent", or "personalized insights" branding alone is insufficient. For `official_pricing_or_plan`, it must state a public plan, price, free/trial tier, subscription, paid membership, app purchase, quote-based plan, or comparable commercial access signal; a bare homepage CTA is not enough. For `official_privacy_or_data_handling`, it must state privacy, security, data collection/use, local storage, account data, document/photo handling, sensor data, or comparable data-handling policy for the platform. For `public_access_or_lifecycle_status`, it must state a public access or lifecycle fact rather than an absence claim. For `user_customer_reception_with_text`, it must carry visible reception text or a concrete product-user/customer signal; rating counts alone are insufficient. For `independent_product_context`, it must give product-specific context about the platform's home-operations role or capability, not merely name the platform in a broad list. For `independent_launch_partner_or_market_context`, it must independently describe a launch, funding, acquisition, partner/customer relationship, market traction, or comparable external status/context for the platform. For `service_handoff_or_integration_evidence`, it must show how the platform connects home data or tasks to service professionals, contractors, partners, sensors, inspections, utilities, property records, calendars, warranties/manuals, or comparable systems.

Write one JSON object per line to `results_ai_home_operations_platforms.jsonl`:
{"item": { "platform": "<platform>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

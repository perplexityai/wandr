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

## `local_ai_offers`

For each of the 5 AI automation offer families, name 30+ public provider/package offers per family; for each provider/package and each of the 2 evidence roles, supply 1+ public URL from a page about that same offer.

The `offer_family` labels are:
- `review_reputation`: AI-assisted review generation, review monitoring, reputation management, review replies, testimonials, or related public reputation workflows.
- `voice_receptionist`: AI receptionist, virtual receptionist, answering service, phone agent, call assistant, booking/screening, or after-hours voice automation.
- `chatbot_lead_qualifier`: website/chat AI that captures, qualifies, routes, books, or follows up on leads.
- `seo_geo_blog_writer`: AI or automation for SEO, GEO, local-search, blog, article, product, or location-page content used by SMBs, agencies, freelancers, or adjacent operators.
- `invoice_chasing`: invoice chasing, accounts-receivable automation, payment reminders, collections workflow, debtor follow-up, or related billing follow-up automation.

The `evidence_role` labels are:
- `offer_feature`: the cited page shows a concrete AI or automation feature for the submitted offer family.
- `pricing_packaging`: the cited page states the offer's commercial packaging: explicit price, starting price, usage unit, tier/bundle inclusion, marketplace/package price, agency package price, or a source-stated quote/custom/contact-sales state.

Use `provider_package` for a concise provider + offer/package/service identity, such as a SaaS product, platform module, official service package, app-directory offer, marketplace package, white-label/reseller offer, agency package, or freelancer package. A provider-only name can be acceptable when the public offer is sold under the provider name rather than under a separate plan name.

Eligible source surfaces include provider-controlled product/pricing/help/docs pages, public app-directory or integration-marketplace pages, public package listings, public agency/service pages, white-label/reseller platform pages, and freelancer/marketplace package pages that present the offer itself. Generic "best tools" roundups, opportunity rankings, scraped SaaS directories, press coverage, lead lists, contact enrichment pages, sales scripts, implementation how-tos, and private/login-only surfaces are not enough by themselves.

Include a compact finding for each record: name the feature on `offer_feature` records or the price/package/quote/custom state on `pricing_packaging` records. Source-stated provider/package context, target customer, integration, source date, and checked date are helpful when visible, but they are auxiliary and should not be invented.

Requirements:
- The page must identify the same provider_package and bind it to the submitted offer_family rather than an unrelated product, generic category, or different service line.
- The page should support local-business, trades, SMB, agency, freelancer, or adjacent SMB-operator use. This can be explicit target wording, or public self-serve pricing, app-marketplace, agency/white-label/reseller, local-search, invoice-workflow, customer-communication, or small-business workflow context. Do not use clearly enterprise-only, consumer-only, or internal-developer-only pages.
- The page should have a source role appropriate to evidence_role: product/feature/help/docs/marketplace/app-directory/service/package pages for `offer_feature`; pricing/plans/billing/package/quote/custom/contact-sales/app-marketplace/agency/freelancer package pages for `pricing_packaging`.
- The page must provide the role-specific evidence: for `offer_feature`, a concrete AI or automation feature for the submitted offer_family; for `pricing_packaging`, an explicit price, starting price, usage unit, tier/bundle inclusion, marketplace/package price, agency package price, or source-stated quote/custom/contact-sales state for the same provider_package.

Write one JSON object per line to `results_local_ai_offers.jsonl`:
{"item": { "offer_family": "<offer_family>", "provider_package": "<provider_package>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

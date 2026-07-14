You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `local_service_platform_adoption`
  - `local_service_platform_adoption.platform_features`
  - `local_service_platform_adoption.business_presence`

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

## `local_service_platform_adoption`

For 60+ software platforms in the local-service CRM, field-service, marketing automation, or service-business operations ecosystem, supply named customer-adoption sources for 2+ businesses per platform (i.e. 1+ URL per platform/customer-business relationship).

The useful evidence is public provenance for a real adoption relationship, not buyer advice. Customer stories, case studies, substantive testimonials, customer pages, reputable trade articles, and similar pages can count when they name the customer business and show platform use. Anonymous reviews, star-rating-only pages, logo walls without usage detail, category directories, software rankings, listicles, pricing pages, and generic product pages do not count for this adoption source.

Requirements:
- The page must identify the submitted platform and the submitted customer business.
- The page must substantiate that the submitted customer business uses, switched to, implemented, credits, or is otherwise a named customer of the submitted platform.

Write one JSON object per line to `results_local_service_platform_adoption.jsonl`:
{"item": { "platform": "<platform>", "business": "<business>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `local_service_platform_adoption.platform_features`

Cross-tasknode identifier discipline: this task is for the same {= platform =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= platform =}+ platforms, cover each of the 3 local-service feature facets by supplying a public feature-fit source (i.e. 1+ URL per platform/facet).

Feature facets:
- `local_service_scope`: the platform is publicly framed for local-service, trade, home-service, field-service, or comparable appointment/job-based service businesses
- `field_service_operations`: the platform exposes operational capabilities such as scheduling, dispatch, work orders, job management, technician mobile workflows, estimates, invoicing, routing, or service plans
- `crm_or_marketing_automation`: the platform exposes customer records, lead capture, pipeline, customer communication, campaigns, follow-ups, reviews/referrals, client portal, or comparable CRM/marketing automation

The source should be a platform feature, product, vertical, help-doc, release-note, pricing, module, marketplace, or integration page with concrete feature evidence. Review sites, category directories, rankings, listicles, and buyer guides do not count for this feature-fit source.

Requirements:
- The page must identify the submitted platform in a product, feature, module, vertical, help, release, pricing, marketplace, or integration context.
- The page must give concrete evidence for the selected `feature_facet`, not just generic "small business software" copy.

Write one JSON object per line to `results_local_service_platform_adoption.platform_features.jsonl`:
{"item": { "platform": "<platform>", "feature_facet": "<feature_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `local_service_platform_adoption.business_presence`

Cross-tasknode identifier discipline: this task is for the same {= customer_business =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= customer_business =}+ platform/customer-business relationships, supply an independent public business-presence source (i.e. 1+ URL) showing that the named customer business is a real operating local-service business.

The source should be independent from the platform named in the relationship. Business-owned sites, official social profiles, regulatory or license pages, trade profiles, chamber pages, and entity-scoped business profiles can count when they identify the business and its local-service operation. Platform case studies, software review pages, generic directories, software listicles, and lead-enrichment pages do not count for this independent proof.

Requirements:
- The page must identify the submitted customer business.
- The page must show the business operates in a local-service vertical, such as plumbing, HVAC, junk removal, cleaning, pest control, lawn care, garage door, appliance repair, electrical, or a comparable service trade.

Write one JSON object per line to `results_local_service_platform_adoption.business_presence.jsonl`:
{"item": { "platform": "<platform>", "business": "<business>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

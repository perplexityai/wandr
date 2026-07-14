You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `va_provider_pricing`
  - `va_provider_pricing.provider_policy`

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

## `va_provider_pricing`

For 50+ providers, cover 4+ service segments per provider from the segment list below; for each provider/segment pair, supply a provider-controlled public source (i.e. 1+ URL) proving segment-scoped managed human assistant/admin/receptionist/support delivery.

The useful evidence is the provider's own public buyer-facing service language, not a buyer recommendation, third-party profile, market-pricing article, ranking, review-sentiment claim, procurement judgment, contact-discovery lead, or outreach target.

Service segments in scope:
- **medical_admin**: medical-practice admin, healthcare virtual assistant, HIPAA-aware front-office, clinical-office support, patient scheduling, billing-support, or comparable medical admin service
- **legal_admin**: legal virtual assistant, paralegal-style admin support, law-firm intake, legal document/admin workflow, or comparable law-practice support
- **real_estate_admin**: real-estate transaction coordination, ISA, listing/admin support, CRM follow-up, property-management admin, or comparable real-estate support
- **bookkeeping_finance_admin**: bookkeeping, accounts payable/receivable, invoicing, payroll admin, expense tracking, or comparable finance-admin support
- **virtual_receptionist_customer_support**: virtual receptionist, call answering, live chat, customer support, helpdesk, appointment setting, or comparable front-line support
- **executive_admin**: executive assistant, founder assistant, calendar/inbox/travel coordination, operations admin, or comparable executive admin support

Providers ought to offer a managed human assistant, receptionist, admin, or support layer to clients. Pure accounting firms, SaaS bookkeeping products, self-managed freelancer marketplaces, software-only or AI-assistant products, individual freelancer profiles, worker-side employment pages, job boards, generic BPO/contact-center vendors, and professional-service firms are out of scope unless the page clearly offers a managed human assistant/receptionist/admin/support service. The source should be a segment-dedicated or clearly segment-scoped service, industry, specialty, package, or provider-owned resource context. Broad homepages, all-purpose service pages, pricing pages, FAQ pages, and "industries served" pages count only when a durable URL, page title, heading, navigation label, or self-contained section visibly scopes the cited evidence to the claimed segment; a general capability menu or passing industry mention is not enough.

Requirements:
- The page must clearly identify the named provider.
- The page should communicate that it is a provider-controlled official source for the named provider, such as an official service, pricing, package, FAQ/help, terms/legal, policy, agreement, or provider-owned resource page. Third-party directories, review platforms, competitor comparison pages, SEO roundups, generic market-pricing articles, public profile pages, and similar non-provider-controlled surfaces do not count.
- The page must make the claimed service segment visible as the page's source context, such as through a segment-specific URL, title, heading, navigation label, service/industry/specialty framing, package name, or self-contained page section.
- The page must show concrete managed human assistant/admin/receptionist/support delivery detail for the claimed segment, such as task scope, workflow, staffing, vetting/training, coverage hours, handoff model, dedicated/team model, compliance-facing handling, service package, or comparable operational detail. A bare segment list such as "we serve healthcare, legal, and real estate" without segment-specific delivery detail is not enough.

Write one JSON object per line to `results_va_provider_pricing.jsonl`:
{"item": { "provider": "<provider>", "service_segment": "<service_segment>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `va_provider_pricing.provider_policy`

Cross-tasknode identifier discipline: this task is for the same {= provider =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= provider =}+ providers, cover each of the 4 client-service policy families per provider from the list below; for each provider/policy-family pair, supply a provider-controlled public source (i.e. 1+ URL) stating an exact binding commercial mechanic for that provider's managed human assistant/admin/receptionist/support service.

The useful evidence is the provider's own public buyer-facing policy, terms, FAQ/help, pricing, package, agreement, or service language, not a third-party pricing roundup, provider ranking, review-sentiment claim, procurement recommendation, contact-discovery lead, worker-side employment term, or software subscription term.

Policy families, which we refer to as `policy_family`, are:
- `cancellation_commitment`: cancellation notice, minimum commitment, renewal, pause, downgrade, or termination mechanics for the client service relationship.
- `refund_guarantee_trial`: refund, no-refund, pro-rata credit, satisfaction guarantee, service guarantee, free trial, paid trial, or trial-conversion mechanics.
- `rollover_extra_unit`: unused-hour rollover or expiry, added-hour or added-seat charge, overtime, plan credit, or extra-unit mechanics.
- `setup_onboarding_replacement`: setup fee, onboarding, assistant replacement, rematch, backup coverage, or service-transfer mechanics.

Providers ought to offer a managed human assistant, receptionist, admin, or support layer to clients. Pure accounting firms, SaaS bookkeeping products, self-managed freelancer marketplaces, software-only or AI-assistant products, individual freelancer profiles, worker-side employment pages, job boards, generic BPO/contact-center vendors, and professional-service firms are out of scope unless the page clearly offers a managed human assistant/receptionist/admin/support service. The source should be a policy-family-specific terms, FAQ/help, pricing/package, agreement, billing, plan, or provider-owned resource context. Broad homepages and all-purpose service pages count only when a durable URL, page title, heading, FAQ item, table row, plan note, or self-contained page section visibly scopes the cited rule to the claimed policy family. The same pricing, FAQ, terms, or billing page may support multiple policy families only when each cited family has its own visible policy context and exact rule on that page. A price, rate table, "contact us", "custom quote", "flexible plan", or broad sales claim is not a policy mechanic unless the page also states an exact client-facing rule.

Requirements:
- The page must clearly identify the named provider or clearly govern the named provider's client-service relationship.
- The page should communicate that it is a provider-controlled official source for the named provider, such as an official service, pricing, package, FAQ/help, terms/legal, policy, agreement, or provider-owned resource page. Third-party directories, review platforms, competitor comparison pages, SEO roundups, generic market-pricing articles, public profile pages, and similar non-provider-controlled surfaces do not count.
- The page must make the claimed policy family's source context visible: for `cancellation_commitment`, a terms, renewal, cancellation, commitment, account, subscription, FAQ, or plan context; for `refund_guarantee_trial`, a refund, guarantee, trial, credit, satisfaction, FAQ, or plan context; for `rollover_extra_unit`, a rollover, unused-hour, expiry, overage, added-unit, billing, plan-credit, package, FAQ, or rate-table context; for `setup_onboarding_replacement`, a setup-fee, onboarding, replacement, rematch, backup-coverage, transfer, account-management, FAQ, or plan context. A page reused across policy families must visibly localize each family separately rather than relying on a page-wide pricing or FAQ label.
- The page must state an exact binding client-service commercial mechanic matching the claimed `policy_family`: for `cancellation_commitment`, a cancellation, renewal, notice, commitment, pause, downgrade, or termination rule; for `refund_guarantee_trial`, a refund/no-refund/pro-rata, satisfaction guarantee, service guarantee, free-trial, paid-trial, or trial-conversion rule; for `rollover_extra_unit`, an unused-hour rollover/expiry, extra-hour, extra-seat, overtime, plan-credit, or extra-unit rule; for `setup_onboarding_replacement`, a setup fee, onboarding, assistant replacement/rematch, backup coverage, or service-transfer rule.

Write one JSON object per line to `results_va_provider_pricing.provider_policy.jsonl`:
{"item": { "provider": "<provider>", "policy_family": "<policy_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

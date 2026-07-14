You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `merchant_kyb_onboarding_source_provenance`
  - `merchant_kyb_onboarding_source_provenance.admission_gate`

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

## `merchant_kyb_onboarding_source_provenance`

For 75+ merchant/KYB onboarding or merchant-risk lifecycle vendors/platforms, cover 3+ classes from the following source-class list per vendor and supply a public source for each class (i.e. 1+ URL under each selected source class).

The work is source provenance, not vendor comparison. Keep claims source-stated: pages should show what a public source can prove about a vendor's merchant onboarding, KYB/business onboarding, merchant underwriting, payfac/acquirer/marketplace onboarding, or ongoing merchant monitoring role.

Source classes:
- `official_onboarding_product`: vendor-controlled product, solution, use-case, or docs page where merchant onboarding, KYB/business onboarding, merchant underwriting, payfac/acquirer/marketplace onboarding, or merchant monitoring is explicit and central
- `docs_or_api_or_integration`: developer docs, API guide, workflow docs, endpoint or field reference, dashboard/rules docs, webhook guide, or integration docs that expose source-stated mechanics
- `named_customer_case`: customer story, case study, joint story, or substantive testimonial that names a customer and describes use of the vendor/platform
- `dated_change_or_release`: own-domain changelog, release note, product update, press release, or dated docs page with an explicit source date and relevant feature claim
- `dated_independent_editorial`: fetchable independent payments, risk, fintech, or trade-publication coverage with an explicit source date and substantive vendor, feature, or relationship coverage

Broad fraud, AML, identity, chargeback, or transaction-monitoring sources do not count unless the page ties the vendor to the merchant/KYB/business onboarding or merchant monitoring lifecycle. Rankings, recommendation roundups, procurement grids, review aggregator profiles, lead-generation pages, login-walled pages, funding-only mentions, broad educational pages that do not name the vendor/platform as provider, and vendor-authored "best" listicles do not count.

Do not rank vendors, recommend vendors, infer compliance adequacy, design risk systems, provide implementation advice, contact or enrich leads, or describe fraud-evasion tactics.

Requirements:
- The page must clearly identify the claimed vendor/platform.
- The page must make the declared source class visible and substantive, with the class-specific source role described for that source class.
- The page must explicitly tie the vendor/platform to merchant onboarding, KYB/business onboarding, merchant underwriting, payfac/acquirer/marketplace onboarding, or ongoing merchant monitoring.
- The page must contribute a source-class-appropriate provenance detail: product positioning or use-case evidence for official product pages; mechanics such as workflow, API, fields, decisions, cases, rules, dashboards, integrations, or webhooks for docs/API/integration pages; named customer use for customer/case rows; dated feature/change evidence for release rows; dated substantive third-party coverage for independent editorial rows.
- For dated release/change or dated independent editorial rows, the page must show an explicit source date.

Write one JSON object per line to `results_merchant_kyb_onboarding_source_provenance.jsonl`:
{"item": { "vendor_platform": "<vendor_platform>", "source_class": "<source_class>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `merchant_kyb_onboarding_source_provenance.admission_gate`

Cross-tasknode identifier discipline: this task is for the same {= vendor_platform =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= vendor_platform =}+ merchant/KYB onboarding or merchant-risk lifecycle vendors/platforms, supply an official gate source for each vendor (i.e. 1+ URL).

The gate source should be vendor-controlled product, solution, use-case, documentation, integration, release, or comparable official material that explicitly ties the vendor/platform to merchant onboarding, KYB/business onboarding, merchant underwriting, payfac/acquirer/marketplace onboarding, or ongoing merchant monitoring.

Broad fraud, AML, identity, chargeback, or transaction-monitoring sources do not count unless the official source makes that merchant/KYB/business onboarding or merchant-monitoring lifecycle tie explicit.

Requirements:
- The page must clearly identify the claimed vendor/platform.
- The page must be an official controlled source for the vendor/platform, not a third-party article, review grid, procurement listing, ranking/listicle, lead-generation page, or login-walled stub.
- The page must explicitly tie the vendor/platform to merchant onboarding, KYB/business onboarding, merchant underwriting, payfac/acquirer/marketplace onboarding, or ongoing merchant monitoring.
- The page must expose a concrete official gate detail, such as KYB/business verification, beneficial-owner checks, merchant underwriting, onboarding workflow, API or integration mechanics, risk decisions, monitoring alerts, reviews, rules, cases, or comparable source-stated functionality.

Write one JSON object per line to `results_merchant_kyb_onboarding_source_provenance.admission_gate.jsonl`:
{"item": { "vendor_platform": "<vendor_platform>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `rcm_website_surfaces`

For 70+ companies in the healthcare revenue cycle / healthcare financial workflow ecosystem, find 2+ named public proof objects per company. For each company / proof object, supply public evidence in 2+ different source roles, with 1+ URL for each role.

The unit of work is a specific public proof object, not a common website page. A valid record says, in effect: this RCM-adjacent company has this named proof datum, and this public page identifies the company, the proof object, and the submitted source role. Do not fill a fixed proof-kind matrix for every company; choose proof objects that public evidence actually supports. Across the whole answer, represent at least four of the proof kinds below and all three source roles when support exists. Use additional effort for more companies rather than harvesting extra proof objects from one large vendor.

Eligible company scope: revenue cycle management, healthcare payments, revenue integrity, patient financial engagement, clearinghouse, medical billing, coding, denials / appeals, payment integrity, patient access, or adjacent healthcare financial workflow software or services. Provider health systems, payers, generic trade associations, generic software vendors, and article publishers are not the submitted company, though they may appear as customers or independent sources for a proof object.

Use one of these controlled `proof_kind` values in the answer:
- `named_customer_outcome`: a named customer, provider, payer, or care-organization outcome, deployment, case study, testimonial, or metric.
- `independent_accreditation_or_certification`: a named accreditation, certification, attestation, or comparable named status from an accreditor, certification body, or public trust / security source.
- `platform_or_partner_directory_listing`: a named app, integration, platform, marketplace, partner, payer, clearinghouse, or directory listing.
- `association_peer_review_or_award`: a named peer review, award, analyst/evaluator recognition, industry association review, or comparable public recognition.
- `named_workflow_deployment`: a named product, integration, workflow deployment, implementation, or metric tied to a concrete RCM workflow.

Use one of these controlled `evidence_role` values as the key:
- `claimant_or_vendor_surface`: the cited page is primary for the vendor's or claimant's own claim about the proof object.
- `customer_or_independent_surface`: the cited page is primary for a customer, provider, independent evaluator, analyst, association, media, or comparable non-vendor account of the proof object.
- `directory_or_platform_surface`: the cited page is primary for a directory, marketplace, platform, accreditor, certification body, peer-review list, partner list, or comparable listing / status surface.

The same proof object should not be a generic page category such as "trust center," "case study page," "product page," "login page," or "RCM services." It should be a named public datum: a named customer, named accreditation or certification, named platform listing, named award or peer review, named workflow deployment, named integration, named metric, named standard, or a similarly specific proof object. Deduplicate proof objects by company plus named proof object, even when multiple URLs repeat it.

Sources should be public pages that are primary for the asserted source role. Generic product pages, homepages, contact / demo pages, login shells, search results, rankings/listicles, generic "trusted by" language, generic "secure/compliant" language, and broad RCM capability claims fail unless the page itself carries the named proof object and the submitted source role. Gated reports, private portals, forms that require submission, authenticated content, paywalled pages, and broken pages do not count as the public evidence URL.

For each record, the answer must include:
- `proof_kind`: one controlled proof-kind value from the list above.
- `date_checked`: the date you checked the public page.
- `date_or_status`: the proof object's visible date, status, publication date, certification/listing status, or `not visible` if the page does not show one.
- `named_customer_or_standard`: the named customer, standard, certification, platform, directory, award, workflow, integration, or comparable named object anchor.
- `metric_or_scope`: the visible metric, workflow scope, listing scope, deployment scope, or `not visible` if the page has no metric.
- `caveat`: a concise caveat about staleness, access boundary, acquisition / aliasing, gated artifacts, role limits, or `no caveat visible`.

Do not rank vendors, recommend procurement decisions, collect contact details, test workflows behind authentication, infer PHI handling, or state that a company is secure, compliant, currently certified, or suitable for use beyond what the cited public page directly says. Do not treat missing public evidence as a successful record.

Requirements:
- The page must identify the submitted company, public brand, acquired brand, or claimant surface and tie it to the healthcare revenue cycle / healthcare financial workflow ecosystem.
- The page must identify the submitted proof object as a named and specific public datum, not just a broad capability or page type.
- The page must be primary for the submitted `evidence_role`.
- The page must substantively support the answer's `proof_kind`, date/status, named anchor, metric/scope, and caveat fields without stretching the public evidence into a ranking, recommendation, contact lead, or security / compliance adequacy conclusion.

Write one JSON object per line to `results_rcm_website_surfaces.jsonl`:
{"item": { "company": "<company>", "proof_object": "<proof_object>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

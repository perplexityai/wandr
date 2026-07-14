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

## `healthcare_edi_api_developer_capability_evidence`

For 55+ healthcare EDI/API vendor products, cover 3+ distinct capability buckets per vendor product with 2+ distinct public evidence URLs per capability.

The vendor/product should be a stable commercial healthcare EDI/API, clearinghouse, interoperability, provider-data, prior-authorization, FHIR/HL7, healthcare iPaaS, or managed EDI/API integration product or product family. Payers, standards bodies, regulators, pure open-source projects, generic RCM agencies, and pure EHR products without a distinct integration/API surface are outside scope. A payer/customer/source-system/EHR-specific connection, connector, profile, implementation-status page, or listing nested under a vendor/operator product is not a separate vendor/product; for example, an Aetna page in Stedi's payer network is evidence for Stedi Healthcare APIs / Stedi Payer Network, and a generated managed-connector page for AdvancedMD, eClinicalWorks, ChiroTouch, Tebra, or a similar downstream system is evidence for the operator's stable integration product family at most, not a distinct vendor/product by itself.

Capability buckets, referred to as `capability_bucket`, are:
- `eligibility_benefits`: X12 270/271, eligibility or benefits checks, coverage or benefits APIs
- `claims_submission`: X12 837 professional/institutional/dental claims or claim-submission APIs
- `remittance`: X12 835 ERA, payment/remittance retrieval, or source-stated 835-to-claim-response mapping
- `claim_status`: X12 276/277 claim status request/response
- `claim_attachments`: X12 275, PWK attachment references, 277 request-for-additional-information attachment workflows, or claim attachment APIs
- `prior_authorization`: X12 278, Da Vinci CRD/DTR/PAS, or prior-authorization submit/inquire/status APIs
- `provider_directory`: provider directory, provider network, provider data API, or Plan-Net evidence when source-stated
- `clinical_or_payer_fhir_api`: clinical or payer FHIR API evidence such as FHIR R4, US Core, CARIN, patient access, provider access, payer-to-payer, or bulk export
- `integration_bridge_or_managed_edi`: managed EDI/API integration, healthcare iPaaS connector, HL7 v2 interface, X12-to-FHIR bridge, HL7-to-FHIR bridge, or a related source-stated healthcare integration surface

Sources should be public and usable without login, account creation, sales contact, or hidden PDF/report access. Vendor/product-controlled or official technical implementation surfaces are the normal evidence home: official API references, developer docs, implementation guides, OpenAPI/schema pages, transaction or standard mappings, developer changelogs, capability-specific marketplace technical listings, and technical product pages that name specific standards or programmatic support modes. For each vendor/product and capability bucket, each public evidence URL should independently identify the vendor/product, tie it to the same capability bucket, and carry technical or implementation substance; one URL should not merely fill a missing fragment from another. Generic "we do EDI", "interoperability platform", "HIPAA compliant", "connects to many payers", logo-wall, ranking, listicle, scraper profile, unofficial wrapper, trust/security-only page, state/payer approved-vendor list, and generic companion-guide vendor menu pages are outside the primary capability evidence shape. Standards-body, regulator, payer, and companion-guide pages can provide context or corroboration, but they do not by themselves establish a vendor/product capability. No-source and missing-source states are diagnostics, not capability evidence.

Requirements:
- The page or official URL/title must clearly identify the named vendor/product or an accepted alias, rebrand, or acquisition identity.
- The page must tie that vendor/product to the selected capability bucket through explicit capability, transaction, standard, endpoint, mapping, API, implementation-guide, or programmatic-support evidence.
- The page must include concrete technical or implementation substance from a vendor/product-controlled or official technical implementation surface. Endpoint/method/schema, API reference, OpenAPI docs, implementation guide, transaction mapping, developer changelog, capability-specific marketplace technical listing, or a technical product page naming specific standards/programmatic modes can pass. Broad product positioning, payer/vendor lists, and one-page transaction menus do not.

Write one JSON object per line to `results_healthcare_edi_api_developer_capability_evidence.jsonl`:
{"item": { "vendor_product": "<vendor_product>", "capability_bucket": "<capability_bucket>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

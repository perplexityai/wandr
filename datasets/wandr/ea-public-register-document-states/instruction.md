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

## `ea_public_register_document_states`

For each of the 4 Environment Agency public-register categories listed below, cover 15+ official permission or exemption records; for each record, supply the 2 document-state-family findings listed below, with 1+ official URL for each finding.

The purpose is a current public-register provenance table: what the official register exposes about record identity, permit/document availability, CAR availability, missing/request-only details, publication-window caveats, and link conflicts. It is not a task about whether a site is compliant, risky, well-run, polluted, enforceable, or worth contacting.

Register categories:
- `waste_operations`: Waste Operations; waste operations register; Environmental Permitting Regulations - Waste Operations; waste permit; waste-operations
- `installations`: Installations; industrial installations; industrial-installations; installations register; Environmental Permitting Regulations - Installations
- `water_discharges`: Water Discharges; discharges to water and groundwater; water discharge activity; Environmental Permitting Regulations - Discharges to water and groundwater; water-discharges
- `waste_exemptions`: Waste Exemptions; Waste Exemption Registrations; registered waste exemptions; exempt waste operations; waste exemption register; waste-exemptions

Document-state families:
- `primary_document_state`: primary document state; permit document state; permit or registration document availability; primary permit document evidence; public primary document evidence
- `car_publication_state`: CAR publication state; CAR availability; compliance assessment report publication state; CAR/publication-scope evidence; public CAR evidence

The document-state families are exactly `primary_document_state` and `car_publication_state`. More specific availability labels are finding details, not separate document-state families.

Each `primary_document_state` family finding should preserve the source-stated record labels needed to identify the record and identify the primary-document availability detail shown by the official record:
- `permit_document_available`: a published permit, registration, standard-rules, or primary document link is shown for the exact record
- `no_public_permit_document_shown`: the exact record is shown but no public primary document link/table entry is shown
- `request_only_or_unclear_document`: the exact record uses request-document wording or unclear primary-document availability
- `conflict_or_link_issue`: an official primary-document link/table/search-detail conflict is visible for the exact record

Each `car_publication_state` family finding should preserve the source-stated record labels and CAR/publication evidence visible for that exact record and identify the CAR/publication availability detail shown by the official record:
- `car_available`: a CAR or compliance-assessment document link is shown for the exact record
- `car_not_shown`: the exact record is shown but no CAR link/table entry is shown
- `outside_car_publication_scope`: the record category/date is visibly outside the stated online CAR publication scope
- `car_holding_period_possible`: record-level timing plus official CAR publication wording makes the holding-period state plausible
- `request_only_or_unclear_document`: the exact record uses request-document wording or unclear CAR availability
- `conflict_or_link_issue`: an official CAR link/table/search-detail conflict is visible for the exact record

GOV.UK and EA support/FAQ pages are background for register scope, CAR publication windows, request semantics, and holding-period caveats. A cited URL still needs record-scoped official EA public-register evidence. Passing record-level evidence is normally a record-detail page, a record-level document table, an official document or CAR link tied to the exact record, or another official public-register page whose visible content is scoped to that one record. Generic complete-register downloads, search-all pages, broad search result pages, bulk endpoints, and API response blobs or endpoints do not count as record-level evidence.

Requirements:
- The page must be official Environment Agency public-register evidence scoped to the claimed category and exact record: a record-detail page, record-level document table, official public-register document or CAR link tied to that record, or another official public-register page whose visible content is scoped to that one record. Generic complete-register downloads, search-all pages, broad search results, bulk endpoints, API response blobs or endpoints, standalone guidance/FAQ pages, commercial products, operator websites, legal summaries, news/local commentary, and third-party aggregators do not count as record-level evidence.
- The page must preserve the category-specific record identity: the official identifier label and value, plus holder/operator, site/activity/location, status, and date labels when those fields are public for that register family. Do not force missing category-specific fields into invented universal fields.
- The page must support the claimed `document_state_family` for that exact record without interpreting document contents: `primary_document_state` findings need primary permit/registration document availability evidence, while `car_publication_state` findings need CAR availability, publication-scope, holding-period, request-only, or CAR-link evidence. The evidence must not summarize CAR breaches, scores, remedial actions, permit-condition meaning, or operator performance.

Write one JSON object per line to `results_ea_public_register_document_states.jsonl`:
{"item": { "register_category": "<register_category>", "record_identifier": "<record_identifier>", "holder_or_operator": "<holder_or_operator>", "site_or_activity": "<site_or_activity>", "document_state_family": "<document_state_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

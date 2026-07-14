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

## `healthy_building_firms`

For each of the 6 credential families listed below, find 42+ healthy-building, indoor-environmental-quality, mold/IAQ, EMF, green/wellness-building, building-biology, performance-testing, or comparable service firms or public practices per family; for each (`credential_family`, `firm_or_practice`) pair and each of the 2 evidence sides listed below, supply a public provenance source (i.e. 1+ URL).

The useful claim is public cross-source provenance for providers in a fragmented professional ecosystem, not a vendor ranking, hiring recommendation, contact list, health-efficacy claim, legal-compliance conclusion, or safety verdict.

Credential families:
- `building_biology`: building-biology, healthy-home biology, EMF/RF assessment, low-toxicity building, or comparable building-biology professional programs.
- `indoor_environmental_or_mold`: indoor environmental, IAQ, industrial-hygiene, mold, microbial, radon, or comparable indoor environmental professional programs.
- `healthy_building_or_wellness_standard`: healthy-building, wellness-building, building-health rating, wellness-standard, ambassador, provider, or comparable programs.
- `green_building_professional_program`: green-building, passive-house, LEED-like, high-performance-building, sustainability professional, or comparable building-performance programs.
- `regulator_license`: public regulator licenses, registrations, or lookups for mold, IAQ, environmental testing, radon, industrial hygiene, or comparable services.
- `iaq_or_performance_testing_program`: IAQ, performance-testing, verification-provider, data-provider, commissioning/testing, or comparable built-environment performance programs.

Evidence sides:
- `authority_record`: an issuer, regulator, association, certification, membership, professional directory, program-provider, license lookup, or comparable authority/program source tying the provider or a named principal to the credential family.
- `independent_service_surface`: a separate service, case, project, official practice, or focused trade/editorial surface tying the same provider to relevant healthy-building, IEQ, mold/IAQ, EMF, green/wellness-building, or performance-testing service work.

A valid `firm_or_practice` is a real firm, consultancy, public solo practice, or comparable service provider with public source-stated healthy-building, IEQ, building-biology, mold/IAQ, EMF, green/wellness-building, performance-testing, or adjacent service identity. Product-only monitor/device/platform vendors, pure directories, certifiers or standards owners without provider service work, generic construction firms without source-stated health/IEQ capability, medical clinics, blogs, marketplaces, lead-generation pages, ranking/listicle-only entities, and contact-enrichment surfaces do not count. A named individual credential can support a firm or practice only when the page visibly ties that person to the firm/practice; public solo practices count.

Requirements:
- The page must clearly identify the named firm/practice, or a named principal visibly tied to that firm/practice.
- The page must make the `evidence_side` source role visible: for `authority_record`, it must communicate (possibly via URL among other things) an issuer, regulator, association, certification, membership, professional-directory, license-lookup, program-provider, or comparable authority/program context for the claimed `credential_family`; for `independent_service_surface`, it must read as a service, case, project, official practice, or focused trade/editorial context for the same provider, rather than an authority/program listing used only for the credential tie.
- The page must state the side-appropriate provenance finding: for `authority_record`, a credential, license, membership, certification, directory/program participation, named-principal tie, or comparable authority-family tie; for `independent_service_surface`, a relevant healthy-building, IEQ, mold/IAQ, EMF, building-biology, green/wellness-building, performance-testing, or comparable service capability.

Write one JSON object per line to `results_healthy_building_firms.jsonl`:
{"item": { "credential_family": "<credential_family>", "firm_or_practice": "<firm_or_practice>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `final_mile_carriers`

For 250+ operating U.S.-focused final-mile, courier, same-day, expedited, or specialty delivery carrier companies, supply evidence for each of the 2 evidence types, with source URL coverage for each type (minimum 1 per type). ECA can be a useful discovery surface, but the company universe is open and valid carriers do not need to appear in ECA.

The evidence types are:
- `company_capability`: a company-controlled source, usually the carrier's own site or official profile, that shows the company's delivery/carrier services and public geography or service area.
- `independent_legitimacy`: a non-company public source showing identity, authority, association membership, directory presence, credential, registry status, industry listing, or comparable legitimacy signal.

For downstream reading, include the canonical company name, legal name or DBA when the source reveals one, official company URL when known, primary geography or service area, carrier service lane, capability or legitimacy signal, independent source type when relevant, public regulatory ID or credential when relevant, checked date, confidence, and source notes. Use 2026-06-29 as the checked date unless the source was checked later.

Useful service lanes include:
- `same-day courier`
- `final mile / last mile delivery`
- `expedited / hot shot delivery`
- `medical / life-science courier`
- `air-cargo ground service`
- `white glove delivery`
- `regional route delivery`
- `refrigerated / cold-chain delivery`
- `warehousing or cross-dock plus delivery`
- `specialty local or regional delivery carrier`

Independent source type should be factual, not promotional. Useful independent source types include:
- `association_or_member_directory`
- `regulator_or_public_registry`
- `credential_or_certification_surface`
- `state_or_regional_industry_directory`
- `public_airport_or_cargo_ecosystem_source`
- `trade_publication_or_event_source`
- `reputable_industry_database`
- `other_independent_public_source`

Public sources can include company service pages, carrier association directories, FMCSA/SAFER or other registries, state or regional courier/trucking associations, credential or certification surfaces, industry directories, trade publications, venue or conference pages, and public airport or cargo ecosystem pages. Private lead-enrichment databases, quote-request funnels, rankings, customer reviews without carrier facts, generic SEO pages, procurement advice, and delivery recommendations are out of scope. ECA or other association pages may support independent legitimacy when they identify a carrier/provider, but mixed vendor/sponsor pages do not make a company a carrier by themselves.

Requirements:
- The page must identify the claimed company, or bridge the submitted trade name to a legal/DBA name, with enough public context to distinguish it from unrelated same-name entities.
- The page must fit the claimed `evidence_type`: `company_capability` evidence should be company-controlled service/geography evidence, while `independent_legitimacy` evidence should come from a non-company public source showing identity, authority, membership, credential, registry status, directory presence, industry listing, venue listing, or comparable legitimacy.
- The page must support concrete carrier substance at the claimed evidence type. For `company_capability`, it should show a final-mile, courier, same-day, expedited, specialty delivery, or carrier-adjacent operating capability and a public geography or service area. For `independent_legitimacy`, it should show a concrete public legitimacy signal for the same company, such as current carrier authority, active directory or association presence, public credential, registry status, industry listing, venue listing, or equivalent non-company corroboration.

Write one JSON object per line to `results_final_mile_carriers.jsonl`:
{"item": { "carrier_company": "<carrier_company>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `public_company_data_asset_provenance`

For each of the 6 `data_domain` labels below, cover 20+ US/Canada public companies per domain. For each company, name at least 1+ concrete data asset, product, corpus, database, or dataset, and provide one source for each of the 2 evidence axes (i.e. 1+ URL per axis).

Use `ticker_exchange` to disambiguate the public company. The company should be publicly traded and headquartered or incorporated in the United States or Canada; foreign or private companies do not count.

The `data_domain` labels are:
- `financial_market_company_intelligence`: financial, market, issuer, company-intelligence, research, ratings, filings, or benchmark data.
- `credit_risk_business_identity_records`: credit, risk, business identity, corporate-public-record, ownership, due-diligence, or entity-reference data.
- `insurance_real_estate_property`: insurance, claims, catastrophe, real-estate, mortgage, building, rental, listing, or property data.
- `scientific_medical_healthcare`: scientific, clinical, pharmaceutical, provider, patient, healthcare-market, or life-sciences data.
- `geospatial_mobility_logistics_climate`: geospatial, mapping, mobility, fleet, logistics, weather, climate, satellite, or earth-observation data.
- `consumer_marketing_sports_alternative`: consumer, marketing, advertising, audience, transaction, sports, media, web, or alternative data.

The `evidence_axis` labels are:
- `asset_provenance`: a company-controlled or regulatory source explicitly states that the named asset/product/corpus is proprietary, owned, curated, authoritative, unique, exclusive, internally assembled, first-party, or otherwise company-controlled. A broad product page that merely says the company offers a platform, data, insights, AI, or analytics is not enough.
- `ai_search_analytics_linkage`: a company-controlled or regulatory source explicitly ties the same named asset/product/corpus to a named AI, search, analytics, question-answering, research, workflow-intelligence, decisioning, scoring, model, API, or analytical-product use. Generic statements that the company uses AI/analytics, offers dashboards, or provides data-driven insights are not enough unless the source ties that capability to the named asset/product/corpus.

Eligible sources are high-specificity company-controlled or regulatory pages such as SEC/SEDAR filings, issuer annual reports, investor presentations, official product/data-asset pages, official data catalogs, API or customer documentation, and official press releases. Product pages, investor decks, and press releases pass only when they name the submitted asset and contain the axis-specific claim. Third-party articles, vendor rankings, investment pieces, generic RAG explainers, data-quality verdicts, implementation guides, contact or lead-enrichment pages, and marketplaces that mainly package third-party datasets do not establish a row by themselves.

Requirements:
- The page must identify the named asset/product/corpus and tie it to the claimed company and `data_domain`.
- The page must support the claimed `evidence_axis` for that same named asset/product/corpus.
- The `data_asset` should be the data-bearing asset itself. End-user dashboards, AI assistants, advertising tools, workflow suites, and generic platforms count only when the source makes the underlying named data asset/corpus/database visible for that same submitted name.
- Reusing the same URL for both evidence axes can pass only if separate excerpts from that page independently satisfy each axis-specific bar for the exact same named asset/product/corpus.

Write one JSON object per line to `results_public_company_data_asset_provenance.jsonl`:
{"item": { "data_domain": "<data_domain>", "company": "<company>", "ticker_exchange": "<ticker_exchange>", "data_asset": "<data_asset>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

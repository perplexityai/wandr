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

## `uk_foam_company_provenance`

For 250+ UK-operating companies that publicly state foam conversion, upholstery, seating, mattress or bedding, technical-foam, foam bonding or lamination, transport seating, or closely adjacent manufacturing capability, cover the 4 provenance facets listed below for each company by supplying a public source (i.e. 1+ URL per facet).

This is a public provenance map, not a supplier recommendation list or sales workbook. Do not report emails, phone numbers, named contacts, quote forms, outreach paths, rankings, lead scores, procurement strategy, CRM dedupe notes, or private financial-performance claims.

Use one stable submitted `company` string for the same operating company across all facets. Legal names, registered names, trading styles, and alias evidence can appear in `answer` or excerpts, but an unrelated real company or statutory registry entry is not valid merely because it has a Companies House-style page.

Provenance facets:
- `capability_statement`: the page states the company's relevant foam, upholstery, seating, mattress, bedding, bonding, lamination, technical-foam, transport-seating, or adjacent manufacturing capability in source wording.
- `uk_operating_presence`: the page ties the company to a concrete UK operating site, factory, plant, production location, office, or comparable operating presence. A Companies House registered office alone is not enough for this facet.
- `corporate_registration`: the page is a Companies House profile or comparable statutory registry surface for the company's registered identity, status, company number, incorporation, or similar registration fact.
- `sector_evidence`: the page states a served market, application, customer type, customer group, or sector for the company's relevant products or services.

Official company websites, capability pages, product pages, public association or member profiles, certification pages, reputable trade directories, industry articles, and statutory registry pages can all work when the cited page visibly earns the facet role. Companies House-style registry pages work for `corporate_registration`; they do not establish `capability_statement` or `sector_evidence`, and registered-office-only text does not establish `uk_operating_presence`.

Requirements:
- The page must clearly identify the submitted company, legal entity, trading name, or operating brand.
- The page should have the source role required by `provenance_facet`.
- The page must support the claimed provenance fact for `provenance_facet`.

Write one JSON object per line to `results_uk_foam_company_provenance.jsonl`:
{"item": { "company": "<company>", "provenance_facet": "<provenance_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

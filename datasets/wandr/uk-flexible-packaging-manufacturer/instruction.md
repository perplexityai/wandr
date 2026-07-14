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

## `uk_flexible_packaging_manufacturer`

For 120+ UK legal entities that are publicly evidenced as active/current flexible-packaging manufacturers or converters, cover each of the 4 evidence axes listed below for each company by supplying a public source (i.e. 1+ URL under each axis).

Use `company_name` for the legal Companies House name, and `company_number` for the Companies House number. Trading names, brand names, group ownership, subsidiaries, prior names, and acquisition ambiguity should be recorded as context in the answer rather than replacing the legal-entity identity.

The evidence axes of interest, which we refer to as `evidence_axis`, are:
- `registry_identity`: Companies House identity and currentness for the submitted legal entity.
- `product_scope`: flexible-packaging product evidence, such as polythene bags, films, sheeting, pouches, lidding films, shrink film, laminates, barrier films, sacks, or flexible food packaging.
- `manufacturing_capability`: production or conversion evidence, such as manufacture, conversion, extrusion, printing, lamination, slitting, pouch making, or film production.
- `public_size_or_filing_state`: a public source-scoped state such as average employee count when disclosed, latest accounts date or status, accounts document type, confirmation-statement currentness, a simple filed balance-sheet field, or `not_disclosed_in_cited_filing` when the cited filing scope supports that state.

Official company pages are preferred for product and manufacturing evidence. BPF/BPIF member profiles and reputable industry profiles can also count when they make the product-specific or production/conversion claim themselves. Companies House is required for `registry_identity`. Lead-generation directories, contact-enrichment pages, supplier-matching pages, rankings, and procurement-style pages do not count as product/manufacturing evidence.

Answer metadata should include `product_family` when the cited page supports it, plus any trading-name, brand, subsidiary, prior-name, acquisition, filing-state, checked-date, conflict, or source-scoped non-disclosure notes needed to keep the legal entity and evidence state clear. Do not make supplier recommendations, vendor rankings, creditworthiness claims, solvency claims, investment conclusions, procurement advice, or financial-health judgments.

Requirements:
- The page must identify the submitted company or a named operating/trading identity that the answer links to the submitted Companies House legal entity.
- The page must have the source role required by `evidence_axis`: Companies House for `registry_identity`; an official company page, BPF/BPIF profile, or reputable industry profile for `product_scope` and `manufacturing_capability`; and Companies House, a filed account/filing-history page, an official company profile, or another reliable public source for `public_size_or_filing_state`.
- The page must support the evidence content required by `evidence_axis`: legal name, company number, active/current status or explicit non-current state, and legal-to-operating context for `registry_identity`; specific flexible-packaging products for `product_scope`; explicit production/conversion activity for `manufacturing_capability`; or a source-scoped filing/size state for `public_size_or_filing_state`.

Write one JSON object per line to `results_uk_flexible_packaging_manufacturer.jsonl`:
{"item": { "company_name": "<company_name>", "company_number": "<company_number>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

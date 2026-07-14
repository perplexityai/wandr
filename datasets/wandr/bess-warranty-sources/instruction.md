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

## `bess_warranty_sources`

For 100+ companies, identify 1+ named stationary commercial, C&I, or utility BESS product or product family per company, and cover the 3 public source-state facets below with a source (i.e. 1+ URL) that keeps product, warranty/SoH/performance, and source-standing claims scoped to what the cited page actually shows.

This is a public source-state task, not a warranty-generosity ranking, procurement recommendation, vendor firmographic table, or project pipeline list.

Evidence facets:
- `commercial_bess_product_identity`: official or vendor-controlled evidence that the named company markets the named stationary commercial/C&I/utility BESS product or product family.
- `public_warranty_or_soh_state`: public evidence for the product or product family warranty, state of health, retained-capacity term, performance guarantee, cycle life, throughput life, warranty-scope period, operating-condition limit, or explicit contract/local-service deferral. Generic product pages without warranty, SoH, retained-capacity, cycle, throughput, guarantee, or deferral language do not satisfy this facet.
- `source_applicability_and_standing`: evidence that the source host or issuer, document date/version, region/model/product scope, and source class are what the finding claims. This facet is about source applicability and provenance, not simply repeating a product or warranty fact.

Companies should be actual vendors or company brands associated with stationary commercial/C&I/utility BESS systems. Products should be real cabinet, rack, container, modular, or product-family offerings tied to the company. Exclude residential-only storage, inverter-only products, EMS-only/software-only products, cells/modules without a system product, EPC/project-service-only pages, procurement/ranking/investment/safety/design advice, and generic distributor catalog entries without a source-state signal.

Requirements:
- The page must clearly identify the named company and named product or product family in a stationary commercial/C&I/utility BESS context.
- The page must make source standing visible at the bar appropriate to `evidence_facet`: official/vendor-controlled for `commercial_bess_product_identity`; explicit source class for `public_warranty_or_soh_state` when using vendor pages, official-linked CDN assets, company-issued releases, distributor mirrors, or third-party guides; and host/issuer/date/version/region/model/source-class evidence for `source_applicability_and_standing`. A mirror can be useful only when represented as a mirror or distributor source, not as official vendor-hosted evidence.
- The page must contribute a facet-specific public source-state signal for the submitted `evidence_facet`, not just a generic mention of batteries or a generic company profile.
- The page must keep the claim scoped to the cited source's visible product/model, region, date/version, source class, warranty trigger, operating conditions, cycle/throughput limit, retained-capacity percentage, performance guarantee, or explicit deferral language when those limits are present. Source-local absence or deferral is not a global statement that the vendor has no warranty or SoH policy.

Write one JSON object per line to `results_bess_warranty_sources.jsonl`:
{"item": { "company": "<company>", "product": "<product>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

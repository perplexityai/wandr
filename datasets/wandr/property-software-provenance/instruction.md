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

## `property_software_provenance`

For 70+ property, rental, community-association, condo/HOA, commercial, hospitality, affordable-housing, self-storage, or adjacent real-estate operations software products, cover 5+ public provenance facets per product by supplying 1+ source-backed URLs for each product-facet record.

Name the vendor, the specific product/suite/edition, and source-stated or source-supported segment tags such as residential, multifamily, HOA, condo, commercial, short-term-rental, hospitality, affordable, self-storage, or mixed portfolio. The product set is open; the seed's vendor examples are not a canon.

This task is public capability and transparency provenance. It is not a vendor ranking, buyer guide, procurement recommendation, easiest-setup score, migration guide, implementation advice, accounting or legal advice, review-sentiment task, lead list, contact-enrichment task, or reliability guarantee.

Evidence facets:
- `segment_fit`: official or reputable locator evidence that the product is for one or more property/community-management segments.
- `leasing_resident_operations`: official evidence for leasing, applications, tenant/resident portals, rent collection, communications, work orders, inspections, or comparable property operations.
- `accounting_payments`: official evidence for property accounting, payments, fees, invoicing, budgets, financial reporting, CAM/accounting, or similar finance workflows.
- `maintenance_inspections`: official evidence for maintenance, inspections, service requests, work orders, violations, tasks, or field operations.
- `community_association_hoa`: official evidence for HOA, condo, community-association, board, violations, ARC/ACC, amenity, or association-management workflows.
- `integration_api`: official evidence for APIs, developer docs, integrations, marketplaces, connector directories, interface partners, or named integration surfaces.
- `pricing_transparency`: official pricing, plan, free/freemium, quote/demo/contact-sales, no-public-pricing, conflict, or comparable source-stated commercial transparency state.
- `review_locator`: locator-only evidence from a reputable product/category review profile or software directory. Do not report ratings, sentiment, rankings, or "best" claims.
- `trust_status_locator`: source-stated trust, security, privacy, status, uptime, compliance, subprocessor, or incident/status locator evidence. This is provenance only, not reliability assurance.

Capability and pricing evidence should come from official, vendor-owned, or official-channel pages. Review locator evidence is the only facet that can be satisfied by a third-party review/category profile, and it is locator-only. Third-party pricing blogs, review profiles, comparison pages, listicles, vendor-authored "best software" pages, and generic aggregator summaries do not prove official capability or pricing facets.

Requirements:
- The page must identify or bind the submitted vendor/product/suite/edition and property/community-management segment context.
- The page must visibly fit the submitted evidence facet's source role: official product/help/docs/pricing/integration/trust/status surfaces for official facets, and reputable third-party product/category profile surfaces only for `review_locator`.
- The page must source-state a concrete facet-specific finding. A broad homepage, logo wall, category page, or aggregator profile cannot satisfy a capability, pricing, integration, or trust facet unless it contains the facet-specific source-owned evidence required for that facet.
- The submitted finding should preserve source owner, source date when visible, checked date, pricing/transparency state when relevant, confidence, and any source-backed missing or conflict state without turning public evidence into advice or assurance.

Write one JSON object per line to `results_property_software_provenance.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>", "segment_tags": "<segment_tags>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

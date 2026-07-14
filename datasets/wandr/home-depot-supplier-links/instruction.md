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

## `home_depot_supplier_links`

For 160+ supplier, brand, manufacturer, private-label, licensed-brand, service-vendor, or named program-supplier entities publicly tied to The Home Depot, cover each of the 3 evidence sides below by supplying a source (i.e. 1+ URL per side) that states what the public page itself proves about the relationship.

This is a public provenance task, not a lead list. Keep the claim to source-backed relationship evidence; do not collect contacts, outreach targets, phone numbers, emails, sales rankings, recommendations, procurement strategy, or logistics-broker targeting.

The evidence sides of interest, called `evidence_side`, are:
- `retailer_acknowledged`: a Home Depot-controlled or public Home Depot-facing page naming the supplier/brand/entity with relationship substance. Home Depot retail product pages, corporate newsroom pages, supplier profiles, Eco Actions pages, supplier-diversity pages, Innovation Awards pages, and comparable Home Depot public surfaces can work when they identify the entity and relationship.
- `supplier_stated`: a supplier/manufacturer/brand-controlled page, or a clearly supplier-attributed announcement, stating the Home Depot relationship. Official company sites, investor/newsroom pages, catalogs, store-locator / where-to-buy pages, Home-Depot-specific supplier pages, and supplier-attributed press-wire releases can work when attribution and relationship substance are visible.
- `supplier_substantial_corroboration`: a supplier/manufacturer/brand-controlled page, or a clearly supplier-attributed announcement, that corroborates a harder Home Depot relationship fact beyond ordinary retail availability. The page must state supplier-side substance such as a Home Depot-specific agreement, exclusivity, supplier award/profile/program, service relationship, special-order or shipping/distribution arrangement, private-label/licensed-brand owner relationship, or comparable named Home Depot relationship detail.

Product listings and press-wire pages are secondary source classes: a Home Depot product listing can prove Home Depot availability for a named brand/product, not hidden legal manufacturer identity, and cannot satisfy `supplier_substantial_corroboration` by itself; a wire-service page can prove a supplier-side evidence side only when the issuing or attributed supplier is visible. Supplier store-locator, where-to-buy, catalog, or ordinary product-availability pages can satisfy `supplier_stated`, but they do not satisfy `supplier_substantial_corroboration` unless they also state one of the harder Home Depot relationship facts above. Public shipment, import, or distribution pages count only when they explicitly name the submitted entity and The Home Depot relationship. General routing guides, vendor application instructions, supplier shipping manuals, generic importer pages, and gated commercial shipment/lead databases do not prove a named supplier relationship by themselves.

Source dates, checked dates, confidence labels, and conflict or missing-state notes are provenance details; keep them restrained to what the cited page visibly supports.

Requirements:
- The page must clearly identify the submitted `supplier_or_brand` itself.
- The page must match the declared `evidence_side`: Home Depot-controlled or Home Depot-facing for `retailer_acknowledged`; supplier/manufacturer/brand-controlled or clearly supplier-attributed for `supplier_stated`; supplier/manufacturer/brand-controlled or clearly supplier-attributed with harder Home Depot relationship substance for `supplier_substantial_corroboration`.
- The page must directly tie the submitted entity to The Home Depot through availability, supply, partnership, agreement, program, award, profile, service, or explicit distribution/shipping language.
- The page must expose concrete relationship substance, such as product/category detail, retail availability or exclusivity, supplier relationship wording, program/profile/award context, agreement terms, service role, source-stated date, or explicit shipping/distribution detail. For `supplier_substantial_corroboration`, routine "sold at Home Depot", store-locator, catalog, or product listing availability is not enough without a harder supplier-side relationship fact.

Write one JSON object per line to `results_home_depot_supplier_links.jsonl`:
{"item": { "supplier_or_brand": "<supplier_or_brand>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

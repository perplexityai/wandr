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

## `prd_packaging_suppliers`

Within each of the 6 packaging material families listed below, supply supplier-source evidence for 8+ Pearl River Delta packaging-product/material suppliers per family and each of the 2 source roles, with at least 1 supplier-specific URL for each supplier/source-role combination.

This is a public provenance task anchored to June 20, 2026: the useful work is supplier identity, PRD location, product family, capability, and source-class evidence from public pages, not buying advice.

Target region: Guangdong / Pearl River Delta, China.

Material families:
- `plastic_cosmetic_containers`: plastic cosmetic or personal-care containers such as bottles, jars, tubes, pumps, PET/PP/PETG/HDPE containers, and related molded packaging products.
- `flexible_films_pouches`: flexible packaging such as stand-up pouches, spout pouches, film rolls, retort/vacuum bags, food pouches, and laminated packaging bags.
- `paper_carton_packaging`: paper, carton, corrugated, rigid-box, gift-box, food-box, cosmetic-box, and printed paper packaging products.
- `glass_bottles_containers`: glass bottles, jars, perfume or cosmetic glass containers, dropper bottles, vials, and other glass packaging products.
- `nonwoven_reusable_bags`: non-woven, PP non-woven, reusable shopping, tote, promotional, garment, or fabric-like packaging bags.
- `metal_tin_hardware_packaging`: metal/tin boxes, tin cans, aluminum or metal containers, lids, closures, and packaging hardware/accessory products.

Source roles:
- `supplier_published_surface`: a public page whose URL, title, branding, or text visibly communicates that the supplier publishes or officially controls the surface, such as the supplier's own domain, official channel, or supplier-hosted catalog/profile/certification page; ordinary third-party marketplace storefronts, directory profiles, and trade-fair pages do not count for this role.
- `third_party_authority_surface`: a supplier-specific public page whose URL, title, branding, or publisher context visibly communicates third-party authority, such as a trade-fair organizer exhibitor page, business/industry registry, certification or audit body page/PDF, standards/testing body page, or independently published industry directory profile; supplier-operated storefronts, marketplace product listings, search/category pages, rankings, buying guides, and contact-only pages do not count for this role.

For each supplier/source-role combination, make clear the source-stated supplier name, page-local source-class evidence, PRD location, product/category evidence, and manufacturing or capability evidence. Source-class evidence can come from the URL, title, branding, publisher context, or page text. Source-stated certification, export/market, source-date, missing-source, or name-conflict notes are useful when present, but do not infer them when the page does not state them.

Do not extract contact people, email addresses, phone numbers, prices, MOQ, quote/RFQ mechanics, availability guarantees, rankings, recommendations, lead scores, or procurement advice.

Requirements:
- The page must be supplier-specific and match the submitted `source_role`: `supplier_published_surface` must visibly communicate that the supplier publishes or officially controls the surface, while `third_party_authority_surface` must visibly communicate a third-party publisher, event organizer, registry, certifier, testing/standards body, or independent industry-directory authority rather than a supplier-operated storefront/profile, marketplace product listing, search/category page, ranking, buying guide, contact-only page, or weakly identified product page.
- The page must identify the submitted supplier, or a clear English/Chinese/legal/trade-name alias of that same supplier.
- The page must state a Guangdong or Pearl River Delta location, address, factory, office, or company place for the supplier.
- The page must state packaging products or materials matching the submitted `material_family`; machinery-only vendors and unrelated products do not count.
- The page must state supplier capability or manufacturing/product evidence, such as manufacturer/factory identity, production lines, product catalog depth, custom manufacturing, R&D, quality/certification claims, or comparable capability detail.

Write one JSON object per line to `results_prd_packaging_suppliers.jsonl`:
{"item": { "material_family": "<material_family>", "supplier": "<supplier>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

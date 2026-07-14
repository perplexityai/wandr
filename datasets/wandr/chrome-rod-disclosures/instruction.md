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

## `chrome_rod_disclosures`

For at least 75+ distinct US-based or clearly US-facing suppliers of hard-chrome-plated hydraulic/cylinder rod, piston-rod stock, chrome-plated bar, or chrome-plated shafting, cover the 4 disclosure facets listed below by supplying 1+ public source URL for each facet under each supplier.

A supplier is an organization, distributor, manufacturer, or seller identity. Product lines, SKUs, diameters, stock rows, lengths, local branches, marketplace item IDs, and grade-family names can be useful evidence details, but they do not count as separate suppliers. Different chrome-plated rod lines from the same supplier still belong to the same supplier.

Disclosure facets:
- `rod_offer_and_size`: supplier-tied chrome rod/bar/shafting product identity plus a source-stated diameter, size, stock row, stock length, size range, or dimensional availability signal
- `material_mechanical_properties`: source-stated material grade, steel family, yield strength, tensile strength, hardness, case depth, ASTM/standard reference, or similar mechanical property
- `chrome_surface_spec`: source-stated chrome/plating/surface detail such as chrome thickness, chrome hardness, surface finish, corrosion/salt-spray statement, CPO/IHCP/HCP condition, or induction hardening plus chrome plating
- `commercial_access_state`: positive public commercial state such as price basis, price tiers, stock, order unit, request-quote/call-for-quote language, cut-length rule, lead time, shipping, or freight caveat

This is a public disclosure task, not a procurement comparison. Do not include supplier ranking, lowest-landed-cost analysis, contact enrichment, outreach targets, compatibility guarantees, engineering suitability conclusions, installation advice, or purchasing recommendations.

The sources should be public and usable supplier-owned or supplier-controlled product/spec/catalog pages, manufacturer pages, official distributor pages, fetchable supplier PDFs, or seller-controlled commercial-offer pages. A source should be specific to the named supplier's own chrome rod/bar/shafting offer. Seller-controlled marketplace listings can support `commercial_access_state`; they can support a technical facet only when the listing itself states the needed chrome-rod product and spec facts and makes the seller identity visible. Do not use supplier directories, multi-supplier roundups, generic search/result pages, generic blog guides, plating or rechroming service pages, finished hydraulic-cylinder pages where the rod appears only as a component, seal/gland/tube pages, bare TG&P or cold-finished shafting pages without chrome plating, nitrided-only alternative pages, or pages that only discuss design suitability without product/source-state disclosure.

Requirements:
- The page must identify the submitted supplier, seller, or controlled offer owner and tie that supplier to hard-chrome-plated hydraulic/cylinder rod, piston-rod stock, chrome-plated bar, chrome-plated shafting, IHCP/CPO/HCP, or a directly equivalent chrome-plated rod/bar stock product.
- The page must visibly fit the source role for the submitted `disclosure_facet`: technical facets need product/spec/catalog evidence from a supplier, manufacturer, distributor, or seller-controlled offer that states the technical detail; `commercial_access_state` needs a product-tied commercial source state such as public price, stock, order, quote, cutting, lead-time, shipping, or freight language.
- The page must expose a source-stated disclosure for the submitted `disclosure_facet`. For `rod_offer_and_size`, this means a supplier-tied chrome rod/bar/shafting product identity plus size or dimensional availability. For `material_mechanical_properties`, this means grade or mechanical-property disclosure. For `chrome_surface_spec`, this means chrome/plating/surface disclosure. For `commercial_access_state`, this means a positive public commercial state; silence or absence of a price/MOQ/lead-time field is not enough.

Write one JSON object per line to `results_chrome_rod_disclosures.jsonl`:
{"item": { "supplier": "<supplier>", "disclosure_facet": "<disclosure_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

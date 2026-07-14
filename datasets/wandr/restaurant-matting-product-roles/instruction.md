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

## `restaurant_matting_product_roles`

For each of the 6 restaurant floor zones listed below, identify 8+ distinct commercial matting suppliers/providers; for each supplier in that zone, identify 3+ bounded matting offerings from that supplier; for each restaurant-zone/supplier/offering pair and each of the 8 source roles listed below, supply a role-substantiating source (i.e. 1+ URL).

Restaurant floor zones:
- `entrance_or_vestibule`
- `kitchen_line_or_prep`
- `dishwashing_or_wet_area`
- `bar_or_beverage_area`
- `service_counter_or_cashier_standing`
- `logo_or_guest_facing_branding`

Source roles:
- `official_offering_identity`: supplier-controlled offering material identifies the bounded commercial matting offering.
- `restaurant_zone_foodservice_application`: the page ties the offering to restaurant/foodservice use, the submitted zone, or a matching restaurant-floor hazard/use.
- `official_spec_sheet_or_catalog_pdf`: an official spec sheet, catalog PDF, cut sheet, SDS, sell sheet, or product-document page gives offering-specific technical/material/performance data; an ordinary product page passes only if it clearly presents or links that product-document evidence.
- `cleaning_service_or_warranty_terms`: the page gives offering-specific cleaning, laundering, maintenance, service-cadence, replacement, care, or warranty terms.
- `installation_sizing_or_customization_document`: the page gives offering-specific sizing, installation, edging, thickness, modular/cut-to-fit, placement, custom-logo, color, or configuration documentation.
- `third_party_distributor_product_listing`: a non-supplier distributor, reseller, procurement catalog, or marketplace product page identifies the same offering and gives a commerce path such as price, SKU/order unit, cart, quote, or availability.
- `foodservice_procurement_or_restaurant_supply_context`: a non-supplier restaurant-supply, foodservice-equipment, institutional procurement, bid/spec, facilities catalog, or comparable procurement source places the same offering in restaurant/foodservice/facility purchasing context; a generic distributor page without restaurant/foodservice/procurement context is not enough.
- `independent_standard_certification_or_test_report`: an independent certifier, standards body, lab/test report, certificate/listing, or externally authored test document ties the exact offering to a concrete tested, certified, listed, or evaluated result. Supplier-hosted pages pass only when they reproduce or link an external certificate/report/listing with a named certifier, standard, test method, certificate/listing, or report; supplier marketing claims alone fail.

A valid supplier is a named manufacturer, distributor-owned brand, rental/service provider, custom/logo mat provider, or commercial matting program provider with public commercial floor-matting offerings. Supplier breadth is substantive: parent brands, acquired brands, local branch pages, distributor aliases, and same-company channel names are one supplier identity for a zone unless the cited evidence establishes materially separate providers. A valid supplier offering is a real public commercial floor-matting product line, bounded product family, custom/logo program, or rental/service program from the submitted supplier. One-off size/color/SKU variants, broad retailer departments, generic supplier homepages, consumer home-kitchen mats, non-matting flooring systems, recommendation articles, ranking articles, procurement advice, and contact-only pages that do not identify a public offering are outside this offering universe. Do not split the same supplier/offering into multiple identities because of size, color, backing, SKU, distributor wording, restaurant zone, local service page, or source role; use one stable supplier and one stable offering identity across zones unless the page evidence establishes a genuinely different bounded offering. Foodservice suitability is source-stated: generic commercial, office, hotel, industrial, or architectural matting does not establish a restaurant-zone offering unless the cited evidence ties the offering to restaurant, kitchen, foodservice, bar/beverage, dishwashing/wet-area, guest-facing/logo, cashier/host standing, or a comparable restaurant-floor hazard/use.

Requirements:
- The source must identify the named supplier and bounded offering as commercial floor matting, a commercial mat product line or family, a custom/logo mat program, or a rental/service mat program.
- The submitted supplier must be a real supplier/provider identity, not a local branch, retailer category, reseller page standing in for the manufacturer, or alias of another submitted supplier in the same zone.
- Each supplier must contribute distinct bounded offerings; size/color/SKU/backing/thickness variants and distributor wording variants do not count as separate offerings.
- The source must fit the submitted role:
  - `official_offering_identity` comes from the supplier or official offering materials and identifies the bounded offering.
  - `restaurant_zone_foodservice_application` states restaurant/foodservice zone use or a matching restaurant-floor hazard/use for the submitted zone.
  - `official_spec_sheet_or_catalog_pdf` requires official product-document evidence such as a spec sheet, catalog PDF, cut sheet, SDS, sell sheet, or product-document page with offering-specific technical/material/performance data; a broad catalog or ordinary supplier product page is insufficient unless the cited excerpt is anchored to the exact offering and document-class evidence.
  - `cleaning_service_or_warranty_terms` gives offering-specific cleaning, laundering, maintenance, replacement, service cadence, care, or warranty terms; a generic care page is insufficient unless it names or unambiguously applies to the exact offering/program.
  - `installation_sizing_or_customization_document` gives offering-specific sizing, installation, edging, thickness, modular/cut-to-fit, placement, custom-logo, color, or configuration documentation; a generic size guide is insufficient unless it names or unambiguously applies to the exact offering/program.
  - `third_party_distributor_product_listing` comes from a non-supplier distributor, reseller, procurement catalog, or marketplace product page for the same offering and gives a commerce path such as price, SKU/order unit, cart, quote, or availability.
  - `foodservice_procurement_or_restaurant_supply_context` comes from a non-supplier restaurant-supply, foodservice-equipment, institutional procurement, bid/spec, facilities catalog, or comparable procurement source and ties the same offering to restaurant/foodservice/facility purchasing context; a generic marketplace page with only price/cart information is not enough.
  - `independent_standard_certification_or_test_report` gives independent or externally authored evidence such as a product-specific third-party certificate/listing, lab/test report, named certification body, named standard with offering-specific tested/certified/listed result, NFSI/NSF/ASTM/fire-rating documentation, or comparable non-mere-marketing support. Supplier-hosted pages pass only when they reproduce or link an external certificate/report/listing with a named certifier, standard, test method, certificate/listing, or report for the exact offering. Broad certified-product index pages and supplier marketing claims fail unless the cited excerpt ties the exact offering to the external result.
- The stated finding must be supported for the submitted restaurant zone, supplier, offering, and source role. Same-URL reuse is acceptable only when the page independently earns the submitted role and finding; broad catalog pages that merely list many mats are not enough for the harder third-party, procurement, cleaning/warranty, customization, or independent-standard roles.
- Use source-class diversity for hard roles. A supplier product page may be useful for identity or zone use, but distributor, procurement/restaurant-supply, official document, and independent-standard roles require pages whose source class visibly matches the role and whose excerpt is anchored to the exact offering.

Write one JSON object per line to `results_restaurant_matting_product_roles.jsonl`:
{"item": { "restaurant_zone": "<restaurant_zone>", "supplier": "<supplier>", "offering": "<offering>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

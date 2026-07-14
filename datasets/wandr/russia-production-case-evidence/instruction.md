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

## `russia_production_case_evidence`

For each of the 3 sector bands listed below, cover 24+ Russian production cases and each of the 3 evidence facets listed below. For every production case / evidence facet combination, supply 1+ public URL that gives page-specific evidence for that case and facet.

A production case is a named producer together with a concrete product, product line, facility project, material capability, or production project. The producer alone is too broad, and a product name without a producer is too ambiguous.

Sector bands:
- `rider_or_sport_technical_apparel`: motorcycle gear, cycling apparel, sport technical apparel, or weather/protective rider-facing garments
- `protective_workwear_or_ppe_apparel`: spetsodezhda, protective clothing, safety apparel, or PPE-adjacent sewn products
- `technical_textile_or_material_input`: membrane fabrics, aramid/UHMWPE/polyamide inputs, coated/protective textiles, technical fabrics, thread, fiber, or material inputs relevant to protective apparel

Evidence facets:
- `product_boundary_and_use_case`: what the product, project, product line, or capability is and how it fits the selected sector band
- `domestic_production_or_capacity`: Russia-scope production, development, facility, manufacturer status, production volume, capacity, localization, expansion, or modernization
- `support_import_substitution_or_market_signal`: case-specific public support, import-substitution or domestic-share signal, registry/status signal, named project financing, or independent market, trade, retail, or exhibition signal

Russian-language sources are welcome. Strong source surfaces include producer catalogs and production pages, technical sheets, official FRP/GISP/ministry/regional project pages, industry or trade-association pages, exhibition pages, registries used only as factual status evidence, credible manufacturing news, and case-specific retail or market pages when they identify the producer/product and the Russian market signal. Global market-report pages, generic light-industry policy pages, generic ecommerce listings, and broad program descriptions do not work unless the page names the submitted production case and carries the claimed facet-specific signal.

This is a factual public-evidence task. Do not give funding, sanctions, procurement, legal, accounting, eligibility, or investment advice; registry, public-support, and market pages should be treated only as source evidence for what the page says.

Requirements:
- The page must identify the submitted producer and the submitted product, project, product line, facility project, or material capability as a connected production case.
- The page must tie that case to the claimed sector band.
- The page must situate the case in a Russian production or Russian-scope market context.
- The page must make its facet-appropriate source role visible. For `product_boundary_and_use_case`, it should read as a product, catalog, technical, trade, exhibition, or descriptive source explaining what the case is used for. For `domestic_production_or_capacity`, it should read as a production, facility, manufacturer, capacity, volume, localization, expansion, or modernization source. For `support_import_substitution_or_market_signal`, it should read as a case-specific public-support, import-substitution, registry/status, financing, trade, exhibition, retail, or market-signal source.
- The page must expose concrete evidence for the claimed facet and case, not just generic light-industry, policy, retail, or market background.

Write one JSON object per line to `results_russia_production_case_evidence.jsonl`:
{"item": { "sector_band": "<sector_band>", "producer": "<producer>", "product_or_project": "<product_or_project>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `restaurant_ingredient_prices`

For each of the 2 market countries and each of the 3 source roles listed below, cover 18+ distinct public price-source contexts; within each country/source-role/source-context branch, supply public restaurant-ingredient price observations for 2+ restaurant-relevant ingredient components, with a source (i.e. 1+ URL) for each ingredient observation.

The goal is a public ingredient-cost provenance atlas: source-stated price observations, units, package or market basis, source organization, and stated market/date context where the source provides it. It is not a dish-margin model, menu-pricing exercise, supplier ranking, procurement recommendation, or contact/source-lead collection.

Market countries:
- **United States**: source-stated US, U.S. city/region, or US-facing public price evidence.
- **Canada**: source-stated Canadian, province/city/market, or Canada-facing public price evidence.

Source roles:
- `restaurant_supply_catalog`: a public restaurant-supply or foodservice catalog/product page.
- `wholesale_cash_carry_or_club`: a public cash-and-carry, wholesale club, distributor, or comparable wholesale-facing listing.
- `commodity_or_market_report`: an official, government, agricultural market-news, terminal-market, or comparable market-report source.

Each source context should name a distinct public price-source setting. For supplier and wholesale roles, this means a source organization plus a narrower catalog, store, product-line, market, or listing context; for market reports, this means a report setting such as source organization plus report title, terminal market, commodity table, issue date, or comparable report issue. A source context should be more specific than only a domain, country, source role, ingredient name, or source organization. Catalog and wholesale ingredient evidence should be product- or ingredient-dedicated rather than a broad search or category page carrying many unrelated products; report-table pages can count when the source context identifies the report setting and the ingredient-specific price line is localized.

The page evidence should stay within public ingredient-price provenance: ingredient price observations, source context, source role, market-country context, and stated unit/package/report basis. Contacts, account-only quote workflows, availability-only claims, private negotiated prices, supplier rankings, purchasing recommendations, recipe quantities, food-safety or nutrition advice, menu-price advice, profit/margin conclusions, negotiation guidance, outreach targets, lead scores, and business-strategy recommendations are outside the task scope.

Requirements:
- The page must clearly identify the named ingredient component as a food ingredient, commodity, product family, or restaurant-relevant ingredient product, not merely a dish, recipe, supplier, brand, SKU, package size, or price value.
- The page must support the submitted market country through source-stated country, city, region, market, report title, source organization, currency/market context, or other public page evidence.
- The page must tie the price observation to the submitted source context through visible source organization, catalog/store/product-line context, report title, terminal market, issue date, commodity table, URL path, page title, or comparable public page evidence.
- The page must make the declared source role visible through page content. Supplier and wholesale listings should expose catalog, distributor, club, foodservice, or public listing cues; market reports should expose report, market-news, commodity, terminal-market, or official price-report cues.
- The page must expose a source-stated ingredient price observation: a price, price range, market price, index, or comparable public price datum tied to the named ingredient component, together with the page's stated unit, package, pack/count/weight, or report basis. Dates or observed-date claims should be source-stated when reported.

Write one JSON object per line to `results_restaurant_ingredient_prices.jsonl`:
{"item": { "market_country": "<market_country>", "source_role": "<source_role>", "source_context": "<source_context>", "ingredient_component": "<ingredient_component>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

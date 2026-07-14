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

## `game_meat_exporter_provenance`

For 50+ named exporters, processors, distributors, establishments, plants, brand owners, or comparable public supply-chain actors tied to hare, rabbit, wild hare, wild land mammal, or adjacent game-meat products, supply public provenance sources for each of the 6 evidence facets below, with 1+ source for each actor-facet pair.

Keep the work to public-source provenance resolution. "Patagonia" is a source-stated claim to record when present, not a required geography. Confidence means confidence in the evidence on the cited page, not supplier quality, safety, compliance adequacy, or procurement suitability.

Evidence facets:
- `product_species`: source-stated hare, rabbit, wild hare, wild land mammal, game meat, or close product / commodity wording; generic livestock, beef, poultry, seafood, or unspecified meat wording is not enough.
- `origin_or_method`: source-stated country, region, sourcing area, wild / farmed / free-roaming / harvest-method wording, or a grounded no-public-origin state.
- `export_or_market`: public export, import, market, destination, eligibility, or shipment evidence, or a grounded no-export-evidence state.
- `establishment_or_approval`: named plant, establishment, registration number, competent authority approval, inspection listing, or a grounded no-public-establishment state.
- `certification_or_food_safety`: named certification standard, certifier, certificate, food-safety system, official food-safety claim, or a grounded no-certification-source state.
- `brand_or_customer_relationship`: publicly stated brand, customer, importer, retailer, private-label, or buyer relationship, or a grounded no-public-brand-relationship state.

The sources should be public pages such as actor-controlled product or supplier pages, official regulator/register pages or PDFs, establishment-specific pages, certification pages or directories, reputable government / industry / trade coverage, and public shipment rows when they state the relevant commodity or market fact for the submitted actor. Do not use generic livestock, beef, poultry, seafood, or unspecified meat pages as evidence unless the cited page also anchors the actor to hare, rabbit, wild hare, wild land mammal, or adjacent game-meat provenance. Do not use recipe pages, restaurants, hunting-tourism pages, pure shopping pages without provenance, contact-only listings, health/pathogen/veterinary/raw-feeding material, supplier rankings, lead-generation advice, outreach/contact details, prices, availability, or procurement guidance as answer evidence.

For each source, the answer ought to record the source class, checked date, source date when visible, source-stated product/species wording, origin/region/method wording, plant or establishment identity when visible, export or market fact when visible, inspection/approval or certification fact when visible, any public brand/customer relationship when visible, an explicit no-public-source / no-origin-source / no-export-evidence / no-certification-source / no-public-brand-relationship / conflict state where that is the honest resolution, and evidential confidence only.

Requirements:
- The page must clearly identify the named actor and place that actor in hare, rabbit, wild-hare, wild-land-mammal, or adjacent game-meat provenance. A generic meat, livestock, beef, poultry, seafood, food-processing, export/import, certification, or official-register context does not qualify by itself.
- The page should have a source role suited to `provenance_facet`: product and supplier pages for product/origin facts; supplier/exporter pages, government/trade coverage, official eligibility sources, or public shipment rows for market facts; regulator/register or establishment-specific pages for approval facts; certification directories, certificates, or supplier food-safety pages for certification facts; and brand/customer/source-checked pages for relationship or grounded-absence facts. For every facet, that source role must be actor-specific and within the hare/rabbit/wild-hare/adjacent-game-meat scope, not merely a generic meat-business source.
- The page must resolve the submitted facet through source-stated facts, a source-visible conflict, or a grounded missing-state check about the actor's hare, rabbit, wild-hare, wild-land-mammal, or adjacent game-meat provenance. A marketing word like "quality" is not a certification; a shipment row is not a brand relationship unless it publicly states that relationship; a contact block is not provenance evidence; and beef-only or generic livestock evidence does not resolve a non-product facet for this task.

Write one JSON object per line to `results_game_meat_exporter_provenance.jsonl`:
{"item": { "provenance_actor": "<provenance_actor>", "provenance_facet": "<provenance_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

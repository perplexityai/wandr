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

## `industrial_gas_consumption_plants`

For 60+ U.S. industrial manufacturing or processing facilities with material natural-gas load relevance, cover each of the 3 evidence axes below. For every (facility, evidence axis) cell, report 1+ concrete facility finding, supplying a source (1+ URL per (facility, evidence axis) cell).

Treat the current date for page-date and operating-status interpretation as May 12, 2026.

This is a practitioner roster for industrial-energy, gas-supply, procurement, and heavy-industry market mapping. The roster should favor named plant or complex pages and public records that let a reader identify the operator, physical facility, state, products/NAICS or supply-chain role, gas-load relevance, and permit/emissions/public-record footprint. The gas-load row needs a materiality proxy such as substantial production capacity, high reported emissions, major-source permitting, named gas-fired equipment, or reported source/process categories.

Use the operator or owner named by the qualifying source, preferring the operator shown as current as of May 12, 2026 when the page distinguishes ownership over time. Name the physical plant, complex, refinery, mill, or manufacturing site, the U.S. state, a compact industry category, and the concrete per-axis fact supported by the URL.

Industry-category examples:

- **ammonia_fertilizer** - ammonia, urea, UAN, nitric acid, DEF, or related nitrogen products
- **methanol_petrochemical** - methanol or petrochemical process units with natural-gas feedstock/fuel relevance
- **direct_reduced_iron_steel** - DRI/HBI or steel facilities using natural gas as reductant, fuel, or process energy
- **refining** - petroleum refineries and refinery-integrated chemical assets
- **petrochemical_chemical** - ethylene, olefins, polymers, industrial gases, chlor-alkali, or other chemical plants
- **minerals_materials** - cement, lime, glass, ceramics, gypsum, or other mineral/material manufacturing
- **pulp_paper_food_other** - large heat/process-load plants such as pulp/paper, food processing, and other industrial manufacturing

Evidence axes:

- **operator_product_profile** - facility identity plus product slate, manufacturing role, capacity, or supply-chain relevance
- **gas_load_signal** - facility-specific evidence that natural gas is a feedstock, fuel, reductant, stationary-combustion fuel, fired-equipment fuel, or process input, together with a materiality proxy such as plant capacity, major-source permitting, high emissions, named large process equipment, or reported source/process categories
- **permitting_emissions_record** - facility-specific public record: EPA/state/local permit, Title V/NSR notice, EPA GHGRP facility summary, EIA facility record, emissions inventory, SEC filing, or comparable official regulatory record

Use source pages whose standing fits the evidence axis:

- **operator_product_profile** - operator-controlled site pages, operator news releases, corporate annual reports/10-Ks, investor presentations, or official public authority pages that identify products, capacity, manufacturing role, or supply-chain relevance for the named facility
- **gas_load_signal** - operator-controlled material, EPA/state/local public records, permits, EPA GHGRP facility summaries, corporate filings, official public-authority economic development pages, or comparable primary/public records that directly describe natural gas at the facility and carry a materiality proxy
- **permitting_emissions_record** - EPA GHGRP facility summaries, EPA NSR, state/local air permits, Title V permits, emissions inventories, EIA facility records, SEC filings, or comparable official public records tied to the facility

The following are outside the facility universe:

- **standalone_power_generation** - electric-only power plants and merchant generators
- **lng_terminal** - LNG liquefaction/import/export terminals and regasification terminals
- **gas_transport** - interstate pipelines, compressor stations, storage fields, gathering systems, and meter stations
- **upstream_midstream_processing** - gas processing/fractionation plants whose main business is gas/oil production or processing
- **corporate_or_site_aggregate** - corporate headquarters, investor homepages, and broad multi-site company pages
- **non_us_or_future_only** - non-U.S. plants and cancelled/never-built facilities without operating, reporting, construction, or permit evidence dated within January 1, 2020 through May 12, 2026

Requirements:
- The page must tie the row operator, facility/site name, state, and industry category to the same physical U.S. industrial plant or complex.
- The page source class must fit the row evidence axis.
- The page must substantively support the row finding under the row evidence axis.
- The page must anchor the facility as operating, reporting, permitted, constructed for operation, or otherwise active within January 1, 2020 through May 12, 2026.

Write one JSON object per line to `results_industrial_gas_consumption_plants.jsonl`:
{"item": { "operator": "<operator>", "facility": "<facility>", "state": "<state>", "industry_category": "<industry_category>", "evidence_axis": "<evidence_axis>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

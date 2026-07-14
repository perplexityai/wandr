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

## `eu_ftl_trucking_carrier_landscape`

For each of the 15 countries listed below and each of the 3 haulage types, name at least 6+ road-freight carriers suitable for an FTL tender long-list. For each carrier, supply evidence for at least 2+ distinct market scopes, with at least 1 source URL per scope.

Treat the current date for page interpretation as May 12, 2026.

This is the kind of public market map a logistics procurement team would build before a multi-country road-freight tender. Public sources rarely expose private shipper accounts, so use public customer, sector, cargo, or specialist-service signals instead of guessing hidden relationships.

The countries in scope are:

- **Germany** (also written as: Deutschland, Federal Republic of Germany, DE)
- **France** (also written as: French Republic, FR)
- **United Kingdom** (also written as: UK, Great Britain, GB)
- **Italy** (also written as: Italia, Italian Republic, IT)
- **Spain** (also written as: España, Kingdom of Spain, ES)
- **Poland** (also written as: Polska, Republic of Poland, PL)
- **Netherlands** (also written as: Holland, The Netherlands, NL)
- **Belgium** (also written as: België, Belgique, Kingdom of Belgium, BE)
- **Austria** (also written as: Österreich, Republic of Austria, AT)
- **Czechia** (also written as: Czech Republic, Česko, CZ)
- **Romania** (also written as: România, RO)
- **Hungary** (also written as: Magyarország, HU)
- **Sweden** (also written as: Sverige, Kingdom of Sweden, SE)
- **Portugal** (also written as: Portuguese Republic, PT)
- **Ireland** (also written as: Republic of Ireland, IE)

The haulage types are:

- **domestic_regional_ftl** - same-country FTL service framed operationally as a scheduled shuttle, port-hinterland run, plant-to-DC lane, day-run, or other short-haul service inside the selected country; typically named for a region or short city pair rather than a national network
- **domestic_long_haul_ftl** - same-country FTL service framed operationally as a national or long-distance B2B haul, depot-to-depot trunk, or direct full-load transport across the selected country; typically irregular long-distance work rather than a fixed regional shuttle
- **international_ftl** - cross-border European FTL service with the selected country as origin, destination, base, subsidiary market, or named operating corridor

Evidence comes from commercially credible pages. Strong evidence includes carrier-controlled service / branch / country pages, annual or sustainability reports, official press releases, named customer case studies, tender or award announcements, Eurostat road-freight statistics, IRU member directories, national haulier-association rolls such as TLP, FNTR, BGL, Transport en Logistiek Nederland, etc., national operator licensing registers such as the German Bundesamt für Logistik und Mobilität, etc., or credible trade-publication profiles with quoted carrier or customer detail. Weak discovery pages such as freight-matching marketplaces and load boards such as TimoCom, Trans.eu, Teleroute, etc., broker-aggregator carrier-rating sites, generic directory listings, unattributed listicles, and pages covering only non-road modes without a carrier-FTL service signal do not count.

Useful customer-overlap proxies include named shipper or case-study customer; explicit vertical such as retail, FMCG, automotive, consumer goods, food and beverage, healthcare, chemicals, packaging, pallets, reusable containers, industrial parts, dangerous goods, high-value freight, or temperature-controlled cargo. Treat these as examples, not a closed list.

Requirements:
- The page must tie the carrier's FTL service to the selected country and submitted market scope — a regional operation, branch/base market, national service page, origin or destination, named corridor, or comparable concrete binding.
- The page must support the submitted haulage type per the definitions above, as full-truckload or direct-load road service rather than a generic "road freight" or non-road mode.
- The page must give a concrete fleet, network, capacity, route, terminal, branch, partner, daily-departure, control-tower, or similar operations signal for that carrier.
- The page must provide a public customer-overlap proxy — a named shipper, named case-study customer, relevant sector, or relevant cargo class fit for pallet/FMCG/retail/industrial/healthcare/chemicals/food/high-value/temperature-controlled tendering.
- The page must read as a commercially credible source class for carrier-market evidence.

Write one JSON object per line to `results_eu_ftl_trucking_carrier_landscape.jsonl`:
{"item": { "country": "<country>", "haulage_type": "<haulage_type>", "carrier": "<carrier>", "market_scope": "<market_scope>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

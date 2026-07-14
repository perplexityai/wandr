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

## `chile_industrial_decommissioning`

For 24+ Chilean industrial assets affecting 2025-2031, cover 3+ different opportunity aspects per asset, supplying a source (1+ URL under each asset-aspect leg) substantiating each opportunity. Each supplied asset is in scope as one of the three Chilean industrial asset classes below, with the supplied source also substantiating that the asset is a discrete physical site, unit, plant, mine, smelter, refinery, terminal, fuel facility, or comparable industrial installation. Each asset is consistently identified, using its Chilean region and name.

Think of this as a market-entry asset roster a specialist industrial-decommissioning firm would build before pursuing Chilean opportunities — discrete sites with their own closure, remediation, rehabilitation, or conversion lifecycle, not company-wide decarbonization narratives or generic national policy timelines.

Asset classes:
- `coal_thermal_power` (Coal / Thermal Power): thermal-power generation infrastructure in Chile — boilers, turbines, generation units, or whole power-station complexes fired by coal, gas, oil, diesel, or other thermal fuel.
- `mining_metallurgy` (Mining / Metallurgy): mining or metallurgical infrastructure in Chile — mines, smelters, refineries, tailings or slag facilities, processing plants, or mining-support industrial assets.
- `oil_gas_fuel` (Oil / Gas / Fuel): hydrocarbon fuel-handling infrastructure in Chile — onshore oil or gas production wells, fuel-storage tanks, fuel-distribution pipelines, refineries, LNG terminals, or other dedicated fuel-handling facilities.

Opportunity aspects:
- `closure_stage_timing`: retirement, closure, disconnection, temporary/definitive closure, decommissioning stage, planned start, completion, or target-window timing.
- `permit_environment`: environmental assessment, DIA/EIA/RCA, SMA/SERNAGEOMIN/CNE authorization, inspection, compliance, enforcement, or remediation-order evidence.
- `cost_workforce`: investment, cost, budget, liability, compensation, labor-transition, workforce, employment, contractor-headcount, or community-impact evidence.
- `rehabilitation_reuse`: land rehabilitation, ash/tailings/fuel-site remediation, biodiversity restoration, battery/storage project, gas conversion, industrial reuse, or circular-economy reuse.
- `contractor_procurement`: named contractor, consultant, bidder/tender, inspection provider, engineering or security service, procurement route, or competitive-context signal.
- `technical_scope`: physical dismantling, demolition, removal, isolation, cota-cero work, marine works, tanks, turbines, boilers, stacks, conveyors, fuel systems, hazardous materials, or other asset-specific technical scope.

Requirements:

- The page must communicate its own public relationship to the asset strongly enough to stand as independent evidence, not merely list, summarize, or market around the fact from afar.
- The page must name the Chilean asset, or an asset-specific unit/site within it, and tie it to the claimed Chilean region.
- The page must substantiate the asset's industrial character and its membership in the claimed asset class.
- The page must support closure, decommissioning, remediation, rehabilitation, dismantling, or conversion activity affecting 2025-2031.
- The page must support the chosen opportunity aspect for the asset.

Write one JSON object per line to `results_chile_industrial_decommissioning.jsonl`:
{"item": { "region": "<region>", "asset": "<asset>", "asset_class": "<asset_class>", "opportunity_aspect": "<opportunity_aspect>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

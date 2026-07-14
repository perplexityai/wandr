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

## `thermal_area_suppliers`

For each of the 7 automotive thermal-management areas listed below, name 12+ suppliers per area; for every supplier-area pair, supply a source (i.e. 1+ URL) for each of the 2 evidence roles.

The aim is a public provenance panel for vehicle thermal-management supplier capability, not a supplier ranking, outreach list, sales deck, procurement recommendation, or technical design guide. The same supplier may appear in multiple thermal areas only when each area has its own source-backed evidence.

Thermal areas:
- `battery_thermal_interfaces`: battery thermal interface materials such as gap fillers, gap pads, potting, thermally conductive adhesives, or pack/module TIMs
- `battery_cooling_plates`: liquid cold plates, cooling plates, roll-bond plates, or direct-contact plate components for EV or hybrid battery packs/modules
- `battery_chillers_heat_exchangers`: battery chillers, refrigerant-to-coolant heat exchangers, contact heat exchangers, or battery-loop heat-exchange modules
- `cabin_hvac_heat_pumps`: automotive HVAC, heat-pump systems, e-compressors, refrigerant modules, or cabin thermal systems for electric, hybrid, or ICE vehicles
- `coolant_modules_pumps_valves`: coolant modules, electric coolant pumps, thermal valves, manifolds, high-voltage coolant heaters, or coolant-control assemblies
- `powertrain_power_electronics_cooling`: cooling for inverters, onboard chargers, DC-DC converters, e-motors, e-axles, power electronics, or electric drivetrain thermal loads
- `thermal_fire_barriers`: thermal runaway barriers, flame barriers, aerogel insulation, mica or fire-protection layers, battery-pack thermal propagation materials

Evidence roles:
- `official_technical`: supplier-owned product, application, datasheet, technical, or similarly specific page proving a concrete automotive thermal-management product or technology in the claimed area
- `external_presence`: non-own-domain or public counterpart/institutional source tying the same supplier to the same automotive thermal area

Sources should be public, source-backed, and specific to the supplier and thermal area. Do not use contact-enrichment pages, lead lists, generic market reports, SEO supplier rankings, broad procurement databases, or sources that merely imply a named OEM/platform/customer relationship.

Requirements:
- The page must clearly tie the named supplier to the claimed thermal area and to an automotive, vehicle, EV, hybrid, ICE, battery-pack, powertrain, cabin-climate, or comparable vehicle-system context.
- The page must make the claimed evidence role visible: supplier-owned technical/product/application evidence for `official_technical`, or non-own-domain/public footprint evidence for `external_presence`.
- The page must expose concrete product, technology, application, program, patent/R&D, event, facility, filing, or comparable footprint detail for the supplier in the claimed thermal area. Named OEM, platform, customer, certification, standard, facility, or relationship details count only when source-stated.

Write one JSON object per line to `results_thermal_area_suppliers.jsonl`:
{"item": { "thermal_area": "<thermal_area>", "supplier": "<supplier>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

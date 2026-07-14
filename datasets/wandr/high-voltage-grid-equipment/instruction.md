You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `high_voltage_grid_equipment`
  - `high_voltage_grid_equipment.public_references`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `high_voltage_grid_equipment`

For each of the 4 high-voltage equipment classes listed below, supply official product-family evidence for 25+ OEM manufacturers. For each manufacturer, name 1+ product family, series, platform, or source-framed product category in that equipment class and provide 1+ manufacturer-controlled official source for it.

Equipment classes:
- `gas_insulated_switchgear_or_high_voltage_breakers`
- `large_power_transformers_or_reactors`
- `instrument_transformers_or_bushings`
- `disconnectors_surge_arresters_or_switchyard_components`

A valid manufacturer is an OEM or manufacturer-controlled business unit for high-voltage grid or substation equipment. A valid equipment family can be a named family, series, platform, or source-framed product category; a voltage level, MVA value, customer name, geography, or single SKU by itself does not count.

The source should be a manufacturer-controlled official surface or official technical literature, preferably a fetchable HTML product page. Broad corporate pages, reseller marketplaces, distributor catalogs, EPC/service pages, market reports, listicles, supplier rankings, lead directories, or RFQ/contact surfaces do not count.

Keep the evidence neutral and public. Supplier recommendations, rankings, "best supplier" conclusions, market-share rankings, engineering design advice, installation guidance, compatibility guarantees, compliance/safety advice, pricing/RFQ collection, lead scoring, outreach targeting, and contact enrichment are out of scope.

Requirements:
- The page must identify the submitted manufacturer or manufacturer-controlled business unit.
- The page must identify the submitted product family, series, platform, or source-framed product category.
- The page must tie that family or category to the selected equipment class.
- The page must state a qualifying high-voltage rating tied to that family or category. For AC equipment, the rated or highest voltage for equipment must be at least 72.5 kV; pages whose only stated voltage is 52 kV or below do not count. The voltage must be a voltage rating, not an MVA rating, current rating, breaking-current value, project capacity, or a generic "high voltage" phrase.

Write one JSON object per line to `results_high_voltage_grid_equipment.jsonl`:
{"item": { "equipment_class": "<equipment_class>", "manufacturer": "<manufacturer>", "product_family": "<product_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `high_voltage_grid_equipment.public_references`

Cross-tasknode identifier discipline: this task is for the same {= equipment_family =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= equipment_family =}+ high-voltage equipment families, supply 2+ concrete public-reference or scale facts per family, each backed by 1+ URL.

The reference may be a named project, order, customer/operator, installed-base metric, procurement or approval listing, dated deployment, or dated source-stated scale fact. It should be tied to the same family, a named family variant, or a tightly scoped same manufacturer/equipment-class category. Company-level "leading supplier", market-share, ranking, broad reputation, or supplier-selection claims do not count.

Valid sources include official project or press pages, grid operator/customer/procurement/approval bodies, annual reports, and credible transmission-and-distribution trade or project coverage. The URL does not need to be on the OEM domain. Market reports, generic listicles, marketplaces, distributor catalogs, lead directories, RFQ/contact pages, and pages that turn the fact into procurement advice or supplier ranking do not count.

Keep the evidence neutral and public. Source-stated "approved vendor" or "preferred supplier" phrases can be recorded only as public-reference facts, not as advice or comparative evaluation.

Requirements:
- The page must identify the submitted manufacturer as the supplier, manufacturer, vendor, awardee, technology provider, or equipment provider in the reference.
- The page must tie the reference to the same product family, a named family variant, or a tightly scoped same manufacturer/equipment-class category.
- The page must support the concrete public-reference or scale fact named in the submitted reference.

Write one JSON object per line to `results_high_voltage_grid_equipment.public_references.jsonl`:
{"item": { "equipment_class": "<equipment_class>", "manufacturer": "<manufacturer>", "product_family": "<product_family>", "reference": "<reference>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

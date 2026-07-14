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

## `australia_food_equipment`

For 400+ well-identified Australian food or beverage manufacturing or processing facility cases, name concrete equipment applications (1+ per case) and supply public URLs (1+ per application). Facility cases may be named operators/facilities or anonymous descriptors when the source gives enough concrete Australia, segment, and process context to distinguish the case. The equipment application should involve pumps, hoses, fluid transfer, hygienic bearings, conveying, washdown, pneumatic, actuator, hydraulic, or related motion-control equipment used in a food or beverage production process.

Public application stories, supplier case studies, trade articles, official operator pages, distributor application pages, technical datasheets, and public project records can work when the page itself ties the equipment to the manufacturing or process application. Generic supplier catalogs, product pages, category pages, "trusted by" logos, investment stories without relevant equipment, retail/restaurant uses, logistics-only or IT-only automation, and non-Australian pages without an Australian process application do not count.

For downstream comparison, source-stated supplier/model/product family, geography, segment, hygiene/food-grade/standards language, and problem/outcome details can be included when present. This is public provenance work only; equipment ratings, supplier rankings, procurement/cost/RFQ/contact/outreach work, food-safety assurance, compliance verdicts, and maintenance or engineering advice are out of scope.

Requirements:
- The page must tie the submitted facility case to an Australian food, beverage, brewing, wine, dairy, bakery, packaged-food, ingredient, meat, or similar manufacturing or processing context.
- The page must state the submitted equipment application as a concrete use of pumps, hoses, fluid-transfer, hygienic bearing, conveying, washdown, pneumatic, actuator, hydraulic, or related motion-control equipment.
- The page must connect that equipment to a specific manufacturing or process application, problem, installation, site audit, project, production line, or source-stated outcome for the submitted facility case.

Write one JSON object per line to `results_australia_food_equipment.jsonl`:
{"item": { "facility_case": "<facility_case>", "equipment_application": "<equipment_application>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

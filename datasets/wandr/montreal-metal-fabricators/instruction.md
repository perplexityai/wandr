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

## `montreal_metal_fabricators`

For metal-fabrication operator-sites in Greater Montreal, Laval, Longueuil, the South Shore, the North Shore, and adjacent CMM-linked Quebec industrial communities, cover 24+ operator-sites for each of the 4 capability families listed below; for each operator-site and each of the 2 source roles, supply 1+ public URLs that show the local operating presence and the capability-family evidence.

Capability families:
- `structural_steel_and_installation`: structural steel, miscellaneous metals, stairs, platforms, building steel, erection, installation, or comparable fabricated structural/architectural steel work
- `welding_and_custom_fabrication`: custom metal fabrication, welding, repairs, assemblies, prototypes, industrial fabrications, or comparable made-to-order fabrication work
- `laser_sheet_cutting_and_forming`: laser cutting, sheet-metal cutting, bending, forming, press-brake work, punching, or comparable sheet-processing services
- `cnc_machining_and_machine_shop`: CNC machining, milling, turning, precision machining, machine-shop work, or comparable subtractive manufacturing

Source roles:
- `owned_or_controlled`: an official company website, service page, project page, branch page, company-controlled profile, or other public surface controlled by the operator
- `independent_public_profile`: an entity-scoped public profile, trade or association profile, chamber/economic-development profile, trade article, case study, project article, certification/license/public record, or similar public source that independently names the operator-site and carries locality plus capability evidence

The goal is public capability provenance, not contact collection, procurement advice, vendor ranking, quote solicitation, employee or revenue estimates, lead scoring, or outreach enrichment. The operator-site ought to be a real local facility, branch, shop, plant, or comparable local operating presence in the target region. An out-of-region company page that merely targets Montreal as an SEO service area is not enough.

Requirements:
- The page must clearly identify the submitted operator-site, using the operator name or a clear alias.
- The page must tie the operator-site to the submitted locality or another genuine local operating basis in the target region.
- The page must state capability evidence matching the submitted `capability_family` in its body text or entity-specific content.
- The page must earn the submitted `source_role`; broad search/list/category pages, repeated generic directory-result pages, contact modules, RFQ forms, rankings, and private estimate widgets do not prove the role by themselves.

Write one JSON object per line to `results_montreal_metal_fabricators.jsonl`:
{"item": { "capability_family": "<capability_family>", "operator": "<operator>", "locality": "<locality>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

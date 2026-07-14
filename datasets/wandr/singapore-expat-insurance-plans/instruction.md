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

## `singapore_expat_insurance_plans`

For at least 45+ private medical insurance provider-plan tiers relevant to Singapore expat or PR families, and for each of the 9 comparison facets, supply a corroborating source (i.e. 1+ URL) substantively evidencing the claimed facet for the named plan.

This mirrors the work of replacing employer group medical cover with individually purchased cover: plan names are not enough, and neither are generic brand pages. Each cell should point to an insurer-controlled plan-specific page, benefit schedule, policy document, brochure, or customer guide carrying the plan fact.

The facets are:
- `inpatient_annual_limit`: the plan's maximum annual inpatient / overall medical benefit limit, or the hospital ward entitlement when the plan is an Integrated Shield-style plan
- `outpatient_cover`: whether ordinary outpatient / day-to-day treatment is included, optional, limited, or excluded for the plan
- `maternity_or_pregnancy`: the maternity, pregnancy-complication, childbirth, or newborn-care treatment position, including any waiting period when stated
- `pre_existing_handling`: how the plan handles pre-existing medical conditions: exclusion, underwriting, moratorium, selected-condition coverage, or stated non-coverage
- `singapore_network_or_direct_billing`: the Singapore hospital, specialist-panel, direct-billing, guarantee-of-payment, or free-choice-provider position
- `area_of_cover`: the geographic area of cover: Singapore-only, regional Asia, worldwide, worldwide excluding USA, USA elective option, or similar
- `evacuation_repatriation`: whether medical evacuation, emergency assistance, or repatriation is included, optional, limited, or absent
- `pricing_basis`: a static pricing signal: published age-band premium, starting price, discount, premium table, or plan-specific quote basis tied to benefit choices
- `family_or_dependant_terms`: family, dependant, newborn, immediate-family, or household-member terms relevant to a family replacing employer group cover

Each claimed provider-plan ought to be a real named medical insurance plan tier or rider bundle marketed to Singapore residents, PRs, foreigners, or expats for individual/family purchase.

Requirements:
- The page must substantively evidence the claimed facet for the claimed provider-plan, per the per-facet bar.
- The page's facet content must be attributed to the claimed provider-plan rather than only to a provider brand, a multi-plan roundup, an unrelated rider, or a different plan tier.
- The page must communicate, possibly via URL among other things, that it is on an admissible insurer-controlled plan-specific source class: insurer-controlled plan page or insurer PDF such as a brochure, benefit schedule, customer guide, or policy wording quoting plan-specific benefit or premium facts.

Write one JSON object per line to `results_singapore_expat_insurance_plans.jsonl`:
{"item": { "provider": "<provider>", "plan": "<plan>", "facet": "<facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `ambient_food_3pl`

For 350+ US third-party logistics providers that publicly support ambient, dry, shelf-stable, non-perishable, packaged, or room-temperature human food / beverage fulfillment, supply provider-specific evidence (i.e. 1+ URL) for each of the 3 capability axes.

The capability axes are:
- `ambient_food_scope`: direct evidence that the provider handles ambient, dry, shelf-stable, non-perishable, packaged, pantry, coffee / tea, beverage, snack, or comparable room-temperature human food or beverage products.
- `compliance_or_traceability`: provider-specific food-grade, FDA / FSMA / GMP / cGMP, SQF, BRCGS, AIB, GFSI, USDA Organic, kosher, allergen-control, audit, lot / batch, date-code, expiration, FIFO / FEFO, recall, quarantine, or comparable food-safety / shelf-life evidence.
- `fulfillment_operations`: provider-specific service evidence for DTC or ecommerce pick-pack-ship, B2B / retail distribution, wholesale / EDI, marketplace or FBA prep, kitting or subscriptions, cross-docking, value-added services, returns / disposition, or comparable fulfillment operations tied to the ambient food scope.

For each source, report the source language as a public claim, the capability evidence it supports, and whether the evidence is facility-specific, network / provider-level, case-backed, certification / registry-backed, or another provider-specific source shape. Capture marketing wording as wording from the source; do not convert claims such as FDA-registered, FDA-approved, SQF-certified, AIB-audited, or food-grade into stronger legal conclusions.

Provider-owned service, compliance, facility, industry, and case-study pages are the expected core evidence. Official certification or registry records and credible provider-specific public sources can also support the right row. Broad 3PL directories, lead-generation marketplaces, ranked lists, search/category pages, generic standards or regulatory explainers, and shallow third-party profiles can be useful discovery surfaces, but they should not be the sole proof for a core capability row.

Requirements:
- The page must identify the claimed provider as a 3PL, fulfillment, warehousing, distribution, public warehouse, or comparable logistics operator and tie it to a US footprint, US facility, US market, or US service context.
- The page must support human ambient food or beverage scope: ambient, dry, shelf-stable, non-perishable, packaged, pantry, coffee / tea, beverage, snack, or comparable room-temperature food / beverage products. Mixed-temperature providers qualify only when the ambient / dry / shelf-stable or room-temperature food capability is explicit; supplements, pet food, cosmetics, pharma, generic CPG, or cold-chain food alone do not replace the human ambient food / beverage signal.
- The page must support the submitted `capability_axis` with provider-specific evidence: direct ambient food scope for `ambient_food_scope`; food-grade, compliance, audit, certification, lot, batch, expiration, FIFO / FEFO, recall, quarantine, or comparable food-safety / shelf-life evidence for `compliance_or_traceability`; or DTC, ecommerce, B2B, retail, wholesale, EDI, marketplace prep, kitting, cross-dock, value-added, returns, or comparable fulfillment operations tied to ambient food for `fulfillment_operations`.
- The page must give enough specificity to distinguish provider-level, network-level, facility / site-specific, case-backed, certification / registry-backed, or other provider-specific public claims, without recasting the source's wording more strongly than the page states.

Write one JSON object per line to `results_ambient_food_3pl.jsonl`:
{"item": { "provider": "<provider>", "capability_axis": "<capability_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

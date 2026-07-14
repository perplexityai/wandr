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

## `pulsed_capacitor_claims`

For 35+ vendors or vendor-owned capacitor brands that publicly state pulsed-power, high-energy-discharge, pulse-discharge, high-voltage-pulse, or adjacent rapid-discharge capacitor capability, supply evidence for 3+ bounded capability claims per vendor. For each claim and each of the 2 provenance roles below, provide 1+ source URL.

This is a provenance and disclosure task, not a vendor ranking or buying guide. Do not submit evidence for product recommendations, procurement advice, pricing estimates, contact details, outreach, or engineering design guidance.

A bounded `capability_claim` should be specific enough that two pages can be checked against the same proposition: numeric voltage, capacitance, current, energy, shot-life, or temperature envelopes; named construction or form factor; named product family; stated qualification or compliance; or an explicit custom-build capability. Generic statements that a company "makes capacitors" or "serves pulsed power" without a concrete bound do not count.

The 3+ claims for a vendor must be genuinely distinct bounded propositions. Do not split one generic product-line statement, one part-number table, or near-restatements of the same voltage/current/energy envelope into multiple claims. Claims from the same family can count separately only when each claim names a different source-stated bound, construction feature, qualification, or custom capability that each page can verify on its own.

The provenance roles of interest are:
- `vendor_stated`: an official vendor-controlled product page, datasheet, catalog, application note, product guide, or comparable official surface.
- `secondary_public_visibility`: a public source not controlled by the claimed vendor that visibly repeats or contextualizes the same vendor/product/capability claim, such as a distributor or representative page, technical article, trade page, report, public procurement or award page, or catalog mirror with clear non-vendor publication or catalog context. A bare copied vendor datasheet or isolated file without visible non-vendor hosting context does not count for this role.

Requirements:
- The page must fit the declared provenance role.
- The page must identify the claimed vendor, a vendor-owned brand line, or a vendor-attributed product family in the relevant capacitor context.
- The page must tie the vendor/product capability to pulsed power, high-energy discharge, pulse discharge, high-voltage pulse, pulsed plasma/fusion, or analogous rapid-discharge capacitor use.
- The page must substantiate the submitted bounded capability claim on that page; numeric claims need source-stated values and units, and nonnumeric claims need concrete product-family, construction, qualification, or custom-capability support. Do not stitch a vendor identity from one source together with a capability value from another source to make a record pass.

Write one JSON object per line to `results_pulsed_capacitor_claims.jsonl`:
{"item": { "vendor": "<vendor>", "capability_claim": "<capability_claim>", "provenance_role": "<provenance_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

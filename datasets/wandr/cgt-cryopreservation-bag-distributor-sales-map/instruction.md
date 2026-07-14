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

## `cgt_cryopreservation_bag_distributor_sales_map`

For 80+ potential distributors of cell- and gene-therapy-relevant cryopreservation bag products, name the distributor, market, and region label, supplying a source (1+ URL per candidate). Each candidate is a named distributor, reseller, importer, catalog supplier, or local sales channel in a concrete market, not just a manufacturer's own product page.

Use exactly one of these five canonical region labels for each candidate. The countries and markets listed under each label are concrete market examples that belong in that label, not alternate region names, subregions, or aliases:

- **North America** (example markets: United States, Canada)
- **Europe** (example markets: United Kingdom, Germany, France, Italy, Spain, Netherlands, Norway, Switzerland)
- **East Asia** (example markets: Japan, China, South Korea, Taiwan, Hong Kong)
- **South and Southeast Asia / Oceania** (example markets: India, Singapore, Malaysia, Vietnam, Thailand, Indonesia, Philippines, Australia, New Zealand)
- **Latin America / Middle East / Africa** (example markets: Brazil, Mexico, Argentina, Chile, Israel, Turkey, United Arab Emirates, Saudi Arabia, South Africa, Egypt)

For each candidate, also name the represented manufacturer or product line, the product family, the channel role, and a concise rationale for prioritizing this distributor.

The cited page must place the distributor's commercial channel in the submitted market and describe a cryopreservation/freezing bag product suitable for cells, HPCs, stem cells, blood components, or other CGT-adjacent material. A distributor's own product page on its own domain (`<distributor>.com`, `<distributor>.<cc-tld>`, country-specific storefront) or a directory-marketplace product page whose seller block names the distributor is the canonical evidence shape.

Requirements:

- The page communicates (possibly via URL among other things) that it is the named distributor's local commercial channel serving the submitted market. Market evidence on the page can take the form of a country TLD in the hostname, an explicit country/state/city/address mention in the title or body, a native-language body that matches the submitted market, or a market-specific business identifier or regulatory clearance. A distributor's generic `.com` storefront with no country, language, address, or regulatory signal anywhere on the page does not by itself evidence which market that distributor serves.
- The page must show that the submitted product family is a cryopreservation, freezing, cryogenic storage, or closed single-use bag suitable for cell, blood-component, stem-cell, HPC, tissue, biologic, or similar CGT-adjacent material.

Write one JSON object per line to `results_cgt_cryopreservation_bag_distributor_sales_map.jsonl`:
{"item": { "region": "<region>", "distributor_name": "<distributor_name>", "market": "<market>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `global_solar_pv_component_manufacturers`

For each of the 10 PV stack tiers listed below, identify 12+ companies as manufacturers in that tier; for each stack-tier/company pair, cover each of the 2 evidence roles with a source (i.e. 1+ URL) showing the company actually manufactures products or materials in that part of the solar PV stack.

The point is a global component-manufacturer map that reaches past finished-module brands into upstream materials and balance-of-module components.

Stack tiers:
- **polysilicon**: solar-grade polysilicon feedstock for crystalline-silicon PV
- **ingot_wafer**: silicon ingots, mono/multi crystalline wafers, wafer slicing, or comparable wafer-stage production
- **solar_cell**: photovoltaic cell manufacturing before module assembly
- **module**: finished PV module / panel manufacturing, including thin-film modules
- **solar_glass**: PV cover glass, solar glass, or photovoltaic glass for modules
- **encapsulant**: EVA, POE, EPE, or comparable encapsulant films for PV modules
- **backsheet**: polymer backsheets or comparable rear-side module films
- **junction_box_connector**: PV junction boxes, module connectors, cable assemblies, or connector systems used at module/string level
- **ribbon_interconnect**: PV ribbon, tabbing wire, bus wire, interconnect wire, or comparable cell/module interconnect materials
- **metallization_paste**: silver/aluminum/copper metallization paste or conductive paste for solar-cell contacts

The evidence roles of interest, which we refer to as `evidence_role`, are:
- `self_presented_manufacturing`: manufacturer-side self-presentation by the claimed company for the selected stack tier.
- `independent_manufacturer_placement`: outside placement of the claimed company as a manufacturer in the selected stack tier.

`company` ought to be a real named business or manufacturing organization for the selected stack tier. Product families, component categories, marketplaces, pure distributors/resellers, certification bodies, article publishers, research institutes with no manufacturing offering, and placeholder names are not manufacturers. Vertically integrated companies can count in multiple stack tiers only when the page evidence supports each tier separately. Pages should be fully public and usable; paywalled previews, login shells, search result pages, empty catalog cards, machine-generated directory stubs, and market-report teasers are not enough by themselves.

Requirements:
- The page must clearly identify the named company.
- The page must tie the company to the selected stack tier as a manufacturer of the tier's products or materials, not merely as a solar developer, installer, buyer, distributor, research subject, or generic "solar company."
- The page should make its `evidence_role` fit visible: for `self_presented_manufacturing`, manufacturer-controlled or formal company-surface anchors such as official product pages, annual reports, investor materials, datasheets, filings, official announcements, facility pages, or controlled brand/channel pages; for `independent_manufacturer_placement`, independent PV/trade/association/news/research treatment that gives company-specific manufacturer placement rather than a bare directory entry, scraped profile, market-report teaser, or generic "key players include" list.
- The page should expose a focused tier-specific manufacturing, product, facility, capacity, production-line, commissioning/expansion, datasheet/specification, or comparable detail for the company. A bare statement that the company makes solar products is not enough.

Write one JSON object per line to `results_global_solar_pv_component_manufacturers.jsonl`:
{"item": { "stack_tier": "<stack_tier>", "company": "<company>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

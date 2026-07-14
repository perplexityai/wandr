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

## `australian_vrfb_atlas`

For 31+ Australian vanadium redox/flow battery assets, supply at least 2+ public evidence URLs per asset. A qualifying asset can be a deployment, planned deployment, electrolyte facility, manufacturing or supply-chain asset, or upstream asset only when the public source ties it directly to VRFB electrolyte or a named VRFB battery deliverable. Small pilots count when a public-sector or industrial host and source-backed status are visible. Generic BESS records, pure mining projects with no electrolyte/VRFB deliverable, market forecasts, investment theses, procurement advice, technology recommendations, and unsupported national-pipeline totals do not count.

Each evidence URL should let a reader normalize the asset as a dated public record: project or facility name, record type, Australian location and state/territory, proponent/developer/host and public partners, explicit vanadium-flow chemistry evidence, public status label and milestone dates, capacity fields with units and basis when public, public-money or procurement evidence when public, public supply-chain relationships when public, source type/date, checked date, confidence, and missing/conflict/stale flags. For downstream use, include those normalized labels in the answer. Mark a field as not public or not present on the cited page rather than inferring it.

Use public source labels instead of forcing one source family. Official funding or procurement pages, utility or host reports, project fact sheets, company or ASX announcements, supplier case studies, dated trade reporting, and similar public pages can all be eligible when the asset-specific evidence is present and the source type is labeled.

Requirements:
- The page must explicitly tie `vrfb_asset` to vanadium redox/flow battery chemistry and an Australian project, site, facility, host, region, or deliverable.
- The page must communicate a public status or milestone for that asset, such as proposed, procurement, EOI, approval, construction, installation, commissioning, launch, operating, completed, funding awarded, target operation, or comparable dated status evidence.
- The page must support the material details submitted from that source: location/state, proponent/developer/host or public partners, capacity units and basis if reported, public-money or procurement evidence if reported, and supply-chain/OEM/electrolyte/installer/host relationships if reported.
- The normalized record must keep caveats visible: planned versus awarded versus operating, source date versus checked date, capacity basis, funding form, relationship status, and missing/conflict/stale states. It must not infer selected developers, paid amounts, commercial viability, technology recommendations, or national pipeline totals from partial evidence.

Write one JSON object per line to `results_australian_vrfb_atlas.jsonl`:
{"item": { "vrfb_asset": "<vrfb_asset>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

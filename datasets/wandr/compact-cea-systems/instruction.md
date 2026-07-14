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

## `compact_cea_systems`

For at least 85+ companies offering compact controlled-environment agriculture farm systems as of May 22, 2026, name at least 1+ compact farm-system offering per company and supply at least 1+ URLs on public pages substantiating that company-system pair.

The target systems include shipping-container farms, modular farm units, pods, cabinets, greenhouse modules, or comparable small-footprint indoor or vertical farm systems. This is public capability provenance: keep rankings, buying advice, ROI or price advice, project-suitability guidance, outreach, contacts, lead scoring, and recommendations out of scope.

Public source roles that fit the task include official product pages, specification pages, brochures, product-family pages, official case studies or press releases, customer or project deployment pages, reputable CEA or agriculture trade coverage, and reputable vendor directories when they provide specific dated product/system evidence. Generic "top vertical farming companies" pages, ROI or cost guides, investment pages, contact/lead pages, and pages about produce growers or farm operators do not count by themselves.

Where the page states it, preserve form factor, crop or use-case capability, footprint or dimensions, lighting, HVAC or climate, water or irrigation, automation, software or remote-monitoring claims, deployment/customer/project evidence, geography served, source date, product status, acquisition, pivot, discontinuation, and explicit missing or conflict states. Leave a detail unstated when the source does not say it.

Requirements:
- The page should have a public evidence role suited to the claim: official product/specification/brochure/product-family/case-study/press-release source, customer or project deployment source, reputable CEA or agriculture trade/status source, or reputable vendor directory with specific dated system evidence.
- The page must identify the submitted company and the submitted compact farm system or clearly bounded system offering.
- The page must support that the company offers or offered the system to customers as a product, productized service, deployable farm system, lease, franchise, or comparable commercial/public offering.
- The page must source-state the compact controlled-environment farm form factor or system type, not merely generic vertical-farming interest.
- The page must contribute at least one concrete source-stated system detail, such as crop/use-case capability, dimensions or footprint, environmental-control or automation claims, deployment/project evidence, geography, status, source-stated missing state, or conflict state.

Write one JSON object per line to `results_compact_cea_systems.jsonl`:
{"item": { "company": "<company>", "system": "<system>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

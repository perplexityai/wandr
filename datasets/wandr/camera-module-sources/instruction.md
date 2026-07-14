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

## `camera_module_sources`

For 50+ suppliers or brands, name 2+ public miniature or embedded camera modules per supplier or brand; for each module, supply 1+ public URL for each of the 5 source-evidence areas below.

A module in scope is a source-presented finished camera module, board camera, cabled camera module, or sensor assembly with supplier and part/product identity. Bare image sensors, host boards without a named camera module, phone repair assemblies, consumer webcams, IP cameras, marketplace lead lists, supplier rankings, and compatibility/substitution advice are outside scope.

The source-evidence areas are:
- `catalog_identity`: the supplier or brand publicly presents the named item as a camera module, board camera, cabled module, or sensor assembly.
- `imaging_sensor`: source-stated imaging or sensor facts, such as camera type, resolution, sensor model, sensor size or optical format, shutter type, color/mono/NIR variant, or related sensor characteristics.
- `interface_electrical`: source-stated interface or electrical facts, such as MIPI CSI-2, USB, parallel, LVDS, connector, voltage, power, or current.
- `mechanical_optical`: source-stated mechanical or optical facts, such as module dimensions, lens mount, field of view, focal length, focus type, cable/form factor, or related optics.
- `commercial_public_state`: source-stated current public commercial facts, such as price, stock, lead time, orderability, MOQ, sample availability, request-sample, request-quote, or quote-required. This is page-scoped: quote-required or request-sample counts when the page says it, but a page's silence does not prove global absence.

Valid sources include official manufacturer or supplier product pages, catalog pages, datasheets/PDFs, developer documentation, official distributor catalog pages, and reputable component directories when they bind the named module and fact. The same URL may be used for more than one source-evidence area only when the cited page carries a distinct fact for each selected area.

Requirements:
- The page must clearly bind the named supplier or brand to the named module or part.
- The page must communicate an eligible module-bound source role, not just a generic marketplace, contact, lead-list, ranking, repair-part, or compatibility page.
- The page must state a concrete fact appropriate to the selected `spec_facet`; do not infer suitability, private availability, supplier quality, or global commercial absence from context.

Write one JSON object per line to `results_camera_module_sources.jsonl`:
{"item": { "supplier_or_brand": "<supplier_or_brand>", "module_or_part": "<module_or_part>", "spec_facet": "<spec_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `specialty_hardwood_offering_provenance`

For 90+ specialty hardwood suppliers, sawmills, lumber dealers, slab or live-edge sellers, or similar public commercial hardwood sources, name 3+ distinct hardwood species or marketed hardwood types per supplier and supply evidence for each of the 2 provenance roles (i.e. 1+ URL per role).

The aim is a public provenance map for supplier wood offerings, not a vendor comparison. Do not rank suppliers, recommend vendors, solicit quotes, collect contact details, score leads, or turn volatile price / shipping notes into purchase advice.

Wood types should be hardwood species or recognized marketed hardwood types. Figured categories such as curly maple or birdseye maple count when the source treats them as a distinct marketed wood type; thicknesses, board dimensions, grades, surfacing, slab/lumber forms, and house collection names do not count by themselves.

The provenance roles, called `source_role`, are:
- `primary_offer`: a supplier-owned official offer surface, such as the supplier's exact product page, inventory page, catalog or price-list PDF, sawmill product page, or official shop page. It must show the exact wood type in concrete sellable-offering context. Generic home pages, about pages, species galleries, broad species menus, and "we carry many hardwoods" pages do not work unless the exact wood type appears in itemized product, inventory, price-list, or catalog detail on that page.
- `outside_surface`: a distinct public surface outside the supplier's main owned website that is both supplier-specific and exact-wood-type-specific. Platform shops, marketplace listings, third-party product listings, supplier-specific articles, and detailed directory profiles can work only when the page identifies the supplier/storefront and shows the exact wood type in concrete product, listing, inventory, price, profile, or itemized catalog detail. Generic species articles, shallow name / location / contact directory entries, broad multi-species directory profiles or storefronts without row-specific offering detail, social chatter, recommendation threads, same owned-domain pages, and pages that do not identify the supplier's offering do not work.

Requirements:
- The page must visibly fit the submitted `source_role`.
- The page must clearly tie the named supplier to the exact named wood type as a hardwood product, stock category, listing, or comparable commercial offering; do not infer one walnut, maple, oak, mahogany, or figured variant from another.
- The page must show concrete offering detail for the submitted wood type, such as dimensions, thickness, grade, form, surfacing, slab or lumber category, stock / availability, price, marketplace item detail, an itemized product/species line with product class, or similar per-wood product evidence. Generic supplier capabilities or product detail elsewhere on the page do not substitute for exact wood-type offering detail.

Write one JSON object per line to `results_specialty_hardwood_offering_provenance.jsonl`:
{"item": { "supplier": "<supplier>", "wood_type": "<wood_type>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

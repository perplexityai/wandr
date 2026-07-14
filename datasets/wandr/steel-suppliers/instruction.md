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

## `steel_suppliers`

For each of the 8 steel product families below, cover at least 40+ Australian-operating suppliers per family; for every supplier-family pairing, supply at least 1+ public URL on a page where the supplier publicly states the capability.

Product families:
- `structural_sections` — structural steel / sections: structural sections such as beams, columns, channels, angles, and hollow sections
- `stainless_steel` — stainless steel: stainless steel products as a family, including stainless flat, long, tube, pipe, or specialty products
- `plate` — plate: steel plate or stainless plate supplied as plate stock, plate products, or plate processing stock
- `tube_pipe` — tube / pipe: steel, stainless, carbon, structural, precision, or commercial tube and pipe products
- `sheet_coil` — sheet / coil: sheet, coil, strip, flat product, or similar sheet-and-coil steel products
- `bar_merchant` — bar / merchant bar: merchant or engineering bar stock such as flat bar, round bar, square bar, angle bar, or similar non-reinforcing long products
- `mesh_reinforcing` — mesh / reinforcing: reinforcing steel products such as rebar, reinforcing bar, deformed bar, reo bar, reinforcing mesh, concrete mesh, or related reinforcement products
- `processing_fabrication` — processing / fabrication services: steel processing or fabrication services such as cutting, bending, profiling, drilling, welding, or fabricated steel supply

Each supplier must be a named business operating in Australia as a steel or metals stockist, distributor, manufacturer, supplier, or steel processing / fabrication provider. Product-family claims must be source-stated; broad "steel products" wording is not enough for a narrower family unless the page also names that family or clearly equivalent terms.

For downstream analysis, optional notes can capture source-stated public access or fulfillment details visible on the cited page: minimum order or quote-required status, delivery or pickup geography, online ordering, customer portal, API/EDI, and page or catalog date. Leave these details absent rather than inferring. Supplier rankings, recommendations, procurement advice, partnership outreach, lead scores, contact names, phone numbers, email addresses, and contact-form harvesting are out of scope.

Requirements:
- The page must identify the supplier as an Australia-operating steel / metals supplier, distributor, stockist, manufacturer, or steel processing / fabrication provider.
- The page must explicitly tie that supplier to the claimed `product_family` capability.
- The page must be a public provenance source for the claim: supplier-controlled product / capability / catalog pages, public catalogs or PDFs, and supplier-specific industry / trade / registry pages can count; contact-only pages, generic search or listing stubs, ranking / recommendation pages, and pages requiring private login do not.

Write one JSON object per line to `results_steel_suppliers.jsonl`:
{"item": { "product_family": "<product_family>", "supplier": "<supplier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

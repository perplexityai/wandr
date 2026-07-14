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

## `essilorluxottica_2026_frames`

For each of the 16 in-scope EssilorLuxottica-owned or licensed eyewear brands listed below, supply current 2026-window frame catalog rows: 8+ model/SKU frames per brand, 2+ colorways per frame, and a product-detail source (1+ URL per colorway). For each row, report the frame category, style or shape, frame material, colorway, and a numeric RRP/MSRP or current listed frame price.

Current-as-of date: 2026-05-07. The target is active/current catalog or retail-listing evidence available in the 2026 window, not proof that the frame was first released in 2026. Do not claim a release year unless the page itself states it.

Brands in scope:

- **Bvlgari** (also known as: BVLGARI, Bulgari)
- **Burberry**
- **Coach**
- **Costa** (also known as: Costa Del Mar)
- **Michael Kors**
- **Miu Miu**
- **Oakley**
- **Oliver Peoples**
- **Persol**
- **Prada**
- **Ralph Lauren** (also known as: Polo Ralph Lauren, Ralph by Ralph Lauren, Ralph)
- **Ray-Ban** (also known as: Ray Ban)
- **Tiffany** (also known as: Tiffany & Co., Tiffany and Co.)
- **Tory Burch**
- **Versace**
- **Vogue Eyewear** (also known as: Vogue)

Use official brand product pages where possible. Admitted retailer product-detail pages include Sunglass Hut, LensCrafters, Frames Direct, and other clearly transactional eyewear retailers only when the retailer page carries stable product-detail facts for the exact frame/colorway being claimed. Surfaces that aren't product-detail pages for the claimed frame/colorway, such as category grids, search pages, aggregator or listicle pages, etc., do not count.

Requirements:

- The page must communicate (possibly via URL host among other things) that it is an official brand page or an admitted retailer product-detail page for eyewear.
- The page must identify the claimed brand, model/SKU, and colorway or frame color for the row. For sunglasses, lens color can be part of the colorway when the page treats the frame/lens pairing as the SKU.
- The page must show frame category, style or shape, and frame material for the claimed frame/colorway. Mere page-existence of these attributes for a different SKU on the same page is not enough.
- The page must show a numeric RRP/MSRP or current listed frame/product price. Current listed price is fine when RRP is not published, but do not label a sale/current price as RRP/MSRP unless the page does.
- The page must communicate current catalog or active retail-listing status as of the 2026 window, such as active price/add-to-bag/select-lenses controls, current color options, or an official product detail page. Pages whose listing is no longer current, such as discontinued or sold-out-only surfaces, do not count.

Write one JSON object per line to `results_essilorluxottica_2026_frames.jsonl`:
{"item": { "brand": "<brand>", "model_or_sku": "<model_or_sku>", "colorway": "<colorway>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

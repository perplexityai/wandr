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

## `protein_cookie_labels`

For 45+ public US-market packaged products marketed as protein cookies, name the brand and product variant with flavor, package size, UPC, or formula/package version when visible. For each product, cover each of the 3 public source families below; under each family, supply 1+ matching source-surface category and 1+ URL with source-specific label, package, currentness, or provenance evidence.

Each submitted source is source-specific. Retailer, marketplace, and database/archive sources can preserve stale or disclaimer-limited label evidence; official FAQ or policy sources can preserve brand-controlled allergen/manufacturing policy but do not replace product-specific ingredient-label evidence. Package-image submissions are useful only when they are tied to the submitted product and preserve a visible label/package surface, readable label text, or a clear image-only limitation.

Source families:
- `brand_controlled`: brand- or manufacturer-controlled product, label, FAQ, allergen, or manufacturing-policy evidence.
- `retail_marketplace`: retailer, grocery, delivery, or marketplace listing evidence that preserves product-label text, package imagery, disclaimers, or supplier context.
- `public_database_archive`: public label, nutrition, UPC, branded-food, or package-data archive evidence with source/capture/version context.

Source-surface categories:
- `official_product_page` (brand_controlled): brand-owned product, nutrition, or ingredient page for the specific protein-cookie product, with visible current label or package-version context.
- `official_label_image` (brand_controlled): brand-owned package, nutrition, ingredient, or allergen image for the product, including readable label/OCR text or a clearly identified label-panel/package-image surface.
- `official_brand_policy` (brand_controlled): brand-owned FAQ, allergen, or manufacturing-policy page clearly tied to the protein-cookie line.
- `retailer_label_text` (retail_marketplace): retailer or grocery page with visible product label, ingredient, allergen, package-size, UPC, supplier, or package-disclaimer text.
- `retailer_label_image` (retail_marketplace): retailer or grocery package/label image surface, including image-only submissions when the package or label panel is product-specific.
- `marketplace_listing` (retail_marketplace): marketplace product listing with label text, package identity, seller/supplier context, or packaging-information disclaimer.
- `public_label_database` (public_database_archive): public label, nutrition, UPC, or branded-food database with label facts, capture/date metadata, package-source context, or manufacturer-change disclaimers.

Keep the evidence factual: public label/source wording only, with no allergy safety advice, diet compliance claims, product ranking, purchase recommendation, or claims that a product is safe or unsafe for any person.

Requirements:
- The page must identify the submitted product, or for `official_brand_policy`, identify a brand-controlled policy clearly tied to the protein-cookie product line.
- The page must fit the declared `source_family` and `source_surface`, and must make the relevant source control visible: brand/manufacturer control, retailer/marketplace control, or public database/archive control.
- The page must preserve source-specific currentness, version, or limitation context, such as package size, UPC, formula/package version, label-image-only status, database capture/source date, retailer or supplier disclaimer, stale-risk cue, discontinued/missing label state, or no-current-official-product context.
- The page must support source-specific label evidence: exact ingredient wording, allergen/may-contain/facility wording, visible product-label image evidence, or a supported absence/missing/currentness state. Marketing-only protein claims are not enough. When the source contains soy lecithin, soy derivatives, pea protein, brown rice/pea protein blends, bean/canola/other legume-derived protein phrases, or other legume-derived ingredients, the exact source wording for those terms must be preserved rather than normalized into a yes/no interpretation.

Write one JSON object per line to `results_protein_cookie_labels.jsonl`:
{"item": { "brand": "<brand>", "product_variant": "<product_variant>", "source_family": "<source_family>", "source_surface": "<source_surface>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

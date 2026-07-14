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

## `passive_speaker_specs`

Identify 35+ brands as manufacturers of passive home-audio loudspeakers; for each brand, cover each of the 2 speaker types (`bookshelf` and `floorstanding`) and find 4+ exact speaker models per brand/type. For each such brand/type/model, cover each of the 2 source roles listed below with a manufacturer-controlled public source (i.e. 1+ URL per source role).

The source roles, referred to as `source_role`, are:
- `official_product_or_archive_page`: a manufacturer product page, archive page, discontinued-product page, or official model page for the exact speaker model
- `official_document_or_support_source`: a distinct manufacturer manual, spec sheet, brochure, info sheet, downloadable PDF, documentation page, download page, or support-documentation surface for the exact speaker model

Brands ought to be real manufacturer or market-facing speaker brands, not retailers or marketplaces. Models ought to be exact passive bookshelf or floorstanding loudspeaker models; active/powered/wireless speakers with built-in amplification, center channels, architectural/in-wall/in-ceiling speakers, outdoor speakers, subwoofers, soundbars, packages, accessories, and bare series names are outside scope. Retailer pages, marketplaces, manual mirrors, forums, reviews, measurement sites, pricing pages, receiver-compatibility advice, bass-equivalence claims, rankings, setup guidance, and purchase recommendations are outside the evidence claim even when they repeat official specifications.

Requirements:
- The page should communicate that it is manufacturer-controlled or an official manufacturer documentation/support/download surface for the claimed brand or exact model.
- The page must identify the exact claimed brand and model/generation and show it as a passive bookshelf or floorstanding loudspeaker matching the claimed speaker type.
- The page should fit the claimed `source_role`: for `official_product_or_archive_page`, a product/archive/discontinued/model page; for `official_document_or_support_source`, a distinct manufacturer manual, spec sheet, brochure, info sheet, PDF, documentation page, download page, or support-documentation surface for the exact model. An ordinary product/archive/model page does not satisfy the document/support role merely because it has specifications, a downloads tab, or a link to a manual.
- The page must expose at least two concrete public technical specification values for the exact model. At least one must be an acoustic, electrical, or physical speaker specification such as nominal or minimum impedance, sensitivity, frequency response/range, driver complement, dimensions, crossover, or power handling. Document version/date, official region, discontinued status, and generation cues can help bind the source to the exact model, but they do not by themselves satisfy the technical-specification requirement.

Write one JSON object per line to `results_passive_speaker_specs.jsonl`:
{"item": { "brand": "<brand>", "speaker_type": "<speaker_type>", "model": "<model>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

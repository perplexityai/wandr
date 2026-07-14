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

## `community_association_software`

For 35+ commercial software products used for HOA, condo, COA, or community-association management, name the vendor and product and supply public evidence for 5+ closed evidence facets per vendor/product; the five labels listed below are all required. Supply 1+ URL for each submitted facet.

The work is about public provenance, not sales advice. Pricing absence, quote-only routing, and secondary-directory restatements are useful states when labeled as such; they are not invitations to estimate hidden fees or rank products.

Evidence facets:
- `pricing_publication_state`: official public pricing, official quote/contact-sales state, official no-public-price state, or carefully labeled secondary-only/conflicting pricing evidence
- `capability_mechanism`: official product/help/docs or workflow-page evidence showing page-specific mechanics for a community-association workflow
- `workflow_documentation`: official public help, support, training, implementation, release-note, or product-documentation evidence showing operational setup or use instructions for a community-association workflow
- `target_segment`: official source-stated audience or market positioning for HOA, condo, COA, board, resident, LCAM, association-manager, or adjacent association use
- `review_footprint`: product-specific secondary review-profile or equivalent product-specific review-surface metadata limited to rating, review count, platform, review-date window, verification text, and source-date text

Property-management-first products count when the submitted page ties the product to association-specific use. Generic association or membership tools count only when the page ties them to HOA, condo, COA, community-association, resident/owner, board, LCAM, or association-management workflows.

For each row, state a concise finding, the source role, the date you checked the source, and either the visible source date or `source_date_not_shown`. For pricing rows, state the pricing publication state. Treat exact prices and review counts as observed on the checked date.

Requirements:
- The page must identify the named vendor/product and tie it to community-association software use or an association-specific product module.
- The page must fit the source role for `evidence_facet`: official vendor/order/terms surfaces for official pricing truth; official product/help/docs/workflow surfaces for capability mechanisms; official public help-center, support, training, implementation, release-note, or product-documentation pages for workflow documentation; official market or company surfaces for target segment; and product-specific review profiles, review pages, app-store listings, or equivalent product-specific review surfaces for review metadata. Broad category, list, search, best-of, or comparison directory pages do not satisfy `review_footprint` even when a product card on the page shows rating or review-count text. Secondary pricing pages can support only secondary-only or conflict state. Product, pricing, market, and directory pages do not satisfy `workflow_documentation` unless they are also a genuine public documentation/training/support artifact.
- The page must expose a concrete facet finding. Pricing rows must preserve official price, quote-only, official no-public-price, or secondary-only/conflicting state; capability rows need mechanism-level workflow detail such as who acts, what is submitted, routed, tracked, paid, notified, approved, integrated, or recorded; workflow-documentation rows need operational setup, usage, training, troubleshooting, release, or administrator/user instruction detail from a public official documentation surface; target rows need source-stated segment language; review rows may use metadata only and need visible product-specific rating/review-count/source-date or review-window metadata. Source-stated company or traction facts may appear as extra answer detail when relevant, but they are not an `evidence_facet` and cannot replace any required facet.

Write one JSON object per line to `results_community_association_software.jsonl`:
{"item": { "vendor": "<vendor>", "product": "<product>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

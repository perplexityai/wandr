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

## `reading_app_capability_provenance`

For each of the 5 reading/study capability classes below, cover 40+ product-and-developer app capability identities; for each app capability, supply each of the 2 source roles listed below, with 1+ URL for each role.

The goal is factual public provenance for reading, study, annotation, flashcard, summarization, and multi-source reading apps. Keep the evidence source-bound: no rankings, app recommendations, procurement advice, personalized education advice, medical or learning-disability advice, or unsupported claims that a product improves learning outcomes.

Capability classes:
- `book_or_article_summary`: summarizes books, articles, PDFs, videos, or other reading material into short summaries, key ideas, briefs, blinks, or similar condensed reading outputs
- `ai_generated_flashcards_or_quizzes`: uses AI to generate flashcards, quizzes, practice questions, tests, or similar study artifacts from notes, documents, slides, videos, or other source material
- `annotation_or_pdf_to_study_workflow`: supports annotation, highlighting, PDF/deep-reading markup, or conversion from marked-up reading material into notes, mind maps, flashcards, or study workflows
- `spaced_repetition_or_review_scheduling`: claims spaced repetition, SRS, adaptive review scheduling, or named review timing mechanics for remembered material
- `read_it_later_or_multi_source_reading`: saves, imports, or unifies multiple reading-source types such as articles, newsletters, RSS, PDFs, EPUBs, web pages, or read-it-later queues

Source roles:
- `official_capability_claim`: product-controlled evidence that explicitly describes the selected capability
- `distribution_or_storefront_context`: public distribution, store, download, package, or availability evidence for the same product

Product identity should stay precise. The same product may appear under multiple capabilities, but each `(capability, product, developer)` identity should refer to a real publicly available app/product and should not blur rebrands, major version splits, ecosystem companions, unofficial clones, or similarly named apps from different developers.

Requirements:
- The page must identify the submitted product/app and tie it to the submitted developer, publisher, official ecosystem, package ID, store identity, or otherwise clear app identity.
- The page must make the submitted source role visible. `official_capability_claim` must come from a product/developer-controlled official source such as a product site, help center, docs/manual, support article, official blog, pricing page, or official product page; app-store listings, generic review blogs, recommendation posts, Reddit threads, and SEO comparison pages do not satisfy this role. `distribution_or_storefront_context` must come from a public distribution or availability surface such as Apple App Store, Google Play, Microsoft Store, Chrome Web Store, official download pages, GitHub/project distribution pages for open-source tools, or comparable app/package/download surfaces; generic review blogs, recommendation posts, Reddit threads, and SEO comparison pages do not satisfy this role.
- The page must carry the source-role payload. For `official_capability_claim`, it must explicitly describe the selected capability for the product; vague claims like "AI-powered learning" are not enough without saying what the AI does or generates. For `distribution_or_storefront_context`, it must expose concrete distribution/storefront context for the same product, such as platform, app/package ID, developer/publisher, rating or review count, update date, price/IAP/free/open-source signal, supported distribution channel, or similar checked-at-source facts.

Write one JSON object per line to `results_reading_app_capability_provenance.jsonl`:
{"item": { "capability": "<capability>", "product": "<product>", "developer": "<developer>", "source_role": "<source_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

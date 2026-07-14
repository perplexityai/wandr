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

## `neurovascular_open_payments`

For 120+ well-identified publication-author clusters from 2018-2026 aneurysm or neurovascular-device publications, supply public source URLs (1+ per evidence layer) for each of the 3 evidence layers below. The cluster anchor is a public article and one US neurosurgeon or neurovascular physician author with a concrete public CMS Open Payments payment row, not a physician ranking or a claim that any payment influenced any publication.

Evidence should preserve source scope: CMS Open Payments facts are limited to the checked detailed payment years 2018-2024 (checked 2026-06-26), product fields may be missing or generic on a specific payment record, and no-confident-author-match / name-conflict states count only on identity evidence that visibly supports the uncertainty. Generic CMS overview, methodology, annual-release, source-version, or homepage material may support source-year context, but it cannot by itself satisfy the `cms_payment` evidence layer.

The intended breadth is publication-author evidence, not a profile roll-up for a small set of prolific clinicians. When the same clinician appears in multiple clusters, each cluster still needs its own publication-specific article evidence and `cms_payment` evidence for a concrete payment row whose date, company, product/device field state, or no-product-field state is compared to that publication. Reusing one physician or payment-profile page unchanged across many article clusters is not enough, and a generic or no-product payment row is not portable across many publications unless the row still has a concrete publication-scoped date/company/device-class comparison.

Evidence layers:
- `publication_topic`: publication metadata plus aneurysm / neurovascular device-topic evidence for the article and the named author as published.
- `author_identity`: public evidence that the named article author is the submitted US neurosurgeon or neurovascular physician, including specialty and NPI or Open Payments identity support when public.
- `cms_payment`: record-specific CMS Open Payments evidence for the matched covered recipient and one concrete payment row.

Eligible source scope is layer-specific: use scholarly metadata, article / full-text, study, or device records for `publication_topic`; NPPES, official institutional / faculty / hospital profiles, or Open Payments profile evidence for `author_identity`; and official CMS Open Payments payment-detail, record-keyed search-result, or public-use-file/download row evidence for `cms_payment`. Broad recipient profiles, yearly totals, third-party historical mirrors, generic payment summaries, and generic CMS source pages are auxiliary context only for `cms_payment` unless the cited page or file is anchored to the submitted concrete payment row.

Submissions that draw conflict-of-interest conclusions, influence claims, clinical-quality judgments, legal allegations, patient guidance, physician rankings, or alert-service assurances do not count.

Requirements:
- The page must support the submitted publication-author cluster at the layer's natural level: article plus named author for `publication_topic`; the submitted clinician identity and match support or identity conflict for `author_identity`; the matched covered recipient name plus NPI/profile ID and payment record key for `cms_payment`.
- The page must provide the layer's factual details: publication identifiers and neurovascular device-topic evidence for `publication_topic`; US clinician, specialty, affiliation, NPI or Open Payments identity support where public for `author_identity`; CMS program year/source version plus the concrete payment row's recipient key, company, amount, date, nature, dispute status, and product fields where public for `cms_payment`.
- The page must support the submitted relation or uncertainty state, such as article topic / author roster evidence, high-confidence identity match, no confident author match, name conflict, or, for `cms_payment`, a publication-scoped comparison between the concrete payment row and the article's year/topic/device context: before/during/after publication window, same company/product/device class, no public product field on that payment row, or product mismatch on that payment row.

Write one JSON object per line to `results_neurovascular_open_payments.jsonl`:
{"item": { "publication": "<publication>", "author_clinician": "<author_clinician>", "evidence_layer": "<evidence_layer>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

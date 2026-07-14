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

## `religion_nonfiction_publisher_imprint_provenance`

For each of the 3 publisher-type groups listed below, identify 20+ public publishers, imprints, or publishing programs, and for each publisher or imprint cover each of the 3 evidence facets with a page-specific source (1+ URL per facet). Publishers and imprints should have public source-stated Christian, theology, religious-studies, spirituality, philosophy-of-religion, religion-and-culture, church/ministry, or adjacent nonfiction publishing scope.

This is public publishing-source provenance, not a publisher ranking, manuscript-fit verdict, query strategy, outreach list, contact-enrichment task, procurement recommendation, legal advice, financial advice, or publishing advice.

Publisher-type groups:
- `religious_trade_publisher`: a trade, independent, denominational, or ministry-facing publisher or imprint whose public nonfiction list is framed around Christian, theology, faith-and-culture, church/ministry, spirituality, or comparable religion-adjacent readerships
- `academic_religion_press`: a university press, academic-society press, scholarly publisher, or scholarly imprint/program with public religious studies, theology, biblical studies, church history, philosophy-of-religion, or comparable religion nonfiction publishing
- `general_house_religion_imprint`: a distinct religion, faith, spirituality, theology, or religion-adjacent nonfiction imprint or publishing program inside a broader general trade or mainstream publishing house

Evidence facets:
- `submission_posture`: the entity's public book-proposal or manuscript-submission posture, including direct, agented-only, invited, conference-only, closed, or no-unsolicited posture
- `catalog_representation`: the entity's official catalog, list, series, subject, or title evidence showing representative in-scope nonfiction publishing
- `ecosystem_context`: entity-specific publishing-ecosystem context from a parent house, association, conference, directory/profile, trade article, or comparable public source

The named entity ought to be a real publisher, imprint, or publishing program that public sources treat as distinct. Imprints count separately when they are publicly presented as distinct publishing programs; do not split a publisher into ordinary series, book lines, or subject shelves unless the public source presents them as an imprint or comparable publishing program. Closed, agent-only, invited, or no-unsolicited submission posture is eligible public provenance; the task is not limited to entities accepting direct unsolicited submissions.

Requirements:
- The page must clearly identify the named publisher or imprint and tie it to Christian, theology, religious studies, spirituality, philosophy-of-religion, religion-and-culture, church/ministry, or adjacent nonfiction publishing.
- The page should visibly fit the source role for the selected evidence facet: for `submission_posture`, an official, owned, or controlled publisher/imprint source; for `catalog_representation`, an official, owned, or controlled catalog, list, series, subject, or title source; for `ecosystem_context`, an entity-specific parent-house, association, conference, directory/profile, trade article, or comparable publishing-context source rather than a generic list or search page.
- The page must contribute the facet-specific public evidence: for `submission_posture`, public book-proposal or manuscript-submission posture; for `catalog_representation`, representative in-scope nonfiction books, series, subject categories, catalogs, or lists; for `ecosystem_context`, public context explaining the publisher's place in religion, theology, faith, spirituality, religious-studies, or adjacent nonfiction publishing.

Write one JSON object per line to `results_religion_nonfiction_publisher_imprint_provenance.jsonl`:
{"item": { "publisher_type": "<publisher_type>", "publisher_or_imprint": "<publisher_or_imprint>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `sitecore_award_engagement_provenance`

For 75+ public Sitecore Experience Awards winning client/project engagements announced on or before 2026-06-09, provide one source for each of the 2 evidence types below, with 1+ URL per evidence type.

The evidence types are:
- `award_confirmation`: A public source that explicitly confirms the Sitecore Experience Awards win for the named client/project engagement.
- `implementation_case_study`: A public source about the same client/project implementation that states concrete implementation substance.

Reputable public sources can include Sitecore award pages, Sitecore customer stories, partner or client case studies, client or partner news pages, reputable industry press, press-wire copy, or comparable public pages when the page itself satisfies the selected evidence type. Social-only posts, search snippets, directory cards, and shallow portfolio index cards are discovery leads rather than final evidence pages.

Scope and validity bars: the engagement must be a public Sitecore Experience Awards winning client/project engagement. Out-of-scope programs such as Adobe Experience Maker Awards, Acquia Engage Awards, Optimizely awards, Kentico awards, Contentful awards, and similar non-Sitecore awards do not count. The client or project must be public and source-stated; partner-only awards, partner-tier recognition, MVP recognition, generic partner-of-the-year recognition, and awards without a named client/project engagement do not count.

Requirements:
- `award_confirmation` sources must be award/winner-confirmation sources that explicitly state a Sitecore Experience Awards win, category or award scope, and enough year, partner, and client/project identity to bind the engagement. A client, partner, or Sitecore implementation story that merely mentions an award is not an `award_confirmation` source unless its source role is clearly winner confirmation. Finalist, nomination, shortlist, honorable-mention, or "winner to be announced" pages do not count without a separate source proving winner status.
- `implementation_case_study` sources must be about the same named client/project implementation and state concrete implementation substance: Sitecore products, migration details, search/content/commerce/personalization work, integrations, headless or composable architecture, project scope, or implementation outcomes/metrics. Winner lists, award announcements, finalist pages, and award-category summaries do not count as implementation evidence unless they contain source-stated implementation substance beyond award/category language, and no technical stack or architecture should be inferred from the award program, category name, or agency specialty.

Write one JSON object per line to `results_sitecore_award_engagement_provenance.jsonl`:
{"item": { "award_year": "<award_year>", "region_or_scope": "<region_or_scope>", "award_category": "<award_category>", "partner_name": "<partner_name>", "client_or_project_name": "<client_or_project_name>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

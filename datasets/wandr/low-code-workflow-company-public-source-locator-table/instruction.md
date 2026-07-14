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

## `low_code_workflow_company_public_source_locator_table`

For 120+ companies or OSS/hybrid projects in low-code, no-code, workflow automation, iPaaS, agent-workflow, orchestration, RPA/browser automation, or adjacent AI/workflow software, supply 6+ non-homepage public source locators per company/project, with 1+ URL for each source class.

This is a public provenance atlas for a seed originally dated 2026-03-21. The submitted evidence should use public pages available to check directly, preserve visible source dates when the page has them, and avoid turning locator evidence into monitoring, ranking, vendor-selection, affiliate-strategy, procurement, outreach, or implementation advice.

`source_class` must be one of:
- `docs`: official documentation, help center, API docs, or developer docs controlled by the company/project.
- `blog_news`: official blog, news, press, or update page controlled by the company/project.
- `changelog_release_notes`: official release notes, changelog, version-history, or comparable dated update source controlled by the company/project.
- `pricing`: official pricing, plans, packaging, or subscription page controlled by the company/project.
- `affiliate_partner`: source-stated public affiliate, partner, technology-partner, solution-partner, or comparable program/presence page controlled by the company/project.
- `marketplace_app_directory`: the company/project's owned app, integration, connector, template, marketplace, or directory surface.
- `source_repo`: official source repository for an OSS or hybrid project, normally on a recognized code-hosting site or linked from the official project.
- `community`: official or clearly company-run community/forum/support-community surface for users, builders, or developers.
- `product_directory`: reputable independent product/category directory evidence; this is the only third-party source class and must be treated as corroboration, not ranking, procurement, or selection advice.

Plain official homepages are useful identity anchors but are not a counted source class here. A homepage URL only works when the cited page itself also behaves as one of the listed source classes.

Requirements:
- The page must identify the submitted company/project and support its connection to low-code/no-code/workflow automation, integration, agent workflow, orchestration, RPA/browser automation, or adjacent AI/workflow software.
- The page must fit the declared `source_class`, including the ownership rule for that class: official or company-controlled for all classes except `product_directory`, and reputable independent product/category corroboration for `product_directory`; wrong surfaces such as comparison verdicts, listicle rankings, customer use cases for "affiliate" or "RSS", third-party directories submitted as official classes, unrelated service-provider pages, or unresolved name-conflict pages do not satisfy the source-class fit.
- The page must contribute concrete locator substance for the declared class: class-appropriate page content, source-stated affiliate/partner presence where claimed, official repository identity for `source_repo`, owned app/integration directory content for `marketplace_app_directory`, and dated update/source-date signals where the cited class is date-bearing.

Write one JSON object per line to `results_low_code_workflow_company_public_source_locator_table.jsonl`:
{"item": { "company_project": "<company_project>", "source_class": "<source_class>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

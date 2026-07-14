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

## `mineral_partnership_events`

For 120+ public copper or copper-adjacent critical-minerals supply-growth partnership milestone events dated from 2020-01-01 through 2026-06-30, supply sources for each of the 2 source sides (i.e. 1+ URL per side).

A partnership event is a source-stated dated milestone, not just a relationship mention. It must have concrete actors plus project, district, mine, asset, program, region, or comparable mineral-supply context, and it must advance or document copper or adjacent critical-minerals supply growth. Valid milestone types include announcement, signing, closing, effective date, binding offtake or funding step that creates or advances a partnership, joint-venture formation, acquisition-completion milestone, technology deployment, program partnership, or source-stated project/program update. Announcement and closing are different events when the sources present them as different milestones.

The universe is open: major producers, developers, state entities, traders, offtakers, technology owners, strategic investors, and program operators can all appear. Do not count generic strategy pages, generic collaboration interest, loose investor-news lists, routine financing or investor updates without partnership substance, project profiles with no milestone, or continuing relationship mentions.

The source sides of interest, which we refer to as `source_side`, are:
- `primary_disclosure`
- `independent_corroboration`

`primary_disclosure` means an event actor's own public disclosure, a JV/project-controlled source, a stock-exchange or regulator filing, an official investor or technical release, or a comparable primary source. `independent_corroboration` means a separate public surface that corroborates the same event without being a same-release mirror or same-corporate-family republication: for example a counterparty-controlled source, separate filing, project/government/institutional page, or credible mining trade/news source.

For each source, name the normalized source-stated actors, project/district/mine/asset/program/region or comparable setting, commodity, event type, source-stated status, event date, date type (`announced`, `signed`, `closed`, `effective`, `updated`, or `unclear`), and the source-stated finding. Keep the output to public evidence; do not provide investment advice, mineral-project recommendations, supplier/procurement rankings, deal sourcing, lead scoring, contact enrichment, legal conclusions, or compliance conclusions.

Requirements:
- The page must describe a specific source-stated partnership event or milestone, not merely a continuing relationship, broad company strategy, project profile, generic collaboration interest, loose investor-news list, routine financing or investor update without partnership substance, or recurring relationship mention.
- The page must name the source-stated actors and tie the event to a project, district, mine, asset, program, region, or comparable mineral-supply setting with enough role/context detail to distinguish the event.
- The page must support a dated event/status in the task window, including whether the date is an announcement, signing, closing, effective date, update, or unclear source-stated event date.
- The page must tie the event to copper or adjacent critical-minerals supply growth such as exploration, development, production, processing, offtake, infrastructure, technology deployment, or asset/program funding that binds parties to the supply-growth milestone.
- The page must fit the submitted `source_side`: primary-style disclosure for `primary_disclosure`, or separate corroborating public evidence for `independent_corroboration`.

Write one JSON object per line to `results_mineral_partnership_events.jsonl`:
{"item": { "partnership_event": "<partnership_event>", "source_side": "<source_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

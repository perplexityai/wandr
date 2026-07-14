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

## `bi_analytics_ai_capability_provenance`

For 125+ public BI, embedded analytics, data-app, or AI-first analytics software vendors, name 1+ specific AI / copilot / agent / conversational-analytics capabilities per vendor, and cover each of the 2 official evidence roles below for every vendor-capability pair with a source (i.e. 1+ URL per role).

The dated evidence window is 2025-01-01 through 2026-06-24, inclusive. The goal is public official-source provenance for what the vendor said, where it said it, and what source-stated date or current capability wording attaches to the named capability. This is not a competitor ranking, buyer recommendation, pricing comparison, sales battlecard, displacement narrative, lead list, outreach task, or Vizpresso-relevance exercise.

The evidence roles of interest, which we refer to as `evidence_role`, are:
- `official_dated_release_source`: a vendor-owned or official product-family release note, changelog, what's-new page, official blog/news post, or official documentation page that states a publication, release, update, or version date within the dated evidence window and ties that date to the named capability.
- `current_official_capability_surface`: a vendor-owned product, documentation, help, setup, support, or product-family page that currently describes the same capability's functionality or availability. This page may be undated, but it cannot supply the dated-release role unless it states an eligible source date.

Official primary sources are required for both roles. Third-party recaps, Gartner/MQ/G2/Capterra pages, outside listicles, review sites, marketplace profiles, vendor-authored "best BI tools" articles, third-party pricing estimates, and comparable discovery surfaces do not count as row evidence for either role.

Requirements:
- The page must communicate that it is a vendor-owned or official product-family source for the declared vendor or capability.
- The page must have the source role required by `evidence_role`.
- The page must name the declared capability or clearly describe the same specific AI workflow; generic "AI-powered analytics" slogans are not enough.
- The page must tie the capability to analytics, BI, data analysis, dashboards, semantic models, embedded analytics, data apps, or closely related analytics workflows.
- The page must expose the role-specific source-stated detail: for `official_dated_release_source`, a stated publication/release/update/version date in the dated evidence window and release/update/documentation wording for the capability; for `current_official_capability_surface`, current source-stated functionality or availability for the same capability.

Write one JSON object per line to `results_bi_analytics_ai_capability_provenance.jsonl`:
{"item": { "vendor": "<vendor>", "capability": "<capability>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

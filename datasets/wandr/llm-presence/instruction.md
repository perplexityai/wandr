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

## `llm_presence`

Identify 10+ companies as LLM-producers and compile a panel on public-community sentiment / feedback dynamics: for each company, cover each of the 12 months going backward from 2026-03 (individually); for every producer-month pair, provide at least 3 different sites, with each site contributing 2+ distinct standalone posts / discussion pages regarding the named company's model(s) and scoped to that target month. Companies ought to be actual public LLM-producer labs / enterprises, and the models discussed ought to be the named company's creation; however, the model(s) themselves could be outside the strict LLM universe, as long as the producer is in scope.

The provided sources should be standalone, dedicated discussion / impression pages: mere landings / in-bulk thread views / intra-search-result displays (to name a few examples) won't do. The source's nature should also have personal, first-hand impression transmission as one of its primary intents, exhibiting a particular-user voice-hosting function rather than an editorial / analytical angle: in that sense, news articles / aggregated feedback report pages and such wouldn't qualify (even when providing direct actual-user-originating citations), whereas community discussion forums / personal websites would.

Requirements:
- The page must clearly communicate (possibly via URL, when URL-shape signal is genuinely relevant) the target-month match: explicit in-content dates / post timestamps / thread-level date markers / etc. For pages with multiple dated elements, the most titular date is the relevant one, e.g. main-post-level for thread / forum discussion chains, earliest-comment if that's the first visible date anchoring the page, etc.
- The page must be directly and primarily about the target company's model(s); e.g. a comment about some model X from a page dedicated to another model Y main-topic-wise won't do, even when that comment is very expansive and thorough.
- The page should showcase real public reception: opinions, reactions, experiences, and so on; e.g. a bare neutral release-note re-share wouldn't be eligible, whereas a substantive opinion accompanying said re-share and/or actual voiced reactions / relevant post-motivated discussions as responses to it would.

Write one JSON object per line to `results_llm_presence.jsonl`:
{"item": { "company": "<company>", "month": "<month>", "site": "<site>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

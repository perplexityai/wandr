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

## `restaurant_openings_nyc`

For 100+ restaurants that opened in New York City (the five boroughs) during 2024, name the cuisine, chef or owner, opening period, and neighborhood — and supply at least 2 URLs, each on a page corroborating all of the claims. The entity must be a brick-and-mortar restaurant; food carts, pop-up-only operations, private-events-only spaces, and bars without a real food menu do not count. Reopenings under new ownership of long-shuttered spaces count when the relaunch is within 2024; namesake spinoffs under a distinct identity count; chain second-locations under the same identity do not.

Requirements:
- The page must support the claimed restaurant name and address — same name (formatting variations like accents, capitalization, possessives are fine) at the same address (formatting variations like abbreviations are fine).
- The page must show or support the opening event occurring within 2024: a specific opening date, an explicit month-and-year, or "now open" framing on a page itself dated within 2024.
- The page must describe the restaurant's cuisine in a way consistent with the claim — different vocabulary for the same cuisine ("French bistro" vs "French") is fine; clearly different cuisines do not match.
- The page must identify the named chef or owner in their claimed role (chef, owner, restaurateur, culinary director, partner, co-owner). Naming any one of multiple co-chefs or co-owners works as long as the page supports that role for that named person.
- The page must situate the restaurant in the claimed neighborhood or borough — borough claims are subsumed by named neighborhoods within them; substantially equivalent neighborhoods (across a fluid line like Astoria / Long Island City) are fine; clearly different neighborhoods do not match.

Write one JSON object per line to `results_restaurant_openings_nyc.jsonl`:
{"item": { "restaurant_name": "<restaurant_name>", "address": "<address>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

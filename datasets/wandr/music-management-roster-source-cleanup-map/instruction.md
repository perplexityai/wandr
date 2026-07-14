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

## `music_management_roster_source_cleanup_map`

For 70+ music-management or artist-representation companies, find 3+ artists per company whose public management relationship is acknowledged from both sides; for each such (`management_company`, `artist`) pair and each of the 2 representation sides listed below, supply a relationship-substantiating source (i.e. 1+ URL).

A management roster mention by itself can be stale or one-sided; the useful object here is a public representation relationship that the management company claims and the artist side also acknowledges.

The representation sides of interest, which we refer to as `reference_type`, are:
- `roster_claim`: the management-company side claiming the artist as rostered, represented, managed, or a client.
- `artist_acknowledgment`: the artist side acknowledging the same company, or a company-affiliated manager, as management or representation.

`management_company` ought to be a real music-management or artist-representation company, and `artist` ought to be a real music artist, band, act, or recording project. Labels, booking-only agencies, venues, festivals, media outlets, fan pages, and other non-management/non-artist nodes are outside this relationship.

Requirements:
- The page should communicate that it is an officially-controlled channel for the party being cited: for `roster_claim`, that party is `management_company`; for `artist_acknowledgment`, that party is `artist`. Owned domains, verified public channels, official artist sites, official EPK / team / release pages, and visibly documented subdomain or account affiliation can carry this; third-party aggregators, contact-enrichment pages, press-wire mirrors, fan pages, and generic directories usually cannot.
- The page must explicitly identify the opposite party: for `roster_claim`, `artist` should be clearly identifiable; for `artist_acknowledgment`, `management_company` should be clearly identifiable, either directly named or through a named manager whose affiliation with the claimed management company is visible on the page. A bare person name without a firm tie does not establish the company relationship.
- The page should acknowledge the management relationship at the bar appropriate to `reference_type`: for `roster_claim`, roster, client, artist, management, or representation context from the management-company side can count; for `artist_acknowledgment`, the artist-side page must carry an actual management, team, representation, or manager-credit acknowledgment tied to the claimed management company, not merely booking, label, publishing, PR, fan/wiki, general thanks, or unrelated credits.

Write one JSON object per line to `results_music_management_roster_source_cleanup_map.jsonl`:
{"item": { "management_company": "<management_company>", "artist": "<artist>", "reference_type": "<reference_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

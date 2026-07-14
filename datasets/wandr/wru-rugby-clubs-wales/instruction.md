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

## `wru_rugby_clubs_wales`

For each of the 30 current senior men's WRU league divisions listed below,
supply at least 8 current club-or-senior-side membership rows per
division as of 2026-05-07, with one source URL per row. Additional current club rows are
welcome, especially in divisions with more than eight teams.

Requirements:
- Club/side identity: evidence must name the claimed club or named senior side in a
  senior men's rugby context.
- Division membership: evidence must show that the claimed club or side participates in
  the claimed WRU/SRC league division.
- Current season: evidence must be for the 2025-26 season or the current competition
  context as of 2026-05-07.

Use official WRU/MyWRU competition table, fixture, or results pages; official
club-controlled fixture, table, news, or team pages; or official regional rugby body pages
when they establish current WRU league membership. Do not rely on BBC tables, All Wales
Sport, Wikipedia, fan directories, generic club histories, social media pages, search
snippets, old-season pages, cup-only fixtures, women's/youth/schools competitions, URC
regional professional teams, or district/Athletic Conference rows unless the same club or
side is also evidenced in one of the divisions below.

The closed division set is:

- Super Rygbi Cymru (aliases: SRC, Super Rugby Cymru, Super Rygbi Cymru League)
- Admiral Men's Premiership (aliases: Community Premiership, WRU Premiership, Admiral Premiership, WRU Community Premiership)
- Admiral Men's National Championship East (aliases: Championship East, WRU Championship East, Admiral Championship East, National Championship East)
- Admiral Men's National Championship West (aliases: Championship West, WRU Championship West, Admiral Championship West, National Championship West)
- Admiral National League 1 East (aliases: League 1 East, Division 1 East, National League Div. 1 East)
- Admiral National League 1 East Central (aliases: League 1 East Central, Division 1 East Central, National League Div. 1 East Central)
- Admiral National League 1 North (aliases: League 1 North, Division 1 North, National League Div. 1 North)
- Admiral National League 1 West (aliases: League 1 West, Division 1 West, National League Div. 1 West)
- Admiral National League 1 West Central (aliases: League 1 West Central, Division 1 West Central, National League Div. 1 West Central)
- Admiral National League 2 East (aliases: League 2 East, Division 2 East, National League Div. 2 East)
- Admiral National League 2 East Central (aliases: League 2 East Central, Division 2 East Central, National League Div. 2 East Central)
- Admiral National League 2 North (aliases: League 2 North, Division 2 North, National League Div. 2 North)
- Admiral National League 2 West (aliases: League 2 West, Division 2 West, National League Div. 2 West)
- Admiral National League 2 West Central (aliases: League 2 West Central, Division 2 West Central, National League Div. 2 West Central)
- Admiral National League 3 East (aliases: League 3 East, Division 3 East, National League Div. 3 East)
- Admiral National League 3 East Central (aliases: League 3 East Central, Division 3 East Central, National League Div. 3 East Central)
- Admiral National League 3 North East (aliases: League 3 North East, Division 3 North East, National League Div. 3 North East)
- Admiral National League 3 North West (aliases: League 3 North West, Division 3 North West, National League Div. 3 North West)
- Admiral National League 3 West (aliases: League 3 West, Division 3 West, National League Div. 3 West)
- Admiral National League 3 West Central (aliases: League 3 West Central, Division 3 West Central, National League Div. 3 West Central)
- Admiral National League 4 East (aliases: League 4 East, Division 4 East, National League Div. 4 East)
- Admiral National League 4 East Central (aliases: League 4 East Central, Division 4 East Central, National League Div. 4 East Central)
- Admiral National League 4 West A (aliases: League 4 West A, Division 4 West A, National League Div. 4 West A)
- Admiral National League 4 West B (aliases: League 4 West B, Division 4 West B, National League Div. 4 West B)
- Admiral National League 4 West Central (aliases: League 4 West Central, Division 4 West Central, National League Div. 4 West Central)
- Admiral National League 5 East (aliases: League 5 East, Division 5 East, National League Div. 5 East)
- Admiral National League 5 East Central (aliases: League 5 East Central, Division 5 East Central, National League Div. 5 East Central)
- Admiral National League 5 West Central (aliases: League 5 West Central, Division 5 West Central, National League Div. 5 West Central)
- Admiral National League 6 East (aliases: League 6 East, Division 6 East, National League Div. 6 East)
- Admiral National League 6 East Central (aliases: League 6 East Central, Division 6 East Central, National League Div. 6 East Central)

Write one JSON object per line to `results_wru_rugby_clubs_wales.jsonl`:
{"item": { "division": "<division>", "club": "<club>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

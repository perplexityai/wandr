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

## `usports_basketball_coaches`

For each of the 48 U SPORTS men's basketball universities listed below, name at least 3+ in-scope men's basketball coaches currently on the 2025-26 / current-season coaching staff as of 2026-05-07, with the coach's name, role or title, and an official source URL corroborating that the named person currently holds that coaching role at that university.

Requirements:
- The evidence must be for the claimed university's men's basketball program and the currently published 2025-26 / current-season staff context as of 2026-05-07.
- The evidence must name the claimed coach and show the claimed role or title, or a materially equivalent title for that university.
- The role must be an in-scope men's basketball coaching role, not a support, medical, administrative, social, operations, or directory contact role. In-scope roles include head coach, interim head coach, associate coach, lead assistant coach, assistant coach, and coaching-primary specialist roles such as analytics coach, player development coach, or athletic development coach.

The closed 2025-26 U SPORTS men's basketball university set is:

- University of Victoria (aliases: Victoria, UVic, Victoria Vikes, Vikes)
- Bishop's University (aliases: Bishop's, Bishops, Bishop's Gaiters, Gaiters)
- Carleton University (aliases: Carleton, Carleton Ravens, Ravens)
- University of Winnipeg (aliases: Winnipeg, Winnipeg Wesmen, Wesmen)
- Toronto Metropolitan University (aliases: Toronto Metropolitan, TMU, TMU Bold, Ryerson)
- University of British Columbia (aliases: UBC, UBC Thunderbirds, British Columbia)
- Western University (aliases: Western, University of Western Ontario, Western Ontario Mustangs, Western Mustangs, Mustangs)
- University of Ottawa (aliases: Ottawa, uOttawa, Ottawa Gee-Gees, Gee-Gees)
- St. Francis Xavier University (aliases: StFX, St. FX, StFX X-Men, X-Men)
- Brock University (aliases: Brock, Brock Badgers, Badgers)
- Queen's University (aliases: Queen's, Queens, Queen's Gaels, Gaels)
- Université Laval (aliases: Laval, Rouge et Or, Laval Rouge et Or, University Laval)
- University of Alberta (aliases: Alberta, Alberta Golden Bears, Golden Bears)
- University of the Fraser Valley (aliases: UFV, Fraser Valley, UFV Cascades, Cascades)
- University of Manitoba (aliases: Manitoba, Manitoba Bisons, Bisons)
- University of Calgary (aliases: Calgary, Calgary Dinos, Dinos)
- Lakehead University (aliases: Lakehead, Lakehead Thunderwolves, Thunderwolves)
- Concordia University (aliases: Concordia, Concordia Stingers, Stingers)
- Acadia University (aliases: Acadia, Acadia Axemen, Axemen)
- University of Guelph (aliases: Guelph, Guelph Gryphons, Gryphons)
- University of New Brunswick (aliases: UNB, New Brunswick, UNB Reds, Reds)
- Trinity Western University (aliases: Trinity Western, TWU, TWU Spartans, Spartans)
- Mount Royal University (aliases: Mount Royal, MRU, MRU Cougars, Cougars)
- Thompson Rivers University (aliases: Thompson Rivers, TRU, TRU WolfPack, WolfPack)
- University of Windsor (aliases: Windsor, Windsor Lancers, Lancers)
- Laurentian University (aliases: Laurentian, Laurentian Voyageurs, Voyageurs)
- University of Toronto (aliases: Toronto, U of T, University of Toronto Varsity Blues, Varsity Blues)
- Brandon University (aliases: Brandon, Brandon Bobcats, Bobcats)
- Université du Québec à Montréal (aliases: UQAM, UQAM Citadins, Citadins, University of Quebec at Montreal)
- University of Prince Edward Island (aliases: UPEI, Prince Edward Island, UPEI Panthers, Panthers)
- Cape Breton University (aliases: Cape Breton, CBU, CBU Capers, Capers)
- Memorial University of Newfoundland (aliases: Memorial, Memorial Sea-Hawks, MUN, Sea-Hawks)
- Wilfrid Laurier University (aliases: Laurier, Wilfrid Laurier, Laurier Golden Hawks, Golden Hawks)
- Ontario Tech University (aliases: Ontario Tech, Ontario Tech Ridgebacks, Ridgebacks)
- University of Regina (aliases: Regina, Regina Cougars)
- University of Waterloo (aliases: Waterloo, Waterloo Warriors, Warriors)
- University of Lethbridge (aliases: Lethbridge, Lethbridge Pronghorns, Pronghorns)
- Dalhousie University (aliases: Dalhousie, Dalhousie Tigers, Tigers)
- University of Saskatchewan (aliases: Saskatchewan, Saskatchewan Huskies, Huskies)
- Saint Mary's University (aliases: Saint Mary's, Saint Marys, SMU, SMU Huskies)
- McGill University (aliases: McGill, McGill Redbirds, Redbirds)
- Nipissing University (aliases: Nipissing, Nipissing Lakers, Lakers)
- York University (aliases: York, York Lions, Lions)
- McMaster University (aliases: McMaster, McMaster Marauders, Marauders)
- MacEwan University (aliases: MacEwan, MacEwan Griffins, Griffins)
- University of British Columbia Okanagan (aliases: UBCO, UBC Okanagan, UBC Okanagan Heat, Heat)
- University of Northern British Columbia (aliases: UNBC, Northern British Columbia, UNBC Timberwolves, Timberwolves)
- Algoma University (aliases: Algoma, Algoma Thunderbirds, Thunderbirds)

Write one JSON object per line to `results_usports_basketball_coaches.jsonl`:
{"item": { "university": "<university>", "coach_name": "<coach_name>", "role": "<role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

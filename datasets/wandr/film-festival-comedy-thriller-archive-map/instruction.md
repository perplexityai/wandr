You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `film_festival_comedy_thriller_archive_map`
  - `film_festival_comedy_thriller_archive_map.genre_evidence`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `film_festival_comedy_thriller_archive_map`

For 80+ feature films, identify 2+ distinct public film festivals per film where the film had a festival appearance during 1990-2010. For each film-festival pair, identify 1+ public festival appearance and supply a festival-authoritative placement source for that appearance (i.e. 1+ URL per film appearance).

The focus is the placement record itself: a page that shows the film in the festival's own program, archive, award, selection, lineup, retrospective, or comparable public festival context. The festival spread is part of the task: alternate names, translated names, official archive labels, annual editions, and sections or awards of the same festival do not count as distinct festivals for a film.

The film ought to be a real released feature-length work. Each festival should be a real public film festival or independently curated public film-festival sidebar/strand, and the distinct festival keys for a film should represent distinct recurring festival organizations rather than aliases, annual editions, sections, awards, or archive labels for one festival. The festival appearance should be tied to a public festival edition during 1990-2010; ordinary theatrical releases, streaming listings, non-festival awards, trailers, shorts, TV episodes, and series do not count.

Requirements:
- The page must clearly identify the named film, with enough title, director, release-year, country, cast, or synopsis context to disambiguate remakes, same-title films, and alternate titles.
- The page should communicate festival-authoritative provenance, such as a festival-owned site, official archive, official program/yearbook/catalogue, or comparably direct festival-controlled publication.
- The page must tie the film to the named festival, edition year, and a section, program, award, selection, lineup, retrospective, or comparable placement context.

Write one JSON object per line to `results_film_festival_comedy_thriller_archive_map.jsonl`:
{"item": { "film_title": "<film_title>", "release_year": "<release_year>", "director": "<director>", "festival": "<festival>", "festival_country_or_city": "<festival_country_or_city>", "edition_year": "<edition_year>", "section_or_award": "<section_or_award>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `film_festival_comedy_thriller_archive_map.genre_evidence`

Cross-tasknode identifier discipline: this task is for the same {= film =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= film =}+ comedy or thriller feature films, supply 2+ distinct public film-reference URLs per film that classify the film as comedy or thriller.

The source should be a film-reference or classification surface for the film itself, not a festival-program page being used as a genre proxy.

The film ought to be a real released feature-length work. Mixed, compound, or hyphenated genre labels count when comedy or thriller is explicit; curatorial labels, festival section names, marketing taglines, and plot descriptions without an explicit genre classification do not.

Requirements:
- The page must clearly identify the named film, with enough title, director, release-year, country, cast, or synopsis context to disambiguate remakes, same-title films, and alternate titles.
- The page should communicate a film-reference or classification role for the named film, such as a dedicated film catalog, database title page, institutional film record, encyclopedic film entry, review-source title page with genre metadata, or comparable page where film-level genres are presented.
- The page must explicitly classify the film as comedy or thriller, including compound labels such as black comedy, comedy-drama, crime thriller, psychological thriller, or horror-thriller when comedy or thriller is named.

Write one JSON object per line to `results_film_festival_comedy_thriller_archive_map.genre_evidence.jsonl`:
{"item": { "film_title": "<film_title>", "release_year": "<release_year>", "director": "<director>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

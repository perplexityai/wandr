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

## `australian_universities`

For each of the 43 universities in Australia's 2024 higher-education market baseline below, provide a public operating-status panel by covering the 5 below-specified information panes and supplying a source (i.e. 1+ URL) per each pane.

Universities:
- **Australian Catholic University**
- **Australian National University**
- **Avondale University**
- **Bond University**
- **Carnegie Mellon University Australia**
- **Charles Darwin University**
- **Charles Sturt University**
- **CQUniversity Australia**
- **Curtin University**
- **Deakin University**
- **Edith Cowan University**
- **Federation University Australia**
- **Flinders University**
- **Griffith University**
- **James Cook University**
- **La Trobe University**
- **Macquarie University**
- **Monash University**
- **Murdoch University**
- **Queensland University of Technology**
- **RMIT University**
- **Southern Cross University**
- **Swinburne University of Technology**
- **Torrens University Australia**
- **University of Adelaide**
- **University of Canberra**
- **University of Divinity**
- **University of Melbourne**
- **University of New England**
- **University of New South Wales**
- **University of Newcastle**
- **University of Notre Dame Australia**
- **University of Queensland**
- **University of South Australia**
- **University of Southern Queensland**
- **University of Sydney**
- **University of Tasmania**
- **University of Technology Sydney**
- **University of the Sunshine Coast**
- **University of Western Australia**
- **University of Wollongong**
- **Victoria University**
- **Western Sydney University**

Information panes:
- `registration`: the provider's recognition by the national tertiary regulator
- `sector`: kind / class of higher-education provider
- `site`: physical operating presence of the provider in Australia
- `location`: official seat / base of the operating organization
- `governance`: people / bodies running the operating organization

Target pages differ by information pane: for `registration`, the national tertiary regulator's register entry; for `sector`, sources that establish, recognize, or characterize the provider's sectoral status — for instance, an establishing / enabling Act, a recognized sector body's publication (Universities Australia, IHEA, the federal department's higher-education pages, and so on), or the provider's own corporate-structure / quality-assurance page; for `site`, sources mapping the provider's physical footprint — typically the provider's own campus / locations directory or annual-report site enumeration; for `location`, sources pinning the administrative seat — for instance, the provider's own corporate-affairs / governance page or annual-report front matter; for `governance`, sources naming the people or bodies in charge — for instance, the provider's own leadership / governance / vice-chancellor page or annual-report leadership section. All as opposed to generic SEO directories, scraped lead pages, social posts, student forums, multi-university bulk-list pages, national marketing pages, unsourced encyclopedic summaries, and the like.

Requirements:
- The page must clearly identify the named university.
- The page should expose tangible evidence / factoids clearly scoped to the information pane intended: for `registration`, concrete legal-recognition anchors (for instance, provider ID, registration period, CRICOS identity, registered or withdrawn standing, regulator's provider category); for `sector`, status disambiguators (such as public / private / independent / Table-A/B / statutory / overseas-university status); for `site`, named physical sites (campuses, study centres, college sites, etc.); for `location`, official-seat data (head office state or territory, registered Australian address, primary operating jurisdiction, and the like); for `governance`, named office-holders or governing bodies (for instance, vice-chancellor / president / chancellor roles, governing council, senior executive leadership).

Write one JSON object per line to `results_australian_universities.jsonl`:
{"item": { "university": "<university>", "information_pane": "<information_pane>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

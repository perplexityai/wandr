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

## `eu_emissions_cross_register`

For each of the 3 citable country splits listed below, supply official cross-register industrial-emissions release evidence for 5+ facilities and 2+ 2022 pollutant-release events per facility. For each release event, cover every source-layer record listed below, with 1+ URL per source-layer record.

The work is neutral source provenance: a submitted release event is the same facility, pollutant, release medium, and reporting year 2022 as seen in an official EU row source and official national-register facility/release sources.

Reporting-year and EU-vintage pin: reporting year 2022; EEA tabular vintage eea_t_ied-eprtr_p_2007-2022_v11_r00, version 11.0 July 2024, status as of 2024-07-10.

Citable country split:
- `DE` - Germany; national evidence from official thru.de / UBA API JSON row responses.
- `FR` - France; national evidence from paired official Georisques IREP JSON detail and emission API responses.
- `SE` - Sweden; national evidence from official Naturvardsverket server-rendered facility pages.

Source-layer records:
- `eu_layer` - official EEA Discodata SQL JSON over [IED].[latest].[PollutantRelease] joined to [IED].[latest].[ProductionFacilityReport] and [IED].[latest].[ProductionFacility]
- `national_register_facility` - official national register API/JSON/HTML facility identity evidence for the submitted country and facility; for FR this is the Georisques IREP etablissement detail API
- `national_register_release` - official national register API/JSON/HTML release-row evidence for the submitted country, facility identifier, pollutant, medium, year, quantity, and unit; for FR this is the Georisques IREP etablissement emission API. Binary ZIP or download-only archive URLs are not leaf evidence unless the fetched page itself exposes the row text

The `eu_layer` URL must be an official EEA Discodata SQL JSON query that exposes the release row value from `[IED].[latest].[PollutantRelease]` joined to the facility-report and facility tables. The `national_register_facility` URL must identify the national-register facility/site/reporting unit, with country, location, or source-visible identifier in fetch-visible text. The `national_register_release` URL must expose the national-register release row as fetch-visible text: 2022, pollutant, direct medium, quantity, unit, and the national facility identifier or URL path that pairs with the `national_register_facility` record. For FR, use official Georisques IREP JSON detail evidence for `national_register_facility` and official Georisques IREP JSON emission evidence for `national_register_release`; do not treat the emission endpoint alone as facility-name evidence. Generic dataset landing pages, metadata pages, Tableau/JS shells, article summaries, binary ZIP/download-only archives, and explanatory pages do not count as release-event evidence when they do not expose the required facility or release row text for the submitted source-layer record.

Use only facility/site/industrial-complex/reporting-unit release rows. Do not use national totals, sector totals, maps without row values, company sustainability pages, news/NGO summaries, ranking pages, health-risk/cost/damage material, compliance commentary, enforcement pages, investment/policy advice, or dashboard/alert product framing.

Blank cells, missing pollutant rows, absent quantities, and absent source rows are not zero-emission claims. A numeric zero, below-threshold state, confidential/withheld state, non-reportable state, or absent-source condition counts only when the cited source explicitly states that bounded condition for the submitted facility, pollutant, medium, and year.

Requirements:
- For `eu_layer`, the cited source must expose the joined EU row: facility identity, reporting year 2022, pollutant, direct medium, quantity, unit or kg context, and EEA/IED source context.
- For `national_register_facility`, the cited source must identify the submitted facility together with a country, location discriminator, or source-visible identifier sufficient to distinguish the facility/site/reporting unit.
- For `national_register_release`, the cited source must expose the source-stated year 2022, pollutant name/code or unambiguous alias, direct release medium, quantity, and unit, with a national facility identifier or URL path that pairs it to the corresponding facility-identity record.
- The cited source or URL context must identify the relevant official source layer and row/vintage context for the submitted source.

Write one JSON object per line to `results_eu_emissions_cross_register.jsonl`:
{"item": { "country": "<country>", "facility": "<facility>", "pollutant": "<pollutant>", "medium": "<medium>", "year": "<year>", "source_layer": "<source_layer>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

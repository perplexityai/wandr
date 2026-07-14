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

## `eu_ets_installation_emissions`

For each of the 5 EU ETS participating countries listed below, name at least 25+ individual stationary-installation entity-year records for reporting year 2024, and supply 1+ public source URL for each record showing the source-stated verified-emissions figure.

The task is data provenance for regulated EU ETS records: installation/operator identity, country, reporting year, verified-emissions value, activity/scope cue, and source/report vintage stay tied to the cited source. Compliance verdicts, market/trading analysis, operator rankings, legal conclusions, procurement advice, offset strategy, and dashboard alerts are out of scope.

Target countries:
- **Germany**
- **Ireland**
- **Netherlands**
- **Sweden**
- **Estonia**

The country is the participating country, the entity is the source-stated installation/operator/entity name, the source-row identifier is the row's public installation, permit, account, registry, or other source-stated identifier when visible, such as `INSTALLATION_IDENTIFIER`, `PERMIT_IDENTIFIER`, `IDENTIFIER_IN_REG`, or an equivalent source row code, and `not_public` applies only when the cited row exposes no public row identifier. Emissions, activity, allocation, surrendered units, status, and source vintage are evidence fields rather than entity identity.

Eligible source shapes include official European Commission / DG CLIMA / Union Registry reports or spreadsheet downloads, national administrator records, and official-derived per-installation pages that visibly tie the data to EUTL or Union Registry provenance. EEA aggregate viewer/Datahub pages can explain context or source vintage, but cannot by themselves satisfy an individual installation/operator row. Maritime-operator and aircraft-operator rows are out of scope for this first stationary-installation package.

When using a spreadsheet/workbook download, the row-local workbook text must be visible in the rendered source: workbook filename or sheet/vintage cue, extraction or publication context, header cells that identify the reporting-year verified-emissions column, the exact entity row with source row identifier cells and the `VERIFIED_EMISSIONS_2024` value, and the activity/scope code or label cell. A synthesized or normalized table row is insufficient unless those exact cells are visible in the cited source text.

Requirements:
- The source must state or tabulate the submitted individual installation/operator entity, tie it to the submitted country through a country, registry code, permit/account identifier, address, or equivalent row-level cue, and support the submitted row identifier when one is public.
- The source must tie that same entity row to reporting year 2024.
- The source must state a concrete verified-emissions figure for that entity-year. Blank, null, `-1`, `Excluded`, or no-emissions-verified states are not positive rows.
- The source must state a stationary-installation-compatible EU ETS activity or scope cue for the row, such as a main activity type code/label, installation/permit/account wording, or explicit non-aircraft/non-maritime operator flags.
- The source must state the evidence source/report vintage or release/extraction context, such as Date of Extraction, report title/year, filename, publication date, updated-on field, or comparable source-stated metadata.

Each URL evidence leaf stands on its own for the submitted entity-year.

Write one JSON object per line to `results_eu_ets_installation_emissions.jsonl`:
{"item": { "country": "<country>", "entity": "<entity>", "source_row_identifier": "<source_row_identifier>", "reporting_year": "<reporting_year>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

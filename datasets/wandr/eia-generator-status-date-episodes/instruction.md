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

## `eia_generator_status_date_episodes`

For all 5 lifecycle episode families, use 3+ independent public source-family buckets per episode family. Under each source-family bucket, supply 6+ U.S. generator or unit status-date episodes tied to EIA generator identity, and for each episode supply each of the 2 evidence sides with 1+ URL per side.

A status-date episode is a source-grounded lifecycle claim about a specific generator/unit, or a clearly bounded plant-level episode when public evidence does not separate generator IDs. The episode identity should preserve EIA plant code, generator ID or documented generator-ID ambiguity, and a short episode name. This is a descriptive provenance atlas, not a current inventory table or a capacity forecast.

The episode families are:
- `operating_start`: operating start, commercial operation, or first-generator service episodes.
- `planned_in_service_shift`: planned online/in-service date changes for proposed or under-construction generators.
- `retirement_or_standby_shift`: retired, planned-retirement, mothball, standby, or delayed-retirement episodes.
- `cancellation_or_indefinite_postponement`: canceled, withdrawn, shelved, or indefinitely postponed generator/unit projects.
- `reactivation_or_conversion`: reactivation, repowering, fuel-conversion, ownership/unit reconfiguration, or comparable status reclassification episodes.

The independent source-family bucket records what kind of public non-EIA source is paired with the episode. The paired `eia_baseline` row repeats this bucket only to keep the two sides in the same hierarchy branch; the EIA row is still judged as EIA evidence, not as an independent source.
- `federal_regulatory`: federal regulatory or reliability sources such as FERC, NRC, DOE, NERC, or federal docket materials.
- `state_regulatory_or_planning`: state PUC/PSC, siting-board, state energy-office, integrated-resource-plan, or local-government materials.
- `grid_or_market_operator`: ISO/RTO, balancing-authority, interconnection-queue, market-monitor, or transmission-planning materials.
- `owner_operator_or_sec`: owner/operator, developer, utility, investor, SEC, lender, or project-company disclosures.
- `local_or_trade_reporting`: substantive local news, trade press, industry reporting, or analyst/publication coverage that is not EIA-derived.

The evidence sides are:
- `eia_baseline`: the official EIA-860M or EIA-860 file row, with a direct workbook/ZIP URL and structured row citation, that states the generator/unit status or date in a named release vintage.
- `independent_signal`: a non-EIA-derived public source that speaks to the same generator/unit or bounded plant-level status/date episode.

Comparison notes are useful atlas metadata, but they are not a substitute for the side-specific source evidence. When you include a comparison note, use one of these labels:
- `confirmed`: the independent source supports the same status/date claim without materially changing it.
- `refined`: the independent source narrows, updates, or explains the EIA claim without making it wrong.
- `contradicted`: the independent source conflicts with the EIA status/date claim for the same episode.
- `unresolved`: the sides are relevant but do not settle the comparison.
- `identity_ambiguous`: the comparison turns on unresolved generator/unit versus plant-level identity.

The family/source buckets are binding, not a preference list. The scored unit below `independent_source_family` is source-family-bucketed status episode evidence: within the same `episode_family` + `independent_source_family` bucket, the required `status_episode` records must be distinct lifecycle status/date episodes. The same underlying episode may appear in another independent source-family bucket only when that branch is backed by a truthful independent source from that other bucket and its paired EIA row. A single catalog, workbook, queue, docket index, or recurring source family can fill only the source-family bucket it actually belongs to; do not relabel one NRC/FERC/ISO/company/trade catalog as several source families. Within a given episode family, the required independent source-family buckets should come from meaningfully different publisher families rather than one repeated catalog source.

Requirements:
- The submitted URL/source should communicate the evidence-side role. For `eia_baseline`, cite a direct official EIA-860M monthly workbook URL, EIA-860 annual or early-release ZIP/workbook URL, or an official EIA field-semantics document needed to interpret the cited status/date field; do not use only a generic EIA landing page when the claim depends on a hidden workbook row. For `independent_signal`, it should be a public non-EIA-derived source such as DOE/FERC records, state PUC filings, ISO/RTO materials, operator/company disclosures, SEC filings, or substantive trade press; EIA API-only current inventory, PUDL/crosswalk-only entries, EPA derivative maps, and EIA Today in Energy discovery articles do not by themselves count as independent signals.
- The source-supported status/date claim must fit the submitted `episode_family`. For `independent_signal`, the source must also belong to the submitted `independent_source_family`; for `eia_baseline`, the submitted `independent_source_family` is pairing metadata for the episode's independent side.
- The source evidence must tie the status/date claim to the claimed EIA identity: plant code and generator ID when the source supplies them, or a source-stated plant/unit-group event that covers the submitted EIA generator set. For `eia_baseline`, the structured official row-citation fields can supply this identity tie. When the source is coarser than generator level and does not cleanly identify the submitted generator IDs, the episode must honestly preserve that generator-ID boundary instead of over-claiming an exact unit match.
- The source evidence must support a lifecycle status/date claim for the episode, such as operating start, operating/standby status on a stated EIA vintage, planned in-service date, planned retirement date, retired status, cancellation/postponement, delayed retirement, or comparable source-stated status/date shift.
- The source and submitted evidence must carry enough provenance for the claimed side. EIA-side evidence should preserve release month or annual vintage, data month or annual year, official direct workbook/ZIP URL, workbook or ZIP file name, tab or internal file, row number or row-key identifier, plant-code field/value, generator-ID field/value, status/date field names, status/date field values, and a compact row excerpt or value bundle. If the official EIA URL is a workbook or ZIP rather than a rendered web page, put those row-citation details in structured `answer` fields such as `eia_official_url`, `eia_workbook_or_zip_file`, `eia_tab_or_internal_file`, `eia_row_identifier`, `eia_plant_code_field`, `eia_generator_id_field`, `eia_status_field`, `eia_date_field`, and `eia_row_excerpt`; those fields are the judgeable official row-citation convention for workbook/ZIP records. An EIA landing page that only links to a workbook is not enough unless the submitted URL or structured citation names the exact direct official workbook/ZIP and row-level fields. Independent-side evidence should preserve source date, source family, source-stated status/date language, and how it relates to the EIA generator/unit identity.

Write one JSON object per line to `results_eia_generator_status_date_episodes.jsonl`:
{"item": { "episode_family": "<episode_family>", "independent_source_family": "<independent_source_family>", "plant_code": "<plant_code>", "generator_id": "<generator_id>", "episode_name": "<episode_name>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

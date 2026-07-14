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

## `eu_ecall_psap_infrastructure`

As of May 7, 2026, every EU member state shares the 112 and eCall legal baseline, but the public evidence for PSAP routing, NG112 migration, operator obligations, and language coverage remains scattered across national PSAP operators, telecom regulators, emergency-service authorities, and country-specific EENA reporting.

For each of the 27 EU member states listed below and each of the 5 eCall / PSAP infrastructure axes, name the country's specific operative finding for that axis (1+ per cell), supplying a source (1+ URL per finding) on an axis-appropriate authoritative page that substantiates the country-specific finding and its current or as-of status.

For each finding, also report the source-authority class, the currentness or as-of period supported by the page, and any technical standard, routing topology, network obligation, or language-coverage detail the page itself gives.

The EU member states in scope are:

- **Austria** (also written as: Österreich, Republik Österreich)
- **Belgium** (also written as: België, Belgique, Belgien, Royaume de Belgique, Koninkrijk België)
- **Bulgaria** (also written as: България, Република България, Republic of Bulgaria)
- **Croatia** (also written as: Hrvatska, Republika Hrvatska, Republic of Croatia)
- **Cyprus** (also written as: Κύπρος, Kıbrıs, Republic of Cyprus, Kypros)
- **Czechia** (also written as: Czech Republic, Česko, Česká republika)
- **Denmark** (also written as: Danmark, Kongeriget Danmark, Kingdom of Denmark)
- **Estonia** (also written as: Eesti, Eesti Vabariik, Republic of Estonia)
- **Finland** (also written as: Suomi, Suomen tasavalta, Republic of Finland)
- **France** (also written as: République française, French Republic)
- **Germany** (also written as: Deutschland, Bundesrepublik Deutschland, Federal Republic of Germany)
- **Greece** (also written as: Ελλάδα, Ελληνική Δημοκρατία, Hellenic Republic, Hellas)
- **Hungary** (also written as: Magyarország)
- **Ireland** (also written as: Éire, Republic of Ireland)
- **Italy** (also written as: Italia, Repubblica Italiana, Italian Republic)
- **Latvia** (also written as: Latvija, Latvijas Republika, Republic of Latvia)
- **Lithuania** (also written as: Lietuva, Lietuvos Respublika, Republic of Lithuania)
- **Luxembourg** (also written as: Lëtzebuerg, Luxemburg, Grand-Duché de Luxembourg, Grand Duchy of Luxembourg)
- **Malta** (also written as: Repubblika ta' Malta, Republic of Malta)
- **Netherlands** (also written as: Nederland, Koninkrijk der Nederlanden, Kingdom of the Netherlands, Holland)
- **Poland** (also written as: Polska, Rzeczpospolita Polska, Republic of Poland)
- **Portugal** (also written as: República Portuguesa, Portuguese Republic)
- **Romania** (also written as: România)
- **Slovakia** (also written as: Slovensko, Slovenská republika, Slovak Republic)
- **Slovenia** (also written as: Slovenija, Republika Slovenija, Republic of Slovenia)
- **Spain** (also written as: España, Reino de España, Kingdom of Spain)
- **Sweden** (also written as: Sverige, Konungariket Sverige, Kingdom of Sweden)

The European jurisdictions below are outside this task's country universe:

- **United Kingdom** (also written as: UK, Britain, Great Britain, England, Scotland, Wales, Northern Ireland, GB)
- **Norway** (also written as: Norge, Noreg, Kongeriket Norge, Kingdom of Norway)
- **Switzerland** (also written as: Schweiz, Suisse, Svizzera, Svizra, Schweizerische Eidgenossenschaft, Confédération suisse, Confederazione Svizzera)
- **Iceland** (also written as: Ísland, Lýðveldið Ísland, Republic of Iceland)
- **Liechtenstein** (also written as: Fürstentum Liechtenstein, Principality of Liechtenstein)
- **Moldova** (also written as: Republic of Moldova)

The infrastructure axes are:

- **ecall_deployment** — country-specific reception and handling of 112 eCall by eCall-capable PSAPs or the national 112 service, including MSD-plus-voice handling, deployment date, geographic coverage, or service-routing statement
- **ng112_status** — country-specific status of NG112 / IP-based PSAP migration, including implementation ongoing, planned, working-group, no-official-plan, or equivalent country status
- **psap_topology** — country-specific PSAP routing architecture: first-level vs service-specific transfer, centralised vs regional centres, number and location of centres, or dispatch handoff
- **mno_network_obligation** — country-specific MNO / electronic-communications-provider emergency-call obligation, 112 routing obligation, caller-location transmission, VoLTE / 2G / 3G continuity action, or eCall network-readiness obligation
- **language_coverage** — country-specific 112 / PSAP call-taking language coverage, interpreting service, multilingual support, or clear statement of language handling for emergency callers

Per-axis authoritative-source scope:

- **ecall_deployment** — national or officially delegated regional PSAP / 112 operator, fire-rescue or emergency-service authority, national transport / telecom authority, or a country-specific eCall deployment page
- **ng112_status** — national PSAP / regulator NG112 page, EENA country-specific 112 reporting, or a country-specific PSAP-operator presentation or report
- **psap_topology** — national or officially delegated regional PSAP / 112 operator, emergency-service authority, interior / civil-protection authority, or telecom regulator page describing routing or PSAP catchment architecture
- **mno_network_obligation** — national telecom regulator, official legal text, or MNO-controlled page for that operator's own emergency-call / eCall network-status finding
- **language_coverage** — national or officially delegated regional PSAP / 112 service, emergency-service authority, or country-specific PSAP reporting page describing call-taking or interpreting language support

Requirements:
- The page must pin the row's specific finding for the row country and infrastructure axis, not only generic 112 availability, generic EU eCall legislation, or a different country's emergency-call arrangement.
- The page must support the axis-specific infrastructure substance for the row: eCall PSAP handling, NG112 status, PSAP topology, MNO / network obligation, or language coverage, depending on the row's axis.
- The page must communicate (possibly via URL among other things) an authoritative source class for that axis.
- The page must provide an as-of signal, publication date, active-service framing, current legal force, or on-page status sufficient for the row's currentness claim.

Write one JSON object per line to `results_eu_ecall_psap_infrastructure.jsonl`:
{"item": { "country": "<country>", "infrastructure_axis": "<infrastructure_axis>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

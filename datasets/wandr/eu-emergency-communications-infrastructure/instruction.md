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

## `eu_emergency_communications_infrastructure`

In the EU 27, each member state implements 112 emergency-communications infrastructure under shared standards but with substantively different per-country choices on caller-location, public warning, accessibility channels, and PSAP architecture.

For each of the 27 EU member states (listed below) and the 4 emergency-communications infrastructure axes (listed below), name the country's specific operative finding for that (country, axis) cell (1+ per cell that admits one), supplying a source (1+ URL per finding) on that country's own national regulator / PSAP-operator / civil-protection publication channel for that axis evidencing the finding as the country's specific operative state on that axis. A finding is a specific deployment-fact with a technology / coverage qualifier, a named program / instrument with regulator / operator anchor, a substantive deployment-fact text on a country that has not yet branded its own program by name, etc. — not every (country, axis) cell will admit one.

The EU member states in scope are:

- **Austria** (also written as: Österreich, Republik Österreich)
- **Belgium** (also written as: België, Belgique, Belgien, Royaume de Belgique, Koninkrijk België)
- **Bulgaria** (also written as: България, Република България, Republic of Bulgaria)
- **Croatia** (also written as: Hrvatska, Republika Hrvatska, Republic of Croatia)
- **Cyprus** (also written as: Κύπρος, Kıbrıs, Κυπριακή Δημοκρατία, Kıbrıs Cumhuriyeti, Republic of Cyprus, Kypros)
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

The four infrastructure axes are housed in different artifact families per country; the row's `axis` selects which of the four:

- **aml_caller_location** — the country's handset-derived caller-location payload — generated by the smartphone OS from on-device positioning signals and delivered to the PSAP at the moment of a 112 emergency call.
- **public_warning_system** — the country's mass-population alerting infrastructure that delivers public-warning messages directly to mobile phones in an affected geographic area.
- **disability_access** — the country's text-based or sign-language relay channels that route into 112 itself, providing equivalent-access pathways for deaf, hard-of-hearing, and speech-impaired callers to reach 112 emergency services.
- **ng112_migration** — the country's PSAP-architecture transition from legacy E112 call-handling to a Next-Generation 112 (NG112) IP-based architecture supporting multimedia emergency communications.

Per-axis authoritative-publication-channel scope — the row country's own institutional publication channel under its own authority for the row's axis:

- **aml_caller_location** — the row country's national telecommunications regulator's AML / handset-derived caller-location publication, the country's PSAP-authority publication, the national civil-protection authority's caller-location publication where it is the operative 112-services publisher, or the country's central-government / interior-ministry national 112 portal where it substantively publishes the country's AML deployment
- **public_warning_system** — the row country's civil-protection authority / interior-ministry / PSAP-operator national PWS announcement page, or the country's national telecommunications regulator where it substantively publishes the country's Article 110 EECC transposition / PWS deployment
- **disability_access** — the row country's national or regional PSAP-operator / civil-protection / PSAP-equivalent national-authority publication channel that publishes the country's 112 equivalent-access service
- **ng112_migration** — the row country's national or regional PSAP-operator / Special Telecommunications Service / call-handling-system rollout publication channel for the row's axis, or the country's national telecommunications regulator where it substantively publishes the country's national NG112 plan / regulatory framework

Requirements:
- The page must pin the row's specific operative finding for the (country, axis) cell sufficient that a reader could uniquely locate the finding within the country's emergency-communications landscape on the row's axis.
- The page's identified finding must be of the row's claimed axis-character per the axis scope above.
- The page must substantively bind the operative finding to the row country — a national authority's surface communicating its country-of-origin, the row country named in the finding text, a country-specific regulator / agency / operator named as the finding's actor, etc.
- The page must communicate (possibly via URL among other things) that it is on the row country's own national regulator / PSAP-operator / civil-protection publication channel for the row's axis.
- The page must present the operative finding as currently in force.

Write one JSON object per line to `results_eu_emergency_communications_infrastructure.jsonl`:
{"item": { "country": "<country>", "axis": "<axis>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

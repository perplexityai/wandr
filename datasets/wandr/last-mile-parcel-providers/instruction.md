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

## `last_mile_parcel_providers`

For each of the 42 in-scope countries (EU-27 + United Kingdom + EFTA (Iceland, Liechtenstein, Norway, Switzerland) + Western Balkans + Ukraine + Moldova + Türkiye + Georgia), name 3+ last-mile postal or parcel delivery providers per country. For each provider, supply all 3 evidence types listed below — with a source (1+ URL per (country, provider, evidence-type)).

The in-scope countries are:
- **Albania** (also written as: Shqipëria, Republic of Albania)
- **Austria** (also written as: Österreich, Republic of Austria)
- **Belgium** (also written as: Belgique, België, Kingdom of Belgium)
- **Bosnia and Herzegovina** (also written as: Bosnia & Herzegovina, BiH)
- **Bulgaria** (also written as: Republic of Bulgaria)
- **Croatia** (also written as: Hrvatska, Republic of Croatia)
- **Cyprus** (also written as: Republic of Cyprus)
- **Czechia** (also written as: Czech Republic, Česko)
- **Denmark** (also written as: Kingdom of Denmark)
- **Estonia** (also written as: Eesti, Republic of Estonia)
- **Finland** (also written as: Suomi, Republic of Finland)
- **France** (also written as: French Republic, République française)
- **Georgia** (also written as: Sakartvelo)
- **Germany** (also written as: Deutschland, Federal Republic of Germany)
- **Greece** (also written as: Hellenic Republic)
- **Hungary** (also written as: Magyarország)
- **Iceland** (also written as: Ísland, Republic of Iceland)
- **Ireland** (also written as: Éire, Republic of Ireland)
- **Italy** (also written as: Italia, Italian Republic)
- **Kosovo** (also written as: Republic of Kosovo)
- **Latvia** (also written as: Latvija, Republic of Latvia)
- **Liechtenstein** (also written as: Principality of Liechtenstein)
- **Lithuania** (also written as: Lietuva, Republic of Lithuania)
- **Luxembourg** (also written as: Grand Duchy of Luxembourg)
- **Malta** (also written as: Republic of Malta)
- **Moldova** (also written as: Republic of Moldova, Rep. of Moldova)
- **Montenegro** (also written as: Crna Gora)
- **Netherlands** (also written as: Holland, Netherlands (Kingdom of the), Kingdom of the Netherlands)
- **North Macedonia** (also written as: Macedonia, Republic of North Macedonia)
- **Norway** (also written as: Norge, Kingdom of Norway)
- **Poland** (also written as: Polska, Republic of Poland)
- **Portugal** (also written as: Portuguese Republic)
- **Romania** (also written as: România)
- **Serbia** (also written as: Republic of Serbia)
- **Slovakia** (also written as: Slovak Republic)
- **Slovenia** (also written as: Slovenija)
- **Spain** (also written as: España, Kingdom of Spain)
- **Sweden** (also written as: Sverige, Kingdom of Sweden)
- **Switzerland** (also written as: Swiss Confederation, Schweiz, Suisse, Svizzera)
- **Türkiye** (also written as: Turkey, Turkiye, Republic of Türkiye)
- **Ukraine** (also written as: Україна)
- **United Kingdom** (also written as: UK, Great Britain, United Kingdom of Great Britain and Northern Ireland)

Each named provider must be an actual operating entity that accepts, transports, or delivers letters or parcels — not a service category, page heading, or descriptive label.

The evidence types are:
- **operator_status** — operator type and country-grounded status: designated postal operator, licensed / registered postal operator, domestic parcel carrier, express carrier, parcel-locker or PUDO network, or equivalent last-mile delivery operator
- **service_area** — service area or final-mile network in the row-country: nationwide coverage, named domestic regions / cities, postal outlets, parcel lockers, PUDO points, courier pickup / delivery routes, or equivalent domestic coverage evidence
- **tracking_integration_service** — customer- or merchant-facing service capability: parcel tracking, delivery notifications, API / e-commerce integration, label creation, return service, named delivery class, locker handoff, or equivalent operational service-class evidence

Use source pages whose authorial standing fits the evidence type: national regulator or licensee registers, UPU country profiles, ministry / universal-service pages, provider-controlled service pages, provider developer portals, or comparable official surfaces. Generic courier directories, shipping-rate comparison pages, and third-party tracking aggregators can help discovery, but they do not count as evidence sources for this task.

Requirements:
- The page must communicate (possibly via URL among other things) a source class appropriate to the claimed evidence type.
- The page must tie the named provider to postal, parcel, express, locker, PUDO, or courier delivery operations in the named country.
- The page must substantively support the evidence-type fact: operator type for **operator_status**, service area or final-mile network for **service_area**, or a concrete tracking / integration / service-class capability for **tracking_integration_service**.

Write one JSON object per line to `results_last_mile_parcel_providers.jsonl`:
{"item": { "country": "<country>", "provider": "<provider>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

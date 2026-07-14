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

## `chennai_trucking`

For each of the 3 geography buckets, cover 80+ distinct road-freight or goods-transport operators with a Chennai or Tamil Nadu link, and supply evidence for each of the 2 evidence types and at least 1+ URL per type. Medavakkam is the seed locality, not the whole universe; the broader Chennai and Tamil Nadu freight ecosystem should provide the long tail.

The geography buckets are:
- `south_chennai_seed`: Medavakkam, Madipakkam, Puzhuthivakkam, Pallikaranai, Keelkattalai, Sholinganallur, Perungudi, OMR, Guindy / Velachery, or adjacent South Chennai service surfaces.
- `chennai_metro`: Chennai metro, port, or industrial freight surfaces outside the seed slice, including Ambattur, Manali, Red Hills, Parrys / Mannady, Ennore, Kattupalli, Sriperumbudur, Oragadam, or similar Chennai-linked zones.
- `tamil_nadu_freight_nodes`: Tamil Nadu road-freight nodes beyond Chennai, such as Namakkal, Sankagiri, Tiruchengode, Salem, Coimbatore, Hosur, Tiruppur, Tuticorin / Thoothukudi, or statewide Tamil Nadu operator surfaces.

The evidence types are:
- `capability`: a public source showing concrete goods-transport capability: lorry, truck, mini truck, load van, Tata Ace, parcel cargo, FTL, LTL / PTL, container, trailer, tanker, reefer, ODC, route / corridor, pickup zone, fleet, branch network, facility, rate table, or comparable service detail.
- `identity_legitimacy`: a public source corroborating the operator's identity, locality, legal / trade-name bridge, registration, association, IBA / industry presence, registry profile, durable public address trail, or comparable legitimacy signal.

For downstream reading, include the canonical operator name, legal name or trade-name bridge when public, geography bucket, address / branch / route / service-area signal, road-freight service signal, vehicle or load class when public, identity or legitimacy signal, source family, registration or public ID when relevant, checked date, confidence, and source notes. Use 2026-06-29 as the checked date unless the source was checked later.

Useful service signals include:
- `lorry / truck transport`
- `mini truck / Tata Ace / load van`
- `parcel cargo or goods transport`
- `full truck load / FTL`
- `less-than-truckload or part load / LTL / PTL`
- `container transport`
- `trailer, low-bed, ODC, project cargo, or heavy cargo`
- `tanker, reefer, or specialized freight`
- `pickup / drop zone or route corridor`
- `warehouse, branch network, depot, or fleet evidence tied to road freight`

Useful identity or legitimacy signals include:
- `CIN or MCA / company-registry profile`
- `GSTIN or public tax-registration clue`
- `Udyam / MSME profile`
- `registered office, branch, depot, or stable public address trail`
- `association, IBA, industry, or trade-publication listing`
- `legal name / DBA / trade-name bridge`
- `official company site with durable identity details`
- `credible marketplace, platform, or B2B profile with entity-specific identity facts`

Source family should be factual rather than promotional. Useful public sources include:
- `operator-owned site or official profile`
- `registry / legal / MSME / GST / MCA-style profile`
- `association, IBA, or industry source`
- `trade press or institutional source`
- `platform or marketplace service page`
- `B2B provider profile with entity-specific facts`
- `local directory or discovery page with concrete row-specific details`
- `official transport / permit context when it directly supports the record`

Directory pages, search result pages, quote funnels, review snippets, generic "transporters near me" pages, and SEO lead-generation pages can be useful discovery surfaces, but they do not carry the final bar by themselves. Pure passenger transport, courier-only services with no goods-fleet evidence, generic logistics marketing, freight brokers with no visible operating road-freight footprint, and relocation-only pages with no truck / lorry / load-vehicle / FTL / LTL / goods-transport capability are out of scope.

Requirements:
- The page must identify the claimed operator, or bridge the submitted trade name to a legal / DBA name, with enough public context to distinguish it from unrelated same-name entities.
- The page must support the claimed `geography_bucket` through an address, operating location, branch, depot, route, pickup zone, service area, local profile, or other Chennai / Tamil Nadu operational link.
- The page must fit the claimed `evidence_type`: `capability` evidence should show concrete road-freight or goods-transport capability, while `identity_legitimacy` evidence should show a public identity, locality, legal, registration, association, industry, registry, durable address, or comparable legitimacy signal.
- The page must support concrete operator substance at the claimed evidence type. For `capability`, it should show real goods-transport service, vehicle / load class, route / corridor, fleet, facility, rate, or service-mode evidence. For `identity_legitimacy`, it should corroborate the same operator's identity or legitimacy beyond a generic category label or bare directory row.

Write one JSON object per line to `results_chennai_trucking.jsonl`:
{"item": { "geography_bucket": "<geography_bucket>", "operator": "<operator>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

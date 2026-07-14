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

## `acma_rrl_licensee_provenance`

For each of the 6 ACMA radiocommunications service buckets below, for 12+ ABN-backed organisational licensees, supply 1+ source URL for each of the 3 provenance facets.

The aim is organisational provenance across independent public surfaces, not a table of radio sites or technical operating details.

The service buckets are:
- `fixed_public_network`: ACMA Fixed licences tied to public-network or carrier-style communications services.
- `spectrum_public_network`: ACMA Spectrum licences tied to public-network, mobile, or carrier-style communications services.
- `broadcasting`: ACMA Broadcasting licences for broadcasters or broadcasting bodies.
- `aeronautical_services`: ACMA Aeronautical licences for aviation communications, navigation, safety, or air-services organisations.
- `maritime_coast`: ACMA Maritime Coast licences for maritime safety, coast-station, port, VTS, or GMDSS-style communications roles.
- `public_safety_land_mobile`: ACMA Land Mobile licences tied to public-safety, emergency-services, government critical-communications, or essential-services radio networks.

The provenance facets, which we refer to as `evidence_facet`, are:
- `rrl_licence_presence`: a public, judge-fetchable text/HTML/JSON row artifact or proven row-viewer page extracted from an official ACMA RRL current download or archive. The submitted `url` must visibly contain the official ACMA source URL, data vintage or archive date, `client.csv` locator, `licence.csv` locator, `CLIENT_TYPE_ID` or an equivalent official non-natural-person client classification, organisation or ABN, licence number, licence type/category, and licence status for the claimed service bucket. The raw binary ZIP URL by itself, direct `client.csv` or `licence.csv` URLs, private notes, solver-only transcripts, and ACMA RRL help/overview pages do not count as entity-specific licence-presence evidence.
- `business_register_identity`: ABR or equivalent official business-register evidence showing ABN, legal name, registration/status, and organisational entity type.
- `independent_role_context`: an official, entity-owned, regulator-owned, or regulated-sector public source outside ACMA RRL and ABR tying the same organisation to the relevant communications, broadcasting, maritime, aviation, spectrum, public-network, or public-safety role.

Only organisational, ABN-backed licensees count. Natural-person, private-person, no-ABN, sole/private-person, and ACMA `CLIENT_TYPE_ID=7` licensees are out of scope even when a trading name or ABN is present. Sources and excerpts should stay at organisation/licence-provenance level; coordinates, detailed frequencies, site names or locations, antenna/device details, VHF channels, contact details, postal/contact addresses, RFNSA pages, outreach targets, infrastructure targeting, spectrum trading/acquisition, interference coordination, RF engineering, and legal/compliance advice are out of scope.

Requirements:
- The source must identify the same organisation by ABN, ACN, legal name, or unmistakable official organisation name.
- The source must fit the declared `evidence_facet`; ACMA RRL/download/archive evidence cannot satisfy business-register or independent-role evidence, ABR cannot satisfy RRL or role evidence, and ACMA RRL overview/help pages cannot satisfy any entity-specific facet.
- The source must provide the facet-specific substance: official ACMA row-artifact provenance, non-`CLIENT_TYPE_ID=7` organisational client classification, licence number, licence type/category, status, and service-bucket presence for `rrl_licence_presence`; ABN/legal-name/status/entity-type identity for `business_register_identity`; relevant non-RRL/non-ABR role context for `independent_role_context`.

Write one JSON object per line to `results_acma_rrl_licensee_provenance.jsonl`:
{"item": { "service_bucket": "<service_bucket>", "abn": "<abn>", "organisation_name": "<organisation_name>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

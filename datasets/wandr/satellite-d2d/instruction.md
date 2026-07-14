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

## `satellite_d2d`

For 100+ public organization-role records in the satellite direct-to-device / direct-to-cell / NTN / MSS / handset satellite connectivity ecosystem as of 2026-04-24, cover 2+ distinct evidence facets per organization-role record and supply a source for each facet (i.e. 1+ URL).

The goal is public provenance: who appears in what ecosystem role, what the source actually says, and how source-class/date context limits the claim. This is not an operator ranking, market-size table, investment thesis, legal/regulatory advice, engineering feasibility analysis, spectrum plan, consumer support directory, or partnership-only graph.

Use `organization` plus `role` as the identity. The role should be one of:
- `satellite_operator`
- `mobile_network_operator`
- `service_platform`
- `device_oem_or_support`
- `chipset_or_module_vendor`
- `network_or_infrastructure_vendor`
- `regulator_or_public_authority`
- `standards_or_industry_body`
- `other_ecosystem_organization`

The closed evidence facets are:
- `capability_or_service_state`
- `partnership_or_customer`
- `regulatory_or_spectrum`
- `technical_or_device_enablement`
- `filing_or_investor_claim`

Accepted `source_class` labels for the cited page are:
- `official_company_or_product`
- `carrier_or_partner_channel`
- `regulator_or_license_record`
- `investor_or_sec_filing`
- `device_oem_or_support`
- `standards_or_technical_vendor`
- `industry_association`
- `telecom_satcom_trade_press`

Generic source hubs, trackers, partnership-count reports, and market-report landing pages can guide discovery, but they do not by themselves establish a submitted organization-role/facet record. IoT NTN records count only when the source explicitly ties the product, module, device, service, or standard to NTN, MSS, direct-to-device cellular/satellite connectivity, or a comparable satellite-to-device mode.

For each record, state a compact finding with the source class, source date or observed date, source-stated capability/status where any is claimed, and source-stated geography, spectrum/standard, partner/customer, regulatory/filing signal, device/chipset detail, and caveats where those appear.

Requirements:
- The page must identify the organization and support the submitted role in this ecosystem, not merely mention a same-name organization or list a logo without role substance.
- The page must substantively support the declared `evidence_facet`: source-stated capability/service state, named partner/customer relationship, regulatory/spectrum action, technical/device enablement, or filing/investor claim. The page must do more than repeat generic direct-to-device background.
- The finding should report only source-stated detail. Do not inflate planned, enabled, trial, authorized, emergency-only, app-mediated, or marketing language into commercial/public service status unless the source states that status.
- The evidence must be anchored to 2026-04-24 or earlier by a source date, release date, filing date, page date, or restrained observed-by-cutoff framing. Later events may explain why the cutoff matters, but they do not upgrade the as-of status.

Write one JSON object per line to `results_satellite_d2d.jsonl`:
{"item": { "organization": "<organization>", "role": "<role>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

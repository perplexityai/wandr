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

## `annual_report_compliance_calendar`

For the 51 U.S. jurisdictions listed below, and for each of the 4 entity categories in every jurisdiction, supply 1+ official URL for each of the 4 recurring compliance evidence facets.

The atlas is for recurring business-entity maintenance filings that belong on a compliance calendar: annual reports, biennial statements, statements of information, franchise-tax annual-report hybrids, public-information reports, or official no-recurring-report / portal-only variants. It is not about certificates of status, good-standing certificate ordering, initial formation, or first-time foreign qualification packets.

Use only official sources: Secretary of State / Division of Corporations / equivalent business registry pages, official business-registry portals, official fee schedules and forms, official statute or administrative-code sites, and official tax or franchise authorities only when they administer the recurring entity-maintenance report, tax/report hybrid, or return. Third-party registered-agent pages, compliance-vendor pages, certificate shelf-life tables, and legal-advice pages do not count.

Entity categories:
- `domestic_llc`: Domestic limited liability company.
- `foreign_llc`: Foreign limited liability company registered or authorized in the jurisdiction.
- `domestic_corporation`: Domestic profit, stock, or business corporation.
- `foreign_corporation`: Foreign profit, stock, or business corporation registered or authorized in the jurisdiction.

Evidence facets:
- `cadence_due`: report or statement name, filing frequency, due date/window, or official no-recurring-maintenance-filing marker.
- `base_fee`: base filing fee, tax, minimum tax, calculation method, no-fee marker, or official portal-only / entity-specific fee marker.
- `penalty_status`: late fee, penalty, interest, reinstatement/status consequence, cure path, or official no-penalty/no-detail marker.
- `filing_channel`: official filing portal, e-file service, form, mail, counter, or other filing channel; or official no-channel / not-applicable marker.

Jurisdictions:
- **Alabama**
- **Alaska**
- **Arizona**
- **Arkansas**
- **California**
- **Colorado**
- **Connecticut**
- **Delaware**
- **District of Columbia**
- **Florida**
- **Georgia**
- **Hawaii**
- **Idaho**
- **Illinois**
- **Indiana**
- **Iowa**
- **Kansas**
- **Kentucky**
- **Louisiana**
- **Maine**
- **Maryland**
- **Massachusetts**
- **Michigan**
- **Minnesota**
- **Mississippi**
- **Missouri**
- **Montana**
- **Nebraska**
- **Nevada**
- **New Hampshire**
- **New Jersey**
- **New Mexico**
- **New York**
- **North Carolina**
- **North Dakota**
- **Ohio**
- **Oklahoma**
- **Oregon**
- **Pennsylvania**
- **Rhode Island**
- **South Carolina**
- **South Dakota**
- **Tennessee**
- **Texas**
- **Utah**
- **Vermont**
- **Virginia**
- **Washington**
- **West Virginia**
- **Wisconsin**
- **Wyoming**

Each citation should state the facet-specific value the source supports. Taken together, the four facets for a jurisdiction/category pair should cover the report or statement name, filing frequency, due date or window, base fee, late fee / penalty / interest / status consequence when officially stated, filing channel, and any explicit official absence marker, no-detail marker, not-applicable marker, portal-only marker, or entity-specific fee marker that the cited source supports.

Requirements:
- The page must tie the filing rule to the claimed jurisdiction and entity category. A page that explicitly applies the same rule to all relevant business entities, corporations, LLCs, or domestic/foreign entities can support multiple categories.
- The page must anchor an existing-entity recurring maintenance obligation, official no-recurring-report position, or official portal-only maintenance filing context. Formation filings, first-time foreign registration, certificates of status, account-status certificates, federal beneficial-ownership notices, and generic tax registration pages are not enough.
- The page must supply the evidence called for by `evidence_facet`. `cadence_due` needs the filing name plus cadence and due timing, or an official no-recurring-maintenance-filing marker. `base_fee` needs base fee / tax / minimum tax / calculation / no-fee / portal-only / entity-specific fee evidence. `penalty_status` needs late fee, penalty, interest, reinstatement/status consequence, cure path, or official no-penalty/no-detail evidence. `filing_channel` needs an official portal, e-file service, form, mail, counter, other filing channel, or official no-channel / not-applicable marker.

Write one JSON object per line to `results_annual_report_compliance_calendar.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "entity_category": "<entity_category>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

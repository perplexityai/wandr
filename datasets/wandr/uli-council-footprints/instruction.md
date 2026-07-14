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

## `uli_council_footprints`

For each of the 3 ULI regions listed below, name 21+ officially linked district, national, local, satellite, or comparable council-like ULI networks per region. For every council, supply 6+ evidence-type records from the allowed evidence types, each backed by 1+ public URL.

The goal is a factual public provenance base for ULI council footprints: official identity, geography, activity, reports, tools, and source-access states. Do not rank councils, recommend strategy, infer market performance, advise on membership or fundraising, enrich contacts, or use private/member-only content.

Target ULI regions:
- **Americas**
- **Europe**
- **Asia Pacific**

Allowed evidence types:
- `identity_geography`: official council identity, label variants, geography served, and official URL or subdomain
- `membership_scale`: membership, participation, attendee, location-count, or other public scale claim
- `event_program_activity`: event, conference, program, UrbanPlan, local initiative, or comparable activity evidence
- `annual_impact_report`: annual report, impact report, year-in-review, or explicit report availability/access state
- `tap_research_publication`: Technical Assistance Panel, Advisory Services, research, report, publication, or resource output
- `leadership_committee`: leadership role, committee, council, advisory group, or governance structure
- `dashboard_tool_resource`: dashboard, public tool, data/resource page, documentation, or dashboard-shell access state
- `access_missing_state`: checked public source family where evidence is missing, member-only, sign-in-only, broken, redirecting, stale, conflicting, or JavaScript-only

Suitable public sources include official ULI regional lists, council home/about pages and subdomains, annual or impact PDFs, event/program pages, TAP/research/resource pages, Navigator public metadata, dashboard/tool documentation, and public pages that demonstrate access failure or absence after a source family was checked. Regional lists and broad source-hub pages are normally identity/geography evidence. For `event_program_activity`, `annual_impact_report`, `tap_research_publication`, `dashboard_tool_resource`, or `access_missing_state`, do not cite a broad list or hub unless that page itself exposes council-specific, facet-specific substance or a precise checked access/missing observation. Member-only, sign-in-only, redirecting, JavaScript-only, or broken surfaces can support access-state evidence, but hidden content behind those surfaces does not count as factual evidence.

Each evidence record should identify the official council name, useful label variants, geography served, official URL or subdomain when visible, source family, source title or page identity, source date or period when available, checked date, access state, confidence, and any missing/conflict note. Keep numeric scale claims factual and period-aware; do not treat self-reported membership, event, sponsorship, or attendance numbers as standardized comparative metrics.

Requirements:
- The page must tie the source to the named ULI council and claimed ULI region.
- The page must support the selected evidence type with a factual council-footprint claim or a precise missing/access-state observation from a checked public source family.
- For non-identity evidence from a regional list or broad source-hub page, the cited page must contain council-specific substance for the selected evidence type or a precise checked access/missing observation, not just the council's name in a regional directory.
- The page must preserve enough source context for the claim: source family, source title or page identity, date or period when available, access state, and whether the evidence is positive, missing, gated, stale, redirecting, JavaScript-only, or conflicting.

Write one JSON object per line to `results_uli_council_footprints.jsonl`:
{"item": { "uli_region": "<uli_region>", "uli_council": "<uli_council>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

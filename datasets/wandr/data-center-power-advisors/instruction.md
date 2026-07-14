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

## `data_center_power_advisors`

For 250+ organizations that publicly advise on data-center grid-side power strategy, utility or load interconnection planning, power procurement, tariffs or rates, grid connection studies, transmission or substation energy infrastructure, power feasibility, utility timelines, or comparable grid-side power planning, supply evidence for each of the 2 evidence roles, with 1+ source URL per role. This is public advisor provenance, not provider ranking, procurement recommendation, utility-negotiation advice, site-selection advice, private relationship inference, customer targeting, contact enrichment, outreach, or lead scoring.

The evidence roles are:
- `official_power_advisory_capability`: an official or durable organization-controlled source proving data-center-specific grid-side power advisory capability.
- `public_power_engagement`: a separate public source showing the same organization, or a source-stated affiliated person, publicly engaging on data-center power, interconnection, procurement, tariff, grid-constraint, time-to-power, or comparable grid-side power issues.

For downstream reading, optional factual notes can include source-stated practice name, source-stated affiliated public person and title, source geography, public source class, grid-side power topic, source date or event date, checked date, and brief source notes. Use 2026-06-30 as the checked date unless the source was checked later. Do not include phone numbers, emails, contact forms, LinkedIn profiles, private relationship guesses, rankings, scores, recommendations, target customers, or outreach fields.

Grid-side data-center power substance includes:
- data-center power strategy or power supply strategy.
- utility or load interconnection planning.
- power procurement, PPAs, or energy contracting for data centers.
- tariff, rate, cost-allocation, or regulatory strategy tied to data-center load.
- grid connection, grid impact, feasibility, queue, or transmission studies.
- transmission, substation, or other utility-side energy infrastructure planning.
- power availability, power feasibility, or time-to-power advisory.
- large-load resource adequacy, grid constraint, or utility timeline advisory.

Public engagement sources can include:
- conference, course, webinar, panel, or public training page.
- bylined article, interview, quote, whitepaper, report, or public presentation.
- public testimony, public regulatory article, or reputable industry coverage.
- organization-controlled insight page that is substantive thought leadership rather than a duplicate service pitch.

Law firms, product-vendor consulting arms, engineering firms, market advisors, and research or policy organizations count only when they satisfy the same data-center grid-side power advisory bars as any other organization. The qualifying organization remains the root entity even when the public engagement source names an affiliated person.

Boundary classes to keep out unless the submitted evidence role is directly satisfied:
- generic data-center design or inside-the-fence MEP/electrical engineering.
- sustainability-only, carbon-accounting-only, cooling-only, or hardware/product pages.
- real-estate, site-selection, powered-land, available-capacity, or market-attractiveness content.
- data-center developer, operator, REIT, hyperscaler, utility, or public agency acting only as a customer, host, or regulator.
- recruiting, staffing, lead-generation, contact database, ranking, buyer guide, or outreach material.
- pure load forecasting or generic energy/procurement/legal primers without advisory positioning.
- event pages that give only a name or title without data-center power substance.

Requirements:
- The page must identify the claimed advisor organization, or bridge the source-stated person, practice, subsidiary, parent, rebrand, or operating-brand name to that organization with enough context to distinguish unrelated same-name organizations.
- The submitted page itself must fulfill the claimed `evidence_role`: `official_power_advisory_capability` evidence should be official or durable organization-controlled capability evidence, while `public_power_engagement` evidence should be a separate public engagement source rather than a duplicate generic service page.
- The page must support role-specific grid-side data-center power substance. For `official_power_advisory_capability`, it must show public advisory capability for data-center power strategy, interconnection, procurement, tariffs/rates, grid studies, transmission/substation infrastructure, power feasibility, utility timelines, or comparable grid-side planning. For `public_power_engagement`, it must show the organization, or a source-stated affiliated person, publicly engaging on data-center power, interconnection, procurement, tariffs, grid constraints, time-to-power, or comparable grid-side issues.

Write one JSON object per line to `results_data_center_power_advisors.jsonl`:
{"item": { "advisor_org": "<advisor_org>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

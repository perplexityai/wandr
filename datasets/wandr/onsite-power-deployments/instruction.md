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

## `onsite_power_deployments`

For 160+ public onsite or stationary power deployments, orders, or project-specific contracted projects in the Bloom-adjacent commercial / industrial and critical-load power arena, supply one source for each of the 2 evidence roles below (i.e. 1+ URL per role).

Bloom Energy is only an arena anchor here. Valid projects may involve fuel cells, microgrids, reciprocating generator sets, gas turbines, microturbines, linear generators, backup or critical-load systems, or hybrid onsite power for data centers, campuses, industrial sites, logistics facilities, utilities, or similar C&I settings.

Use source pages whose visible publication, filing, announcement, or source date is on or before March 13, 2026. Visibly post-cutoff pages do not count as eligible answer evidence. Durable pages with no visible source date can count only when the checked or observed date basis is explicit and kept separate from the project facts.

The evidence roles, reported as `evidence_role`, are:
- `originator_or_project_party_source`: a direct project-party source establishing the deployment, order, or project. The page or document should be authored by, released for, filed or submitted by, or visibly controlled by a provider, vendor, developer, customer or host, sponsor, procurement owner, utility, public agency, or similar entity only when that entity is itself a project owner, host, sponsor, procurement party, petitioner, or equivalent project party.
- `external_confirmation_source`: a non-originator source that confirms the same deployment, order, or project. This can include a customer or host page, independent project-specific trade reporting, neutral utility or regulatory material, permit, procurement award, public filing, program-register entry, third-party database, government or analyst material, or comparable confirmation outside the originator's own marketing surface.

Neutral regulator indexes, agency petition-list summaries, public-record aggregations, third-party databases, independent media, and generic government or analyst records do not count as `originator_or_project_party_source` merely because they mention a project party. A regulatory or public-agency document can count for that role only when the cited page or document itself is visibly filed, submitted, authored, or controlled by the project party; a neutral docket page, petition-list entry, database row, or agency summary is external confirmation at most.

Each URL must be source-local to the submitted deployment: a project page, case study, announcement, permit, application, filing attachment, single-project register record or stable single-record anchor, or similarly bounded source for that deployment. Vendor-wide customer/logo pages, developer portfolio indexes, search-result tables, program-wide registers, many-project database/listing pages, and broad market pages do not count when cited only as collection-level surfaces, even when one row or logo on the page can be cross-walked to another source.

Name each deployment with enough source-stated identity anchors to keep it disambiguatable: provider or project party, host or project/site label if public, geography, technology, date/status, permit or program identifier, or similar concrete anchors. Public customer names are not required when the source only gives an anonymized host, project identifier, site, or formal record, but do not infer or enrich the customer.

Alongside each URL, report only facts stated by the cited source: provider/vendor/developer, customer or host, project/site name, geography, capacity, price or contract value, status, technical wording, source date, checked date, and explicit missing or conflict states such as no-named-customer-source, no-pricing-source, no-technology-source, no-visible-source-date, or name-conflict. This is public deployment provenance, not vendor ranking, product recommendation, investment analysis, procurement advice, competitive strategy, customer targeting, contact lookup, outreach, or contact enrichment.

Requirements:
- The cited URL must be source-local to the submitted deployment, not only a collection-level customer page, portfolio, multi-project table, or vendor/developer-wide database page.
- The page must describe a concrete physical deployment, order, contract, facility, permit, incentive application, or project-specific plan; generic product, capability, "solutions for data centers", market-commentary, and technology-positioning pages do not count by themselves.
- The page must source-state that the project concerns onsite, stationary, distributed, backup, microgrid, or similar power in scope for a C&I, data-center, utility-edge, campus, industrial, or critical-load setting.
- The page must visibly fit the declared `evidence_role`: `originator_or_project_party_source` evidence comes directly from a project party or that party's released, controlled, filed, or submitted document; `external_confirmation_source` evidence comes from a genuinely non-originator source and must not be merely a syndicated copy of the same originator announcement.
- The row should localize source-stated deployment facts from this URL, including a project-party/provider, host/project/site label or formal identifier, plus at least one concrete geography, capacity, status, technology, date, or record anchor; do not infer those facts from another page, generic company knowledge, rankings, sales intelligence, or contact-enrichment work.

Write one JSON object per line to `results_onsite_power_deployments.jsonl`:
{"item": { "onsite_power_deployment": "<onsite_power_deployment>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

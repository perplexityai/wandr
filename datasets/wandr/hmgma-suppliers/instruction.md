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

## `hmgma_suppliers`

For 34+ supplier facilities in Georgia publicly tied to Hyundai Motor Group Metaplant America, Hyundai Motor Group, Kia Georgia, or a mediated Metaplant supplier relationship, name the supplier and Georgia facility/project location or site and supply public-source evidence for each of the 3 required evidence roles per facility (i.e. 1+ URLs for each role).

The entity is the supplier plus the Georgia facility/project, not the supplier company in the abstract. Public source fragments often split the facility evidence: one source may carry announced jobs/investment, another may carry independent component/customer wording, and a later or site-specific source may carry opening, production, construction, address, regulatory, current, or conflict context.

Required evidence roles:
- `announcement_terms`: a source that states announced or planned facility/project terms, such as announced jobs, announced capital investment, project creation, timing, or opening/production plans
- `relationship_component`: an independent non-Georgia-state-announcement and non-aggregate source that states the supplier relationship or customer channel and the component/product category, including direct or mediated ties through HMGMA, Hyundai Motor Group, Kia Georgia, Hyundai Mobis, Hyundai Transys, or comparable Metaplant supplier wording
- `site_status`: a source beyond the original project announcement that states later opening, operating, production, construction, expansion, permit, regulatory, address/occupancy, or other source-dated site/status evidence for the same Georgia facility

The evidence load is intentionally independent across roles. Statewide Georgia Governor/GDEcD announcement pages and their Georgia.org mirrors can support `announcement_terms`, but they do not by themselves satisfy `relationship_component` or `site_status`. Aggregate HMGMA supplier-network pages, broad economic-development tables, and supplier lists can help discovery, but they do not replace facility-specific evidence for any role.

Eligible scored source surfaces include facility-specific Georgia Department of Economic Development or Governor's Office announcements for announcement terms; county/city/economic-development authority pages; supplier/company project or press pages; HMGMA/Hyundai pages when they substantiate the submitted facility or role; reputable local/business coverage; and role-relevant regulatory, permit, property, engineering, or technical filings for site/status evidence. Industry PDFs/tables are discovery or secondary corroboration, not sole authority for facility identity, relationship/component evidence, or site/status evidence. Recruitment, job-fair, contact, social-only, vendor-ranking, procurement-advice, investment-thesis, incentive-opinion, generic supplier-homepage, and table-only surfaces do not count as primary facility-fact evidence unless the page itself substantively supports the submitted facility and role.

Keep each answer source-scoped: preserve supplier aliases, Georgia city/county/site/address when public, component/product category, relationship class and wording, announced capital investment, announced jobs, source date, later/opening/current status, and conflict or missing states only when the cited page states or supports them. Do not call announced jobs or investment current or realized unless the cited page says so.

Requirements:
- The page must identify the named supplier and tie it to the submitted Georgia facility, project location, city/county, site, or address.
- The page must contribute evidence for the declared `evidence_role`.
- The answer must keep facts source-scoped, including temporal labels for announced/planned/current/opening language and any conflict or missing-state claim.

Write one JSON object per line to `results_hmgma_suppliers.jsonl`:
{"item": { "supplier": "<supplier>", "facility": "<facility>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

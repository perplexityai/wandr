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

## `adventure_resort_hiring_provenance`

For each of the 4 adventure-hospitality operator types listed below, cover 35+ named operators and each of the 3 public hiring evidence facets per operator; for each (`operator_type`, `operator`, `hiring_evidence_facet`) case, supply a hiring-provenance source (i.e. 1+ URL).

The task is public hiring-source provenance for surf, dive, remote/coastal resort, and adventure operators, not hiring emails, contacts, applicant strategy, work/visa/travel advice, salary guidance, resort ranking, recommendations, outreach, lead scoring, or contact enrichment.

Operator types:
- `surf_or_watersports_camp`: surf camps, surf schools, watersports camps, beach-club activity operators, and guest operators centered on surfing, kitesurfing, windsurfing, sailing, stand-up paddling, or comparable water-based instruction/activities.
- `dive_or_liveaboard_operator`: dive resorts, dive centers, dive lodges, scuba operators, liveaboards, and operators centered on guest diving or boat/dive operations.
- `remote_island_or_coastal_resort`: named island, coastal, remote-shore, or coastal-lodge resort/hospitality operators where the location or setting is part of the public guest-facing operation.
- `adventure_lodge_or_tour_operator`: adventure lodges, tour operators, expedition operators, outdoor activity operators, fishing lodges, rafting/hiking/wildlife operators, and comparable guest adventure operations.

Hiring evidence facets:
- `owned_recruiting_surface`: an operator-controlled careers, jobs, employment, work-with-us, hiring, recruiting, or official social/account surface that communicates public recruitment.
- `role_or_season_signal`: a public posting, notice, or recruiting page that names a concrete role, current opening, current hiring status, or page-stated 2026 season/window for the operator. A page that is explicitly expired, closed, or past-deadline does not satisfy this facet unless it also states a still-open/current hiring signal.
- `independent_hiring_footprint`: a non-operator public board, listing, profile, trade/community source, or comparable source that names the operator and carries a hiring, opening, recruiting, or seasonal-job signal.

Eligible operators are named guest-facing hospitality or activity operators, not job boards, directories, recruiter firms, employer lists, broad resort groups with no named property/operator, or role categories. Public role, season/date, credential, and requirement details count only as page-stated hiring facts; those details are provenance, not eligibility or application advice.

Requirements:
- The page must clearly identify the named operator.
- The page must tie the operator to the claimed `operator_type`.
- The page should make its facet-appropriate source role visible: operator-controlled for `owned_recruiting_surface`; posting/notice/recruiting context with a concrete role, current opening, current hiring status, or page-stated 2026 season/window for `role_or_season_signal`, without being explicitly expired, closed, or past-deadline; non-operator hiring-board, listing, profile, trade/community, or comparable context for `independent_hiring_footprint`.
- The page must state a facet-scoped hiring signal: an owned recruiting invitation or employment surface for `owned_recruiting_surface`; a concrete role/opening/current-hiring status or page-stated 2026 season/window for `role_or_season_signal` that is not explicitly expired, closed, or past-deadline; an independent public hiring/opening/recruiting/seasonal-job signal naming the operator for `independent_hiring_footprint`.

Write one JSON object per line to `results_adventure_resort_hiring_provenance.jsonl`:
{"item": { "operator_type": "<operator_type>", "operator": "<operator>", "hiring_evidence_facet": "<hiring_evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

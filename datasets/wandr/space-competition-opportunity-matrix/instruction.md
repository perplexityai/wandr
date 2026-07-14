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

## `space_competition_opportunity_matrix`

For 24+ public NASA or space-ecosystem opportunities suitable for U.S. college CubeSat, smallsat, or space-systems teams, supply at least 1 source URL for each of the 6 evidence axes below.

Name each opportunity as `program|cycle`, where `cycle` is the official season, campaign, call, challenge year, flight-opportunity window, or other cycle/window label used on the page, as long as that label explicitly includes a 2026 or 2027 participation event. The panel is for a faculty advisor deciding what a student team can actually pursue: a bare contest title is not enough.

Evidence axes:
- **official_identity** -- the opportunity's official name, sponsoring or managing organization, and cycle/window identity that explicitly includes a 2026 or 2027 participation event.
- **eligibility** -- who can enter, with enough student, institution, citizenship, faculty advisor, or team-composition detail for a U.S. college team to screen itself.
- **deadline_window** -- a 2026 or 2027 submission, registration, notice-of-intent, finalist, forum, test, launch, final-round, or award window.
- **deliverables_challenge** -- the mission problem, design challenge, required deliverables, proposal package, prototype, paper, video, pitch, review, or test artifact.
- **award_support_selection** -- prizes, stipends, launch access, hardware packages, mentoring, finalist selection, NASA review, conference presentation, internship, or other support.
- **student_team_fit** -- why the opportunity is a plausible fit for a U.S. college CubeSat, smallsat, or space-systems team.

Use opportunity-specific sources: NASA or sponsoring-agency program pages, official challenge websites, Challenge.gov / USAGov challenge records, grant or solicitation pages, student competition pages, official rules / handbook PDFs, and university or team examples when they are specific to the same opportunity. Generic NASA education pages, unofficial blog/listicle pages, old archive pages, pages for professional-only prizes, and pages for non-space aerospace or robotics contests may help discovery but do not count as the cited evidence for a claimed opportunity and evidence axis.

Each cited page must tie the opportunity to January 1, 2026 through December 31, 2027. A 2024 or 2025 page can count only when that same page states a 2026 or 2027 competition, campaign, forum, final round, selection, award, launch, flight-opportunity, or other participation window.

Each cited page must:
- be opportunity-specific and on an admitted official, administrator, sponsor, rules, solicitation, challenge, or opportunity-specific team / university source class.
- tie the opportunity to a cycle/window that explicitly includes a 2026 or 2027 deadline, event, selection, final round, award, launch, flight opportunity, or other participation anchor.
- substantively support the claimed evidence axis for the claimed opportunity.

Write one JSON object per line to `results_space_competition_opportunity_matrix.jsonl`:
{"item": { "program": "<program>", "cycle": "<cycle>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

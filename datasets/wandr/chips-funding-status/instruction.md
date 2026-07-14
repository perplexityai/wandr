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

## `chips_funding_status`

For 75+ CHIPS for America funding actions, identify the recipient and project/action anchor, then supply one source for each of the 2 evidence roles.

The funding action identity is recipient plus project/action anchor. Include site or location in the anchor when that is needed to distinguish official actions, but do not split one multi-site funding agreement into independent actions unless the official source treats the site entry as the action being evidenced.

The evidence roles of interest, which we refer to as `evidence_role`, are:
- `federal_status_record`: an official NIST, CHIPS for America, Department of Commerce, or other Commerce-hosted action-specific page, release, fact sheet, PDF, or archive record that states the federal source-local status, instrument, or action for the funding action. Broad awards lists, proposed-funding lists, state indexes, search results, generic funding-update indexes, and generic program pages are discovery surfaces, not sufficient evidence for this role.
- `outside_program_project_context`: a public source outside the NIST / CHIPS Program / Department of Commerce primary page family that ties the same recipient and project/action anchor to the CHIPS action or to the specific project implementation. Valid source classes include recipient/operator press releases or investor pages, SEC exhibits or filings, state or local government pages, congressional office pages, regional economic-development pages, or comparable public institutional project pages. The page must be project-specific. It cannot be only a third-party media article, tracker, scraped grant database, generic company profile, generic facility page, or broad semiconductor-policy page.

Eligible funding actions include official CHIPS for America awards, proposed-funding actions, preliminary terms / PMTs, letters of intent, Direct Funding Agreements, final awards, definitive agreements, R&D / NAPMP / SBIR / NSTC award actions, and comparable official CHIPS funding actions. Funding opportunities, procurement notices, generic program accounts, eligibility pages, application guidance, investment topics, and third-party trackers are out of scope.

Preserve the source-local wording. PMT / preliminary terms, proposed funding, LOI, Direct Funding Agreement, Final Award, definitive agreement, award, grant, loan or equity language, revision, rescission, and under-review or update language should not be flattened into one generic award label. Amounts should likewise stay source-local, including "up to" ceilings, direct-funding / loan / equity distinctions, and grouped or split amount phrasing.

Requirements:
- The page must identify the same recipient and project/action anchor, including site geography or project scope enough to bind the page to the claimed funding action.
- The page must have the selected role's source shape: `federal_status_record` needs an action-specific Commerce/NIST/CHIPS federal status record, while `outside_program_project_context` needs a public non-CHIPS-program institutional source that independently ties the same recipient/project to the action or implementation context.
- The page must state the source-local status, instrument, award, proposed-award, implementation, or project-context phrase for the funding action.
- The page must state the source-local amount phrase when shown, or support a source-local omitted, grouped, or split amount state.
- The page must tie the action to CHIPS for America through CHIPS organization/program context and must describe project scope or project/site geography.
- The page must satisfy the selected `evidence_role`: `federal_status_record` must support the federal status or action record, while `outside_program_project_context` must support a non-NIST/Commerce project-context source for the same action.

Write one JSON object per line to `results_chips_funding_status.jsonl`:
{"item": { "recipient": "<recipient>", "project_anchor": "<project_anchor>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `former_us_solicitor_general_private_practice`

For 75+ people, supply public professional-role sources establishing prior service in an eligible U.S. Office of the Solicitor General role, a current private-practice law-firm biography, and a current person-tied practice focus; cover each of the 3 evidence categories listed below for every person with a source (i.e. 1+ URL under each category).

The evidence categories are:
- `osg_role_history`: prior service in the U.S. Office of the Solicitor General as Solicitor General, Acting Solicitor General, Principal Deputy Solicitor General, Deputy Solicitor General, or Assistant to the Solicitor General. Bristow Fellow service alone does not count.
- `current_private_practice`: a current official law-firm biography or firm-controlled profile showing the person is presently in private practice.
- `practice_focus`: a current person-tied description of the person's practice focus, such as appellate, Supreme Court, constitutional, regulatory, commercial litigation, investigations, or another public practice descriptor.

The people should be broadly distributed across current firms; avoid relying on more than about five people from the same current firm unless additional qualifying people make broader distribution impractical. This is a public professional-role evidence task, not a lawyer ranking, referral, contact-enrichment, legal-advice, client-list, or legal-strategy task. Emails, phone numbers, office addresses, vCards, LinkedIn links, client rosters, rankings, "best lawyer" claims, and outreach-ready contact facts are out of scope.

Requirements:
- The page must clearly identify the named person.
- The page must have the source role appropriate to the evidence category. For `osg_role_history`, prefer DOJ OSG historical biographies, DOJ OSG brief PDFs or signature blocks, Supreme Court day-call / hearing-list / docket materials, White House / Senate / court / other official government materials, or high-quality non-firm institutional profiles such as law-school, ALI, Federalist Society, bar/event, C-SPAN, or reputable legal-news pages; current firm biographies by themselves do not count for this category. For `current_private_practice`, the page must be the person's current official firm biography or firm-controlled current profile, not an old move announcement, ranking directory, LinkedIn profile, or third-party contact listing. For `practice_focus`, the page must be a current person-specific firm page, person-specific firm biography, or reputable current profile; generic practice pages count only when they visibly bind the named person to the practice description.
- The page must support the category-specific professional fact. For `osg_role_history`, it must tie the person to one of the eligible OSG roles. For `current_private_practice`, it must show a present-tense private-practice lawyer role at the named firm. For `practice_focus`, it must show the person's current practice focus rather than only a ranking, superlative, old case mention, generic firm capability claim, or unbound team description.

Write one JSON object per line to `results_former_us_solicitor_general_private_practice.jsonl`:
{"item": { "person": "<person>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

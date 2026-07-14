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

## `nurse_pathway_programs`

For 240+ distinct public program hosts connected to Canadian nursing, name 1+ mentorship, pathway, leadership, career-support, settlement-support, credentialing-support, toolkit, summit, report, or similar support program per host, and supply 1+ public source URL per host-program pair.

The useful evidence is program-level: organization profiles can help discover hosts, but each source should document a concrete support program or initiative serving racialized, ethnocultural, internationally educated, newcomer / immigrant, or Indigenous nurse communities in Canada.

Treat the answer set as a broad constituency and source-mix search, not an IEN-page scrape. Aim to include evidence for Black / racialized nursing support, ethnocultural or minority-community nursing support, newcomer / immigrant / internationally educated nurse support, and separately named Indigenous nursing support where public sources support them. Also mix host and source roles, such as nurse associations or chapters, schools / universities, health systems, settlement or credentialing-support organizations, government / funder pages, reports, evaluations, toolkits, summit packages, and partner pages. Each individual record must satisfy the requirements below; this breadth target is meant to keep the open set from collapsing to one obvious source family.

Acceptable sources include official host pages, dated cohort / event / intake / annual-review / announcement pages, funder or government pages, university / school / professional-association / health-system partner pages, and reports, evaluations, toolkits, summit packages, or PDFs that document the program at host or program level. Thin, social-heavy, or current-activity sources are lower-confidence evidence and should be corroborated where possible by official, institutional, government, funder, credible media, report, toolkit, or similar public evidence. A social-only source still has to satisfy the host, program, audience, Canadian nursing, support-activity, and date/currentness requirements from page-side evidence.

Course calendar, ordinary bridging program, employment, or admission pages are not enough by themselves when they merely describe generic nursing education, eligibility, or hiring. They count only when the same page documents a targeted support or pathway function for the named constituency, such as mentorship, transition-to-practice or integration support, licensure / credential navigation, settlement or job-readiness support, clinical practice-gap support, supervised practice, cohort programming, bursary / financial support, or a similar constituency-specific nursing pathway.

Current public pages count. Dated historical sources count when they document a 2020-present program, cohort, report, summit, or initiative. A program does not need to be accepting applications today.

Do not use generic nursing mentorship or retention programs unless the page explicitly ties the program to one of the served constituencies named here and to Canadian nursing. Do not use generic health-care anti-racism pages without nursing-specific and constituency-specific program content. Do not use private forms, emails, phone numbers, contact instructions, individual biographies, LinkedIn / personal profiles, organization rankings, outreach tactics, or inferred identity claims as the evidence target.

Indigenous nursing programs count only when Indigenous communities are named separately and publicly by the source; do not describe Indigenous nurses as merely "racialized."

Requirements:
- The page must tie `program_host` to `support_program` as a named or clearly describable program, cohort, pathway, stream, toolkit, report, summit, or recurring initiative.
- The page must explicitly state the served audience: racialized, Black, ethnocultural, internationally educated, newcomer / immigrant, or separately named Indigenous nurses, nursing students, nurse leaders, nursing applicants, or nursing workforce participants.
- The page must communicate Canadian nursing scope, such as Canadian nurses or nursing students, Canadian nursing education, Canadian licensure / credential recognition, Canadian workforce entry, a Canadian nursing association, or a Canadian health-system partner.
- The page must describe a concrete support activity, such as mentoring, leadership development, professional development, networking, student support, job readiness, settlement support, credentialing or registration guidance, cohort programming, toolkits, reports, or summit programming.
- The page must show that the support activity is targeted to or substantively framed for the served constituency, not merely a generic nursing program plus a stray demographic mention. For IEN / newcomer course or bridging pages, the page must document tailored transition, credential / licensure, settlement / job-readiness, mentorship, clinical-integration / supervised-practice, bursary, cohort, or similar pathway support rather than ordinary admission or curriculum alone.
- The page must provide current or 2020-present context through a page date, cohort / intake period, launch or publication date, event date, report date, annual-review context, or visible current program status.

Write one JSON object per line to `results_nurse_pathway_programs.jsonl`:
{"item": { "program_host": "<program_host>", "support_program": "<support_program>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

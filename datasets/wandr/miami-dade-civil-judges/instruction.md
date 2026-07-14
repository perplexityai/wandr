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

## `miami_dade_civil_judges`

For 40+ jurists, cover the 3 evidence facets listed below for each jurist by supplying a source (i.e. 1+ URL under each facet) that exposes a focused, tangible finding clearly scoped to that jurist and to the facet in question.

The purpose is to assemble, one jurist at a time, the practice-facing profile a litigant would need before appearing in a section: where the jurist sits, how to get matters in front of them, and how to reach chambers.

Evidence facets:
- `section_assignment`: where the jurist sits — their seat within the civil bench of the Eleventh Judicial Circuit.
- `submission_procedure`: how to put work before the jurist — the section's own ground rules for moving a matter forward.
- `chambers_logistics`: how to reach the jurist's chambers — the practical channels for contacting and delivering to the section.

The sources should be fully public, accessible, and usable (e.g. not paywall-guarded, login screens, or dead links).

Requirements:
- The page must identify the named jurist as the presiding judicial officer of a civil section of the Eleventh Judicial Circuit (Miami-Dade), via judicial-identity text, a section/division heading naming the jurist, or an official directory or divisional-document attribution. A bare appearance of the name in a case caption or party list does NOT count. A general magistrate, senior judicial officer, or judicial assistant is NOT a section's presiding officer — they may appear on a qualifying page (e.g. a judicial assistant as the chambers contact), but the named jurist itself must be the section's presiding officer.
- The page must be hosted on the Eleventh Judicial Circuit's own court domain or an officially-controlled court channel (the circuit's site, its administrative-order or divisional-document store, or the county court system). Third-party legal directories, attorney-marketing pages, news outlets, and case-law aggregators do NOT count.
- The page should make its facet-appropriate source role visible — the cited page should read as the right kind of court surface for the facet, not an off-type page that merely happens to mention the detail. For `section_assignment`, a directory, judicial-section-detail, or bench-calendar surface. For `submission_procedure`, a divisional policies-and-procedures, section-instructions, or administrative-order surface. For `chambers_logistics`, a judicial-detail, contact, or divisional-procedures surface.
- The page should expose a focused finding clearly scoped to the named jurist and facet. For `section_assignment`, this means the jurist's specific civil section or division identity (e.g. the labeled section number under which they currently hear civil cases). For `submission_procedure`, it means a concrete divisional rule the section imposes on filings — a stated proposed-order channel, a motion-calendar or hearing-setting step, or a notice / formatting / filing requirement. For `chambers_logistics`, it means a concrete reachability or delivery detail — a named judicial assistant, a chambers email or phone, a room / location, or a courtesy-copy instruction.

Write one JSON object per line to `results_miami_dade_civil_judges.jsonl`:
{"item": { "jurist": "<jurist>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

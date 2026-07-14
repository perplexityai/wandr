You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `legal_ai_publications`
  - `legal_ai_publications.legal_ai_pieces`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `legal_ai_publications`

For 60+ public publications or recurring editorial outlets with legal, regulatory, technology-policy, compliance, legal-tech, or governance commentary scope, cover each of the 2 profile facets below by supplying a source (i.e. 1+ URL) that exposes public, source-stated profile evidence for the named publication.

The useful work is public editorial-source ecology, not publication recommendations or outreach.

Profile facets:
- `publication_identity`: the outlet's public editorial or source-owner identity, such as a masthead, about page, editorial board, publisher page, staff page, journal page, mission page, or comparable publication-identity surface
- `contribution_route_state`: the outlet's public contribution or outside-author route state, such as open submissions, completed-draft submission, guest-author guidelines, member / volunteer contribution, invited-only policy, no-unsolicited-submission policy, closed-window call, or comparable source-stated route condition

Publications ought to be recurring public publications, outlets, journals, professional publications, policy / governance outlets, legal-tech trade publications, compliance / GRC publications, or comparable editorial surfaces. A one-off client alert, generic corporate blog, pure vendor marketing page, product-news stream, procurement list, or buyer guide counts only when the cited evidence establishes a recurring editorial publication identity. Contribution-route evidence is source-stated; absence inferred from search failure does not count. Contact details, editor email addresses, pitch priority, outreach advice, author ranking, lead scoring, and commissioning likelihood are outside the evidence claim.

Requirements:
- The page must clearly identify the named publication.
- The page should make its facet-appropriate profile-source role visible: for `publication_identity`, a public publication-identity, editorial, publisher, source-owner, masthead, board, staff, journal, mission, or equivalent surface; for `contribution_route_state`, a public contribution, submission, guest-author, member / volunteer, invited-only, no-unsolicited-submission, closed-window, or equivalent route-state surface.
- The page must expose a source-stated signal scoped to the selected `profile_facet`: for `publication_identity`, a tangible publication identity, source-owner, editorial body, publisher, staff, board, mission, or recurrent editorial-surface signal; for `contribution_route_state`, a tangible contribution-route condition, submission process, outside-author policy, member / volunteer path, invited-only condition, no-unsolicited-submissions statement, closed-window call, or comparable route state.

Write one JSON object per line to `results_legal_ai_publications.jsonl`:
{"item": { "publication": "<publication>", "profile_facet": "<profile_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `legal_ai_publications.legal_ai_pieces`

Cross-tasknode identifier discipline: this task is for the same {= publication =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= publication =}+ public publications or recurring editorial outlets, supply 3+ distinct dated published pieces per publication from 2025-01-01 through 2026-04-16; each piece should be backed by a dedicated published-piece page (i.e. 1+ URL) on the originating publication surface and centrally about legal AI governance.

Published pieces can be articles, commentary, reports, transcripts, forum essays, or comparable page-level editorial items. Legal AI governance means legal, regulatory, policy, professional-responsibility, courts / litigation / evidence, copyright / data / training, corporate legal-function governance, liability / accountability, privacy / AI governance, or similar governance framing around AI. Passing AI mentions, product marketing, vendor comparisons, procurement advice, buyer guides, implementation recommendations, and legal/safety adequacy conclusions are outside the piece claim.

Requirements:
- The page must identify the named publication as the originating or source-controlled surface for the piece, not merely a hub, search page, topic index, press-wire copy, or aggregator listing for another publisher's work.
- The page must present a dedicated published piece with a stable title or piece identity, a visible publication / release date within 2025-01-01 through 2026-04-16, and a source-stated author, byline, presenter, institutional author, or comparable issuing identity.
- The page must make legal AI governance central to the piece, not incidental: the piece should substantively address AI law, regulation, policy, professional governance, courts / litigation / evidence, copyright / data / training, corporate legal-function governance, liability / accountability, privacy / AI governance, or comparable legal-governance framing.

Write one JSON object per line to `results_legal_ai_publications.legal_ai_pieces.jsonl`:
{"item": { "publication": "<publication>", "title": "<title>", "date": "<date>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `doj_antitrust_document_provenance`
  - `doj_antitrust_document_provenance.case_context`

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

## `doj_antitrust_document_provenance`

For 100+ DOJ Antitrust Division public cases, name 3+ distinct official or public case documents per case, with the case name, document title, and source-stated document date, and supply 1+ document-specific URL for each document.

The task is about neutral filing/document provenance. The URL target itself must be a document-specific official or public enforcement-record surface that exposes the document identity and its tie to the case: DOJ Antitrust case-document page, official DOJ filing attachment/PDF, Federal Register or govinfo page/PDF, fetchable public court-record document, or comparable official/public document page. A DOJ index, alpha list, recent-filings page, broad case page, document-list page, generic case page, search/list/index page, or press release can help locate documents, but it must not stand in for a document-specific evidence page. Do not use PACER login/paywalled pages, news, legal blogs, law-firm alerts, market commentary, company pages, investment analysis, rankings, dashboards, private antitrust suits, or press-release-only narrative allegations/remedy claims.

Document labels such as complaint, indictment, proposed final judgment, final judgment, competitive impact statement, amicus brief, information, plea agreement, order, notice, settlement, or dismissal are document/source labels only. Court, docket, document number, filed header, case type, and status details should be source-stated when reported; source silence is not a legal conclusion.

Requirements:
- The page must tie the document to the submitted DOJ Antitrust case name, caption, parties, or matter.
- The page must identify the submitted document title, document type, filing label, attachment title, notice title, or equivalent source-stated document identity.
- The page must state or display the relevant document date, filed date, publication date, order date, or comparable source-stated date, while preserving what kind of date it is.
- The page must communicate neutral official/public enforcement-record standing, such as DOJ/Antitrust source identity, Federal Register or govinfo publication, public court-record material, or an official government co-plaintiff enforcement-record surface.
- Any court, docket, document number, filed header, case type, or source-stated status reported in the submission must be visibly source-stated; do not infer liability, guilt, remedy adequacy, market definition, damages, legal strategy, investment significance, or current case status.

Write one JSON object per line to `results_doj_antitrust_document_provenance.jsonl`:
{"item": { "case_name": "<case_name>", "document_title": "<document_title>", "document_date": "<document_date>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `doj_antitrust_document_provenance.case_context`

Cross-tasknode identifier discipline: this task is for the same {= case =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= case =}+ DOJ Antitrust Division public cases, supply 1+ case-specific URL that establishes case-level public-record context for each case.

Expected sources are case-specific official or public enforcement-record surfaces: DOJ Antitrust case pages, Federal Register or govinfo pages tied to the case, fetchable public court-record pages/documents, or official government co-plaintiff pages that identify the same DOJ Antitrust matter. Generic DOJ indexes, alpha lists, recent-filings pages, press-release-only narrative pages, PACER login/paywalled pages, news, legal blogs, law-firm alerts, market commentary, company pages, rankings, dashboards, and private antitrust litigation pages do not count for this context source.

Use the source's own labels for case open/filed dates, case type, court, docket, document lists, and status-like fields when they appear. Do not infer liability, guilt, remedy adequacy, market definition, damages, legal strategy, investment significance, or current case status.

Requirements:
- The page must be about the submitted case, caption, parties, or same public enforcement matter.
- The page must tie the case to DOJ Antitrust Division provenance, equivalent United States antitrust public-record provenance, or an official government co-plaintiff enforcement-record source.
- The page must supply case-level public-record context, such as case open or filed date, case type, violation or subject label, court, docket, document list, notice/proceeding context, public-record caption, or comparable case-specific context.
- Any case open/filed date, court, docket, case type, case status, document-list context, or other case metadata reported in the submission must be visibly source-stated rather than inferred.

Write one JSON object per line to `results_doj_antitrust_document_provenance.case_context.jsonl`:
{"item": { "case_name": "<case_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

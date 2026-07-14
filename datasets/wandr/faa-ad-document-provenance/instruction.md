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

## `faa_ad_document_provenance`

For each of the 2 FAA AD document statuses listed below, supply official-document provenance for 175+ airworthiness directive rulemaking documents published from 2026-01-01 through 2026-06-30; for each document, cover each of the 2 evidence roles with 1+ document-level source.

This is a regulatory-document provenance task. Keep the submission to source-stated document metadata and source-stated subject or unsafe-condition summary, not compliance advice or operational guidance.

Document statuses:
- `final_rule`: FAA AD rule/final-rule documents, including corrections, revisions, and emergency final-rule/request-for-comments documents when the official publication status is a rule/final rule.
- `proposed_rule`: FAA AD proposed-rule or NPRM documents, including proposed-rule corrections or revisions when the official publication status is proposed.

Evidence roles:
- `publication_identity`: official publication identity for the document.
- `scope_dates_subject`: product scope, status-appropriate date fields, and source-stated subject or unsafe-condition summary for the document.

Allowed evidence sources are document-level FederalRegister.gov pages, document-specific Federal Register API JSON endpoints, govinfo/GPO PDFs, and official FAA pages or PDFs when the fetched page contains substantive document text. Federal Register list/search API endpoints, search result pages, DRS Angular/search shells, inaccessible DRS deep links, third-party mirrors or summaries, law-firm pages, industry news, vendor/service-bulletin pages, random PDF mirrors, Regulations.gov enhanced-context material, advisory circulars, and compliance-help pages do not count.

For final rules, `ad_identifier` should usually be the FAA AD number. For proposed rules that lack a final AD number, `ad_identifier` may be a docket, project, or proposed-rule identifier paired with the Federal Register document number. Keep final rules, proposed rules, corrections, revisions, and emergency final-rule/request-for-comments documents distinct when the Federal Register document number or status differs.

Requirements:
- The document-level source must identify the same official FAA AD rulemaking document as the submitted `ad_identifier` and `fr_document_number`.
- For `publication_identity` records, the source must directly state FAA/DOT agency identity, final/proposed AD rulemaking status, Federal Register document number or citation, publication date in the target period, and the document's docket/project/amendment/AD identifiers when present.
- For `scope_dates_subject` records, the source must directly state affected product/manufacturer/model or type-certificate-holder scope, the status-appropriate date field, and the source-stated unsafe-condition or subject summary. Final rules usually need the effective date; proposed rules usually need comment-due or proposed-action date context.

Write one JSON object per line to `results_faa_ad_document_provenance.jsonl`:
{"item": { "document_status": "<document_status>", "ad_identifier": "<ad_identifier>", "fr_document_number": "<fr_document_number>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

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

## `easa_publication_relationship_provenance`

For each of the 4 relationship classes listed below, document 18+ source-stated relationships per class between an EASA Safety Publication and a related official publication or source record. For each relationship and each of the 2 evidence sides, supply 1+ official URL.

The work is a provenance map of publication relationships, not a table of maintenance actions. A relationship must be stated by an official source; do not infer it from matching aircraft, approval holder, subject, date, ATA chapter, or product scope alone.

Relationship classes:
- `easa_revision_or_correction`: an EASA Safety Publication revises, is revised by, corrects, or is corrected from another EASA publication or attachment.
- `easa_supersedure_or_pad`: an EASA Safety Publication supersedes or is superseded by another EASA publication, or source-states a PAD-to-final-AD consultation link.
- `foreign_ad_or_adoption_counterpart`: an EASA Safety Publication is a foreign AD or explicitly names a State-of-Design, adoption, prompted-by, or counterpart AD/publication relationship.
- `sib_or_foreign_safety_advisory`: an EASA SIB/Safety Information record or EASA-hosted foreign advisory record points to an official safety advisory, notice, bulletin, investigation, or similar source record.

Evidence sides:
- `easa_record`: the EASA Safety Publications Tool detail record or official EASA attachment.
- `related_record`: the official related record, another EASA record, or official related attachment.

For each relationship, preserve the EASA publication number, EASA type/status, issuer, issue date, effective date or no-effective-date state, subject, approval holder/type/model or broad category, relationship class, exact source-stated relationship language, related authority, related number/title/date, and attachment/PDF/ZIP locator where present. Keep SIBs and foreign advisory records at the category depth their official source gives; do not force them into AD/model-level fields.

The relationship map is descriptive publication provenance, not maintenance instructions, compliance advice, legal interpretation, applicability decisions, airworthiness verdicts, aircraft selection, fleet risk scoring, contact enrichment, or alerting.

Requirements:
- The page must be an official source for the claimed evidence side. EASA list pages, search result pages, and biweekly reports can help discovery, but they are not enough as the final source for a relationship edge unless the URL is a detail record or official attachment carrying the claimed evidence.
- The page must identify the publication on the claimed evidence side and provide side-appropriate provenance metadata: number/title, authority or issuer, issue or effective/no-effective-date state, subject, publication type/status, product/category scope, and attachment/PDF/ZIP locator where present.
- The page must support the side-specific relationship evidence. For `easa_record`, the EASA source must explicitly state the relationship to the related record. For `related_record`, the source must be the official related publication or attachment identified by the relationship, and any relationship language present on that source must be preserved rather than replaced by inference.

Write one JSON object per line to `results_easa_publication_relationship_provenance.jsonl`:
{"item": { "relationship_class": "<relationship_class>", "easa_publication": "<easa_publication>", "related_authority": "<related_authority>", "related_publication": "<related_publication>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

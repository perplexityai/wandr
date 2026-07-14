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

## `italpreziosi_relationships`

Build a public-source provenance table for Italpreziosi as of 16 June 2026. For each of the 5 core evidence families below, provide 25+ distinct provenance units, each with 1+ public URL that supports the unit.

This is a provenance task: record what public sources state, what period or status they support, and what they do not prove. It is not a task to reconstruct the complete real-world supply chain.

Core evidence families:
- `relationship_edge`: a source-stated named relationship or value-chain role involving Italpreziosi and another named entity or status body.
- `ownership_participation`: source-stated ownership, shareholding, participation, subsidiary, accounting holding, control, or beneficial-owner evidence. Preserve exactly which of those the source says.
- `corporate_event`: a dated or period-bound participation, JV, lineage, mine/off-take, processing, technology, licensing, or comparable corporate/value-chain event.
- `certification_status`: a certification, accreditation, membership, good-delivery, audit, or standard-body status unit with scope and period where public.
- `responsible_sourcing_claim`: a named responsible-sourcing initiative, program, due-diligence, traceability, or sustainability claim around Italpreziosi.

Each provenance unit should name the linked entity or status body and a concise claim label. The source should support the unit itself, not merely mention Italpreziosi near an unrelated entity.

Public customs/trade snippets and broad stakeholder or nonproof caveats are supplemental details, not separate evidence families. Use them only when they directly support or limit a core provenance unit.

For each row, report the relationship/status category, source-stated wording or precise paraphrase, source class, date/period or missing-date state, current/historical/unknown state, ownership/control evidence only when source-stated, and the limitation or nonproof state carried by the source. Geography and similar context notes are auxiliary: include them when the source provides them, but do not invent them or treat them as a separate proof obligation.

Requirements:
- The page must explicitly connect Italpreziosi to the linked entity, status body, event, claim, or limitation. For rows not hosted by Italpreziosi, the page still needs to make the Italpreziosi connection visible.
- The page must fit the evidence family. Ownership/control/shareholding claims need filings, registry material, annual reports, counterparty reports, official statements, or similarly strong source surfaces. Certification/status rows must use standard-body, certificate, membership, audit, or official company certification pages. Responsible-sourcing rows must use standard-body, initiative, audit, due-diligence, sustainability-report, or official company responsibility pages. Public customs/trade snippets may support `relationship_edge` or `corporate_event` rows only when they name parties and shipment context, and those snippets remain partial.
- Preserve direction and support level. Italpreziosi holding shares in an entity, an entity naming Italpreziosi as buyer, a standard body certifying Italpreziosi, and a company page listing broad stakeholder classes are different claims.
- Preserve source boundaries. A certification is not supplier-identity proof, a broad stakeholder class is not a named customer relationship, a customs snippet is not complete trade coverage or a largest-customer ranking, and an accounting value is not a control percentage unless the source says so.
- Reject investment analysis, valuation, supply-chain strategy, customer targeting, largest-customer ranking, beneficial-ownership inference beyond source wording, legal/compliance advice, procurement advice, outreach, lead scoring, contact enrichment, or wrongdoing conclusions.

Write one JSON object per line to `results_italpreziosi_relationships.jsonl`:
{"item": { "evidence_family": "<evidence_family>", "linked_entity_or_status_body": "<linked_entity_or_status_body>", "provenance_claim": "<provenance_claim>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

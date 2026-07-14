You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `german_medtech_services`
  - `german_medtech_services.germany_presence`

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

## `german_medtech_services`

For 150+ medical-device or IVD go-to-market service firms, cover at least 3+ of the capability facets below for each firm, with 1+ URL for each firm-facet pair.

Capability facets:
- `regulatory_mdr_qms`: MDR/IVDR regulatory affairs, quality management systems, technical documentation, clinical/performance evaluation, conformity strategy, or related compliance consulting for medical devices or IVDs.
- `market_access_registration`: market-entry strategy, country registration, reimbursement/access pathway support, approval strategy, product registration, or equivalent market-access work for medical devices or IVDs.
- `economic_operator_channel`: authorised representative, importer, distributor, legal manufacturer, responsible-person, wholesale, specialist trade, channel, logistics, or comparable economic-operator services for medical devices or IVDs.
- `lifecycle_pms_reprocessing_service`: post-market surveillance, vigilance, PMCF/PMPF, complaint handling, maintenance, repair, reprocessing, sterilization, or other lifecycle service after placing on the market.
- `certification_accreditation_testing`: notified-body/conformity assessment, ISO 13485 or comparable certification, ISO/IEC 17025 or comparable lab accreditation, product testing, validation, safety, EMC, biological, cybersecurity, or usability testing for medical devices or IVDs.

The useful evidence separates raw public service claims from derived business-model interpretation. Directory and member-list pages can help discover firms, but each capability claim needs a page whose own content visibly carries the capability signal. Eligible capability sources include firm-owned service pages, official certification or accreditation pages, regulator or notified-body pages, and comparable authoritative pages.

Requirements:
- The page must clearly identify the named firm.
- The page must tie the firm or offering to medical devices, IVDs, medtech, or medical technology.
- The page must make its facet-appropriate source role visible.
- The page must expose a concrete capability claim for the reported facet.

Write one JSON object per line to `results_german_medtech_services.jsonl`:
{"item": { "firm": "<firm>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `german_medtech_services.germany_presence`

Cross-tasknode identifier discipline: this task is for the same {= firm =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= firm =}+ firms, supply 1+ German-presence URL each.

A German-presence URL should identify the firm and ground a German office, German legal entity, German trade-association membership, German certified or accredited site, or comparable Germany-specific operating presence. Official firm pages, imprint/contact/location pages, BVMed/SPECTARIS or comparable member profiles, regulator/notified-body/accreditation listings, and official certificates can all work when they visibly tie the firm to Germany.

Requirements:
- The page must clearly identify the named firm.
- The page must be a source type that can credibly ground firm presence.
- The page must tie the firm to Germany through an address, office, subsidiary, member profile, location listing, certified/accredited site, or Germany-specific legal or operating identity.

Write one JSON object per line to `results_german_medtech_services.germany_presence.jsonl`:
{"item": { "firm": "<firm>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

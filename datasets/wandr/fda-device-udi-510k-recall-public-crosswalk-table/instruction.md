You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `fda_device_udi_510k_recall_public_crosswalk_table`
  - `fda_device_udi_510k_recall_public_crosswalk_table.udi_identity`
  - `fda_device_udi_510k_recall_public_crosswalk_table.pathway_record`
  - `fda_device_udi_510k_recall_public_crosswalk_table.identity_conflict_or_note`

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

## `fda_device_udi_510k_recall_public_crosswalk_table`

For 150+ affected medical-device products named in official FDA device recall or early-alert records with a posted, classified, report, or initiation date from 2023-01-01 through 2025-12-31, name the FDA record identity, affected product, and firm/labeler as the `recalled_or_alerted_product`; declare 1 record type per product (`classified_recall` or `early_alert`); and supply 1+ official FDA recall or early-alert record URL.

This is a regulatory-provenance crosswalk, not a safety, clinical, legal, procurement, or recall-response task. A recall or early-alert row is only an FDA record object with source-stated identity, date, status, and classification fields.

Use official FDA medical-device recall database pages, FDA medical-device recall or early-alert pages, and official FDA/openFDA machine-readable recall/enforcement records. openFDA JSON is acceptable when direct FDA CFdocs pages are blocked, but rows still need source-specific record fields and affected-product identity evidence.

Record type labels:
- `classified_recall`: an FDA medical-device recall/enforcement record that FDA has classified or reported as a recall.
- `early_alert`: an FDA medical-device early-alert page or record where FDA has not necessarily classified/confirmed the action as a recall. Do not rewrite it as a classified recall unless FDA itself says so.

Requirements:
- The page must expose the FDA recall or early-alert record identity, the declared record type, a source-stated classification/status or early-alert state, and a relevant date within 2023-01-01 through 2025-12-31.
- The page must identify the claimed affected product through product description/name plus recalling firm, manufacturer, labeler, model, catalog, REF, DI/UDI/GTIN, code information, or comparable source-stated identity details.

Do not count manufacturer marketing pages, distributor listings, recall-news aggregators, MAUDE/adverse-event pages, clinical advice pages, safety rankings, or pages used to tell users what action to take.

Write one JSON object per line to `results_fda_device_udi_510k_recall_public_crosswalk_table.jsonl`:
{"item": { "recall_or_alert_id": "<recall_or_alert_id>", "affected_product": "<affected_product>", "firm_or_labeler": "<firm_or_labeler>", "recall_or_alert_record_type": "<recall_or_alert_record_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `fda_device_udi_510k_recall_public_crosswalk_table.udi_identity`

Cross-tasknode identifier discipline: this task is for the same {= recalled_or_alerted_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= recalled_or_alerted_product =}+ FDA recalled or early-alerted medical-device products in the 2023-01-01 through 2025-12-31 window, name 1+ matching public UDI/GUDID identity per product using the DI/UDI and device name, and supply 1+ official AccessGUDID/NLM or FDA UDI URL.

The UDI row must resolve the same affected product named in the recall or early alert. Prefer AccessGUDID pages/API records; official openFDA UDI records are acceptable when they expose the same source-specific fields.

Requirements:
- The page must show a DI/UDI identity, brand/device name or description, labeler/company, and product code or premarket submission when the source states one.
- The page must support a substantive match to the recalled or alerted product through DI/UDI/GTIN, model, catalog, REF, product code, brand/device description, labeler/firm, premarket number, or product-description overlap.

Do not count package GTINs as primary DIs unless the official UDI/GUDID surface states that relationship. Name-only similarity between a recall product description and a UDI brand name is not enough.

Write one JSON object per line to `results_fda_device_udi_510k_recall_public_crosswalk_table.udi_identity.jsonl`:
{"item": { "recall_or_alert_id": "<recall_or_alert_id>", "affected_product": "<affected_product>", "firm_or_labeler": "<firm_or_labeler>", "di_or_udi": "<di_or_udi>", "udi_device_name": "<udi_device_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `fda_device_udi_510k_recall_public_crosswalk_table.pathway_record`

Cross-tasknode identifier discipline: this task is for the same {= recalled_or_alerted_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= recalled_or_alerted_product =}+ FDA recalled or early-alerted medical-device products in the 2023-01-01 through 2025-12-31 window, choose 1 actual FDA pathway type per product (`510k`, `pma`, `de_novo`, or `classification_or_exemption`), name 1+ pathway or classification record, and supply 1+ official FDA pathway/classification URL.

The pathway row must be positive pathway evidence for the same affected product, not a claim that no 510(k) exists. Use FDA 510(k), PMA, De Novo, product-classification, exemption, or official openFDA pathway/classification surfaces.

Requirements:
- The page must show the pathway type and record number or classification, device name, applicant/manufacturer or product code, and source-stated decision, classification, status, or date fields where available.
- The page must support a substantive match to the recalled or alerted product through product code, device name/description, applicant/labeler/recalling-firm relationship, K/PMA/De Novo number, model/catalog/REF, DI/UDI record linkage, or comparable official identity bridge.

Do not use generic no-510(k) or no-clearance claims. If the product is PMA, De Novo, classified/exempt, or otherwise not represented by a 510(k), cite that positive official pathway or classification surface instead.

Write one JSON object per line to `results_fda_device_udi_510k_recall_public_crosswalk_table.pathway_record.jsonl`:
{"item": { "recall_or_alert_id": "<recall_or_alert_id>", "affected_product": "<affected_product>", "firm_or_labeler": "<firm_or_labeler>", "pathway_type": "<pathway_type>", "pathway_record_id": "<pathway_record_id>", "pathway_device_name": "<pathway_device_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `fda_device_udi_510k_recall_public_crosswalk_table.identity_conflict_or_note`

Cross-tasknode identifier discipline: this task is for the same {= recalled_or_alerted_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= recalled_or_alerted_product =}+ FDA recalled or early-alerted medical-device products in the 2023-01-01 through 2025-12-31 window, choose 1 identity note type per product (`corroboration` or `substantive_conflict`), name 1+ concrete official-source identity bridge or conflict note, and supply 1+ official FDA/NLM URL that corroborates or contradicts the product identity chain.

This sidecar keeps identity discipline visible. Most rows can use `corroboration` for an official non-name-only bridge; use `substantive_conflict` only when official FDA/NLM surfaces substantively disagree on an identity field.

Requirements:
- The page must support the declared note through source-stated identifiers or entity fields such as DI/UDI/GTIN, model, catalog, REF, product code, brand/device name, labeler, applicant, recalling firm, K/PMA/De Novo number, or product description.
- `corroboration` notes must use a non-name-only official bridge, and `substantive_conflict` notes must identify a substantive official-field disagreement rather than a cosmetic spelling, punctuation, abbreviation, or legal-suffix variant.

Do not invent confidence scores. Do not count generic no-UDI, no-product-code, no-recall, or no-510(k) statements as identity notes.

Write one JSON object per line to `results_fda_device_udi_510k_recall_public_crosswalk_table.identity_conflict_or_note.jsonl`:
{"item": { "recall_or_alert_id": "<recall_or_alert_id>", "affected_product": "<affected_product>", "firm_or_labeler": "<firm_or_labeler>", "identity_note_type": "<identity_note_type>", "identity_note": "<identity_note>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

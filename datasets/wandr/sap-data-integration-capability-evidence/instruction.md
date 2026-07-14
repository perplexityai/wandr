You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `sap_data_integration_capability_evidence`
  - `sap_data_integration_capability_evidence.cloud_targets`

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

## `sap_data_integration_capability_evidence`

For 30+ distinct public SAP data-integration tools or services, provide at least 2+ named SAP source-surface rows per tool, with one public evidence URL for each tool/source-surface row.

A row qualifies when the page proves that the named tool/service can extract, replicate, sync, ingest, federate, share, expose, connect to, or otherwise make usable data from the claimed SAP source surface. Use one of these canonical source-surface families: S/4HANA Cloud, S/4HANA On-Premise or Private Cloud, ECC or NetWeaver, BW or BW/4HANA, SAP HANA or CDS Views, ODP, SAPI, or BW Extractors, SAP Datasphere or Business Data Cloud, SLT or Replication Flow.

Use current public evidence. Do not reconstruct a strict historical web state or make SAP Note 3255746, SAP certification, pricing, customer adoption, procurement fit, migration strategy, or vendor ranking the controlling artifact.

Good evidence sources include SAP Help/Architecture/Learning/product docs, vendor product/help/connector docs, hyperscaler or platform docs, concrete marketplace pages, and SAP-hosted partner/product pages that state the limited capability. Do not use generic "best SAP ETL tools" listicles, G2/Gartner/Domo/Integrate.io/SolutionsReview-style pages, Reddit/forum anecdotes, procurement or architecture advice, generic SAP partner badges, or SAP Store listings that only prove listing/status.

Requirements:
- Tool identity: the page must identify the named tool/service or an accepted same-product alias.
- SAP source match: the page must identify the claimed SAP source surface, or specific SAP product/interface language that maps cleanly to that source-surface family.
- Data-access capability: the page must state a source-bound data-access capability for that tool/source relation.

In `answer`, include a concise `capability_summary` and any source-stated `source_date` if visible. Do not fabricate missing dates or exact pricing.

Write one JSON object per line to `results_sap_data_integration_capability_evidence.jsonl`:
{"item": { "tool": "<tool>", "sap_source_surface": "<sap_source_surface>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `sap_data_integration_capability_evidence.cloud_targets`

Cross-tasknode identifier discipline: this task is for the same {= tool =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For the named public SAP data-integration tools or services, provide at least 2+ cloud or analytics target rows per tool, with one public evidence URL for each tool-target row.

A row qualifies when the page proves that the same named tool/service supports the claimed target as a destination, sharing surface, analytics platform, data warehouse, data lake, stream, open-table format, or SAP data-platform target. Examples of good target labels include Snowflake, Databricks, Google BigQuery, Amazon S3, Amazon Redshift, Azure Synapse, Azure Data Lake Storage, Fabric OneLake, Kafka, Apache Iceberg, SAP Datasphere, or SAP HANA; other named targets are allowed when the page is target-specific.

The target URL does not have to restate every SAP source surface because root evidence separately proves the tool's SAP data-integration role. It must still contain substantive target-specific evidence for the claimed tool-target relation. Do not reuse a generic "40+ targets" or "any cloud" catalog for many target rows unless the page has a target-specific section, instructions, marketplace listing, or comparable substance for that target.

Requirements:
- Tool identity: the page must identify the named tool/service or an accepted same-product alias.
- Target identity: the page must identify the claimed cloud or analytics target.
- Target support: the page must state that the tool supports the target through loading, replication, sharing, writing, exposure, connectivity, or comparable target-specific support.

In `answer`, include a concise `target_support_summary` and any source-stated `source_date` if visible. Do not fabricate missing dates or exact pricing.

Write one JSON object per line to `results_sap_data_integration_capability_evidence.cloud_targets.jsonl`:
{"item": { "tool": "<tool>", "target": "<target>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

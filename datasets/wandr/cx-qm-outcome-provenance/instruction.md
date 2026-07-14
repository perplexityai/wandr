You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `cx_qm_outcome_provenance`
  - `cx_qm_outcome_provenance.partial_source_audit`

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

## `cx_qm_outcome_provenance`

For 20+ vendors offering CX quality management, QA automation, interaction analytics, conversation analytics, speech/text analytics, agent coaching analytics, or closely comparable contact-center analytics products, cover 3+ public customer, study, deployment, or source-described use-case outcome contexts per vendor. For each context, include 1+ scoped use-case family and at least 2+ source-stated quantitative customer/study/deployment outcome metric, with 1+ public leaf URL for each metric.

This is an as-of April 14, 2026 provenance table. It is not a vendor comparison, ranking, buyer guide, procurement recommendation, ROI projection, sales-targeting list, outreach list, lead-scoring table, or contact-enrichment dataset.

Use one of these `named_state` labels for each affirmative outcome context:
- `named_customer`
- `anonymous_customer`
- `composite_study`
- `source_described_industry_only`

Affirmative records are about outcome provenance, not product capability inventory. The source must anchor the metric to a named customer deployment, source-described anonymous deployment, composite or named study, or source-described industry/use-case deployment. Product pages, datasheets, generic capability claims, and "100% of interactions analyzed/scored" style product-capability numbers do not count in the main table unless the same page also ties the number to a customer, study, deployment, or use-case outcome. Capability-only sources belong in the partial-source diagnostic sidecar, not as padding in the affirmative rows.

Affirmative metric records should preserve the product/module or suite, source role in free text, source authorship or hosting, source date or observed date, checked date, confidence, and a short scope note when those are known.

The cited URL should be the leaf source that states the metric, not a search result, source hub, generic metric-definition page, market-size statistic, ranking/comparison/buyer-guide page, broad product page, ROI center, customer-story index, or gated teaser that does not itself state the claimed metric and context. A source published after April 14, 2026 does not count as affirmative evidence unless the page itself establishes that the same source was public by the cutoff date.

Build breadth across vendors, customers/studies/deployments, use cases, outcome families, source domains, and leaf URLs. Do not let one vendor hub, one TEI study page/PDF, one ROI-center page, one customer-story index, one source domain, or one exact URL carry a large share of the answer. As a practical cap, use at most two affirmative rows from any exact URL, and only when the same leaf page directly states distinct metrics for the same source context. Extra rows mined from the same hub, landing page, study summary, or generic product page are padding.

Requirements:
- The page must identify the claimed vendor and product/module or clearly named product suite tied to the metric.
- The page must tie the metric to a scoped QM, QA automation, interaction analytics, conversation analytics, speech/text analytics, agent coaching analytics, workforce-quality, or comparable contact-center analytics use case.
- The page must anchor the metric to the claimed named customer, anonymous customer/deployment, composite or named study, or source-described industry/use-case deployment consistent with `named_state`.
- The page itself must state the exact numeric value and unit for the claimed metric; do not infer or estimate numbers.
- The page must be a fitting provenance source for the claimed metric by directly stating the metric, source scope, vendor/product tie, and customer/study/deployment attribution.
- The cited URL must be specific enough to the submitted row rather than a shared hub, ROI center, story index, generic product page, gated teaser, or repeatedly reused study summary that only points toward the real evidence.

Write one JSON object per line to `results_cx_qm_outcome_provenance.jsonl`:
{"item": { "vendor_name": "<vendor_name>", "customer_or_study_name": "<customer_or_study_name>", "named_state": "<named_state>", "use_case_family": "<use_case_family>", "outcome_family": "<outcome_family>", "metric_type": "<metric_type>", "numeric_value": "<numeric_value>", "numeric_unit": "<numeric_unit>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `cx_qm_outcome_provenance.partial_source_audit`

Cross-tasknode identifier discipline: this task is for the same {= vendor =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For each covered vendor offering CX quality management, QA automation, interaction analytics, conversation analytics, speech/text analytics, agent coaching analytics, or closely comparable contact-center analytics products, provide 1+ public tempting source per vendor that should not be counted as an affirmative CX QM or conversation-analytics outcome metric source as of April 14, 2026. Classify each source with one `partial_state`, name the source, and supply 1+ URL.

Allowed `partial_state` labels:
- `no_quant_metric`
- `no_product_link`
- `platform_scope_only`
- `composite_scope_only`
- `product_capability_only`
- `out_of_window`
- `name_conflict`
- `gated_or_insufficient_detail`
- `generic_or_ranking_source`

These records are narrow provenance abstentions. They do not count toward the affirmative customer/study/deployment outcome rows, and they should not be used as filler when stronger affirmative evidence is missing. They should explain why this public source is insufficient for an affirmative metric record; they should not claim no public evidence exists for the vendor, rank vendors, recommend products, project ROI, create sales targets, identify leads, support outreach, or enrich contacts.

Requirements:
- The page must identify the claimed vendor, a relevant product, or a clearly related CX QM / conversation-analytics domain.
- The page should be plausibly tempting for this provenance task, such as a vendor resource, product page, TEI or analyst landing page, customer hub, ranking/comparison page, press item, broad platform story, or similar public surface.
- The page must support the claimed partial or invalid reason from its content, URL, source framing, or date evidence, including product-capability-only pages that state a product number but no customer/study/deployment outcome.
- The submitted finding should keep the abstention narrow to this source and avoid global source-absence, ranking, recommendation, ROI projection, sales, outreach, lead, or contact-enrichment framing.

Write one JSON object per line to `results_cx_qm_outcome_provenance.partial_source_audit.jsonl`:
{"item": { "vendor_name": "<vendor_name>", "partial_state": "<partial_state>", "source_name": "<source_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

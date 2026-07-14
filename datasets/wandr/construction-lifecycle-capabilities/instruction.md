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

## `construction_lifecycle_capabilities`

For each of the 8 construction/property lifecycle topics below, supply source-backed product capability signals: at least 45+ per topic, with at least 1+ page-specific URL per signal. Eligible signals come from public software providers serving construction, property, handover, FDV/FM, facilities, project-management, document-analysis, issue-detection, buyer/resident, maintenance, service, or adjacent built-environment workflows.

A product capability signal is a named company/provider, a named product or module, and a concrete capability stated or directly described by the cited source. The same company may appear in several lifecycle topics when different product/module capabilities are supported by topic-specific pages.

Lifecycle topics:
- `planning_design_review`: planning, preconstruction, estimating, tendering, design coordination, model coordination, plan check, drawing review, or design-change review
- `project_controls`: project management, schedule, cost, contract, change, RFI, submittal, commercial, risk, or portfolio-control workflows during delivery
- `document_knowledge`: searching, classifying, extracting, summarizing, assuring, or querying drawings, specifications, O&M manuals, certificates, reports, photos, or other construction/property documents
- `field_quality_safety`: site inspections, punch lists, QA/QC, defects, issues, observations, permits, safety, or field task capture
- `reality_progress`: reality capture, 360/photo/video site records, computer-vision progress, quantity/progress measurement, delay detection, deviation detection, or out-of-sequence work signals
- `handover_closeout`: handover, closeout, commissioning, as-builts, O&M package assembly, defect closeout, owner turnover, or construction-to-operation transition
- `operations_maintenance`: FDV/FM, facilities operations, asset management, planned maintenance, reactive maintenance, service reports, compliance documentation, or building operations
- `resident_buyer_service`: homebuyer, resident, tenant, customer-care, warranty, defect-reporting, aftercare, homeowner portal, or buyer communication workflows

Sources should be public, accessible, and page-specific to the submitted product/module capability. Official product, feature, documentation, support, release-note, case-study, marketplace, and public-demo pages work naturally; reputable industry articles can work when they identify the product/module and capability. Generic homepages, search pages, unsourced rankings, broad market maps, investor/pitch pages, and procurement recommendation pages do not carry a capability signal by themselves.

This is a public capability-evidence atlas, not a ranking, recommendation list, procurement guide, investor pitch, market-gap analysis, or closed vendor canon.

Requirements:
- The page must clearly identify the named company/provider and product or module as built-environment software.
- The page must tie the submitted capability to the row's lifecycle topic.
- The page must expose a concrete product/module capability stated or directly described by the source; a generic "AI-powered platform" or "digital transformation" claim is not enough.
- If the submitted capability uses AI, machine-learning, assistant, computer-vision, agentic, automation, or comparable intelligent-workflow wording, the page must explicitly support that wording.

Write one JSON object per line to `results_construction_lifecycle_capabilities.jsonl`:
{"item": { "lifecycle_topic": "<lifecycle_topic>", "company": "<company>", "product_or_module": "<product_or_module>", "capability_signal": "<capability_signal>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

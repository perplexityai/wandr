You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `uk_tax_software_evidence`
  - `uk_tax_software_evidence.operating_entity`

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

## `uk_tax_software_evidence`

For 45+ named software products, apps, or product lines used for UK tax, Self Assessment, Making Tax Digital, freelancer bookkeeping, landlord accounting, or small-business accounting, cover at least 4+ of the evidence facets below for each product by supplying a public evidence source (1+ URL under each facet).

The product universe is open: tax apps, self-assessment tools, MTD products, bookkeeping products, bridging tools, and larger-vendor product lines can all work when the page evidence is product-specific. Listicles and comparison pages can help discover products, but they do not satisfy the hard facets unless the facet's source bar below admits that source class.

Evidence facets:
- `category_scope`: official product or company evidence that the product is for UK tax, Self Assessment, Making Tax Digital, freelancer bookkeeping, landlord accounting, or small-business accounting
- `pricing`: official current pricing or plan evidence with a public price, free plan, or clearly source-stated commercial posture
- `recognition_claim`: vendor-controlled wording claiming HMRC, MTD, Self Assessment, or other tax-recognition status, preserving the named regime when the page names one
- `recognition_registry`: GOV.UK or HMRC authority evidence naming the product for a specific recognition regime
- `feature_or_customer_signal`: official product, support, blog, app-store, or professional-directory evidence for a specific feature, user class, filing capability, customer count, or adoption claim
- `source_stated_provenance`: source-stated funding, acquisition, ownership, launch, incorporation, crowdfunding, or positive bootstrapped/self-funded fact

Requirements:
- The page must clearly identify the claimed software product, app, or product line.
- The page should fit the source role required by `evidence_facet`. `category_scope` and `pricing` need official vendor/product surfaces; `recognition_claim` needs a vendor-controlled surface; `recognition_registry` needs a GOV.UK or HMRC authority surface; `feature_or_customer_signal` needs official product/support/blog, app-store, or professional-directory evidence; `source_stated_provenance` needs a source-stated official, investor/crowdfunding, reputable press, Companies House, or labeled-database source.
- The page must state a concrete fact or claim for the facet. For recognition evidence, preserve the exact regime the page supports or claims. For provenance, the source must state the fact positively; absence-inferred bootstrapping, ARR/MRR, valuation, and solver-derived headcount do not count.

Write one JSON object per line to `results_uk_tax_software_evidence.jsonl`:
{"item": { "software_product": "<software_product>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `uk_tax_software_evidence.operating_entity`

Cross-tasknode identifier discipline: this task is for the same {= software_product =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= software_product =}+ UK tax or accounting software products, resolve one operating legal entity per product (at least 1 product/entity pair per product) and cover each of the 2 legal-entity source types below by supplying a public source (1+ URL under each source type).

Legal-entity source types:
- `vendor_legal_disclosure`: vendor-controlled legal, footer, terms, privacy, contact, or similar disclosure tying the product or trading brand to a legal entity or company number
- `companies_house_record`: Companies House company record confirming the legal entity, company number, status, or incorporation details

Companies House name search alone is not enough for ambiguous product brands. The vendor-side source should tie the product, trading name, site, or company number to the legal entity; the Companies House source should then confirm that legal entity.

Requirements:
- The page should fit the source role required by `entity_source_type`: vendor-controlled legal disclosure for `vendor_legal_disclosure`, or an actual Companies House company record for `companies_house_record`.
- The page must provide source-type-specific entity evidence. For `vendor_legal_disclosure`, it should connect the product, site, trading style, or company number to the claimed legal entity. For `companies_house_record`, it should confirm the claimed legal entity, company number, status, registered name, or incorporation details.

Write one JSON object per line to `results_uk_tax_software_evidence.operating_entity.jsonl`:
{"item": { "software_product": "<software_product>", "legal_entity": "<legal_entity>", "entity_source_type": "<entity_source_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

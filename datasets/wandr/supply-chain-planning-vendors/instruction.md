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

## `supply_chain_planning_vendors`

For 50+ companies that offer public software products or platforms used for supply-chain planning, cover the 5 evidence axes below. For each company and axis, supply public evidence URLs (1+ per company/axis) whose pages affirmatively support axis-specific evidence records.

This is a provenance atlas, not a vendor shortlist. Keep the record factual: name the relevant product or platform when available, summarize the source-backed finding, label the source class and claim posture, and give the source date/as-of posture or a checked date for undated pages. Do not rank vendors, recommend products, score buyer fit, make ROI claims, build implementation plans, collect contacts, or create lead lists.

Evidence axes:
- `market_presence`: public third-party or source-class-labeled evidence that the company/product appears in the supply-chain-planning software market
- `planning_scope`: evidence of concrete planning functions such as demand planning, supply planning, S&OP/IBP, replenishment, allocation, inventory optimization, scenario planning, or planning orchestration
- `ai_or_optimization`: product-specific AI, machine-learning, optimization, probabilistic forecasting, scenario-agent, or decision-automation evidence tied to planning work
- `retail_vertical_fit`: retail, grocery, apparel, merchandising, store/DC, omnichannel, replenishment, allocation, or retail customer/deployment evidence
- `deployment_or_integration`: concrete deployability evidence such as developer/docs/API surfaces, connector or integration docs, marketplace listings, partner implementation pages, third-party connectors, or public customer deployment/use pages

Source class labels:
- `independent_analyst_or_review`: analyst, review, or peer-insight category surface not controlled by the vendor
- `trade_press_or_category`: trade press, industry article, or category directory
- `official_product_or_solution`: vendor-controlled product, solution, platform, resource, or company page
- `official_docs_or_developer`: vendor-controlled documentation, support, developer, API, or technical operations page
- `marketplace_or_platform_registry`: public marketplace, app registry, cloud platform listing, or certified-solution registry
- `customer_story_or_deployment`: public customer story, deployment page, case study, or named customer-use source
- `partner_or_integrator`: partner, systems integrator, implementation, or alliance page
- `third_party_connector`: connector vendor, integration-platform, or middleware page outside the SCP vendor's own channels
- `vendor_press_or_newsroom`: vendor newsroom, press release, blog announcement, or sponsored release
- `critical_or_conflict_source`: critical, corrective, limitation, conflict, or counterclaim source

Claim-status labels:
- `directly_supported`: the cited page directly supports the submitted axis finding without extra source-posture claims
- `vendor_claim_only`: the page is vendor-controlled or vendor-distributed and should be read as a vendor claim
- `independently_supported`: the page is independent of the vendor and supports the finding
- `limitation_or_conflict`: the page affirmatively states a limitation, conflict, criticism, or narrower counterpoint for the axis

Valid companies should have a public software product or platform plausibly used for supply-chain planning, planning orchestration, demand/supply planning, S&OP/IBP, replenishment, allocation, inventory optimization, scenario planning, or adjacent planning workflows. Pure WMS, TMS, freight visibility, execution-only logistics, generic ERP, generic analytics, consulting-only, POS, ecommerce, or contact-data vendors do not count unless the cited page ties a named product to planning work.

Analyst, review, category, and trade sources are useful for market presence and discovery. They do not automatically prove planning scope, AI/optimization, retail fit, or deployment/integration. Vendor-owned pages are useful for product claims, but source class and claim status should make the vendor-owned posture visible. One broad homepage, analyst listing, or SEO listicle should not fill every axis for the same company.

The `limitation_or_conflict` claim posture still needs affirmative public evidence: the page must state a limitation, contradiction, criticism, narrower scope, or counterpoint about the selected axis. An absence-only search note, gated-page shell, or statement that the page lacks axis details does not count for the company/axis URL slot.

Requirements:
- The page must identify the company, product, or platform and tie it to supply-chain-planning software or a planning-adjacent workflow.
- The page must make its source role and the submitted claim posture credible for the record.
- The page must support the selected evidence axis with a page-specific affirmative finding, including a concrete limitation or conflict when that claim posture is used.
- Any source date, update date, publication date, as-of date, or checked-date posture in the record must fit what the page shows or reasonably permits.

Write one JSON object per line to `results_supply_chain_planning_vendors.jsonl`:
{"item": { "company": "<company>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

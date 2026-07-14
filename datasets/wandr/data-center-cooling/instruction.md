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

## `data_center_cooling`

For each of the 4 data-center cooling claim types listed below, cover 10+ vendors; for each vendor, name 2+ public capability claims; for each claim, attach 2+ labeled public source classes and 1+ URL per source class that substantiates the claim.

This is public thermal-infrastructure claim normalization, not vendor ranking, procurement advice, or a PUE/WUE comparison table. The vendor and solution universe is open: do not limit work to seed vendors, and treat acquired brands or aliases as the same vendor/solution when the public evidence makes that clear.

Claim types:
- `technical_product_capability`: Named-product or named-solution technical capability claims, such as direct-to-chip, immersion, CDU/HDU, rear-door/rack, chiller/heat-rejection, hybrid air-liquid, waterless, evaporative, retrofit, or high-density operating capability, when the page ties that capability to a concrete product, model family, or source-framed solution.
- `numeric_metric`: Exact numeric capacity, density, efficiency, water, temperature, facility-scale, or study/model metric claims.
- `deployment_or_customer_reference`: Named deployment, customer/operator, counterparty, installation, case-study, or project-reference claims that include cooling-capability substance.
- `validated_reference_or_study`: Validated reference-design, standards/OCP collaboration, official engineering-study, or modeled-design claims with named design scope, assumptions, or measured/model outputs.

Source classes:
- `product_page`: Official vendor product, product-family, or named solution page with concrete capability details, not a generic solution overview.
- `datasheet_download`: Official datasheet, brochure, technical manual, or downloadable product document.
- `press_release`: Official vendor, investor-relations, or newsroom press release.
- `case_study`: Official case study, customer-story, or project-reference page.
- `operator_counterparty_page`: Official operator, customer, partner, buyer, or counterparty page.
- `engineering_explainer`: Official engineering blog, white paper, technical explainer, or study summary with capability-specific substance.
- `reference_design`: Official reference design, validated architecture, blueprint, or standards/OCP-style design page.

The `vendor` should be the company or acquired brand that publicly owns, offers, supplies, or is credited with the cooling solution. The `solution` can be a product family, portfolio component, reference design, deployment/study context, or named cooling architecture when the source itself frames it that way. The `claim` should be a single source-specific capability claim, not a generic company blurb, product-category label, or broad AI-ready positioning statement.

Official blogs and explainers count when the claim is framed as an engineering explainer, study, reference design, or modeled capability. They do not by themselves prove a named product's measured capability unless the page itself ties that product or solution to the submitted claim.

Official vendor product pages, datasheets/downloads, press releases, case studies, operator/counterparty pages, engineering explainers, and reference designs can count when they directly support the submitted claim. Broad solution pages, portfolio overviews, and marketing pages do not count unless they visibly function as a named product or reference/design page and state the concrete submitted capability. Vendor-ranking pages, analyst listicles, market-size reports, SEO "top vendor" pages, reseller pages without vendor-backed documentation, social posts alone, generic news/trade coverage, and press-wire republications do not count.

Requirements:
- The page must tie the submitted vendor and solution to data-center cooling.
- The page must provide content anchors characteristic of the submitted source class, not just a URL pattern, site section, or inferred page label: product/family capability detail for `product_page`, document-style technical detail for `datasheet_download`, dated announcement substance for `press_release`, customer/project context for `case_study` or `operator_counterparty_page`, technical explainer or study substance for `engineering_explainer`, and design/validation scope for `reference_design`.
- The page must place the claim in a concrete evidence context: a named product/model family, named deployment or counterparty, validated reference design, standards collaboration, or official study/model.
- The page must support a capability claim of the submitted claim type.
- The page must explicitly state or directly substantiate the submitted capability claim; generic architecture/application language is insufficient.
- Numeric claims must preserve the exact value, unit, metric type, and source qualifiers or conditions, such as ranges, "up to" language, per-rack/per-tank context, study/model assumptions, approach-temperature conditions, future/provisioning language, or named deployment/reference-design scope.

Write one JSON object per line to `results_data_center_cooling.jsonl`:
{"item": { "claim_type": "<claim_type>", "vendor": "<vendor>", "solution": "<solution>", "claim": "<claim>", "source_class": "<source_class>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

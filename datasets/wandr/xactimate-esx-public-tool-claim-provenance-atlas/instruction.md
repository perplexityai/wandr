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

## `xactimate_esx_public_tool_claim_provenance_atlas`

Build an as-of 2026-06-29 public-source provenance atlas for software products and productized public tools in the property claims, insurance repair, restoration estimating, measurement/sketch, and adjacent claims-workflow ecosystem.

Find about 80-90 distinct products overall, with at least 70 unique qualifying products and about 300-340 product/facet/source records. Each accepted record is one product, one closed `claim_facet`, and one supporting URL. The credited source pool should include at least 60 records for each facet and at least 65 unique source domains.

Do not rectangular-pad the table by reusing one homepage for every facet of a product. As a rule, do not use the same URL for more than 2 facets for the same product, and never use one URL for all four facets. Same-URL reuse only qualifies when the cited excerpts point to distinct, facet-specific sections that independently satisfy each submitted facet.

The product universe is open. CapOut, ClaimsFlow, EstimateHub, and similar PDF-to-ESX tools are seed anchors and traps, not a closed canon. Keep the scope broadened to adjacent public ESX/export/import/sketch/restoration/claims platforms when the source explicitly touches Xactimate, ESX, Verisk, XactRestore, XactNet, XactAnalysis, Symbility, FML, SKX, Cotality, or an equivalent property-claims estimating workflow.

The closed `claim_facet` values are:
- `conversion_or_estimate_input_capability`: The source states what the product converts, extracts, creates, imports, exports, captures, compares, or otherwise accepts/produces for an insurance, restoration, or claims-estimating workflow.
- `xactimate_esx_workflow_mechanism`: The source states a concrete Xactimate, ESX, Verisk, XactRestore, XactNet, XactAnalysis, Symbility, FML, SKX, Cotality, import/export, direct-delivery, Request Data, partner/API, or comparable workflow path. Bare 'integrates with Xactimate' language is not enough.
- `commercial_access_posture`: The source states public price amounts, per-file/per-area/per-line usage terms, credits, a free trial or free conversion, subscription tier access, or an explicit quote/demo/contact-sales path.
- `terms_trust_or_limitation_posture`: The source states relevant service terms, privacy/security/data-handling posture, trust-center posture, accuracy or turnaround limits, refund constraints, or other explicit guarantees/disclaimers tied to the product's estimating/conversion claims.

Missing facets are omissions. Do not submit `no_pricing_source`, `no_speed_source`, `no_accuracy_source`, `no_integration_source`, `no_date`, `name_conflict`, or similar missingness/conflict rows as positive evidence.

Product kinds to use as metadata, not hierarchy axes:
- `dedicated_pdf_to_esx_converter`: A product primarily framed around converting estimate PDFs into ESX/Xactimate artifacts.
- `adjacent_esx_export_or_import_tool`: A product whose public claim centers on ESX/Xactimate/Symbility import, export, delivery, comparison, or bridge workflow.
- `claims_estimating_or_restoration_platform`: A restoration, claims, job-management, or estimating platform with a concrete public Xactimate/ESX/Verisk/Symbility/Cotality workflow claim.
- `measurement_sketch_or_photo_to_estimate_tool`: A measurement, sketch, photo, scan, roof, floor-plan, or 3D-capture tool with a concrete public estimating-workflow output claim.

Source classes to use as metadata, not hierarchy axes:
- `official_product_page`: Product, feature, homepage, or landing page controlled by the product/vendor.
- `official_pricing_page`: Vendor-controlled pricing, plan, checkout, quote, or cost page.
- `official_docs_or_help`: Vendor-controlled help center, docs, support, FAQ, or tutorial page.
- `official_terms_trust_or_security`: Vendor-controlled terms, privacy, trust, security, or legal/support-limits page.
- `official_blog_press_or_demo`: Vendor-controlled blog, press, changelog, webinar, demo, or product-update page.
- `software_marketplace_listing`: Marketplace listing that directly identifies the product and relevant workflow.
- `counterparty_or_platform_page`: Verisk, Cotality, Symbility, partner, or other counterparty page directly naming the product and workflow.
- `reputable_trade_article`: Reputable trade, industry, or professional publication directly naming the product and workflow.

Commercial access types to use as metadata when relevant, not hierarchy axes:
- `public_price_amount`: A stated dollar/price amount.
- `usage_credit_or_line_item_terms`: A stated per-file, per-export, per-line-item, per-area, credit, or usage term.
- `free_trial_or_free_credits`: A stated free trial, free conversion, free credits, or no-card/free-start path.
- `subscription_tier`: A stated plan/tier/subscription access condition.
- `quote_demo_or_contact_sales_path`: A stated demo, quote, contact-sales, book-time, or contact-for-pricing path.

Requirements:
- The product must be public software or a productized public tool in the qualifying ecosystem. Exclude human-only conversion services, Fiverr/Freelancer gigs, individual estimating services, generic PDF/OCR/document editors, broad CRMs with no public Xactimate/ESX/Verisk/Symbility/Cotality workflow, social-only/beta leads with no official product surface, CapOut/CapCut or generic-ESX collisions, and Xactimate/Verisk/Cotality/Symbility themselves as ordinary competitor products.
- Prefer owned product, help, docs, pricing, terms, trust, security, official blog, press, or demo pages. Marketplace listings, counterparty/platform pages, and reputable trade articles can qualify only when they directly name the product and concrete workflow; they cannot replace the vendor's own pricing, speed, accuracy, commercial-access, terms, trust, or limitation claim.
- Vendor-authored comparison pages count only as the author's own claims. They never prove a competitor's pricing, speed, accuracy, capability, or workflow.
- The page must visibly identify the submitted product and source-state the submitted facet. Do not infer price, speed, accuracy, integration depth, output format, or commercial availability from vague marketing or third-party summaries.
- For every facet, the cited source must carry facet-specific text. A generic homepage, product overview, platform overview, or broad restoration-software page does not satisfy `commercial_access_posture` unless the cited section states pricing, trial, free credits, subscription, demo/quote/contact-sales, or similar access terms; it does not satisfy `terms_trust_or_limitation_posture` unless the cited section states terms, privacy/security/data handling, trust posture, warranty/refund, accuracy, turnaround, support, or limitation text relevant to the product's estimating/conversion workflow.
- The `xactimate_esx_workflow_mechanism` facet needs an artifact, direction, setup path, partner/API route, XactNet/XactAnalysis/Request Data route, ESX/FML/SKX file, direct import/export/delivery path, or comparable mechanism. Generic "integrates with Xactimate" language by itself is not enough.
- The `commercial_access_posture` facet may be a public dollar price, usage/credit/line-item/area term, subscription tier, free trial/free conversion/free credits, or explicit quote/demo/contact-sales path. Quote/demo/contact-sales is a valid public commercial posture when the source says it.
- The `terms_trust_or_limitation_posture` facet should come from terms, trust, security, privacy, support, help, disclaimer, or limitation text that is relevant to the product's estimating/conversion workflow, not from generic footer boilerplate alone.
- Keep the atlas as public claim provenance. Reject rankings, recommendations, best-fit flags, contractor buying advice, outreach, lead scoring, account-gated scraping, and procurement guidance.
- Treat broad claims/restoration/estimation software as in scope only when the cited page itself states a concrete Xactimate, ESX, Verisk, XactRestore, XactNet, XactAnalysis, Symbility, FML, SKX, Cotality, import/export/delivery, or equivalent property-claims estimating workflow. General scope-of-work, restoration project management, photo documentation, PDF/OCR, CRM, or supplement drafting language is not enough by itself.

For each accepted record, communicate a concise source-stated claim summary plus metadata such as source class, product kind, commercial access type when relevant, source date or observed date when visible, checked date, confidence, and any source-stated speed/accuracy/pricing only when the cited source itself states it.

Write one JSON object per line to `results_xactimate_esx_public_tool_claim_provenance_atlas.jsonl`:
{"item": { "product": "<product>", "claim_facet": "<claim_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

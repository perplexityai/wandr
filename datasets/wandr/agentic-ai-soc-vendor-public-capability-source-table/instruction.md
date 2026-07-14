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

## `agentic_ai_soc_vendor_public_capability_source_table`

For 85+ agentic AI SOC / autonomous security-operations vendors or comparable platform companies, cover at least 4+ public claim axes per vendor by supplying 1+ source-backed URL for each vendor-axis record.

The purpose is a public provenance ledger: what a source says the vendor can do, where the claim appears, who owns or attests the source, and what date / metric / caveat context is visible. This is not a vendor ranking, maturity rubric, buyer recommendation, security assurance, implementation guide, dashboard build, lead-scoring exercise, or contact-enrichment task.

Claim axes:
- `core_capability`: AI-assisted SOC/SecOps work such as investigation, triage, hunting, remediation, alert enrichment, case management, reporting, or autonomous analyst workflow.
- `integration_ecosystem`: integrations, plugins, marketplaces, partner listings, connectors, or ecosystem relationships relevant to security operations.
- `performance_or_benchmark`: source-stated performance, benchmark, case-study, analyst, or metric claims with concrete metric labels and values.
- `transparency_or_audit_trail`: source-stated transparency, explainability, audit-log, evidence trail, governance, or human-oversight claims.
- `deployment_or_licensing`: source-stated deployment, packaging, procurement, pricing, licensing, cloud/on-prem, MSSP/MDR, or marketplace-availability claims.
- `target_segment_or_customer_profile`: source-stated customer segment, buyer type, industry, company-size, analyst/MSSP, enterprise, mid-market, or role-profile claims.

Use `vendor_or_company` for the company/vendor identity. Carry product, platform, module, or named-agent names as supporting details, not as substitutes for the company identity. The vendor set is open: pure-play startups, regional vendors, incumbent security platforms, AI-SOAR/SIEM/XDR/MDR/MSSP-adjacent offerings, and named security-copilot features can count when the cited source ties them to SOC or security-operations analyst work. Generic AI security posture, securing-AI-agent, AI governance, AI app security, model security, or data-governance vendors do not count without SOC/SecOps operations evidence.

For each URL, report the product/platform/agent name when relevant, the claim as stated, a normalized capability family when useful, source class, source owner, attestation side, source date or period when visible, checked date, metric label/value when relevant, integration partner or marketplace when relevant, and any conflict or caveat state the source itself supports. Useful source-class and attestation labels include vendor-owned product/docs pages, trust/security/deployment/pricing pages, integration catalogs, partner marketplaces, case studies, benchmark/report pages, independent security or business press, analyst/market reports, customer/conference/demo pages, `vendor_stated`, `partner_or_marketplace_stated`, `independent_press_or_analyst`, `customer_stated`, and `missing_or_conflict`.

Sources should be public, accessible, and specific to the vendor-axis claim. A generic homepage, generic product page, category listicle, copied press release, or broad market-map mention should not be repeated across axes unless the page has distinct, visible, axis-specific evidence for the row. Vendor-authored Top-N posts, competitor comparisons, sponsored pages without clear independence, and press-wire republications are not independent corroboration, though they may be labeled as vendor-origin evidence when their owner and limits are clear.

Requirements:
- The page must tie the named vendor to AI-assisted SOC, security-operations automation, alert triage, investigation, hunting, remediation, enrichment, case management, reporting, or comparable autonomous security-analyst workflow.
- The page should visibly fit the claimed source class and attestation side. Non-vendor press, analyst/report, customer, or partner/marketplace claims need non-vendor ownership or attestation; vendor-owned marketing and syndicated vendor PR should be labeled as vendor-origin evidence, not independent corroboration.
- The page must support a concrete, vendor-specific claim or source-backed missing/conflict signal for the declared claim axis, not merely general category context or an item in a crowded vendor list.
- The page must meet the declared axis bar. Performance/benchmark rows need a metric label and value, plus source date/period/attribution when stated; bare slogans or undefined numbers are unqualified marketing, not benchmarks. Integration rows need integration, partner, plugin, marketplace, connector, or ecosystem evidence. Deployment/licensing, target-segment, and transparency/audit-trail rows should preserve only what the source states.
- The row should remain provenance-shaped: attribute claims to the source, preserve source owner/date/metric/caveat context, and avoid turning public claims into rankings, maturity scores, recommendations, security assurances, or implementation advice.

Write one JSON object per line to `results_agentic_ai_soc_vendor_public_capability_source_table.jsonl`:
{"item": { "vendor_or_company": "<vendor_or_company>", "claim_axis": "<claim_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

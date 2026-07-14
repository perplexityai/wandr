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

## `acumatica_distribution_partner_evidence`

For 90+ Acumatica VARs, implementation partners, service or development partners, integration partners, ISV/solution partners, or source-linked ecosystem firms with distribution-adjacent public evidence, cover the 4 evidence facets listed below for each partner by supplying 1+ public URL for each partner/facet record.

This is a public provenance table, not a vendor ranking or procurement report. Keep the evidence to source-linked facts about the firm and its public Acumatica/distribution/capability footprint. Do not recommend partners, score leads, solicit quotes, enrich contacts, plan outreach, diagnose a customer's system, or give implementation advice.

Evidence facets:
- `authorization`: public evidence that the firm is an Acumatica-recognized partner or ecosystem firm.
- `distribution_vertical`: public wording that ties the firm to distribution, wholesale, industrial distribution, chemical/process, lab/medical supply, warehouse, inventory, order management, supply chain, eCommerce, or a closely adjacent operational vertical.
- `capability_claim`: source wording for an operational capability such as UOM, high-SKU catalogs, inventory, multi-warehouse, WMS, pick-pack-ship, barcode, lot/serial/quality, MRP, EDI, shipping, eCommerce, CRM/API, integration, fulfillment, landed cost, or similar.
- `customer_proof`: a public case study, customer story, press release, partner resource, Acumatica success story, or reputable case library tying the named firm to a distribution-adjacent customer or implementation.

Treat 2026-04-06 as a provenance reference point rather than a hard historical gate. As auxiliary provenance metadata, note source dates when visible and the checked date; these notes are not a separate scored extraction requirement, and a page should not be claimed to prove current or pre-cutoff status beyond what the page itself says. Locations, service regions, reviews, community/reception locators, confidence notes, and missing/conflict flags may be noted when they are source-stated or clearly visible, but public reception is optional metadata rather than one of the required facets.

The sources should be public, accessible, and usable as normal pages. Official Acumatica pages, Acumatica Marketplace service profiles, partner-owned pages, partner case studies, public customer stories, reputable ERP articles, and directories can each contribute evidence when their source role fits the facet. Third-party directories are useful for discovery and secondary provenance, but a directory label by itself is not enough for the `authorization` facet.

Requirements:
- The page must clearly identify the named partner or ecosystem firm as the relevant entity, not merely Acumatica, a customer, an individual employee, a generic ERP module, or a standalone app/product with no firm-level service or partner identity.
- The page must make its facet-appropriate source role visible. For `authorization`, the page must communicate Acumatica-recognized partner or ecosystem status through an Acumatica-owned surface, Marketplace service profile, official award/blog page, or partner-owned Acumatica partner/certification claim. For `distribution_vertical`, the page must be an official, partner-owned, customer-story, case-library, or reputable ERP/trade surface that states the distribution-adjacent vertical. For `capability_claim`, the page must carry source wording for the operational capability rather than a generic "ERP implementation" label. For `customer_proof`, the page must be a case-study, success-story, press/resource, or comparable public proof surface tying the partner to a distribution-adjacent customer or implementation.
- The page must expose facet-specific evidence scoped to the named partner. For `authorization`, it should establish the Acumatica relationship. For `distribution_vertical`, it should state the vertical or operational setting without inferring fit from the firm name. For `capability_claim`, it should state the capability wording being preserved. For `customer_proof`, it should name or clearly identify the partner/firm in connection with the customer or implementation.

Write one JSON object per line to `results_acumatica_distribution_partner_evidence.jsonl`:
{"item": { "partner": "<partner>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

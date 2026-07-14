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

## `pls_ri_competitor_capability_provenance_atlas`

Build an open-set public capability provenance atlas for product-led-sales, revenue-intelligence, sales-execution or engagement, revenue-orchestration, conversation-intelligence, and account-signal / product-usage GTM vendor-products. Cover 100+ normalized vendor-products and, for each, the 3 capability facets below with a public source (i.e. 1+ URL under each facet).

The capability facets are:
- `ai_capability_claim`: a source-stated concrete AI workflow or capability.
- `integration_interoperability`: a first-class integration or interoperability surface naming a counterpart system.
- `customer_proof`: named customer evidence tied to the vendor-product.

The work is public provenance, not a ranking or buying guide. Source dates, checked dates, market-adjacency notes, evidence subjects, and identity notes can contextualize a source, but source metadata or missingness by itself is not capability evidence.

Evidence should be current to the cited page's own public framing. Historical pages can help explain category or identity context, but a historical product such as Endgame belongs in current vendor-product coverage only when the cited page itself supports the current product identity and claimed facet.

Scope and validity:
- Vendor-products must be public software products in or adjacent to product-led sales, revenue intelligence, sales execution or engagement, revenue orchestration, conversation intelligence, or account-signal / product-usage GTM.
- Vendor-product identity is semantic: Salesforce Sales Cloud, Agentforce Sales, and Salesforce Revenue Intelligence belong in the same Salesforce sales-product family when the source context makes that identity clear. Ordinary brand and capitalization variants such as Gong / Gong.io, Outreach / Outreach.ai, and Salesloft / SalesLoft are the same vendor-product identity.
- Person, contact, account-list, prospecting, enrichment, private account-status, ranking/procurement advice, no-source/missingness, and private roadmap/gap inferences are outside public vendor-product capability provenance.

Requirements:
- The page must clearly attribute the evidence to the named vendor-product or a normalized equivalent.
- The page must earn the source role for the claimed facet. For `ai_capability_claim`, this means a vendor-owned or vendor-authored surface such as an official product or feature page, docs/help page, official blog/newsroom page, or vendor-attributed release. For `integration_interoperability`, this means a first-class integration surface from vendor docs/help/catalog/marketplace or a partner-side marketplace/catalog/docs page. For `customer_proof`, this means a vendor-owned customer story, case study, customer/logo page, vendor-authored blog or press page, vendor-attributed wire release, or customer-owned testimonial/case story.
- The page must expose the concrete finding required by the claimed facet. For `ai_capability_claim`, it must state a concrete AI workflow or capability, such as account research, agentic action, CRM update, forecasting, conversation summarization, coaching, prioritization, routing, or content generation; generic "AI-powered platform" wording alone does not count. For `integration_interoperability`, it must name the counterpart system and show an integration, sync, connector, API, app, data flow, setup flow, or comparable interoperability substance. For `customer_proof`, it must name a real customer organization and a proof element such as a case-study title, quoted relationship, visible customer listing, outcome, workflow, or deployment detail.

Write one JSON object per line to `results_pls_ri_competitor_capability_provenance_atlas.jsonl`:
{"item": { "vendor_product": "<vendor_product>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

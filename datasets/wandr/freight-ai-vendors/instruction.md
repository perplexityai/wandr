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

## `freight_ai_vendors`

For 600+ vendors or products that publicly offer AI-enabled or workflow automation software for freight broker, 3PL, freight-forwarder, or logistics-provider operations, supply evidence for each of the 2 evidence types, with 1+ source URL per type. This is public vendor capability provenance, not vendor ranking, procurement recommendation, market-entry advice, competitive whitespace analysis, investment validation, customer targeting, outreach, lead scoring, contact enrichment, or contact discovery.

The evidence types are:
- `official_workflow_claim`: a first-party official source controlled by the submitted vendor or product, such as a vendor-owned product, solution, documentation, blog, newsroom, or press-release page, naming the vendor or product and substantiating a concrete freight-operations workflow.
- `public_corroboration`: a distinct public source showing real-world evidence such as adoption, customer or deployment proof, third-party partner/profile or integration marketplace evidence, public launch, acquisition or partnership, marketplace presence, trade coverage, funding database/profile, or comparable public corroboration.

For downstream reading, optional factual notes can include canonical vendor or product name, legal or parent/subsidiary context when source-stated, freight customer segment when source-stated, workflow covered, integration or partner context when source-stated, public customer or deployment evidence, funding or acquisition signal, source class, source date or observed date, checked date, confidence, and source notes. Use 2026-06-30 as the checked date unless the source was checked later. Do not include contacts, leadership names, emails, phone numbers, customer targeting, lead scores, outreach priority, rankings, buyer recommendations, procurement advice, or investment conclusions.

Concrete freight workflow examples include:
- `quote or rate response`
- `order entry or load build`
- `rate confirmation, BOL, POD, invoice, customs, or other freight-document extraction`
- `carrier sourcing, booking, carrier sales calls, or rate negotiation`
- `track-and-trace, check calls, status updates, or customer communication`
- `appointment scheduling`
- `exception management`
- `fraud, compliance, or carrier verification`
- `invoice audit, claims, or payment chasing`

Useful public corroboration source types include:
- `non-vendor customer, deployment, or case-study source`
- `counterparty partner, integration, or marketplace profile`
- `trade press, logistics-technology article, or public launch coverage`
- `public acquisition, partnership, or integration announcement`
- `public funding profile or funding coverage specific to the vendor`
- `vendor-hosted customer story naming a customer, partner, deployment, or concrete workflow`
- `specific G2, Capterra, marketplace, or database profile used only as secondary corroboration`
- `other vendor-specific public real-world evidence source`

Useful source classes include:
- `official product or solution page`
- `official documentation or knowledge-base page`
- `vendor-owned blog, newsroom, press release, launch, or documentation page`
- `named customer story or deployment case`
- `counterparty partner, integration, or marketplace page`
- `trade press or logistics-technology article`
- `funding, acquisition, partnership, or company profile`
- `vendor-specific review or software marketplace profile labeled as secondary`
- `other public vendor-specific source`

Boundary classes to keep out unless the submitted page itself proves the freight broker, 3PL, freight-forwarder, or logistics-provider workflow automation role:
- `bare AI-powered TMS, agentic logistics, or automation banner with no concrete workflow`
- `autonomous trucking, telematics, hardware, sensors, devices, or vehicle technology`
- `pure visibility, tracking, or data-feed product with no broker, 3PL, forwarder, or logistics-provider workflow automation`
- `generic freight marketplace, load board, capacity marketplace, or generic TMS page with no workflow automation claim`
- `shipper-only, carrier-only, fleet-only, warehouse-only, or last-mile-only tooling with no relevant freight-operations workflow`
- `horizontal AI, voice AI, RPA, document AI, or software-development platform with no freight-specific workflow proof`
- `broad category page, generic listicle, review category, funding database entry, or search result used as capability truth`
- `procurement advice, ranking, market-entry strategy, lead list, contact database, outreach material, or customer-targeting surface`

Official workflow evidence must come from first-party sources controlled by the submitted vendor or product, such as official product pages, workflow-specific solution pages, documentation, vendor-owned blogs, newsrooms, or official press releases.
Public corroboration can come from customer/deployment evidence, counterparty partner or integration pages, third-party marketplace or profile pages, app/integration marketplaces, trade press, public launches, acquisitions or partnerships, funding databases/profiles, and comparable public sources.
Use a distinct URL and source role for each evidence type.
Vendor-hosted customer stories count as `public_corroboration` only when they name a customer, partner, or deployment and carry concrete workflow detail; broad review categories, funding databases, listicles, and marketplace category pages are secondary discovery or corroboration surfaces, not capability truth.

Requirements:
- The page must identify the claimed vendor or product, or bridge the submitted product, legal name, acquired brand, subsidiary, parent, or operating brand to the same vendor with enough context to distinguish unrelated same-name entities.
- The submitted page itself must fulfill the claimed `evidence_type`: `official_workflow_claim` evidence should be a first-party official source controlled by the vendor/product, while `public_corroboration` evidence should be a distinct public source for the same vendor/product showing real-world public evidence.
- The page must support role-specific freight workflow substance. For `official_workflow_claim`, it must source-state a concrete AI-enabled or workflow-automation capability for freight broker, 3PL, freight-forwarder, or logistics-provider operations. For `public_corroboration`, it must show a concrete vendor-specific public corroboration signal in the freight or logistics ecosystem; vendor-hosted customer stories need named customer, partner, deployment, or workflow detail.

Write one JSON object per line to `results_freight_ai_vendors.jsonl`:
{"item": { "vendor": "<vendor>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

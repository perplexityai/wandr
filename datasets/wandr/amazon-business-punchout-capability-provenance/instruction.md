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

## `amazon_business_punchout_capability_provenance`

Identify 90+ distinct providers or provider products with public evidence that the named provider/product supports or enables an Amazon Business procurement integration. For each provider, cover each of the 2 evidence facets listed below, with 1+ source URL per facet.

Evidence facets:
- `capability_claim`: the source explicitly ties the named provider/product to Amazon Business and a relevant procurement integration capability, such as PunchOut, Punch-in, Integrated Search, cXML/OCI/OAG-enabled catalog or procurement workflow, or a clearly named Amazon Business e-procurement connector.
- `workflow_or_configuration_detail`: the source gives public setup, configuration, credential, connector, workflow, cart-return, purchase-order, group, shared-secret, PunchOut URL, Integrated Search, or equivalent operational detail for that provider/product's Amazon Business integration.

Providers/products can include buyer-side procurement platforms, spend-management systems, supplier commerce platforms, integration gateways, and similar public e-procurement integration surfaces. Use one stable provider/product name consistently. If two submitted names clearly refer to the same marketed Amazon Business integration surface, treat them as the same provider; keep genuinely distinct products separate when public sources discuss separate integration surfaces.

Requirements:
- The page must clearly identify the named provider/product.
- The page must specifically connect that provider/product to Amazon Business. Generic Amazon, Amazon marketplace, AWS, PunchOut, cXML, OCI, or supplier-catalog evidence without Amazon Business does not satisfy this task.
- The page must connect Amazon Business to a procurement integration capability or workflow, not just to ordinary shopping, pricing, discounts, Prime membership, seller listings, or a broad business-commerce relationship.
- The page must fit the claimed evidence facet. `capability_claim` can come from product pages, help centers, integration docs, Amazon Business partner pages, official marketplace listings, press releases, or reputable procurement-software articles when they name Amazon Business and the integration capability. `workflow_or_configuration_detail` requires concrete workflow, setup, credential, connector, cart-return, purchase-order, group, Integrated Search, or equivalent operational substance.
- Generic connector lists, supported-supplier lists, logo walls, marketplace name lists, broad "200+ systems" or "1000s of integrations" claims, and generic protocol explainers are not enough unless the page specifically states the named provider/product and the Amazon Business relationship being claimed.
- Public customer deployment pages can help discovery, but do not by themselves prove broad provider/product capability unless the page itself states the provider/product's Amazon Business integration capability or operational setup in a generally applicable way.
- Do not use pricing/signup state, checked date, source date, source class, confidence, fit, ranking, recommendations, outreach, contact enrichment, or implementation-consulting advice as scored evidence.

Same-URL reuse across both evidence facets is acceptable only when the page genuinely contains both a qualifying capability claim and qualifying workflow/configuration detail.

Write one JSON object per line to `results_amazon_business_punchout_capability_provenance.jsonl`:
{"item": { "provider": "<provider>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

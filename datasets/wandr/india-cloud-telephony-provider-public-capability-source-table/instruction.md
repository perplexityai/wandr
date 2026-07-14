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

## `india_cloud_telephony_provider_public_capability_source_table`

For 90+ India-present cloud communications providers with substantiated public India presence, cover the 6 provenance facets listed below for each provider by supplying 1+ public URL for each facet.

The provider universe includes public providers of cloud telephony, virtual numbers, IVR, call-center or contact-center software, business phone systems, SIP trunking, WhatsApp or voice APIs, messaging/voice CPaaS, or adjacent cloud communications services. "India-present" means public evidence of a meaningful India operation or India-facing offering: an India office or entity, India-specific offering, INR pricing, Indian telecom/DLT/TRAI support, Indian number inventory, India infrastructure/status component, or reputable Indian business/entity profile. A `.in` domain, +91 phone number, or contact page can help, but is not enough by itself.

Provenance facets:
- `official_india_presence`: a provider-owned page showing the provider's India-present cloud communications offering or India operation
- `pricing_disclosure`: a provider-owned pricing, plan, rate-card, or explicit contact-sales/custom-pricing disclosure
- `developer_or_integration_surface`: a provider-owned API docs, SDK docs, integration page, webhook docs, CRM/WhatsApp/SIP/voice API docs, or similar developer/integration surface
- `support_or_policy_surface`: a provider-owned help, support, knowledge-base, terms, acceptable-use, restriction, escalation, or policy locator
- `reliability_or_status_surface`: a provider-owned status page, SLA page, trust page, uptime page, or source-stated uptime/SLA claim; this is only provenance for a public claim or surface, not a reliability guarantee
- `independent_profile_or_review_locator`: a non-provider-owned public review, marketplace, reputable business profile, or similar independent locator; ratings, sentiment, rankings, and support quality are not part of the finding

For provider-owned facets, the URL should be controlled by the provider or the same corporate family. Third-party summaries, listicles, mirrors, comparison pages, and rewritten pricing or uptime summaries do not satisfy provider-owned facets even when they mention the same facts. For the independent locator facet, the URL should not be controlled by the provider.

Treat provider aliases, rebrands, acquired brands, and same-corporate-family service names as the same provider when the public evidence shows they are one commercial provider identity. Do not count generic categories, individual products without provider identity, directories, telecom regulators, review platforms, or lead-generation pages as providers.

The task is public source provenance only. Do not recommend, rank, compare provider quality, guarantee reliability, evaluate support quality, advise on telecom/legal compliance, optimize pricing, give setup instructions, enrich contacts, score leads, or infer private sales or operational metrics.

Requirements:
- The page must clearly identify the named provider or the same corporate family.
- The page must tie the provider to cloud communications services; on `official_india_presence`, it must also show a substantive public India-presence signal.
- The page must have the source role required by `provenance_facet`: provider-owned or same-corporate-family controlled for the five provider-owned facets, non-provider-owned for the independent locator facet.
- The page must contribute the declared facet evidence, bounded to public source provenance rather than provider quality or recommendation claims.

Write one JSON object per line to `results_india_cloud_telephony_provider_public_capability_source_table.jsonl`:
{"item": { "provider": "<provider>", "provenance_facet": "<provenance_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

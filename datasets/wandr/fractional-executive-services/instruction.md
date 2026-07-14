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

## `fractional_executive_services`

For each of the 6 fractional executive function families listed below, cover 45+ public provider/function claims per family; for each provider/function claim and each of the 3 evidence modes listed below, supply a public source (i.e. 1+ URL) that substantiates the provider's source-stated service claim for US, North American, global, or remote business buyers.

This is public service-claim provenance for fractional executive services. Provider rankings, buyer recommendations, demand estimates, market saturation, lead/contact collection, outreach, and legal/compliance adequacy conclusions are outside scope.

Function families:
- `operations_leadership`: fractional/interim COO, VP Operations, operations executive, or operational Chief of Staff when the role is executive/operational
- `marketing_leadership`: fractional/interim CMO, VP Marketing, growth marketing executive, or comparable senior marketing leadership
- `revenue_or_sales_leadership`: fractional/interim CRO, VP Sales, revenue executive, sales executive, or comparable senior revenue leadership
- `people_or_hr_leadership`: fractional/interim CHRO, Chief People Officer, VP People, HR leader, or comparable senior people leadership
- `compliance_or_risk_leadership`: fractional/interim Chief Compliance Officer, risk executive, compliance executive, or comparable senior risk/compliance leadership
- `business_development_or_partnerships_leadership`: senior strategic business development, partnerships, alliances, channel, marketplace, or strategic-deal leadership

Evidence modes:
- `role_offer`: provider-specific evidence explicitly naming the claimed function family as a fractional/interim/part-time/on-demand executive or senior leadership service
- `function_scope`: provider-specific function responsibilities, buyer situations, deliverables, operating context, or service scope for the claimed function family beyond a bare role/title list
- `commercial_model`: concrete provider-attributable packaging or commercial terms for the claimed service

The provider ought to be a real public firm, platform, collective, consultancy, or intermediary offering fractional/interim/part-time/on-demand executive or senior leadership services. A platform may be the provider, and a provider-specific profile or marketplace page may supply source context for that platform or for a separately branded provider organization; platform-listed individual operators, individual consultant profiles, marketplace category/profile entries, and similar person-level listings are not separate provider identities merely because they advertise a hireable executive. Ordinary permanent executive search, staffing, coaching, generic consulting, low-level outsourcing, SDR/outreach agencies, and individual resume pages do not count unless the page itself frames a qualifying provider organization or platform offer as a fractional/interim executive or senior leadership service.

Requirements:
- The page must clearly identify the claimed provider.
- The page should make its provider-specific source context visible, such as provider-controlled service, FAQ, pricing, case-study, profile, marketplace, directory, or reputable provider-specific profile context. For platform/profile sources, the provider-specific context must be scoped to the platform itself or to a separately branded provider organization, not merely to an individual operator card or marketplace category/profile entry treated as its own provider. Generic market-rate guides, "best provider" rankings, listicles, review-score pages, lead forms, and directory search-result pages do not satisfy this by themselves unless they contain a provider-specific claim that independently meets the task bar.
- The page should visibly support a US, North American, global, or remote business-buyer posture for the provider or service.
- The page must tie the provider to fractional, interim, part-time, on-demand, retainer-based, or comparable executive/senior leadership service.
- The page must support the claimed `function_family` with the corresponding executive/senior-leadership role or function: operations/COO, marketing/CMO, revenue or sales/CRO/VP Sales, people/HR/CHRO/CPO, compliance/risk/CCO, or senior strategic business development/partnerships. CFO, CTO, CISO, general counsel, legal-service, ordinary compliance consulting, business-development representative, lead-generation, and SDR/outreach roles do not satisfy the selected families unless the page separately states one of the in-scope function-family services.
- The page should contribute evidence appropriate to `evidence_mode`: for `role_offer`, it must explicitly name the selected function as a fractional/interim/part-time/on-demand executive or senior leadership service; for `function_scope`, it should give function-specific responsibilities, deliverables, buyer situations, operating context, or service scope beyond a bare role/title list; for `commercial_model`, it should state concrete provider-attributable packaging or terms such as a named package/tier, numeric price/rate, retainer/SOW/project basis, minimum term, hours/month, days/week, interim placement terms, or similar. Generic "flexible", "without full-time hire", "custom proposal", or "contact us" language does not satisfy `commercial_model` by itself.

Write one JSON object per line to `results_fractional_executive_services.jsonl`:
{"item": { "function_family": "<function_family>", "provider": "<provider>", "evidence_mode": "<evidence_mode>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

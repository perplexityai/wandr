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

## `social_api_vendor_evidence`

For 40+ public software vendors or products that mediate social-media publishing, scheduling, management, analytics, data extraction, listening, connector automation, SDK/repository access, or agent/MCP access, cover each of the 5 evidence facets per vendor by supplying a public source (i.e. 1+ URL under each facet).

This is public provenance for a volatile API/vendor ecosystem, with 2026-06-29 as the seed's as-of context. The cited public page checked at solve time is what matters. Do not turn the work into a vendor recommendation, ranking, procurement memo, cost-effectiveness comparison, implementation plan, outreach list, or contact-enrichment exercise.

The evidence facets are:
- `api_or_surface_access`: public evidence of a concrete programmatic surface, such as API docs, a developer hub, SDK or package, public repository, MCP or agent tool, connector action, custom API request module, or a public statement that details are gated behind a plan or dashboard.
- `plan_or_pricing_gate`: public evidence of a plan, edition, paid-access condition, pricing unit, profile or account limit, credit pack, seat, workflow-run, source, brand, or comparable unit that gates the API or surface.
- `usage_limit_or_quota`: public evidence of rate limits, request quotas, post quotas, credits, fair-use wording, pass-through network limits, no-rate-limit wording, or a public gated-details statement about limits.
- `network_or_capability_scope`: source-stated supported networks, social objects, operation families, data categories, connected-account types, or capability boundaries.
- `integration_or_workflow_example`: a concrete source-stated action, trigger, workflow, marketplace module, changelog example, SDK example, MCP or agent tool, or integration-doc example.

Alongside each source, state a concise vendor class, surface type, operation direction, publicness state, and source-stated wording. Use source-grounded labels such as native unified social API, dashboard-first SMM API, open-source or self-hosted product, connector platform, read-only or social-data API, SDK/repository surface, official API docs, pricing or plan page, help or product page, limits page, changelog/status page, public repository, SDK/package page, marketplace/connector listing, official integration docs, labeled secondary locator, read, write, publish, schedule, analytics, comments/inbox, account or profile management, search/extract, trigger, workflow, custom API request, MCP/agent tool, public docs, public overview with gated details, paid-plan API access, connector-only, repo-backed, official-silent-on-rate-limit, secondary-conflict-lead, or name-conflict/rebrand.

Requirements:
- The page must identify the named vendor/product and show a relevant social media management, social publishing, social analytics, social data extraction, social listening/UGC, connector automation, SDK/repo, or agent/MCP capability. First-party social networks themselves do not count merely because they expose platform APIs.
- The page must fit `evidence_facet` and publicly state the facet claim or a narrow gated/silent condition for that facet. Pricing, plan access, supported networks, brand/account/profile/source limits, quotas, and examples must be recorded only when source-stated. For `usage_limit_or_quota`, a generic page that merely omits limits is not enough; the source should state limits, quotas, credits, no-limit/fair-use/pass-through wording, or publicly state that details are gated.
- The stated classifications should be grounded in the cited page without conflating surface types. A connector action or custom API request is connector evidence, not proof of a vendor-native social API; a read-only UGC or social-data API is read/extract/listen evidence, not publishing or scheduling evidence.
- The source-stated wording should be a short claim or paraphrase tied to the cited page and framed as public provenance. Secondary/review/comparison pages can be labeled as locator or conflict-lead evidence, but should not override official sources for pricing, limits, API access, or network support.

Write one JSON object per line to `results_social_api_vendor_evidence.jsonl`:
{"item": { "vendor": "<vendor>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

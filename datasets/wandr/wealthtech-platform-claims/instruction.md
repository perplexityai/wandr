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

## `wealthtech_platform_claims`

As of June 29, 2026, build a public-source provenance atlas for 120+ advisor-facing wealthtech platforms. For each platform, cover 4+ claim axes from the list below, and supply 1+ public URL for each covered axis.

The platform universe is open. Aqua-style alternative-investment platforms are in scope, but so are advisor operating systems, TAMP/OCIO and model platforms, custodians and advisor platforms, risk/proposal analytics, portfolio accounting/reporting, data and AI/automation tools, structured-investment platforms, direct-indexing platforms, and adjacent wealth-management technology workflows.

Claim axes:
- `product_capability`: public product, workflow, platform-category, marketplace, custody, TAMP/OCIO, risk/proposal, portfolio/reporting, direct-indexing, structured-investment, data, or model-delivery capability claims.
- `integration_partner`: public integrations, partner ecosystems, platform connections, data feeds, custody/reporting/CRM/planning/model-delivery edges, partner marketplaces, or integration-status claims.
- `ai_automation_data`: public AI, automation, data extraction, advisor-assistant, data-layer, machine-learning, workflow-automation, or maturity/status claims.
- `customer_metric`: public customer, advisor, user, firm, asset, account, AUM/access, case-study, adoption, or named-public-usage claims.
- `funding_ownership`: public funding, acquisition, take-private, investor, ownership, legal-entity, regulatory, or transaction claims.
- `identity_chronology`: public rebrands, predecessor/successor names, folded-in products, launches, dated product evolution, or identity changes.

For each evidence record, state the platform's sub-vertical, the public claim or constrained public missing/conflict observation, the source class, whether the source is an official self-claim, differently situated corroboration, weak listing, or missing/conflict surface, the source date or observed-page date where available, the checked date, and any maturity/status detail the page actually supports.

Expected public source families include official product, solution, integration, partner, marketplace, case-study, newsroom, help-center, and developer/support pages; SEC filings, annual reports, investor presentations, Form CRS/ADV/BrokerCheck or similar regulatory surfaces where relevant; dated press releases and acquisition, funding, launch, or rebrand announcements; reputable wealthtech, advisor-tech, fintech, investment-management, or institutional trade coverage; public partner-side listings and marketplace listings. Directories, listicles, company databases, and aggregators can help discover candidates, but final evidence from those sources should be narrow and labeled as weak unless separately supported.

Requirements:
- The page must identify the submitted platform, platform company, product family, predecessor, or renamed successor and tie it to advisor-facing or wealth-management technology workflows.
- The page should make its source role visible for the claim axis and evidence posture. Official pages can support source-stated self-claims; trade, filing, regulatory, partner-side, or case-study pages can support differently situated evidence; logo-only, category-only, directory, or listicle pages can support only restrained weak-listing or public-missing/conflict observations.
- The page must source-state or clearly support the claim or public missing/conflict observation. Product, capability, integration, customer, metric, funding, ownership, and chronology facts should not be inferred from category membership, logos, rankings, generic descriptions, or private knowledge.
- The record should preserve date posture: dated events use the page's source/publication date; undated evergreen pages are treated as observed public pages; post-June 29, 2026 events are not in-scope facts.
- Keep the work as public provenance. Do not rank vendors, recommend platforms, make investment or financial-advice claims, give pricing advice, enrich contacts, plan outreach, handle private reports, or infer product quality beyond what public sources state.

Write one JSON object per line to `results_wealthtech_platform_claims.jsonl`:
{"item": { "platform": "<platform>", "claim_axis": "<claim_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

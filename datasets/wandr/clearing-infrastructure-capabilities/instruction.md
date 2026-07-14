You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `clearing_infrastructure_capabilities`
  - `clearing_infrastructure_capabilities.entity_anchors`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `clearing_infrastructure_capabilities`

As of May 6, 2026, find 60+ resolved legal entities that publicly provide clearing, custody, correspondent clearing, prime brokerage, FCM/futures clearing, or embedded brokerage infrastructure to intermediaries, institutions, fintechs, broker-dealers, RIAs, futures introducing brokers, or comparable third-party clients. For each legal entity, identify 1+ source-backed provider service line and 2+ source-stated capabilities for that service line, with 1+ source URL for each capability.

This is a public provenance atlas, not a provider recommendation. Do not rank firms, recommend a provider, compare costs, infer private onboarding terms, give compliance or securities advice, develop outreach lists, enrich contacts, or score leads.

In-scope regimes:
- `securities_broker_dealer`
- `ria_custody`
- `futures_fcm`
- `prime_institutional_brokerage`
- `embedded_brokerage_infrastructure`

In-scope provider roles:
- `carrying_broker`
- `clearing_broker`
- `correspondent_clearing_provider`
- `custodian`
- `fcm`
- `self_clearing_broker_dealer`
- `prime_broker`
- `introducing_facing_platform`
- `embedded_api_brokerage_provider`

Requirements:
- The source must show that the submitted provider service line is infrastructure for third-party or intermediary clients. A consumer brokerage homepage, a retail account feature page, or a self-clearing status claim without third-party infrastructure context is not enough.
- The submitted `regime` and `provider_role` should be source-backed and should not collapse unlike regimes. Securities broker-dealer carrying/clearing, RIA custody, FCM/futures clearing, prime brokerage, embedded brokerage infrastructure, and SEC-registered clearing agencies are different populations.
- Each capability must be directly source-stated for the submitted service line. Broad phrases such as "full service," "turnkey platform," "comprehensive solution," "global access," or "clearing solutions" do not by themselves prove specific capabilities such as options, fixed income, futures, margin, stock loan, mutual funds, managed accounts, international market access, API brokerage, or similar product-level support.
- Capability evidence should come from an official provider page, regulator record, public legal disclosure, public agreement, financial-condition or regulatory-capital filing, issuer filing, or equivalent public source. Trade articles, rankings, and roster pages may help discovery or context, but they do not prove capability rows by themselves.
- For otherwise valid capability records, record the observed source-stated capability claim, source class, source date or reporting period when visible, checked date, and any caution state such as `entity_unresolved`, `name_conflict`, `regime_ambiguous`, `relationship_source_only`, `provider_source_only`, `no_product_level_source`, `no_public_economics_source`, `redacted`, or `stale_source_suspected`. Missing-product-source, no-public-economics, redaction, and stale-source flags are provenance, economics-visibility, or status annotations only; they do not substitute for direct capability proof from an eligible source.
- Public financial-condition or regulatory-capital evidence can support financial-condition provenance when source-stated. Do not convert regulatory net capital, financial statements, or balance-sheet facts into client onboarding minimums unless a source explicitly states an onboarding threshold.

Write one JSON object per line to `results_clearing_infrastructure_capabilities.jsonl`:
{"item": { "resolved_legal_entity": "<resolved_legal_entity>", "provider_brand": "<provider_brand>", "division_or_trade_name": "<division_or_trade_name>", "regime": "<regime>", "provider_role": "<provider_role>", "service_line": "<service_line>", "capability": "<capability>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `clearing_infrastructure_capabilities.entity_anchors`

Cross-tasknode identifier discipline: this task is for the same {= resolved_legal_entity =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

Find {= resolved_legal_entity =}+ resolved legal entities that publicly operate in clearing, custody, correspondent clearing, prime brokerage, FCM/futures clearing, or embedded brokerage infrastructure, and identify public regulator, filing, financial-condition, or legal/disclosure sources that anchor each entity's public identity and registration or filing identifier. For each entity, provide 1+ registration anchor and 1+ source URL.

The source should make the legal entity and identifier public: FINRA CRD, SEC file number or CIK, NFA/CFTC identifier, FCM financial-data identity, BrokerCheck report, X-17A-5 statement of financial condition, public regulatory order, or comparable legal/filing anchor. Marketing pages can help interpret a brand, but they do not count here unless they themselves state a public registration or filing identity.

Requirements:
- The page must identify the submitted legal entity or a clearly tied trade name/division.
- The page must state or visibly anchor the submitted registration system and identifier.
- The page must be an official regulator, filing, financial-condition, legal disclosure, or equivalent public legal-entity source.
- The page should help place the entity in the relevant public regime without turning the registration fact into compliance advice.

Write one JSON object per line to `results_clearing_infrastructure_capabilities.entity_anchors.jsonl`:
{"item": { "resolved_legal_entity": "<resolved_legal_entity>", "registration_system": "<registration_system>", "registration_id": "<registration_id>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

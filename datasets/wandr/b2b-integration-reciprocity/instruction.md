You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `b2b_integration_reciprocity`
  - `b2b_integration_reciprocity.provider_profiles`

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

## `b2b_integration_reciprocity`

For 150+ public B2B SaaS/tool providers in trust, compliance, GRC, status/incident transparency, sales engagement, prospecting, CRM/email-connected GTM automation, or close adjacency, find 3+ distinct external software/platform counterparties per provider where an integration, connector, app, API setup, marketplace listing, supported-platform relationship, or comparable software relationship is acknowledged from both sides; for each (`provider`, `counterpart`) relationship and each of the 2 relationship sides listed below, supply a relationship-substantiating source (i.e. 1+ URL).

The goal is public integration reciprocity rather than buying decisions, audit judgments, sales targeting, or people-data enrichment.

The relationship sides of interest, which we refer to as `reference_type`, are:
- `claim`: a provider-owned or provider-controlled statement naming `counterpart` as an integration, connector, app, API setup, marketplace listing, supported platform, or comparable software relationship.
- `backclaim`: a counterpart-owned or counterpart-controlled statement independently naming `provider` and the same integration, app, listing, setup, or comparable relationship.

`counterpart` ought to be a meaningfully distinct external software/platform counterparty, not the provider itself, a same-company alias, an internal product or feature, a same-corporate-family self-reference, a generic category, a protocol alone, or a non-software customer relationship.

Requirements:
- The page should communicate that it is an officially controlled surface for the party being cited: for `claim`, that party is `provider`; for `backclaim`, that party is `counterpart`. Provider-owned official domains, help centers, docs, marketplaces, and verified product channels can count; counterpart-owned docs/help pages and counterpart-controlled app marketplaces or integration directories can count for `backclaim` only when the page visibly carries counterpart/platform publication or acknowledgment cues beyond merely hosting provider-supplied listing copy. Third-party news, press-wire mirrors, unrelated aggregators, generic marketplace search/listing shells, and wrong-owner pages do not.
- The page must explicitly identify the opposite party: for `claim`, `counterpart` should be clearly identifiable; for `backclaim`, `provider` should be clearly identifiable. Vague references such as "popular CRMs" or "leading code hosts" do not count.
- The page should acknowledge the software/platform relationship at the bar appropriate to `reference_type`: for `claim`, lightweight provider-side relationship evidence such as integration-directory entries, setup docs, supported-platform lists, API/app pages, marketplace listings, and comparable named claims can count; for `backclaim`, the counterpart-controlled page should specifically present the provider's app, connector, setup page, or named relationship as a counterpart/platform-recognized integration, not merely include the provider as one item in a long undifferentiated tools list or as vendor marketing copy inside a bare hosted listing.

Write one JSON object per line to `results_b2b_integration_reciprocity.jsonl`:
{"item": { "provider": "<provider>", "counterpart": "<counterpart>", "reference_type": "<reference_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `b2b_integration_reciprocity.provider_profiles`

Cross-tasknode identifier discipline: this task is for the same {= provider =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= provider =}+ providers, supply a public provider-scope source (i.e. 1+ URL) establishing the named provider as a public B2B SaaS/tool provider in trust, compliance, GRC, status/incident transparency, sales engagement, prospecting, CRM/email-connected GTM automation, or close adjacency.

The source should be about the provider's own product, platform, category, use case, or company identity rather than a bare logo, customer blurb, funding mention, broad market article, people-data page, lead list, or ranking page.

Requirements:
- The page must clearly identify the named provider.
- The page must establish that the provider offers a public B2B software, tool, or platform for trust, compliance, GRC, status/incident transparency, sales engagement, prospecting, CRM/email-connected GTM automation, or a closely adjacent business workflow.

Write one JSON object per line to `results_b2b_integration_reciprocity.provider_profiles.jsonl`:
{"item": { "provider": "<provider>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

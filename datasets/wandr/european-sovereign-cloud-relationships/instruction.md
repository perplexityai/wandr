You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `european_sovereign_cloud_relationships`
  - `european_sovereign_cloud_relationships.provider_qualification`

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

## `european_sovereign_cloud_relationships`

For 65+ cloud providers or branded cloud offerings, supply 6+ named public relationship records per provider (i.e. 1+ URL for each relationship record). A relationship record names a distinct counterparty and uses one of the `relationship_type` labels listed below.

Each record should use a public source that stated the relationship no later than 2026-04-21. In the answer, report the source side/class, source date or `no_date`, checked date, concise source-stated relationship, corroboration state, confidence, and any missing/conflict state. Keep the ledger descriptive: no provider rankings, recommendations, procurement advice, legal/security adequacy judgments, compliance assurances, lead scoring, outreach/contact enrichment, migration plans, or architecture guidance.

Relationship types:
- `customer_case_study`: a named customer deployment or detailed success story
- `public_reference`: a named customer, user, testimonial, logo-wall, or reference-list mention
- `internal_group_deployment`: use by a parent, subsidiary, affiliate, or internal group entity
- `public_sector_procurement_or_framework_award`: a tender, framework, award, or public-sector purchasing relationship
- `strategic_jv_or_operator_arrangement`: a joint venture, national operator, telecom operator, sovereign-cloud operator, or comparable strategic arrangement
- `technology_or_isv_partner`: a technology, software, integration, marketplace, or ISV partner relationship
- `reseller_si_network_or_service_partner`: a reseller, systems integrator, consulting, managed-service, or service-network partner relationship
- `marketplace_or_integration_partner`: a marketplace listing, documented integration, connector, or product-integration relationship

Source sides/classes:
- `provider_side`: source controlled by the provider or its corporate parent
- `counterparty_side`: source controlled by the named counterparty
- `public_body_or_procurement`: government, regulator, public institution, procurement, tender, or award source
- `reputable_press_or_analyst`: reputable business, cloud, technology, analyst, or trade-press source
- `directory_or_marketplace`: partner directory, marketplace, catalog, logo wall, or similar low-context listing

Requirements:
- The page should be an eligible public source for the relationship. Provider-controlled, counterparty-controlled, public/procurement, reputable press/analyst, and relationship-specific marketplace or directory pages can count when the answer reflects the source's actual side and strength. Generic provider lists, ranking pages, SEO listicles, and contact/lead-generation pages do not count by themselves.
- The page must clearly name or unambiguously identify both the provider and the named counterparty as the parties to the relationship.
- The page must support the claimed `relationship_type`, not merely a broader association or a different kind of relationship.
- The page must provide source-stated relationship substance: deployment or use-case detail, award scope, partner role, operator arrangement, integration content, marketplace/listing role, or comparable relationship-specific content.

Write one JSON object per line to `results_european_sovereign_cloud_relationships.jsonl`:
{"item": { "provider": "<provider>", "counterparty": "<counterparty>", "relationship_type": "<relationship_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `european_sovereign_cloud_relationships.provider_qualification`

Cross-tasknode identifier discipline: this task is for the same {= provider =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= provider =}+ cloud providers or branded cloud offerings, supply a public qualification source (i.e. 1+ URL per provider) showing that the provider was publicly positioned no later than 2026-04-21 as European sovereign-cloud, sovereignty-oriented cloud, EU/EEA data-residency cloud, national/public-sector sovereign cloud, trusted cloud, or an equivalent European sovereignty-positioned cloud service.

The source can be provider-controlled, corporate-parent-controlled, public/procurement, reputable press/analyst, or another durable public source that states the positioning. Record only what the source says; do not assess legal/security adequacy, rank providers, or recommend vendors.

Requirements:
- The page must identify the submitted provider or branded cloud offering.
- The page must show that the provider offers cloud infrastructure, cloud platform services, sovereign cloud operations, or a comparable cloud service to organizations.
- The page must source-state the European sovereignty-oriented positioning without requiring the solver to infer legal, compliance, or security adequacy.

Write one JSON object per line to `results_european_sovereign_cloud_relationships.provider_qualification.jsonl`:
{"item": { "provider": "<provider>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

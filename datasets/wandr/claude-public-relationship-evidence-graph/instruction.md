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

## `claude_public_relationship_evidence_graph`

Build a current public evidence graph for the Claude/Anthropic ecosystem: for each of the 5 closed relationship families, identify 35+ counterparties; for every (`relationship_family`, `counterparty`) pair, cover each of the 2 closed evidence roles listed below with a source (i.e. 1+ URL under each role).

Relationship families:
- `cloud_model_distribution` (35+ counterparties): Cloud, model platform, marketplace, procurement, or hosted-model surface making Claude/Anthropic available to external customers or developers.
- `services_or_gsi_partner` (35+ counterparties): Consulting, systems integrator, services, solution, certification, or implementation partnership around Claude/Anthropic.
- `technology_or_product_integration` (35+ counterparties): Named product, platform, connector, data platform, developer tool, workflow, API surface, or enterprise app that integrates, exposes, configures, or documents Claude/Anthropic.
- `public_customer_adoption` (35+ counterparties): Named organization publicly stated to use, deploy, adopt, or build workflows with Claude/Anthropic.
- `powered_by_claude_builder` (35+ counterparties): Product, application, or builder publicly stating that its product or capability is built with, powered by, or materially uses Claude/Anthropic.

The evidence roles of interest, which we refer to as `evidence_role`, are:
- `relationship_statement`: a public high-level source whose main job is to state the qualifying Claude/Anthropic relationship for the submitted (`relationship_family`, `counterparty`) pair.
- `substance_detail`: a detail-oriented public source for the same relationship-family/counterparty pair that adds concrete relationship substance beyond the high-level statement.

Counterparties are open-set, and unsupported or unconfirmed Claude/Anthropic relationships are outside scope. Eligible relationship-evidence pages must be public, currently accessible, usable as normal web pages, and specific to the claimed relationship. Generic aggregators/listicles, generic directories, ranking/recommendation/sales/outreach pages, logo walls or broad catalogs without relationship-specific substance, private materials, and press-wire mirrors presented as owner-controlled detail are not eligible. Anthropic hub, customer, partner, or directory pages can serve as `relationship_statement` evidence when they are specific enough to the claimed pair, but they do not serve as `substance_detail` unless the page itself contains concrete workflow, deployment, product, service, configuration, case-study, or other relationship-specific detail.

Requirements:
- The page must explicitly name Claude or Anthropic and the submitted counterparty, product, platform, builder, or distribution surface, with relationship wording tying them together.
- The page must support the claimed relationship family. Cloud/platform evidence is about Claude/Anthropic availability, hosting, procurement, marketplace, or API access for external users; services/GSI evidence is about consulting, alliance, implementation, training, certification, or services capability; technology/product integration evidence names a specific integration surface, product, connector, platform, workflow, API surface, or enterprise app; customer-adoption evidence states what the customer uses Claude/Anthropic for; powered-by-builder evidence identifies a product, application, or capability as built with, powered by, or materially using Claude/Anthropic.
- The relationship must be direct. Generic AI adoption, generic LLM support, ordinary cloud usage, market plausibility, partner-chain inference, cloud-availability inference, investor/financier relationships, and generic Claude availability on a platform used by the counterparty do not establish the submitted relationship.
- The page must satisfy the submitted `evidence_role`. `relationship_statement` needs a public high-level relationship/adoption/distribution/integration statement, announcement, customer story, partner page, product/platform page, or comparable source whose main job is to state the qualifying relationship. `substance_detail` needs relationship-specific concrete detail beyond a bare announcement, partner overview, logo, directory entry, broad catalog card, or press-wire mirror: implementation docs, model/deployment details, named service or training offering, product configuration detail, release note, workflow detail, case-study substance, or comparable detail normally from the counterparty/product/platform/customer/builder's own public channel or an official technical joint channel.

Write one JSON object per line to `results_claude_public_relationship_evidence_graph.jsonl`:
{"item": { "relationship_family": "<relationship_family>", "counterparty": "<counterparty>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

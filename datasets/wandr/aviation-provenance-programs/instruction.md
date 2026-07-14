You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `aviation_provenance_programs`
  - `aviation_provenance_programs.independent_confirmation`

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

## `aviation_provenance_programs`

For 25+ named public aviation blockchain, DLT, or verifiable-provenance deployments or participant-specific implementations, cover each of the 3 evidence roles listed here with a source (i.e. 1+ URL under each role) about the same deployment, using the role's stated source class.

The work is public provenance mapping for aviation hard assets and regulated records, not commercial diligence. A valid root is narrower than a vendor platform, marketplace, project roster, consortium, alliance, or category page: it should be a named deployment, pilot, customer/counterparty rollout, regulator or standards implementation phase, dated implementation milestone, or similar public initiative with a named aviation participant or implementation context.

Participant variants under one overarching project collapse into that overarching root unless public evidence proves all three of these root-specific facts: a source-class-appropriate mechanism/scope source, a participant-owned or counterparty-owned confirmation surface, and a dated status/scale source from a different source class. A page that lists Air Canada, Jazz, Safran, Bollore, AFI KLM E&M, Parker, Honeywell, Thales, Satair, or other contributors to a broad project/alliance/platform does not create one root per contributor by itself.

Evidence roles:
- `primary_mechanism_scope`: a provider, originator, official program, regulator/standards, or original technical source that identifies the submitted deployment or implementation phase as its own public root and states both the qualifying trust mechanism (blockchain, DLT, immutable ledger, Hyperledger/Fabric, smart contracts, tokenized digital twin/passport, aircraft/part NFT, cryptographic provenance, or comparable tamper-evident provenance/authenticity mechanism) and the aviation hard asset, regulated record, or lifecycle workflow it covers; an independent trade/status article, participant-owned confirmation page, or generic provider homepage does not satisfy this role.
- `counterparty_or_participant_confirmation`: a participant-owned or counterparty-owned aviation surface centered on a named customer, operator, OEM, MRO, lessor, regulator, standards body, implementation partner, or other non-provider counterparty that confirms its own role in the submitted deployment; provider-authored announcements, generic case studies, independent trade/status articles, alliance pages, marketplace pages, and project rosters do not satisfy this role.
- `dated_deployment_scale_or_status`: a dated independent trade, aerospace/aviation media, industry event, or public status surface distinct from the mechanism and participant-confirmation source classes, proving implementation status for the submitted deployment: pilot, proof of concept, go-live, completion, signed commitment, data-loading milestone, named asset/record volume, public event, or comparable concrete status/scale signal tied to the same root; provider mechanism pages, participant-owned confirmation pages, formal deliverables/filings/procurement records reserved for the independent-confirmation subtask, and parent-alliance launch dates do not satisfy this role.

The trust mechanism must be source-stated. Generic digital records, cloud MRO, AI search, ordinary traceability, secure-platform, or maintenance-management pages do not count unless the page states the qualifying trust or provenance mechanism. Passenger identity, loyalty, ticketing, payment/settlement, baggage, and consumer travel NFT projects are out of scope unless the same deployment also clearly satisfies the hard-asset or regulated-record provenance bar.

Sources should materially address the named deployment and fit the role's source class. Provider, originator, official-program, regulator/standards, or original technical surfaces fit `primary_mechanism_scope`; participant-owned or counterparty-owned aviation surfaces fit `counterparty_or_participant_confirmation`; independent trade/status, industry-event, or public status surfaces fit `dated_deployment_scale_or_status`. Generic market lists, broad explainers, fictional reference architectures, generic platform homepages, generic digital-record tools, and technical-only artifacts not tied to a named public deployment do not establish a parent deployment by themselves. Historical pilots and dormant initiatives can count as historical public evidence, but current status must not be inferred from old announcements.

This task also has a same-root `independent_confirmation` subtask, checked as of 2026-06-30. Parent rows should not rely on one broad Digital Aviation Record System, SITA MRO Blockchain Alliance, Honeywell GoDirect, SkyThread, Accenture-Thales, Block Aero, Parts Pedigree, or Satair page to complete many roots or many roles. Those pages can support the overarching program or a truly specific rollout when the source class and root are scoped that way; they do not complete separate participant roots without distinct implementation evidence.

Requirements:
- The page must identify the submitted deployment or implementation, or a clearly named phase, counterparty, or regulator/standards phase of the same public initiative.
- The page must visibly fit the source class for the submitted evidence role.
- The page must support the submitted evidence role according to the listed role definitions.

Write one JSON object per line to `results_aviation_provenance_programs.jsonl`:
{"item": { "deployment_or_implementation": "<deployment_or_implementation>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `aviation_provenance_programs.independent_confirmation`

Cross-tasknode identifier discipline: this task is for the same {= deployment_or_implementation =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= deployment_or_implementation =}+ aviation blockchain, DLT, or verifiable-provenance deployments, provide 1+ public URL from a formal source class outside the parent evidence roles: a regulator or standards record, public program deliverable, grant/project page, procurement or filing record, authority-hosted event page, court/government record, or comparable formal institutional source confirming the same root.

As checked on 2026-06-30, old pilots, proofs of concept, and completed regulator studies can count as historical confirmation. Current operational use should only be treated as current when the cited page itself says so.

The confirmation page must be meaningfully separate from the source classes used by the parent roles. Do not use provider announcements, provider case studies, generic vendor product pages, platform homepages, marketplace pages, customer/logo lists, broad project rosters, alliance launch announcements, participant-owned confirmation pages, independent trade/status articles, press-wire duplicates of the same announcement, or articles that merely list contributors. The formal confirmation source can qualify only when it confirms the same root and implementation scope.

Requirements:
- The page must visibly belong to the formal confirmation source class rather than to the parent mechanism, participant-confirmation, or dated trade/status source classes.
- The page must confirm the same submitted deployment or implementation root, not merely a parent program, platform, alliance, marketplace, contributor name, or adjacent actor.
- For a participant-specific root under a broad program, the page must support a distinct deployment action and asset/record workflow or implementation phase for that participant.

Write one JSON object per line to `results_aviation_provenance_programs.independent_confirmation.jsonl`:
{"item": { "deployment_or_implementation": "<deployment_or_implementation>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

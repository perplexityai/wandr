You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `dach_ai_implementers`
  - `dach_ai_implementers.company_country_nexus`

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

## `dach_ai_implementers`

For each DACH country listed below, identify 20+ company-country pairs that are public enterprise-AI implementers; for each pair cover each of the 3 evidence roles listed below with a source, i.e. 1+ URL per role, showing concrete enterprise-AI implementation capability.

Countries in scope:
- **Austria**
- **Germany**
- **Switzerland**

The evidence roles of interest, which we refer to as `evidence_facet`, are:
- `own_capability_artifact`: a first-party or officially controlled company surface showing a named enterprise-AI product, platform, artifact, service, documentation, repository, or technical implementation mechanism, such as RAG, agents, workflow automation, tool connectors, sovereign or on-prem architecture, or production GenAI integration.
- `external_validation`: a non-company-owned or ecosystem-owned page validating the company's AI implementation standing, such as a cloud or model partner directory, marketplace offer, app exchange listing, vendor competency page, conference or industry page, or comparable third-party surface that is AI-specific and names the company, offering, competency, platform, or role.
- `delivery_trace`: a case study, customer story, implementation description, customer quote, project page, partner or cloud case page, conference talk, release, or reputable article showing a concrete delivered AI use case or implemented workflow. A named customer is high signal; a sufficiently specific anonymized delivery can qualify when the sector, use case, and implementation detail are visible.

The company must be a real company or productized implementation vendor, not a listicle category, buyer, model name, platform family, individual consultant, or internal project name. The task is public capability provenance only; it is not a request for rankings, scoring, acquisition screening, buyer lists, investment advice, contacts, email or phone collection, outreach, lead scoring, or enrichment.

Requirements:
- The page must clearly identify the submitted company.
- The page must show concrete enterprise-AI implementation capability: a named product or platform, named technical mechanism, named deployment or use case, or similarly specific public implementation artifact. Generic AI consulting, AI strategy, digital transformation, AI readiness, or broad advisory positioning alone is not enough.
- The page should make its `evidence_facet` source role visible: first-party or official controlled surface for `own_capability_artifact`; non-company-owned ecosystem, marketplace, partner, vendor, event, analyst, or publication surface for `external_validation`; delivered-project, customer, implementation, case, release, talk, or article surface for `delivery_trace`.
- The page should expose facet-specific provenance: owned product/service/technical artifact for `own_capability_artifact`; AI-specific third-party validation that names the company, offering, competency, platform, or role for `external_validation`; concrete customer/project/use-case/workflow/implementation detail for `delivery_trace`.

Write one JSON object per line to `results_dach_ai_implementers.jsonl`:
{"item": { "country": "<country>", "company": "<company>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `dach_ai_implementers.company_country_nexus`

Cross-tasknode identifier discipline: this task is for the same {= country_company =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For the parent task's company-country pairs, supply a public company-country nexus source, i.e. 1+ URL, showing that the submitted company is tied to the submitted DACH country by headquarters, registered office, local legal entity, official office or imprint, marketplace seller identity, partner profile geography, registry entry, or comparable company-country evidence.

Registry entries and company databases can qualify for this nexus task when they establish the company-country tie, but they do not establish enterprise-AI implementation capability.

Requirements:
- The page must clearly identify the submitted company.
- The page must tie the company to the submitted country through a public company-country nexus, such as headquarters, registered office, local legal entity, official office or imprint, marketplace seller identity, partner profile geography, registry entry, or comparable evidence.
- The page should communicate the nexus source standing: official company surface, public registry or company database, partner or marketplace profile, or comparable public company-country source. A generic listicle or article that merely mentions a country without company-location evidence is not enough.

Write one JSON object per line to `results_dach_ai_implementers.company_country_nexus.jsonl`:
{"item": { "country": "<country>", "company": "<company>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

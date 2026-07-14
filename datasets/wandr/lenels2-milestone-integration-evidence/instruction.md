You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `lenels2_milestone_integration_evidence`
  - `lenels2_milestone_integration_evidence.corroboration_context`

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

## `lenels2_milestone_integration_evidence`

For 45+ distinct source-stated ACS/VMS integration edges involving at least one LenelS2, Milestone/XProtect, or Arcules anchor family listed below as of 2026-06-29, supply public source evidence for the edge (i.e. 1+ URL per edge).

This is a public provenance table for physical-security interoperability claims: what exact systems are connected, what source-stated capability or deployment evidence exists, which side says it, and where public sources are thin, stale, gated, or contradictory. A separate `corroboration_context` sidecar asks for additional corroboration or context evidence for 15+ of these same integration-edge identifiers; do not force every root edge to have every source role. This is not a vendor ranking, procurement recommendation, security architecture recommendation, pricing estimate, lead list, contact lookup, outreach list, or contact-enrichment task.

Anchor families:
- LenelS2 family: LenelS2, Honeywell/Carrier LenelS2, OnGuard, OnGuard Cloud, Elements, NetBox/NetVR when clearly tied to LenelS2
- Milestone/XProtect family: Milestone Systems, Milestone XProtect, XProtect Access, XProtect on AWS, cloud-hosted XProtect, Milestone marketplace or partner-finder XProtect surfaces
- Arcules family: Arcules VSaaS, Arcules Cloud, Milestone/Canon Arcules surfaces, Arcules plugin/help/datasheet surfaces

Source roles worth recording when supported, with corroboration/context counted in the sidecar subset rather than as mandatory roles for every edge:
- primary capability source: edge-specific page that states the basic integration substance or deployment context
- counterpart or technical source: counterpart-side page, help article, guide, PDF, marketplace/per-listing page, or similar corroboration for the same edge
- deployment/license/context source: page that contributes deployment wording, license/SKU/pricing, compatibility, version, assurance, source-date/history, limitation, or source-visible missing/conflict context tied to the edge

Use public official product pages, help docs, integration guides, PDFs, partner pages, marketplace or per-listing pages, press releases, cloud-provider case studies, trust/security pages, and source-specific support articles when they substantiate the edge. Reseller pages and reputable security-industry articles can count as labeled secondary context for price/SKU/date/certification/history details. Listicles, rankings, "best cloud VMS" articles, and paywalled aggregator summaries do not count as primary evidence.

Each root row should keep source wording narrow: name the connected systems, preserve any stated directionality, copy or paraphrase deployment wording faithfully, and record optional source role, license/pricing/SKU, version, scalability, compliance/certification, source-date, checked-date, limitation, missing-state, or conflict-state details only when the public source supports them. Use the sidecar subtask for additional counterpart, technical, deployment, licensing, date, limitation, or conflict context on a counted subset of edges. Do not infer SaaS, cloud-hosted, hybrid, VSaaS, gateway, bidirectionality, price, or certification status from general product positioning.

Requirements:
- The page must identify the submitted integration edge by naming both connected systems, platforms, products, or families, with at least one endpoint belonging to an in-scope anchor family.
- The page must fit public provenance use for the edge: an edge-specific official, partner, help, guide, PDF, marketplace/per-listing, press, cloud-provider, trust/security, support, reseller, or reputable security-industry source that substantiates the edge, not a generic logo wall, ranking, procurement comparison, implementation manual detached from public provenance, contact list, private account surface, or lead-generation page.
- The page must contribute a concrete source-stated finding about the edge, such as events, alarms, door lock/unlock, cardholder or credential context, video verification, live/playback video, PTZ, camera-door mapping, monitoring workflow, API/connector setup, license/SKU, version compatibility, cloud/hybrid deployment, stated limitation, assurance, or similar.
- Any claimed deployment wording, directionality, pricing/licensing/SKU, scalability/compliance, source date, checked date, limitation, missing state, or conflict state must be faithful to the cited page rather than inferred from outside assumptions.

Write one JSON object per line to `results_lenels2_milestone_integration_evidence.jsonl`:
{"item": { "integration_edge": "<integration_edge>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `lenels2_milestone_integration_evidence.corroboration_context`

Cross-tasknode identifier discipline: this task is for the same {= integration_edge =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For at least 15 of the root task's integration-edge identifiers, supply 1+ additional public URL per edge that provides corroboration or source-state context as of 2026-06-29. Use the exact `integration_edge` strings already emitted in the root task.

This is a counted subset surface, not a universal role checklist. Choose root edges where public counterpart, technical, deployment, licensing, date/history, limitation, assurance, missing-state, or conflict-state evidence is findable. Do not create new edges only for this subtask, and do not force weak evidence for every root edge.

Eligible corroboration/context roles:
- counterpart or technical source: counterpart-side page, help article, guide, PDF, marketplace/per-listing page, or similar corroboration for the same edge
- deployment/license/context source: page that contributes deployment wording, license/SKU/pricing, compatibility, version, assurance, source-date/history, limitation, or source-visible missing/conflict context tied to the edge

Requirements:
- The page must identify the same submitted integration edge by naming both connected systems, platforms, products, or families, with at least one endpoint belonging to the LenelS2, Milestone/XProtect, or Arcules anchor scope established in the root task.
- The page must be useful as additional corroboration or context for the edge: counterpart-side source, technical/help/guide/PDF source, marketplace or per-listing source with edge-specific details, or a page contributing deployment, license/SKU/pricing, compatibility, version, source date/history, limitation, missing/conflict, assurance, or similar context.
- The page must contribute a concrete source-stated corroborating or contextual finding about the edge, not merely repeat a generic partner, integration, or seamless-solution claim.
- Any claimed deployment wording, directionality, pricing/licensing/SKU, scalability/compliance, source date, checked date, limitation, missing state, or conflict state must be faithful to the cited page rather than inferred from outside assumptions.
- Keep the same safe public-provenance frame as the root task: no ranking, procurement recommendation, security architecture recommendation, pricing estimate, lead list, contact lookup, outreach list, contact enrichment, private-account extraction, or private-system assessment.

Write one JSON object per line to `results_lenels2_milestone_integration_evidence.corroboration_context.jsonl`:
{"item": { "integration_edge": "<integration_edge>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

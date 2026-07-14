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

## `ai_server_hardware_relationships`

For each of the 8 AI server hardware supply-chain layers listed below, name 10+ source-backed relationships per layer between an upstream company and a downstream company; for each relationship, supply both of the 2 evidence roles below with 1+ URL per role.

This is a public provenance ledger for AI server hardware relationships, not a dependency scorecard. Each row must tie the company pair to a concrete named hardware artifact, process, platform, deployment, facility, manufacturing node/package, or infrastructure design. Inferred customer identities, rankings, market-share estimates, procurement guidance, investment framing, outreach leads, and aggregated exposure conclusions are out of scope.

A relationship edge is scoped by `supply_chain_layer`, `upstream_company`, and `downstream_company`. The same two companies can appear in more than one layer only when the cited page supports the distinct layer-specific relationship.

Supply-chain layers:
- `semiconductor_equipment_and_eda_ip`: equipment, process tooling, EDA, and design-IP relationships used to build AI silicon
- `foundry_and_wafer_manufacturing`: wafer fabrication, foundry, and process-node manufacturing relationships
- `advanced_packaging_substrates_interposers`: advanced packaging, substrates, interposers, chiplet integration, and related assembly relationships
- `hbm_and_server_memory`: HBM, DRAM, and server-memory relationships tied to AI accelerators or AI systems
- `accelerators_cpus_custom_asics`: GPU, CPU, XPU, accelerator, and custom-ASIC relationships for AI compute platforms
- `server_oem_odm_rack_integration`: server OEM, ODM, rack-scale integration, and system-integration relationships
- `networking_optics_interconnect`: AI cluster networking, optics, switching, NIC, cable, and interconnect relationships
- `power_cooling_datacenter_infrastructure`: power, cooling, liquid-cooling, and data-center physical-infrastructure relationships

Evidence roles:
- `primary_or_counterparty_source`: a source controlled by, issued by, or officially filed by one of the two relationship parties
- `independent_public_context`: a reputable public source independent of both relationship parties that names the same relationship and layer context

Requirements:
- The page must match `evidence_role`: `primary_or_counterparty_source` needs a source controlled by, issued by, or officially filed by one of the relationship parties; `independent_public_context` needs a reputable public source independent of both relationship parties.
- The page must explicitly bind both named companies to the relationship. Anonymous customer labels, broad category references, and relationship claims inferred only from market position do not count.
- The page must support the claimed supply-chain layer through source-stated AI server hardware context, such as a product, component, process, platform, filing disclosure, co-development, supply, customer, integration, or infrastructure relationship. Claimed product, component, process, date, period, or exposure details must be source-stated.
- The page must identify the concrete relationship artifact/process/platform/deployment/facility/node/package/design for this exact company pair. Generic partner lists, comma-separated rosters, broad ecosystem pages, market maps, compatibility catalogues, and pages that merely say both companies participate in a layer do not count unless they source-state a specific named hardware context for the submitted pair.

Write one JSON object per line to `results_ai_server_hardware_relationships.jsonl`:
{"item": { "supply_chain_layer": "<supply_chain_layer>", "upstream_company": "<upstream_company>", "downstream_company": "<downstream_company>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

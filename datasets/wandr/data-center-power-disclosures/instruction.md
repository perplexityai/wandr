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

## `data_center_power_disclosures`

Identify 40+ operators as public reporting or public-company-equivalent operators / developers of data-center, colocation, HPC, AI-infrastructure, powered-campus, or similar infrastructure assets; for each operator, cover each of the 5 disclosure facets listed below and each `evidence_side` listed below, and provide 1+ meaningfully distinct public power-delivery signal per operator-facet-side, each backed by a source (i.e. 1+ URL). The cited source, filing, or event should visibly fall within 2024-01-01 through 2026-04-02.

Data-center growth is often constrained less by land than by energization, interconnection, equipment lead times, and customer-delivery timing; this task is about what public company and official-source materials actually say on those points.

Disclosure facets:
- `capacity_or_energization`: public signals about capacity, MW, critical IT load, energization, power coming online, operational data-center capacity, or construction reaching powered service.
- `power_access_or_interconnection`: public signals about secured power, utility access, grid connection, interconnection, load study, large-load service, power sourcing, or power availability for data-center assets.
- `long_lead_electrical_equipment_or_supply_chain`: public signals about named electrical equipment classes, supplier capacity, switchgear, transformers, UPS, generators, power skids, substations, cooling/power infrastructure, or supply-chain timing for data-center delivery.
- `customer_delivery_or_backlog_timing`: public signals about lease, booking, backlog, contracted capacity, commencement, phased delivery, ready-for-service timing, or customer handoff for data-center/HPC/AI-infrastructure capacity.
- `mitigation_or_power_strategy`: public signals about concrete actions or strategy for power constraints, supply-chain resilience, energy sourcing, renewable/clean-power coverage, demand response, behind-the-meter power, battery/storage, grid flexibility, or comparable mitigation.

Evidence sides:
- `operator_disclosure`: operator-controlled public disclosure, filing, report, release, investor material, transcript, or strategy/sustainability report that states the operator-side power-delivery signal
- `delivery_ecosystem_anchor`: materially distinct non-operator utility, regulatory, commission, docket, supplier, customer, counterparty, public-authority, or comparable official/source surface that anchors the delivery ecosystem, equipment, interconnection, service, or customer-delivery context

The operator ought to be a reporting company or public-company-equivalent infrastructure operator / developer. A pure software or cloud-services company does not count merely because a filing mentions third-party hosting services, virtual data centers, office operations, or generic business-continuity risk.

The sources should be public disclosure or official-source surfaces: SEC filings, annual or quarterly reports, official investor materials, company releases, identifiable earnings or conference transcripts, official supplier/operator releases, sustainability or power strategy reports, or official utility/regulatory/commission/tariff/docket pages that state relevant source-visible facts. Utility and regulatory pages count only for the facts they state; tariff burden, legality, customer-cost fairness, buyer guidance, or rate-impact conclusions are outside this task.

Signals under the same operator, disclosure facet, and evidence side should be meaningfully different public evidence points, not paraphrases of the same statement, the same paragraph, the same generic risk factor, or a source/date/source-type label recast as a finding. A valid `power_signal` is a concrete source-backed claim, normally including the named project, customer/counterparty, MW/capacity amount, equipment class, date/status, lease/backlog/delivery milestone, or named strategy/action visible on the page. Generic facet labels such as "public signal of capacity", "public signal of power access", or "public signal of mitigation strategy" do not count. The two evidence sides should normally come from different source roles: an operator-side disclosure and a non-operator delivery-ecosystem anchor such as a utility, regulatory, supplier, customer, public-authority, or comparable official/source surface.

Requirements:
- The page should communicate that it is a public disclosure or official-source surface fit for the claimed `evidence_side`: operator-controlled disclosure for `operator_disclosure`, or a materially distinct non-operator utility, regulatory, docket, supplier, customer, counterparty, public-authority, or comparable delivery-ecosystem source for `delivery_ecosystem_anchor`. An operator-controlled page, operator investor release, operator filing, or operator sustainability report fails the `delivery_ecosystem_anchor` side even when it names a utility, supplier, customer, or power strategy.
- The page must visibly place the source, filing, event, transcript, release, or source-stated signal within 2024-01-01 through 2026-04-02.
- The page must identify the operator or a clearly tied project, campus, facility, lease, customer delivery, supplier agreement, or official service context for that operator.
- The page must tie the statement to data-center, colocation, HPC, AI-infrastructure, powered-campus, hyperscale, or similar infrastructure assets, not generic corporate operations.
- The page must state a concrete signal scoped to `disclosure_facet`: capacity, MW, critical IT load, energization timing, power/interconnection/service context, named long-lead equipment or supplier capacity, lease/backlog/customer-delivery timing, or a concrete mitigation / power strategy. The record's `power_signal` must name that concrete signal rather than restating the facet. Generic risk-factor language is not enough unless it contains operator-specific data-center infrastructure substance.

Write one JSON object per line to `results_data_center_power_disclosures.jsonl`:
{"item": { "operator": "<operator>", "disclosure_facet": "<disclosure_facet>", "evidence_side": "<evidence_side>", "power_signal": "<power_signal>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

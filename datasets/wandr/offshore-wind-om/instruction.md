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

## `offshore_wind_om`

For each of the 7 offshore-wind O&M role families below, identify 30+ organization capability units per role family; for each such organization-capability unit and each of the 2 evidence sides, supply a public evidence source (i.e. 1+ URL).

The aim is a public capability-evidence map of the offshore-wind O&M ecosystem, not supplier selection, outreach, ranking, procurement advice, due diligence, or a complete supplier directory.

The role families of interest, which we refer to as `role_family`, are:
- `om_services`: broad offshore-wind operations and maintenance service packages, operational support, scheduled or corrective maintenance, independent service-provider work, or O&M coordination.
- `blade_turbine_repair`: blade, turbine, rope-access, inspection, retrofit, component-replacement, or wind-turbine-generator repair and maintenance work.
- `bop_hv_substation`: balance-of-plant, foundations, subsea, cable, high-voltage, offshore-substation, OFTO, electrical-safety, condition-monitoring, or related operational infrastructure support.
- `marine_logistics_access`: crew-transfer vessels, SOVs, workboats, O&M bases, marine coordination, lifting, crane, access, or crew/equipment transfer for offshore wind O&M.
- `component_fabrication_spares`: offshore-wind components, secondary steel, CNC or fabricated parts, remanufactured spares, repair facilities, or maintenance-relevant component supply.
- `training_competence`: GWO, offshore-wind safety, high-voltage, blade, rescue, access, or technical competence training for wind workforces.
- `certification_qa_integrity`: certification, inspection, NDT, QA/QHSE, asset integrity, technical documentation, certificate management, or comparable assurance scope for offshore-wind assets or components.

The evidence sides of interest, which we refer to as `evidence_side`, are:
- `capability_claim`: a page that source-states the organization's claimed offshore-wind or wind-O&M capability.
- `practice_trace`: a distinct public trace that anchors the capability in applied work, authority, accreditation, certification, project, contract, programme, or comparable externally scoped evidence.

An `organization_capability` ought to pair a real organization with a concrete role-specific capability scope, not a broad supplier category or undifferentiated "offshore wind" label. Generic fabrication, generic QA, generic training, job-board, professional-profile, construction-opportunity, and compliance-SaaS surfaces count only when they tie the claimed scope to offshore wind O&M, offshore wind components or spares, inspection, certification, training, NDT, asset integrity, project work, or performed / authority-scoped work.

Requirements:
- The page must identify the claimed organization.
- The page must tie the claimed capability scope to the selected `role_family`: for `om_services`, offshore-wind O&M service or operational-support scope; for `blade_turbine_repair`, blade, turbine, rope-access, inspection, retrofit, repair, or component-replacement scope; for `bop_hv_substation`, balance-of-plant, cable, high-voltage, substation, electrical-safety, condition-monitoring, subsea, or foundation scope; for `marine_logistics_access`, vessel, workboat, O&M-base, marine-coordination, lifting, crane, access, or transfer scope; for `component_fabrication_spares`, offshore-wind component, spare, secondary-steel, fabrication, repair-facility, remanufacturing, or named project-supply scope; for `training_competence`, wind-workforce training, GWO, safety, rescue, high-voltage, blade, access, or technical-competence scope; for `certification_qa_integrity`, certification, inspection, NDT, QA/QHSE, asset-integrity, technical-documentation, certificate-management, or assurance scope.
- The page must satisfy the selected `evidence_side`: for `capability_claim`, the page must source-state a concrete capability, service, component/spares, training, certification, inspection/QA, asset-integrity, or maintenance-relevant scope for the organization; for `practice_trace`, the page must provide a concrete trace such as a named project, contract, case, operator or trade-source report, authority listing, accreditation or certification scope, GWO module/provider scope, F4OR/OWGP-style programme profile, project supplier page naming performed scope, credible industry article, or comparable externally scoped trace. A broad directory category label alone is not enough for either side.

Write one JSON object per line to `results_offshore_wind_om.jsonl`:
{"item": { "role_family": "<role_family>", "organization": "<organization>", "capability_scope": "<capability_scope>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

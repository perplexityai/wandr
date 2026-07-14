You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `starlink_eband_evidence`
  - `starlink_eband_evidence.named_external_hardware_supply`
  - `starlink_eband_evidence.internal_rf_hardware_capability`

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

## `starlink_eband_evidence`

Within the fixed `starlink_eband_public_evidence` atlas scope, supply 50+ distinct E-band gateway deployment-need signals and 1+ URL for each signal.

This node is about public traces showing Starlink or SpaceX E-band gateway demand, earth-station use, filings, authorizations, call signs, sites, capacity pressure, or spectrum use. It is one part of a public evidence atlas that separately covers named external hardware supply and internal RF hardware capability; it is not a binary verdict about whether SpaceX insources E-band SSPAs.

Sources should be public and page-specific. Regulatory filings, regulator pages, public notices, consultation documents, filings indexes, company filings, and reputable technical or trade sources can all work when the page substance supports a concrete Starlink/SpaceX E-band deployment-need signal.

Requirements:
- The page must support the submitted `signal_identifier` as a concrete SpaceX/Starlink E-band deployment-need public trace, with a source-specific identifier such as an application, call sign, gateway site, authorization, filing, public-notice item, consultation, frequency band, effective date, or comparable anchor.
- The page must show Starlink/SpaceX E-band gateway, earth-station, STA, authorization, filing, spectrum-use, site, capacity-demand, or comparable deployment-need evidence.
- The page must preserve the claim boundary: E-band deployment need is not E-band SSPA sourcing evidence, named external supply evidence, or internal SpaceX RF hardware capability evidence unless the page separately says so.

Write one JSON object per line to `results_starlink_eband_evidence.jsonl`:
{"item": { "evidence_scope": "<evidence_scope>", "signal_identifier": "<signal_identifier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `starlink_eband_evidence.named_external_hardware_supply`

Cross-tasknode identifier discipline: this task is for the same {= evidence_scope =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

Within the fixed `starlink_eband_public_evidence` atlas scope, supply 20+ distinct named external hardware-supply signals and 1+ URL for each signal.

This node is intentionally narrower than the deployment and internal-capability nodes. Each signal needs a named external supplier, product, order, collaboration, report, customer relationship, or comparable public source tying Starlink or SpaceX to E-band or closely related high-frequency RF amplifier / front-end hardware.

Sources should be public and page-specific. Supplier disclosures, regulatory announcements, annual reports, investor presentations, company statements, and reputable trade or technical reports can all work when the page substance directly names the SpaceX/Starlink relationship and the relevant hardware.

Requirements:
- The page must support the submitted `signal_identifier` as a concrete named external hardware-supply public trace, with a source-specific identifier such as a supplier name, order value, contract date, product generation, report period, warrant milestone, customer quote, or comparable anchor.
- The page must show a named external supplier or product relationship tying Starlink/SpaceX to E-band or closely related high-frequency RF amplifier / front-end hardware. Generic product pages, unnamed "tier-1 LEO" customer claims, and broad supply-chain commentary without a named SpaceX/Starlink relationship do not count.
- The page must preserve the claim boundary: named external supply is not internal SpaceX RF hardware capability or E-band SSPA insourcing evidence unless the page separately says so.

Write one JSON object per line to `results_starlink_eband_evidence.named_external_hardware_supply.jsonl`:
{"item": { "evidence_scope": "<evidence_scope>", "signal_identifier": "<signal_identifier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `starlink_eband_evidence.internal_rf_hardware_capability`

Cross-tasknode identifier discipline: this task is for the same {= evidence_scope =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

Within the fixed `starlink_eband_public_evidence` atlas scope, supply 55+ distinct SpaceX internal RF hardware capability signals and 1+ URL for each signal.

This node is about SpaceX-owned or SpaceX-specific public traces of RFIC, MMIC, power-amplifier, RF front-end, high-frequency payload, test, design, production, manufacturing, patents, public statements, or adjacent amplifier capability. It is one part of a public evidence atlas that separately covers E-band deployment need and named external hardware supply; it is not a binary verdict about whether SpaceX insources E-band SSPAs.

Sources should be public and page-specific. SpaceX job postings, preserved job mirrors, patents, company statements, technical publications, public filings, and reputable technical or trade sources can all work when the page substance ties SpaceX/Starlink to relevant internal RF hardware activity.

Requirements:
- The page must support the submitted `signal_identifier` as a concrete SpaceX internal RF hardware capability public trace, with a source-specific identifier such as a job title, job ID, patent number, publication, public statement, date, facility/manufacturing signal, production-test responsibility, or comparable anchor.
- The page must show SpaceX-owned or SpaceX-specific RF design, test, production, manufacturing, RFIC/MMIC, amplifier, RF front-end, high-frequency payload, module, antenna-front-end, or closely related hardware capability. Generic RF roles with no relevant hardware anchor are too thin.
- The page must preserve the claim boundary: internal RFIC/MMIC, RF module, patent, production-test, payload, or TWTA evidence is not named external supply and is not automatically direct E-band SSPA insourcing evidence. TWTA / vacuum-electronics evidence can count only as adjacent internal amplifier capability, not solid-state SSPA evidence.

Write one JSON object per line to `results_starlink_eband_evidence.internal_rf_hardware_capability.jsonl`:
{"item": { "evidence_scope": "<evidence_scope>", "signal_identifier": "<signal_identifier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

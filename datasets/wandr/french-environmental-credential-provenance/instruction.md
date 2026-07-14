You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `french_environmental_credential_provenance`
  - `french_environmental_credential_provenance.credential_verification`

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

## `french_environmental_credential_provenance`

For each of the 4 French environmental technical-service segments below, cover 20+ French firm/SIREN pairs per segment, and for each firm supply 1+ source under each of the 3 evidence roles.

The work is an evidence-provenance dossier: operating brand, French legal entity, credential scope, and public scale often live on different public pages and sometimes disagree. The dossier is limited to descriptive public evidence provenance; supplier quality judgments, compliance conclusions, procurement rankings, valuations, investment or M&A advice, outreach targets, contacts, private addresses, and person data are outside the task payload.

Segments:
- `sites_sols_pollues`: sites et sols pollues, soil/groundwater pollution studies, SSP assistance, remediation engineering, or ICPE-adjacent polluted-site services
- `biodiversite_genie_ecologique`: biodiversity, ecological engineering, naturalist studies, wetland/ecosystem assessments, ecological restoration, or regulatory ecology services
- `eau_hydrogeologie`: water, hydrogeology, hydrology, aquatic-environment, wastewater, catchment, or water-quality technical services
- `mesures_environnementales`: environmental measurement, sampling, analysis, testing, air/noise/radon/water/solid-matrix monitoring, or comparable environmental laboratory/measurement services

The evidence roles, which we refer to as `evidence_axis`, are:
- `segment_profile`: firm-specific environmental technical-service activity in the selected segment.
- `legal_identity`: operating identity matched to a French legal entity, SIREN, or SIRET.
- `public_scale`: source-stated 2021-or-later scale or financial-publicness evidence for the same entity, such as turnover, effectif/headcount, size category, accounts-publicness, accounts-confidentiality, unavailable/stale accounts state, bounded scale, or an entity-conflict state.

`firm_siren` identifies the operating firm and a nine-digit SIREN. SIRET-level evidence can be cited, but the claimed `siren` should be the SIREN unless the page itself is exposing a different-entity conflict.

Requirements:
- The page must fit the selected `evidence_axis` role. `segment_profile` sources should be firm-specific profile, expertise, project, sector, issuer, or comparable pages with substantive environmental technical-service content; `legal_identity` sources should be public company records, official registers, firm legal pages, certificate identity blocks, or comparable identity sources; `public_scale` sources should be company-record, accounts, filing, registry, or comparable pages that can state scale or financial-publicness evidence. Generic directory stubs, broad NAF rows, and pages that only mention "ingenierie, etudes techniques" are not enough for `segment_profile`.
- The page must tie its evidence to the claimed firm/SIREN/SIRET, or clearly expose a relevant entity conflict such as parent, subsidiary, establishment, old entity, transferred establishment, or different-SIREN evidence. Segment-profile pages can tie through the operating name when the page does not itself state SIREN and does not contradict the claimed entity.
- The page must state the axis-specific evidence: substantive firm-specific activity inside the selected segment for `segment_profile`; legal or operating identity with SIREN/SIRET or equivalent French company-register identity for `legal_identity`; and source-stated 2021-or-later turnover, effectif/headcount, size category, accounts-publication state, accounts-confidentiality state, unavailable/stale accounts state, bounded value, or comparable scale/publicness state for `public_scale`.

Write one JSON object per line to `results_french_environmental_credential_provenance.jsonl`:
{"item": { "segment": "<segment>", "firm": "<firm>", "siren": "<siren>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `french_environmental_credential_provenance.credential_verification`

Cross-tasknode identifier discipline: this task is for the same {= firm_siren =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= firm_siren =}+ French firm/SIREN pairs, cover 1+ named environmental credential claim per firm, and for each credential claim supply 1+ source under each of the 2 evidence sides.

Credential provenance for the same legal entities can be an environmental qualification, accreditation, certification, ministerial approval, or equivalent formal recognition, but it needs a source-verifiable family and scope. Ordinary federation membership or a broad marketing badge is not enough unless an issuer, registry, authority, or ministerial record makes the scope meaningful.

The evidence sides, which we refer to as `credential_side`, are:
- `firm_claim`: a firm-controlled page, certificate page, profile page, or official firm-side channel claiming the named credential and scope.
- `issuer_record`: an issuer, registry, authority, accreditor, or ministerial source confirming the same entity, credential family, scope/domain, status, and date where available.

Requirements:
- The page must fit the selected `credential_side` role. `firm_claim` sources should be controlled by the claimed firm or be an official firm-side channel. `issuer_record` sources should be controlled by the issuer, registry, accreditor, public authority, ministerial source, or an official registry/attestation surface; another firm marketing page or unaffiliated directory is not enough.
- The page must tie the credential evidence to the claimed firm/SIREN/SIRET, or clearly expose a relevant entity conflict such as parent, subsidiary, establishment, old entity, transferred establishment, or different-SIREN evidence. Issuer-side records must match the claimed legal entity or make the mismatch visible.
- The page must confirm the claimed `credential_family` and `claimed_scope`. Firm-side pages must name the credential family and enough scope/domain to connect to the issuer-side claim. Issuer-side pages must confirm the same entity, credential family, scope/domain, and status/date when the source provides them.

Write one JSON object per line to `results_french_environmental_credential_provenance.credential_verification.jsonl`:
{"item": { "firm": "<firm>", "siren": "<siren>", "credential_family": "<credential_family>", "claimed_scope": "<claimed_scope>", "credential_side": "<credential_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

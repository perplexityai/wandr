You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `airport_biometric_border_gates`
  - `airport_biometric_border_gates.passenger_flow_rules`
  - `airport_biometric_border_gates.biometric_governance`

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

## `airport_biometric_border_gates`

For 20+ countries, territories, or self-governing border jurisdictions with automated biometric airport border-control processing, name 1+ program or responsible border authority per jurisdiction and supply 2+ concrete airport deployments per program, each backed by 1+ URL. A deployment can be an airport, terminal, lane group, checkpoint, or arrival/departure border flow, but it should be a concrete passenger-facing border-control setting rather than a generic national program page.

Deployment sources may be official border-authority, government, airport, airport-operator, vendor case-study, airport-technology release, or credible transport/trade press pages. Passenger check-in, bag drop, boarding, lounge access, airport building entry, aviation security screening, TSA/CLEAR-style identity screening, and digital travel-credential programs do not count unless the page explicitly ties the biometric processing to border, passport, or immigration control.

Requirements:
- The page must tie the deployment to the claimed border jurisdiction and named program or responsible border authority.
- The page must identify the claimed airport, terminal, lane group, checkpoint, or arrival/departure border flow.
- The page must show automated biometric processing for border, passport, or immigration control.
- The page must indicate a real passenger-facing implementation, rollout, installation, trial, or public availability rather than only a plan, procurement notice, or vendor capability pitch.

Write one JSON object per line to `results_airport_biometric_border_gates.jsonl`:
{"item": { "border_jurisdiction": "<border_jurisdiction>", "program_or_authority": "<program_or_authority>", "airport": "<airport>", "flow_or_checkpoint": "<flow_or_checkpoint>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `airport_biometric_border_gates.passenger_flow_rules`

Cross-tasknode identifier discipline: this task is for the same {= border_program =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= border_program =}+ automated biometric airport border-control programs or authorities, supply 2+ distinct official passenger-flow or eligibility rules per program, each backed by 1+ URL. Useful rules can describe eligible passenger cohorts, passport/document requirements, age limits, arrival versus departure scope, enrolment or prior-registration conditions, manual alternative conditions, or how a passenger becomes able to use the automated border-control lanes.

Only official border-authority, immigration, government, or official airport pages count here. Third-party news, vendor case studies, Wikipedia-style summaries, and generic travel advice do not count for passenger-flow rules.

Requirements:
- The page must tie the rule to the claimed program or responsible border authority in the claimed border jurisdiction.
- The page must communicate official border, immigration, government, or airport authority.
- The page must state a concrete passenger-flow, eligibility, enrolment, document, age, nationality, arrival/departure, or use-condition rule for the claimed program.

Write one JSON object per line to `results_airport_biometric_border_gates.passenger_flow_rules.jsonl`:
{"item": { "border_jurisdiction": "<border_jurisdiction>", "program_or_authority": "<program_or_authority>", "flow_or_cohort": "<flow_or_cohort>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `airport_biometric_border_gates.biometric_governance`

Cross-tasknode identifier discipline: this task is for the same {= border_program =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= border_program =}+ automated biometric airport border-control programs or authorities, supply 1+ official, legal, regulatory, or official privacy/data-governance URL per program describing data-handling controls for the program's biometric border processing.

The page should be an official border-authority, immigration, government, regulator, official airport, legal, or official privacy/data-governance page. It should describe biometric data handling such as retention or deletion, legal basis, opt-out or manual alternatives, database checks, access rights, sharing, secure transfer or storage, or comparable governance details.

Requirements:
- The page must tie the biometric governance information to the claimed program or responsible border authority in the claimed border jurisdiction.
- The page must communicate official, legal, regulatory, or official privacy/data-governance authority.
- The page must describe a biometric data-handling or governance rule for that border-control program, beyond mere biometric modality, enrolment, or identity-comparison mechanics.

Write one JSON object per line to `results_airport_biometric_border_gates.biometric_governance.jsonl`:
{"item": { "border_jurisdiction": "<border_jurisdiction>", "program_or_authority": "<program_or_authority>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

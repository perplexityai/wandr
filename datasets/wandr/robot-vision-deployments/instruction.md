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

## `robot_vision_deployments`

For each of the 4 use cases listed below, supply evidence for at least 18+ fielded deployment cases per use case where perception guides robot or automation-cell action; for every deployment case, supply evidence for each of the 2 evidence roles listed below, with 1+ URL for each role.

This should be a use-case-first atlas of deployed systems, not a vendor, integrator, product, or logo-reference directory. Keep a provider- and customer-diverse set inside each use case when the public source ecology allows it; repeated customers or providers should represent materially distinct sites, tasks, or rollouts rather than thin variants of the same case.

Use cases:
- `warehouse_parcel_handling`: warehouse logistics deployments such as parcel, package, item, tote, or pallet handling; depalletizing or truck unloading; induction, fulfillment, or sortation.
- `manufacturing_line_operations`: factory-line or production-cell deployments such as assembly, fastening, dispensing, de-racking, bin-picking, machine tending, robot-guided inspection/rework, surface treatment, or finishing.
- `recycling_material_sorting`: recycling, waste, material-recovery, MRF, landfill-diversion, or secondary-material sorting deployments where AI/vision triggers robotic or otherwise actuated sorting.
- `agri_food_field_operations`: field, greenhouse, farm, nursery, or food-production deployments such as harvesting, weeding, pruning, spraying, crop/fruit handling, or packing where perception triggers robot/mechanical action.

Evidence roles:
- `provider_stack_detail`: evidence from a provider, integrator, robot supplier, vision vendor, or automation partner connecting the deployment's robot or automation cell to camera, 3D vision, machine perception, or live sensor guidance that controls the robot/mechanical action. Perception AI counts only when tied to deployed vision or sensor inputs guiding the action; generic AI control or programming claims are not enough. Clearly provider-authored third-party wire releases can satisfy this role when they are deployment-specific.
- `independent_deployment_confirmation`: customer/operator-hosted or independent editorial, trade, local-news, government, project, technical, or comparable evidence confirming the same bounded deployment and a concrete operational fact. Provider, integrator, robot-supplier, vision-vendor, automation-partner, sponsored vendor-channel, or provider-authored wire release pages do not satisfy this role.

A `deployment_case` should identify one bounded fielded case, usually by customer/operator, site or bounded rollout, task/process, and provider/technology context. Real-facility, real-farm, or customer/operator operational pilots can count, but lab demos, trade-show demonstrations, pre-rollout tests, procurement-only announcements, and planned future installations do not. Anonymous customer cases can count only when the page gives enough contextual anchors to distinguish the case from other deployments.

The two evidence roles require disjoint source classes, so the same URL should not appear under both roles for the same deployment case. Do not use generic product pages, logo walls, trade-show demos, lab-only prototypes, passive machine-vision QA dashboards, optical sorters without robot/mechanical actuation, or pages that merely say a vendor "can" automate a task.

For each URL, include a concise `answer.finding` stating the concrete evidence the page supports for the requested role.

Requirements:
- The page must clearly tie to the named fielded deployment case, with enough customer/operator, site or bounded rollout, deployed task/process, and provider/technology context to distinguish the case from generic vendor claims.
- The page must fit the submitted use-case bucket.
- The page must connect the deployment to robot, automation-cell, autonomous-implement, or mechanical actuation; passive inspection/QA, dashboards, analytics-only monitoring, and non-actuated optical sorting do not count.
- The page must satisfy the requested evidence role: deployment-specific robot/cell stack detail tying machine perception, vision, or live-sensor guidance to action for `provider_stack_detail`, or confirmation of the same bounded deployment and a concrete operational fact for `independent_deployment_confirmation`.
- `answer.finding` must be page-grounded and role-specific, not a generic restatement of the deployment case name.

Write one JSON object per line to `results_robot_vision_deployments.jsonl`:
{"item": { "use_case": "<use_case>", "deployment_case": "<deployment_case>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

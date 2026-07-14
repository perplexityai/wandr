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

## `business_restraint_decision_event_provenance`

For each of the 5 business restraint modes listed below, identify 20+ public company decision events, and for each (`company`, `decision`) event supply one public source for each of the 3 evidence roles (i.e. 1+ URL per role).

A qualifying event is a source-stated decision by a company, board, management team, or comparable company authority to stop, withdraw, exit, delay, slow, cut back, simplify, or otherwise restrain a concrete business action. The task is about public provenance for decision events, not lessons, rankings, recommendations, biographies, contact collection, procurement advice, investment advice, legal advice, or reputational judgment.

The `restraint_mode` values are:
- `product_or_service_discontinuation`: ending, retiring, or winding down an existing product, service, program, or offering.
- `market_or_business_exit`: leaving a geography, customer segment, operating market, channel, division, or business line.
- `cancelled_or_withdrawn_plan`: canceling or withdrawing a planned launch, IPO/offering, deal, expansion, facility/project, or initiative before completion.
- `growth_or_investment_restraint`: pausing, slowing, capping, or deferring expansion, investment, hiring, capacity, growth, or rollout.
- `simplification_or_focus_cutback`: a concrete simplification or focus decision that reduces product lines, features, operations, commitments, portfolio scope, or strategic spread.

For each (`company`, `decision`) event, provide these `evidence_role` values:
- `formal_decision`: an authority-bearing public source for the decision and its timing, such as a company-controlled page, issuer release, securities filing, proxy/board record, public regulatory filing, or equivalent formal source.
- `independent_stakes`: an independent non-issuer public source that states what was at stake, the source-stated rationale, or the business context for the decision. Company-owned pages, issuer releases, PR-wire republications, and other company-controlled surfaces do not satisfy this role.
- `public_aftermath`: a later or retrospective public source that states implementation, consequences, outcome, reversal, write-off, customer or employee impact, or durable company change after the decision.

Each source must be public and usable. A single broad profile, advice essay, ranked list, interview transcript, or historical narrative is not enough unless the cited page itself satisfies the requested role for the same named company decision event.

Requirements:
- The page must identify the same named company and specific decision event, and the event described by the page must fit the submitted `restraint_mode`.
- The page must visibly fit the submitted `evidence_role`: authority-bearing for `formal_decision`; independent and non-issuer-controlled for `independent_stakes`; later or retrospective aftermath evidence for `public_aftermath`.
- The page must give enough timing information to anchor the decision, such as a decision date, announcement date, filing date, page publication date plus year-stated event timing, or retrospective year.
- The page must provide role-specific substance: the concrete restraint decision for `formal_decision`; stakes, rationale, or business context for `independent_stakes`; and implementation, outcome, consequence, reversal, write-off, impact, or durable change for `public_aftermath`.

Write one JSON object per line to `results_business_restraint_decision_event_provenance.jsonl`:
{"item": { "restraint_mode": "<restraint_mode>", "company": "<company>", "decision": "<decision>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

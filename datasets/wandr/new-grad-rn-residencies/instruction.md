You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `new_grad_rn_residencies`
  - `new_grad_rn_residencies.magnet_status`
  - `new_grad_rn_residencies.trauma_status`

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

## `new_grad_rn_residencies`

For 25+ hospitals in California, Oregon, Washington, and Montana, supply a source (1+ program-specific URL per hospital) showing a hospital-run or health-system-run new-graduate registered-nurse residency, nurse residency, or RN transition-to-practice program tied to that hospital.

The submitted state must be one of California, Oregon, Washington, and Montana; hospitals in any other state are outside scope.

Program-specific URLs should be nursing residency program pages, new-grad RN residency career pages, or current cohort/requisition pages. A third-party indexed mirror of a hospital or health-system cohort/requisition page counts only when it reproduces program-specific listing content tying the new-grad RN cohort to the claimed hospital. Generic job boards or search pages without that reproduced program-specific content, hospital careers search pages, all-nurse professional development pages, student nurse externships, physician or medical residencies, and non-RN faculty residencies do not count.

Requirements:
- The page must communicate its program-specific nursing residency or transition-to-practice source class.
- The page must tie the program to the claimed hospital or to a parent health system that includes that hospital in the claimed state.
- The page must show that the program is for new-graduate, newly licensed, or new-to-practice registered nurses.
- The page must show the program is current, recurring, or tied to an active or upcoming cohort.

Write one JSON object per line to `results_new_grad_rn_residencies.jsonl`:
{"item": { "hospital": "<hospital>", "state": "<state>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `new_grad_rn_residencies.magnet_status`

Cross-tasknode identifier discipline: this task is for the same {= hospital_state =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= hospital_state =}+ hospitals in California, Oregon, Washington, and Montana, supply a source (1+ URL per hospital) showing current ANCC Magnet designation for that hospital.

The submitted state must be one of California, Oregon, Washington, and Montana; hospitals in any other state are outside scope.

ANCC Magnet lookup pages, ANCC organization pages, hospital-controlled Magnet pages, and hospital-controlled awards or recognition pages that explicitly name Magnet designation by ANCC count. Generic nursing excellence marketing, Pathway to Excellence pages, old site-visit prep pages without an awarded designation, and system-level pages that do not identify the claimed facility do not count.

Requirements:
- The page must communicate an ANCC or hospital-controlled Magnet-designation source class.
- The page must identify the claimed hospital or facility.
- The page must show the claimed hospital currently holds Magnet designation or a designation period covering the present.
- The page must place the hospital in the claimed target state.

Write one JSON object per line to `results_new_grad_rn_residencies.magnet_status.jsonl`:
{"item": { "hospital": "<hospital>", "state": "<state>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `new_grad_rn_residencies.trauma_status`

Cross-tasknode identifier discipline: this task is for the same {= hospital_state =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= hospital_state =}+ hospitals in California, Oregon, Washington, and Montana, supply a source (1+ URL per hospital) showing Level I or Level II trauma center status for that hospital.

The submitted state must be one of California, Oregon, Washington, and Montana; hospitals in any other state are outside scope.

ACS verification pages, state or regional trauma designation registries, and hospital-controlled trauma program, emergency/trauma, fact-sheet, awards, or news pages that clearly state Level I or Level II trauma status count. Generic emergency department pages without a Level I or Level II statement, trauma education pages not tied to the facility, and Level III/IV/V centers do not count.

Requirements:
- The page must communicate an ACS, state-designation, regional-designation, or hospital-controlled source class for trauma status.
- The page must identify the claimed hospital or facility.
- The page must show the claimed hospital has Level I or Level II trauma center status.
- The page must place the hospital in the claimed target state.

Write one JSON object per line to `results_new_grad_rn_residencies.trauma_status.jsonl`:
{"item": { "hospital": "<hospital>", "state": "<state>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

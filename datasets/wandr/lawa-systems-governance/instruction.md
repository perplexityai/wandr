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

## `lawa_systems_governance`

For 220+ discrete LAWA governance actions within January 1, 2021 through June 23, 2026, supply official public record URL(s) showing that LAWA approved, amended, funded, renewed, or justified a mission-critical airport technology, infrastructure, or control system.

A `system_action` is one identifiable board, commission, committee, council, contract, amendment, appropriation, renewal, or comparable official decision. Split related agenda items when the official record treats them separately, including separate contract legs for the same system, later amendments, separate vendors, and distinct appropriations. City Clerk or Council follow-up for the same originating action can sit under the same `system_action` when it independently proves the action.

Primary sources should be official LAWA Board / BOAC agenda packets, staff reports, minutes, or official Los Angeles City Clerk / Council records when the action leaves LAWA. Vendor pages, press coverage, procurement opportunity pages without board action, and generic summaries do not count. Mission-critical systems can include finance / ERP core systems, FMCS / BAS / HVAC controls, radio and access-control systems, surveillance or video analytics, cybersecurity or IT infrastructure, common-use passenger-processing systems, baggage and airport-operations systems, or similar systems, but only when the official record itself states operational necessity.

For each action, name the system function, action context, vendor or platform when official text names one, amount or term, contract / file / resolution identifiers when present, and the official risk or necessity rationale.

Requirements:
- The page must communicate that it is an official LAWA Board / BOAC record or an official Los Angeles City Clerk / Council record for the LAWA action.
- The page must place the action within January 1, 2021 through June 23, 2026 and identify the governance action context: meeting or document date plus approval, award, amendment, funding, renewal, resolution, council file, contract action, appropriation, or comparable official decision.
- The page must identify the technology, infrastructure, or control system and its airport-operational function, not merely ordinary construction, facilities work, or generic office software with incidental IT.
- The page must state material action details: vendor or platform when named by the official record, and at least one amount, term, contract number, resolution number, council file, appropriation, renewal option, or comparable scope / authority detail.
- The page must explicitly state an official risk, necessity, or operational-dependency rationale for the system, such as safety, security, continuity, compliance, capacity, end-of-life, supportability, staffing, control-room operations, passenger-processing dependency, no-action risk, or similar mission-critical need.

Write one JSON object per line to `results_lawa_systems_governance.jsonl`:
{"item": { "system_action": "<system_action>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

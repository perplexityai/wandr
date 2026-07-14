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

## `siirt_hydropower`

For 40+ named hydroelectric dam, regulator, or HES projects tied to Siirt province, cover 4+ distinct evidence roles per project, which means all of the role values listed below. For each (`project`, `evidence_role`) pair, supply 1+ project-specific public URL.

Siirt HES records often appear as partial or conflicting traces: provincial ÇED notices, governorate or district pages, downloadable official files, operator pages, energy trade reports, directories, and local legal/context reporting can disagree on spelling, river name, capacity, operator, or lifecycle status.

The `evidence_role` values are:
- `official_administrative_or_plan`: official Turkish public-authority evidence for a project administrative, ÇED, plan, decision, public-notice, water-use, license, or comparable regulatory document/action
- `operation_capacity_or_operator`: project technical or operating-posture evidence such as capacity, generation, operator, commissioning, license-period, production, or operating-state details
- `dated_status_or_lifecycle_event`: dated lifecycle-event evidence such as ÇED process movement, water-use or production license, pre-license, public consultation, court/reporting event, renewal, cancellation, construction, commissioning, modification, or operation milestone
- `local_legal_or_context`: local, legal, ecology, recreation, academic, conflict, or community-context evidence directly tied to the project, river, affected place, or reported proceeding

Direct EPDK, central e-ÇED, DSİ, or Resmi Gazete records count when they are publicly reachable, but they are not mandatory if project-specific official provincial, company/operator, trade, or local-context sources carry the evidence.

Project-specific energy directories can support discovery, capacity, generation, operator, or operating-state evidence, but province-level lists and directory-only evidence should not be treated as official administrative status by themselves. Official announcements, operator pages, trade/directory profiles, dated lifecycle records, and local/legal/context reporting are separate evidence surfaces. A broad annual report, provincial status PDF, source hub, or project table can count only for the role that its cited section independently supports; the same table row should not be recycled as official, operation, lifecycle, and local/context evidence. Local, legal, ecology, or recreation sources count only for what they directly say about the named project, river/place, event, proceeding, or context; they should not be turned into legal conclusions or unsupported environmental-impact claims.

Requirements:
- The page must clearly identify the named project and tie it to Siirt province through a district, river, village/place, facility location, or project area.
- The page must show content-level cues for the declared role, not just a generic project mention: an administrative or planning action for `official_administrative_or_plan`; technical/operator/production fields for `operation_capacity_or_operator`; a dated action, decision, period, or milestone for `dated_status_or_lifecycle_event`; or local/legal/ecology/recreation/community narrative or proceeding for `local_legal_or_context`.
- The page must expose a concrete project-specific finding for that role, with source type, source date, event date, aliases, status posture, capacity/generation units, operator, conflicts, affected places, or missing-state cues preserved when the page provides them. Generic table columns, province-level inventory text, publication dates, or place names should not be stretched into another role's finding.

Write one JSON object per line to `results_siirt_hydropower.jsonl`:
{"item": { "project": "<project>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

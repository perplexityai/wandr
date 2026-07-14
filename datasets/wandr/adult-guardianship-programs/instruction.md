You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `adult_guardianship_programs`
  - `adult_guardianship_programs.adult_guardianship_legislation`

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

## `adult_guardianship_programs`

For all the 30 jurisdictions listed below, identify the public or last-resort adult-guardianship arrangement (1+ per jurisdiction) and supply a source (i.e. 1+ URL) that substantiates what institutional mechanism serves when an adult needs a guardian and no suitable private guardian is available.

The aim is a DC-and-peer comparison base for adult civil guardianship focused on the institutional fallback.

Target jurisdictions:
- **District of Columbia**
- **Alaska**
- **Maricopa County, Arizona**
- **Ada County, Idaho**
- **Maryland**
- **Minnesota**
- **North Dakota**
- **Washington**
- **Texas**
- **California**
- **New York**
- **Illinois**
- **Florida**
- **Virginia**
- **Massachusetts**
- **Colorado**
- **Oregon**
- **Nevada**
- **Georgia**
- **Maine**
- **Pennsylvania**
- **New Jersey**
- **Tennessee**
- **Ohio**
- **North Carolina**
- **Michigan**
- **Los Angeles County, California**
- **Cook County, Illinois**
- **Multnomah County, Oregon**
- **San Francisco County, California**

Requirements:
- The page must clearly tie the arrangement named to the jurisdiction in scope.
- The page must communicate its adult-guardianship legal / institutional authority, e.g. through court or agency identity, code / statute / rule headings, department or office titles, public guardian / public fiduciary labels, authorizing-law references, official forms or manuals, or comparable authority-bearing page text.
- The page must identify or describe the public or last-resort arrangement itself: a statewide office, agency, public guardianship program, county public guardian / fiduciary, court fiduciary panel, contracted-provider system, etc. A generic rule that a court may appoint "a suitable person" is not enough by itself.
- The page must expose a tangible arrangement detail, such as who serves / when the fallback is triggered / what adult population is covered / what services or duties are performed / ...

Write one JSON object per line to `results_adult_guardianship_programs.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "guardian_arrangement": "<guardian_arrangement>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `adult_guardianship_programs.adult_guardianship_legislation`

Cross-tasknode identifier discipline: this task is for the same {= jurisdiction =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For all the {= jurisdiction =} jurisdictions listed below, cover each of the 5 adult-guardianship legal comparison areas by supplying 5+ meaningfully distinct legal or institutional signals per area, each backed by a source (i.e. 1+ URL) that clearly supports the signal. Expected sources are legal / institutional surfaces, not general web discussion. All the signals should be meaningfully different legal / institutional points, not paraphrases of the same rule.

The purpose is a legal-field scouting panel for adult guardianship: a compact set of focused signals showing how each jurisdiction's adult civil guardianship system expresses appointment standards, alternatives, selection rules, oversight, and retained-rights / revisit mechanisms.

Target jurisdictions:
- **District of Columbia**
- **Alaska**
- **Maricopa County, Arizona**
- **Ada County, Idaho**
- **Maryland**
- **Minnesota**
- **North Dakota**
- **Washington**
- **Texas**
- **California**
- **New York**
- **Illinois**
- **Florida**
- **Virginia**
- **Massachusetts**
- **Colorado**
- **Oregon**
- **Nevada**
- **Georgia**
- **Maine**
- **Pennsylvania**
- **New Jersey**
- **Tennessee**
- **Ohio**
- **North Carolina**
- **Michigan**
- **Los Angeles County, California**
- **Cook County, Illinois**
- **Multnomah County, Oregon**
- **San Francisco County, California**

Comparison areas:
- `appointment_basis_and_scope`: required findings before appointing an adult guardian / conservator, plus how the order's powers / duration / scope are limited
- `decision_support_alternatives`: less-restrictive supports considered before or instead of guardianship, such as supported decision-making, protective arrangements, powers of attorney, health-care agents, services, technology, community supports
- `guardian_selection_priority`: who may serve, who receives priority / preference, who is disqualified, and when a professional / public / agency fallback can be selected
- `post_appointment_oversight`: post-appointment reporting / accountings / care plans / visits / training / monitoring programs / compliance reviews / portals
- `rights_retention_and_revisit`: retained rights / rights notices / objection / appeal / restoration / termination / modification / periodic review mechanisms that can revisit whether guardianship remains needed or least-restrictive

The cited page or visible section should naturally belong to the comparison area in scope: appointment / scope material for `appointment_basis_and_scope`; less-restrictive-alternative / SDM / protective-arrangement / powers-of-attorney / support-service material for `decision_support_alternatives`; selection / priority / nominee / disqualification / fallback-selection material for `guardian_selection_priority`; reporting / accounting / monitoring / training / compliance / guardian-duty material for `post_appointment_oversight`; rights-notice / objection / appeal / restoration / termination / modification / periodic-review material for `rights_retention_and_revisit`. Broad sources such as code chapters / handbooks / manuals / FAQs and such could fit only when there's a well-separated section being cited clearly dedicated to the area in question, with good specificity.

Requirements:
- The page must clearly tie the cited signal to the named jurisdiction's adult civil guardianship / conservatorship system.
- The page must communicate its legal / institutional authority, e.g. through official court or agency identity, code / statute / rule headings, legal-publisher reproduction of a specific code section, court form numbers, agency manual titles, statutory citations, effective-law framing, or comparable authority-bearing page text.
- The page must expose a focused legal or institutional signal clearly scoped to the comparison area in scope. For `appointment_basis_and_scope`, look for a tangible appointment threshold, required finding, incapacity standard, limited-powers rule, duration / scope limitation, written-findings requirement, or comparable appointment/scope rule. Under `decision_support_alternatives`, the signal should be a concrete less-restrictive alternative considered before or instead of guardianship: supported decision-making, protective arrangement, power of attorney, health-care agent, technology support, community service, court redirection away from guardianship, etc. `guardian_selection_priority` calls for a specific eligibility rule, priority list, nominee recognition, preference, disqualification, conflict rule, public / professional fallback trigger, or similar selection mechanism. For `post_appointment_oversight`, use a concrete reporting / accounting / care-plan / visit / training / monitoring / compliance-review / portal / guardian-duty obligation after appointment. `rights_retention_and_revisit` should surface a retained right, rights notice, objection / appeal path, restoration, termination, modification, periodic review, least-restrictive revisit mechanism, or comparable way to revisit the guardianship's continued fit.

Write one JSON object per line to `results_adult_guardianship_programs.adult_guardianship_legislation.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "comparison_area": "<comparison_area>", "legal_signal": "<legal_signal>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

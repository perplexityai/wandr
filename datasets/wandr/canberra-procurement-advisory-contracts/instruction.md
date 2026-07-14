You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `canberra_procurement_advisory_contracts`
  - `canberra_procurement_advisory_contracts.supplier_profiles`

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

## `canberra_procurement_advisory_contracts`

For each of the 3 service lines below, cover 24+ awarded suppliers and at least 2+ public Australian Commonwealth contract notices per supplier, all published or released in 2023-07-01 through 2026-06-26; supply an official contract-data URL for each notice (1+ URL per supplier-notice pair). The supplier must be the awarded supplier, not the procuring entity or an agency contact/team, and the source must fetch to readable official contract-data text: a resolving rendered AusTender notice page, an official AusTender contract-notice export file, or comparable official Australian Government contract notice publication whose fetched text exposes the notice fields. Rendered AusTender notice URLs that use the notice UUID, including `Cn/Show/<uuid>` or `Cn/Show/?Id=<uuid>` forms, are in scope when they fetch to the notice text; a `Cn/Show/CN...` path, search shell, error page, or other URL that does not fetch to the notice fields is not evidence. Official JSON API response URLs are not evidence URLs for this task.

The service lines are:
- `procurement_advisory`: procurement advisory, procurement support, procurement function review, strategic procurement advice, strategic sourcing, or close official wording.
- `probity_advisory_or_audit`: probity advisor, probity advisory, probity assurance, probity audit, probity advice, or close official wording.
- `contract_vendor_or_commercial_management`: contract management, vendor management, tender management, commercial management, contract/commercial negotiation, or close official wording tied to supplier contracts or commercial outcomes.

Report contract values only as public reported contract values or maximum values over the contract life. They are not supplier revenue, annual expenditure, market share, or recommendation evidence.

Requirements:
- The official source must identify the awarded supplier and include its ABN when the source provides one.
- The official source must identify the claimed contract notice ID and show the procuring entity, contract description or title, publication/release date or contract period, and reported contract value.
- The official contract text must support the selected service line.
- Any value claim must be framed as a public reported contract value, not as supplier revenue, annual expenditure, or market evidence.

Write one JSON object per line to `results_canberra_procurement_advisory_contracts.jsonl`:
{"item": { "service_line": "<service_line>", "supplier": "<supplier>", "contract_notice_id": "<contract_notice_id>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `canberra_procurement_advisory_contracts.supplier_profiles`

Cross-tasknode identifier discipline: this task is for the same {= supplier =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= supplier =}+ awarded suppliers, supply public profile evidence for each of the 2 profile facets below (1+ URL per supplier-facet pair). In the complete contract-notice/profile assignment, this profile evidence is calibrated for 72+ supplier identities also covered by the contract-notice evidence. The source must be a public supplier-profile source, not an official AusTender contract notice, Standing Offer Notice, contract-notice export, or notice-like official procurement record. Supplier-specific sources such as individual Finance MAS supplier profiles, firm-owned service pages, annual reports, capability statements, or comparable authoritative public profiles are in scope. Broad Finance/MAS matrices, panellist indexes, search pages, and table-like supplier lists are in scope only for `public_size_or_presence` when they expose a supplier-specific size, business-type, panel-status, ACT/Canberra presence, or Commonwealth-market signal; they do not satisfy `public_service_profile`.

The supplier profile facets are:
- `public_service_profile`: the page shows, in supplier-specific service/profile/capability material, that the supplier offers procurement, probity, contract/vendor management, commercial management, commercial negotiation, or closely related advisory services. Aggregate matrices, indexes, search results, or table-like lists of suppliers and service categories are not enough for this facet.
- `public_size_or_presence`: the page shows a public size/status signal, a panel/business-type signal, a Canberra/ACT presence signal, or a Commonwealth/Australian Government market-presence signal.

MAS size bands, business-type labels, and panel-status labels count as public size/presence signals only as labels or bands. Treat exact headcount or staff count as exact only when the source states the number directly.

Requirements:
- The page must identify the same supplier, using a legal name, trading name, ABN, official profile branding, or a clear alias link.
- The page must support the selected supplier profile facet. If the `public_size_or_presence` evidence uses a broad matrix, index, search page, or table-like list, the `public_service_profile` evidence for that supplier must come from a distinct supplier-specific profile, service, capability, annual-report, or comparable narrative source rather than the same aggregate URL.

Write one JSON object per line to `results_canberra_procurement_advisory_contracts.supplier_profiles.jsonl`:
{"item": { "supplier": "<supplier>", "supplier_profile_facet": "<supplier_profile_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
